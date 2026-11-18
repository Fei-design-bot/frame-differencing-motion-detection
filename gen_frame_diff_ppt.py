# -*- coding: utf-8 -*-
"""帧间差分·时间错开叠加 —— 实验可视化（原理流程图 + 成品 PPT）"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pptx import Presentation
from pptx.util import Inches, Pt, Length
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

DEEP_HEX = "#1F4E79"
BLUE_HEX = "#0070C0"
LIGHT_HEX = "#DEEAF6"
GOLD_HEX = "#C07A00"

# ================= 1. 原理流程图 PNG =================
steps = [
    ("原视频帧", "F(t)"),
    ("复制·反向", "255 − F"),
    ("半透明", "50% 透明度"),
    ("时间轴错开", "Δt"),
    ("叠加·显影", "变化浮出"),
    ("增强·放大", "阈值+形态学"),
]

fig, ax = plt.subplots(figsize=(14, 4.2), dpi=200)
ax.set_xlim(0, 14)
ax.set_ylim(0, 4.2)
ax.axis("off")

n = len(steps)
x0, y0, w, h = 0.35, 1.75, 1.95, 1.5
gap = 0.28
arrow_gap = (14 - 2 * x0 - n * w - (n - 1) * gap) / (n - 1)

for i, (title, sub) in enumerate(steps):
    x = x0 + i * (w + gap + arrow_gap)
    c = DEEP_HEX if i in (0, 4, 5) else BLUE_HEX
    box = FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.06,rounding_size=0.18",
                         linewidth=2, edgecolor=c, facecolor=c, alpha=0.92)
    ax.add_patch(box)
    ax.text(x + w / 2, y0 + h / 2 + 0.32, f"0{i+1}", ha="center", va="center",
            fontsize=13, color="white", fontweight="bold", alpha=0.85)
    ax.text(x + w / 2, y0 + h / 2 - 0.12, title, ha="center", va="center",
            fontsize=15, color="white", fontweight="bold")
    ax.text(x + w / 2, y0 + h / 2 - 0.62, sub, ha="center", va="center",
            fontsize=11.5, color="#DCE9F7")
    if i < n - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.02, y0 + h / 2),
                                     (x + w + arrow_gap - 0.02, y0 + h / 2),
                                     arrowstyle="-|>", mutation_scale=26,
                                     linewidth=2.2, color=GOLD_HEX))

eq = r"$0.5\cdot F(t)\;+\;0.5\cdot\big(255-F(t-\Delta t)\big)\;=\;127.5\;+\;0.5\cdot\big(F(t)-F(t-\Delta t)\big)$"
ax.text(7.0, 0.72, eq, ha="center", va="center", fontsize=16, color=DEEP_HEX, fontweight="bold")
ax.text(7.0, 0.12, "中灰背景  +  放大后的变化量（即帧间差分）  →  只保留“随时间变化的部分”",
        ha="center", va="center", fontsize=12.5, color="#555555")

plt.tight_layout(pad=0.4)
plt.savefig(r"C:\Users\cfy\Desktop\frame_diff_principle.png", facecolor="white", bbox_inches="tight")
print("saved frame_diff_principle.png")
plt.close(fig)

# ================= 2. 成品 PPT =================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

DEEP = RGBColor(0x1F, 0x4E, 0x79)
BLUE = RGBColor(0x00, 0x70, 0xC0)
LIGHT = RGBColor(0xDE, 0xEA, 0xF6)
GOLD = RGBColor(0xC0, 0x7A, 0x00)
DARK = RGBColor(0x33, 0x33, 0x33)
GRAY = RGBColor(0x80, 0x80, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Microsoft YaHei"


def _in(v):
    return v if isinstance(v, Length) else Inches(v)


def add_slide():
    return prs.slides.add_slide(BLANK)


def rect(slide, x, y, w, h, color, line=False, round_=False):
    shp = MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(shp, _in(x), _in(y), _in(w), _in(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    if not line:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def txt(slide, x, y, w, h, text, size=18, color=DARK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font=FONT, line_spacing=1.0, italic=False):
    tb = slide.shapes.add_textbox(_in(x), _in(y), _in(w), _in(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font
    p.line_spacing = line_spacing
    return tb


def header(slide, title, subtitle=""):
    rect(slide, 0, 0, 13.333, 1.1, DEEP)
    txt(slide, 0.6, 0.16, 12, 0.62, title, size=27, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.MIDDLE)
    if subtitle:
        txt(slide, 0.6, 0.76, 12, 0.3, subtitle, size=13, color=RGBColor(0xBD, 0xD7, 0xEE))


def footer(slide, num):
    txt(slide, 12.4, 7.05, 0.8, 0.35, str(num), size=11, color=GRAY, align=PP_ALIGN.RIGHT)


# ---- 第 1 页 · 封面 ----
s = add_slide()
rect(s, 0, 0, 13.333, 7.5, DEEP)
rect(s, 0, 5.3, 13.333, 0.06, BLUE)
txt(s, 1, 1.8, 11.3, 1.2, "帧间差分 · 时间错开叠加", size=46, color=WHITE, bold=True,
    align=PP_ALIGN.CENTER)
txt(s, 1, 3.0, 11.3, 0.7, "视频小目标变化检测 —— 原理与实验验证", size=25,
    color=RGBColor(0xBD, 0xD7, 0xEE), align=PP_ALIGN.CENTER)
txt(s, 1, 4.0, 11.3, 0.5, "保留视频中随时间变化的部分：复制 · 反向 · 半透明 · 时间轴错开",
    size=16, color=RGBColor(0x9D, 0xC3, 0xE6), align=PP_ALIGN.CENTER)
txt(s, 1, 5.55, 11.3, 0.5, "合成视频实验 · 移动小目标显影 · 静止目标抑制", size=15,
    color=RGBColor(0x9D, 0xC3, 0xE6), align=PP_ALIGN.CENTER)

# ---- 第 2 页 · 方法原理 ----
s = add_slide()
header(s, "方法原理", "六步流程与数学等价关系")
s.shapes.add_picture(r"C:\Users\cfy\Desktop\frame_diff_principle.png",
                     Inches(0.5), Inches(1.35), width=Inches(12.33))
rect(s, 0.6, 5.55, 12.13, 1.35, LIGHT)
txt(s, 0.9, 5.7, 11.6, 1.1,
    "核心：静止部分与它的反相相加，正好落回中灰（127.5），被“压掉”；\n"
    "只有随时间变化的部分，其差值被放大、浮出画面。",
    size=15, color=DEEP, bold=True, line_spacing=1.25)
footer(s, 2)

# ---- 第 3 页 · 实验结果 ----
s = add_slide()
header(s, "实验结果", "移动小目标显影 · 静止目标抑制 · 错开量决定明显程度")
s.shapes.add_picture(r"C:\Users\cfy\Desktop\frame_diff_exp.png",
                     Inches(0.5), Inches(1.4), width=Inches(12.33))
footer(s, 3)

# ---- 第 4 页 · 结论 ----
s = add_slide()
header(s, "结论与要点", "三条件验证 · 一个局限")
items = [
    ("① 能显影", "复制→反向→半透明→时间轴错开叠加后，移动小目标清晰浮出，静止亮点被压到中灰、不可见"),
    ("② 错开量决定明显度", "Δt 越小残影越弱（Δt=1），越大残影越强（Δt=7）；与“错开时间 ↔ 变化明显程度”一致"),
    ("③ 可增强", "阈值二值化 + 形态学开运算 + 膨胀，可将 2~3 像素微小目标放大到肉眼易见"),
    ("局限", "真实视频的背景抖动、光照变化会被一并“显影”，需配合背景建模 / 运动补偿才能落地"),
]
y = 1.4
for title, desc in items:
    hl = title == "局限"
    rect(s, 0.6, y, 2.5, 1.05, GOLD if hl else BLUE, round_=True)
    txt(s, 0.7, y + 0.12, 2.3, 0.8, title, size=16, color=WHITE, bold=True,
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    rect(s, 3.3, y + 0.05, 9.4, 0.95, RGBColor(0xFF, 0xF2, 0xCC) if hl else LIGHT, round_=True)
    txt(s, 3.55, y + 0.12, 8.9, 0.8, desc, size=14, color=DARK, anchor=MSO_ANCHOR.MIDDLE,
        line_spacing=1.1)
    y += 1.28
footer(s, 4)

OUT = r"C:\Users\cfy\Desktop\帧间差分-小目标变化检测实验.pptx"
prs.save(OUT)
print("saved:", OUT, " 页数:", len(prs.slides._sldIdLst))
