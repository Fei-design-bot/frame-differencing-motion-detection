# -*- coding: utf-8 -*-
"""帧间差分 / 时间错开叠加 —— 小目标变化检测实验
复现：复制视频 -> 反向 -> 半透明 -> 时间轴错开 -> 变化显影 -> 增强
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cv2
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

W, H, FPS, N = 640, 360, 30, 90

# ---- 1. 合成测试视频：暗灰噪声背景 + 缓慢移动的小亮点（小目标）----
rng = np.random.RandomState(7)
bg = rng.randint(28, 48, (H, W, 3), dtype=np.uint8)   # 静态噪声背景
frames = []
for t in range(N):
    f = bg.copy()
    # 移动小目标：约 2~3 像素见方，从左上缓慢移到右中
    cx = int(80 + 440 * t / (N - 1))
    cy = int(130 + 190 * t / (N - 1))
    f[cy - 1:cy + 2, cx - 1:cx + 2] = (255, 255, 255)
    # 静止亮点：不随时间变化，帧差应将其抑制掉
    f[60:63, 300:303] = (200, 200, 200)
    frames.append(f)


def invert(img):
    return 255 - img


def user_blend(t, dt):
    """用户方法：当前帧 与 反相后的 dt 帧前帧，各 50% 透明度叠加"""
    cur = frames[t].astype(np.float32)
    prev_inv = invert(frames[t - dt]).astype(np.float32)
    return np.clip(0.5 * cur + 0.5 * prev_inv, 0, 255).astype(np.uint8)


def absdiff(t, dt):
    """等价帧差：|F(t) - F(t-dt)|（与上面方法差一个常数与符号，静区都落在中灰）"""
    return cv2.absdiff(frames[t], frames[t - dt])


def enhance(img, thr=40, dilate=5):
    """增强：阈值二值化 + 开运算去噪 + 膨胀放大微小目标"""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(g, thr, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    th = cv2.dilate(th, np.ones((dilate, dilate), np.uint8))
    return cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)


t = 45
panels = [
    ("原始帧 t（含移动小点 + 静止亮点）", frames[t]),
    ("反相叠加 Δt=3（变化显影）", user_blend(t, 3)),
    ("等价帧差 |F(t)-F(t-3)|", absdiff(t, 3)),
    ("增强：阈值+形态学放大", enhance(absdiff(t, 3))),
    ("帧差 Δt=1（错开小，残影弱）", absdiff(t, 1)),
    ("帧差 Δt=3", absdiff(t, 3)),
    ("帧差 Δt=7（错开大，残影强）", absdiff(t, 7)),
    ("Δt=7 增强：小目标放大", enhance(absdiff(t, 7), thr=30, dilate=11)),
]

fig, axes = plt.subplots(2, 4, figsize=(16, 7))
for ax, (title, img) in zip(axes.flat, panels):
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title(title, fontsize=11)
    ax.axis("off")
plt.suptitle("帧间差分 / 时间错开叠加 —— 小目标变化检测", fontsize=15, fontweight="bold", y=1.0)
plt.tight_layout()
plt.savefig(r"C:\Users\cfy\Desktop\frame_diff_exp.png", dpi=110, facecolor="white", bbox_inches="tight")
print("saved frame_diff_exp.png")
