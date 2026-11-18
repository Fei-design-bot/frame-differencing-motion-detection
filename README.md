# 帧间差分 · 时间错开叠加（Frame Differencing for Motion / Small-Target Detection）

保留视频画面中**随时间变化的部分**，面向小目标 / 变化检测的初步实验。

## 方法原理

复制视频 → 反向（`255 − F`）→ 半透明（50%）→ 时间轴错开 `Δt` → 叠加显影 → 任意增强。

数学上等价于帧间差分：

```
0.5·F(t) + 0.5·(255 − F(t−Δt)) = 127.5 + 0.5·(F(t) − F(t−Δt))
```

即「中灰背景 + 放大后的变化量」。静止部分与反相相加落回中灰、被压掉；随时间变化的部分被放大、浮出画面。

## 文件说明

| 文件 | 说明 |
|---|---|
| `gen_frame_diff_exp.py` | 实验脚本：合成视频 + 帧差 + 形态学增强，出对比图 |
| `frame_diff_exp.png` | 实验结果（2×4 对照：原始 / 反相叠加 / 帧差 / 增强 / Δt 扫描） |
| `frame_diff_principle_wide.png` | 方法原理流程图（六步 + 数学等价式） |
| `gen_frame_diff_ppt.py` | 生成独立可视化 PPT（4 页：封面 / 原理 / 结果 / 结论） |
| `gen_frame_diff_slide.py` | 把实验作为「一页」插入已有汇报 PPT（谢谢页之前） |
| `gen_papers_xlsx.py` | 生成「一区以上」顶会 / 顶刊论文清单 |
| `异常视频检测-顶刊顶会论文清单.xlsx` | 论文清单（CCF-A 顶会 + 中科院一区期刊，均含开源代码） |

## 复现

```bash
pip install opencv-python matplotlib numpy pillow openpyxl python-pptx
python gen_frame_diff_exp.py
```

## 结论

- 静止目标被压到中灰、不可见；移动小目标清晰浮出；
- 错开量 `Δt` 越大，变化残影越明显（`Δt=1` 弱 → `Δt=7` 强）；
- 阈值 + 形态学可将 2~3 像素微小目标放大到肉眼易见；
- 局限：真实视频的背景抖动 / 光照变化会被一并显影，需背景建模或运动补偿。

## 参考文献

见 `异常视频检测-顶刊顶会论文清单.xlsx`（主表 7 篇 CCF-A / 中科院一区，另附 2 篇 CCF-B 思想最贴合者）。
