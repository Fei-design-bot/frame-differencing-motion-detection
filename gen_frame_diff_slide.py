# -*- coding: utf-8 -*-
"""把帧差实验作为「一页」插入 周四汇报.pptx（谢谢页之前），并更新页码"""
import shutil, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

DEEP_HEX = "#1F4E79"
BLUE_HEX = "#0070C0"
GOLD_HEX = "#C07A00"

# ---------- 1. 生成紧凑版原理图（宽高比约 5.5:1） ----------
steps = [("原视频帧", "F(t)"), ("复制·反向", "255 − F"), ("半透明", "50%"),
         ("时间轴错开", "Δt"), ("叠加·显影", "变化浮出"), ("增强·放大", "阈值+形态学")]

fig, ax = plt.subplots(figsize=(13, 2.4), dpi=200)
ax.set_xlim(0, 13); ax.set_ylim(0, 2.4); ax.axis("off")
n = len(steps)
x0, y0, w, h = 0.32, 0.95, 1.95, 0.95
gap = 0.20
arrow_gap = (13 - 2 * x0 - n * w - (n - 1) * gap) / (n - 1)
for i, (title, sub) in enumerate(steps):
    x = x0 + i * (w + gap + arrow_gap)
    c = DEEP_HEX if i in (0, 4, 5) else BLUE_HEX
    ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.05,rounding_size=0.13",
                                linewidth=1.8, edgecolor=c, facecolor=c, alpha=0.92))
    ax.text(x + w/2, y0 + h/2 + 0.22, f"0{i+1}", ha="center", va="center",
            fontsize=10, color="white", fontweight="bold", alpha=0.85)
    ax.text(x + w/2, y0 + h/2 - 0.06, title, ha="center", va="center",
            fontsize=12.5, color="white", fontweight="bold")
    ax.text(x + w/2, y0 + h/2 - 0.40, sub, ha="center", va="center",
            fontsize=9, color="#DCE9F7")
    if i < n - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.02, y0 + h/2),
                                     (x + w + arrow_gap - 0.02, y0 + h/2),
                                     arrowstyle="-|>", mutation_scale=20,
                                     linewidth=2.0, color=GOLD_HEX))
eq = (r"$0.5\cdot F(t)+0.5\cdot(255-F(t-\Delta t)) = 127.5+0.5\cdot(F(t)-F(t-\Delta t))$")
ax.text(6.5, 0.30, eq, ha="center", va="center", fontsize=12.5, color=DEEP_HEX, fontweight="bold")
plt.tight_layout(pad=0.3)
PRINCIPLE = r"C:\Users\cfy\Desktop\frame_diff_principle_wide.png"
plt.savefig(PRINCIPLE, facecolor="white", bbox_inches="tight")
plt.close(fig)

# ---------- 2. 读图比例 ----------
def ratio(p):
    im = Image.open(p); return im.width / im.height
r_principle = ratio(PRINCIPLE)
r_exp = ratio(r"C:\Users\cfy\Desktop\frame_diff_exp.png")

# ---------- 3. 备份 + 打开目标 PPT ----------
TARGET = r"C:\Users\cfy\Desktop\周四汇报.pptx"
BACKUP = r"C:\Users\cfy\Desktop\周四汇报_backup.pptx"
shutil.copy2(TARGET, BACKUP)
prs = Presentation(TARGET)
FONT = "Microsoft YaHei"
DEEP = RGBColor(0x1F, 0x4E, 0x79)
BLUE = RGBColor(0x00, 0x70, 0xC0)
LIGHT = RGBColor(0xDE, 0xEA, 0xF6)
GRAY = RGBColor(0x80, 0x80, 0x80)
DARK = RGBColor(0x33, 0x33, 0x33)

blank = prs.slide_layouts[6]
s = prs.slides.add_slide(blank)

def rect(slide, x, y, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = color; sh.line.fill.background(); sh.shadow.inherit = False
    return sh

def txt(slide, x, y, w, h, text, size=18, color=DARK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, line_spacing=1.0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.text = text; p.alignment = align
    p.font.size = Pt(size); p.font.color.rgb = color; p.font.bold = bold
    p.font.name = FONT; p.line_spacing = line_spacing
    return tb

# 标题 + 下划线 + 副标题（匹配原版式）
txt(s, 0.6, 0.28, 12.0, 0.6, "补充 · 初步实验：帧间差分法", size=27, color=DEEP, bold=True,
    anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.62, 1.02, 1.7, 0.05, BLUE)
txt(s, 0.6, 1.14, 12.0, 0.35, "保留视频中随时间变化的部分 · 复制 · 反向 · 半透明 · 时间轴错开",
    size=12.5, color=GRAY)

# 原理图（上部，全宽）
pw = 12.1
ph = pw / r_principle
s.shapes.add_picture(PRINCIPLE, Inches(0.6), Inches(1.58), width=Inches(pw))

# 结果图（左下）+ 结论卡片（右下）
res_y = 1.58 + ph + 0.12
rw = 7.75
rh = rw / r_exp
s.shapes.add_picture(r"C:\Users\cfy\Desktop\frame_diff_exp.png",
                     Inches(0.6), Inches(res_y), width=Inches(rw))

card_x, card_w = 8.55, 4.15
card_h = rh
rect(s, card_x, res_y, card_w, card_h, LIGHT)
txt(s, card_x + 0.25, res_y + 0.16, card_w - 0.5, 0.35, "实验结论", size=15, color=DEEP, bold=True)
concl = [
    "① 静止目标被压到中灰、不可见；移动小目标清晰浮出",
    "② 错开量 Δt 越大，变化残影越明显（Δt=1 弱 → Δt=7 强）",
    "③ 阈值 + 形态学，可将 2~3 像素目标放大到肉眼易见",
    "④ 局限：背景抖动 / 光照变化会被一并显影，需背景建模或运动补偿",
]
ty = res_y + 0.56
for c in concl:
    txt(s, card_x + 0.25, ty, card_w - 0.5, 0.6, c, size=11.5, color=DARK, line_spacing=1.0)
    ty += 0.61

# 页脚
txt(s, 0.6, 7.08, 8.0, 0.35, "水下小目标检测与图像增强 · 2026 文献综述", size=9, color=GRAY)
txt(s, 12.2, 7.08, 0.8, 0.35, "18", size=10, color=GRAY, align=PP_ALIGN.RIGHT)

# ---------- 4. 把新页移到「谢谢」页之前，并更新谢谢页页码 18 -> 19 ----------
xml_slides = prs.slides._sldIdLst
slides = list(xml_slides)
new_index = len(slides) - 1          # 新页当前在末尾
xml_slides.remove(slides[new_index])
xml_slides.insert(len(slides) - 2, slides[new_index])  # 插到「谢谢」之前

# 更新「谢谢」页（现在 index = len-1）右下页码 18 -> 19
thanks = prs.slides[len(prs.slides._sldIdLst) - 1]
for sh in thanks.shapes:
    if sh.has_text_frame and sh.text_frame.text.strip() == "18":
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.text.strip() == "18":
                    r.text = "19"

prs.save(TARGET)
print("已插入一页到「周四汇报.pptx」（谢谢页之前），页码已顺延。备份：周四汇报_backup.pptx")
print("总页数：", len(prs.slides._sldIdLst))
