# -*- coding: utf-8 -*-
"""异常 / 小目标视频检测 —— 顶刊顶会论文清单（一区以上）Excel 生成"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DEEP = "1F4E79"
BLUE = "0070C0"
LIGHT = "DEEAF6"
GRAY = "808080"
WHITE = "FFFFFF"
FONT = "Microsoft YaHei"

wb = Workbook()
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

headers = ["序号", "论文标题（英文）", "方法核心（中文）", "发表出处", "等级", "研究方向",
           "开源代码", "与“帧差法 / 小目标 / 异常”的贴合点"]

rows = [
    ["1", "Self-Distilled Masked Auto-Encoders are Efficient Video Anomaly Detectors",
     "自蒸馏掩码自编码器 + 运动梯度加权前景", "CVPR 2024", "CCF-A", "视频异常检测",
     "https://github.com/ristea/aed-mae",
     "用运动梯度显式强化前景/小目标，与“保留随时间变化的部分”思路一致；异常检测方向最对口"],
    ["2", "Long Short-Term Feature Enhancement Network for Video Small Object Detection",
     "长短期特征增强网络（视频小目标检测）", "CVPR 2023", "CCF-A", "视频小目标检测",
     "https://github.com/WHU-xjs/LSTFE-Net",
     "专门面向“视频 + 小目标”，与“小目标异常检测”需求直接对齐"],
    ["3", "Prompt-Enhanced Multiple Instance Learning for Weakly Supervised Video Anomaly Detection",
     "提示增强的多示例学习（弱监督异常检测）", "CVPR 2024", "CCF-A", "视频异常检测",
     "https://github.com/Junxi-Chen/PE-MIL",
     "弱监督（视频级标注）异常检测，可在变化显影图上做后续判别"],
    ["4", "Small Object Detection via Coarse-to-fine Proposal Generation and Imitation Learning",
     "粗到细提议生成 + 模仿学习（小目标检测）", "ICCV 2023", "CCF-A", "小目标检测",
     "https://github.com/shaunyuan22/CFINet",
     "小目标检测，粗到细定位策略可迁移到“变化图上定位微小异常”"],
    ["5", "Self-Supervised Masked Convolutional Transformer Block for Anomaly Detection",
     "自监督掩码卷积 Transformer 骨干", "TPAMI 2023", "中科院一区", "视频异常检测",
     "https://github.com/ristea/ssmctb",
     "异常检测主干网络，可与运动线索（帧差）结合做小目标异常"],
    ["6", "A Background-Agnostic Framework with Adversarial Training for Abnormal Event Detection in Video",
     "背景无关 + 对抗训练的异常事件检测", "TPAMI 2021", "中科院一区", "视频异常检测",
     "https://github.com/lilygeorgescu/AED",
     "背景无关检测（抑制背景干扰），呼应帧差法“静区抑制、动区保留”"],
    ["7", "Explicit Motion Handling and Interactive Prompting for Video Camouflaged Object Detection",
     "显式运动处理 + 交互提示（视频伪装目标检测）", "TIP 2025", "中科院一区", "视频伪装目标检测",
     "https://github.com/zhangxin06/EMIP",
     "显式利用运动线索分割弱对比目标，运动是“随时间变化”的直接体现"],
]

ws2 = wb.create_sheet("参考-CCF-B")
rows2 = [
    ["1", "Visible and Clear: Finding Tiny Objects in Difference Map",
     "在“差分图”中检测微小目标", "ECCV 2024", "CCF-B", "小目标检测",
     "https://github.com/Hiyuur/SR-TOD",
     "直接在差分图上找微小目标，与你描述的帧差法思路几乎同源（ECCV 为 CCF-B，严格低于一区）"],
    ["2", "DETR with Dynamic Query for Tiny Object Detection",
     "动态查询 DETR（微小目标检测）", "ECCV 2024", "CCF-B", "微小目标检测",
     "https://github.com/hoiliu-0801/DQ-DETR",
     "微小目标检测主干，可配合差分图使用（ECCV 为 CCF-B，仅供参考）"],
]


def fill_sheet(sheet, data, note_row):
    ncol = len(headers)
    for j, h in enumerate(headers, 1):
        c = sheet.cell(1, j, h)
        c.font = Font(name=FONT, size=11, bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=DEEP)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border
    sheet.row_dimensions[1].height = 34
    for i, row in enumerate(data, 2):
        for j, v in enumerate(row, 1):
            c = sheet.cell(i, j, v)
            c.font = Font(name=FONT, size=10, color="333333")
            c.alignment = Alignment(horizontal="center" if j in (1, 4, 5, 6) else "left",
                                    vertical="center", wrap_text=True)
            c.border = border
            c.fill = PatternFill("solid", fgColor=(LIGHT if i % 2 == 0 else WHITE))
            if j == 7:
                c.hyperlink = v
                c.font = Font(name=FONT, size=10, color=BLUE, underline="single")
                c.value = v.replace("https://github.com/", "github.com/")
        sheet.row_dimensions[i].height = 58
    note = sheet.cell(len(data) + 3, 1, note_row)
    note.font = Font(name=FONT, size=10, bold=True, color=GRAY)
    sheet.merge_cells(start_row=len(data) + 3, start_column=1,
                      end_row=len(data) + 3, end_column=ncol)
    widths = [5, 40, 26, 13, 11, 14, 24, 42]
    for j, w in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(j)].width = w
    sheet.freeze_panes = "A2"


ws = wb.active
ws.title = "一区以上"
fill_sheet(ws, rows, "说明：以上 7 篇均为 CCF-A 顶会（CVPR/ICCV）或中科院一区期刊（TPAMI/TIP），均提供开源代码。")
fill_sheet(ws2, rows2, "说明：ECCV 为 CCF-B（不在 CCF-A 之列），严格低于“一区以上”，故单独列为参考。")

OUT = "异常视频检测-顶刊顶会论文清单.xlsx"
wb.save(OUT)
print("saved:", OUT)
