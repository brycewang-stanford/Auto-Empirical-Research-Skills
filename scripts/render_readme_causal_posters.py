#!/usr/bin/env python3
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images"
FONT_DIR = Path("/Users/brycewang/.codex/skills/canvas-design/canvas-fonts")

W, H = 2400, 1350

COLORS = {
    "paper": (247, 244, 235),
    "paper2": (232, 239, 236),
    "ink": (24, 31, 42),
    "muted": (89, 101, 115),
    "line": (197, 190, 177),
    "teal": (31, 111, 104),
    "blue": (48, 92, 143),
    "verm": (195, 89, 58),
    "amber": (215, 155, 69),
    "sage": (124, 154, 109),
    "plum": (99, 83, 132),
}


def font_path(name: str) -> Path:
    return FONT_DIR / name


FONTS = {
    "display": font_path("InstrumentSerif-Regular.ttf"),
    "display_it": font_path("InstrumentSerif-Italic.ttf"),
    "sans": font_path("InstrumentSans-Regular.ttf"),
    "sans_bold": font_path("InstrumentSans-Bold.ttf"),
    "mono": font_path("JetBrainsMono-Regular.ttf"),
    "mono_bold": font_path("JetBrainsMono-Bold.ttf"),
    "zh": Path("/Users/brycewang/Library/Fonts/NotoSerifCJKsc-Regular.otf"),
    "zh_bold": Path("/Users/brycewang/Library/Fonts/NotoSerifCJKsc-Bold.otf"),
    "zh_sans": Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
}


def get_font(key: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS[key]), size=size)


def blend(c1, c2, t):
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def centered_text(draw, box, text, font, fill, dy=0):
    x1, y1, x2, y2 = box
    tw, th = text_size(draw, text, font)
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 + dy), text, font=font, fill=fill)


def fit_font(draw, text, font_key, start_size, max_width):
    size = start_size
    font = get_font(font_key, size)
    while size > 16 and text_size(draw, text, font)[0] > max_width:
        size -= 1
        font = get_font(font_key, size)
    return font


def add_background(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        draw.line((0, y, W, y), fill=blend(COLORS["paper"], COLORS["paper2"], t))

    random.seed(42)
    for _ in range(5600):
        x = random.randrange(W)
        y = random.randrange(H)
        delta = random.choice([-8, -5, 6, 9])
        base = img.getpixel((x, y))
        img.putpixel((x, y), tuple(max(0, min(255, c + delta)) for c in base))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(90, W, 90):
        od.line((x, 0, x, H), fill=(44, 52, 61, 22), width=1)
    for y in range(90, H, 90):
        od.line((0, y, W, y), fill=(44, 52, 61, 18), width=1)
    for x in range(0, W, 180):
        od.line((x, 0, x + 760, H), fill=(44, 52, 61, 10), width=1)

    formulas = [
        "Y(1)-Y(0)",
        "E[Y|D=1]-E[Y|D=0]",
        "Z -> D -> Y",
        "parallel trends",
        "ATE / ATT / CATE",
        "overlap",
        "first stage",
        "counterfactual",
    ]
    mono = get_font("mono", 23)
    for i, text in enumerate(formulas):
        x = 140 + (i % 4) * 570
        y = 214 + (i // 4) * 815
        od.text((x, y), text, font=mono, fill=(24, 31, 42, 45))

    nodes = [(300, 1020), (430, 940), (570, 1060), (1850, 350), (1980, 450), (2100, 320)]
    for a, b in zip(nodes, nodes[1:]):
        od.line((a, b), fill=(31, 111, 104, 64), width=3)
    for x, y in nodes:
        od.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(247, 244, 235, 220), outline=(31, 111, 104, 115), width=3)

    img.alpha_composite(overlay)


def draw_panel(draw, x, y, w, h, title, chips, accent, lang):
    shadow = (18, 22, 26, 38)
    draw.rounded_rectangle((x + 14, y + 16, x + w + 14, y + h + 16), radius=32, fill=shadow)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=32, fill=(255, 253, 247, 238), outline=(24, 31, 42, 215), width=3)
    draw.rounded_rectangle((x, y, x + w, y + 78), radius=32, fill=accent + (245,))
    draw.rectangle((x, y + 44, x + w, y + 78), fill=accent + (245,))

    title_key = "zh_bold" if lang == "zh" else "sans_bold"
    title_font = fit_font(draw, title, title_key, 35, w - 80)
    centered_text(draw, (x + 30, y + 11, x + w - 30, y + 75), title, title_font, (255, 255, 250))

    chip_font_key = "zh_sans" if lang == "zh" else "sans"
    chip_font_bold_key = "zh_bold" if lang == "zh" else "sans_bold"
    chip_w = (w - 104) / 2
    chip_h = 54
    gap_x = 24
    gap_y = 22
    start_y = y + 112
    for idx, text in enumerate(chips):
        col = idx % 2
        row = idx // 2
        cx = x + 40 + col * (chip_w + gap_x)
        cy = start_y + row * (chip_h + gap_y)
        draw.rounded_rectangle((cx + 4, cy + 5, cx + chip_w + 4, cy + chip_h + 5), radius=15, fill=(18, 22, 26, 28))
        draw.rounded_rectangle((cx, cy, cx + chip_w, cy + chip_h), radius=15, fill=(255, 255, 250, 235), outline=accent + (210,), width=2)
        font_key = chip_font_bold_key if idx in (0, 2) else chip_font_key
        font = fit_font(draw, text, font_key, 29, chip_w - 26)
        centered_text(draw, (cx + 10, cy + 2, cx + chip_w - 10, cy + chip_h - 2), text, font, COLORS["ink"])

    for i in range(5):
        dot_x = x + w - 68 + i * 12
        dot_y = y + h - 28
        draw.ellipse((dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3), fill=accent + (80,))


def draw_badge(draw, x, y, text, accent, lang):
    font_key = "zh_sans" if lang == "zh" else "sans_bold"
    font = fit_font(draw, text, font_key, 28, 430)
    tw, th = text_size(draw, text, font)
    pad_x = 24
    draw.rounded_rectangle((x, y, x + tw + pad_x * 2, y + 48), radius=24, fill=(255, 255, 250, 228), outline=accent + (230,), width=2)
    draw.text((x + pad_x, y + 11), text, font=font, fill=COLORS["ink"])
    return x + tw + pad_x * 2


def draw_center_engine(draw, lang):
    cx, cy = W // 2, 670
    accent = COLORS["teal"]
    for r, alpha, width in [(355, 48, 2), (305, 70, 3), (252, 120, 4)]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=accent + (alpha,), width=width)
    for angle in [28, 116, 205, 304]:
        rad = math.radians(angle)
        x = cx + math.cos(rad) * 330
        y = cy + math.sin(rad) * 330
        draw.ellipse((x - 38, y - 38, x + 38, y + 38), fill=(255, 255, 250, 238), outline=accent + (220,), width=3)
        label = {
            28: "DAG",
            116: "ID" if lang == "en" else "识别",
            205: "ATE",
            304: "CI",
        }[angle]
        font = get_font("mono_bold" if label in {"DAG", "ATE", "CI", "ID"} else "zh_bold", 23 if lang == "en" or label in {"DAG", "ATE", "CI"} else 21)
        centered_text(draw, (x - 36, y - 34, x + 36, y + 34), label, font, COLORS["ink"])

    draw.ellipse((cx - 232, cy - 232, cx + 232, cy + 232), fill=(24, 31, 42, 248), outline=(255, 255, 250, 230), width=5)
    draw.ellipse((cx - 186, cy - 186, cx + 186, cy + 186), outline=(215, 155, 69, 210), width=4)
    display = get_font("display", 102)
    mono = get_font("mono_bold", 48)
    small_key = "zh_sans" if lang == "zh" else "sans"
    small = get_font(small_key, 31)
    micro = get_font("mono", 23)

    centered_text(draw, (cx - 185, cy - 118, cx + 185, cy - 20), "AERS", display, (255, 255, 247))
    centered_text(draw, (cx - 195, cy - 8, cx + 195, cy + 58), "sp.causal(...)", mono, (126, 217, 204))
    tagline = "Estimand-first routing" if lang == "en" else "Estimand-first 路由"
    centered_text(draw, (cx - 185, cy + 66, cx + 185, cy + 114), tagline, small, (255, 255, 247))
    centered_text(draw, (cx - 170, cy + 122, cx + 170, cy + 158), "diagnose -> estimate -> stress-test", micro, (215, 155, 69))


def draw_connectors(draw):
    cx, cy = W // 2, 670
    anchors = [
        ((850, 462), COLORS["teal"]),
        ((1550, 462), COLORS["blue"]),
        ((850, 942), COLORS["verm"]),
        ((1550, 942), COLORS["plum"]),
    ]
    for (x, y), color in anchors:
        draw.line((x, y, cx + (x - cx) * 0.55, cy + (y - cy) * 0.55), fill=color + (126,), width=4)
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color + (220,))


def draw_pipeline(draw, labels, lang):
    x, y, w, h = 140, 1142, 2120, 174
    draw.rounded_rectangle((x + 12, y + 12, x + w + 12, y + h + 12), radius=30, fill=(18, 22, 26, 32))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=30, fill=(255, 253, 247, 238), outline=(24, 31, 42, 160), width=2)
    title = "One closed loop" if lang == "en" else "一条闭环自动化"
    title_font = get_font("zh_bold" if lang == "zh" else "sans_bold", 28)
    draw.text((x + 38, y + 24), title, font=title_font, fill=COLORS["ink"])

    start_x = x + 290
    step_w = 225
    step_gap = 28
    colors = [COLORS["teal"], COLORS["blue"], COLORS["amber"], COLORS["verm"], COLORS["plum"], COLORS["sage"]]
    step_h = 68
    for i, label in enumerate(labels):
        sx = start_x + i * (step_w + step_gap)
        sy = y + 58
        draw.rounded_rectangle((sx, sy, sx + step_w, sy + step_h), radius=22, fill=colors[i] + (236,))
        num_font = get_font("mono_bold", 20)
        lab_font = fit_font(draw, label, "zh_sans" if lang == "zh" else "sans_bold", 25, step_w - 54)
        draw.text((sx + 18, sy + 25), f"{i + 1:02d}", font=num_font, fill=(255, 255, 250))
        centered_text(draw, (sx + 50, sy + 4, sx + step_w - 14, sy + step_h - 4), label, lab_font, (255, 255, 250))
        if i < len(labels) - 1:
            ax = sx + step_w + 8
            ay = sy + step_h / 2
            draw.polygon([(ax, ay - 10), (ax + 17, ay), (ax, ay + 10)], fill=(24, 31, 42, 125))

    foot = "Auto-Empirical Research Skills · Stanford REAP x CoPaper.AI"
    foot_font = get_font("sans", 22)
    centered_text(draw, (x + 34, y + h - 42, x + w - 34, y + h - 12), foot, foot_font, COLORS["muted"])


def poster(lang: str) -> Image.Image:
    img = Image.new("RGBA", (W, H), COLORS["paper"] + (255,))
    add_background(img)
    draw = ImageDraw.Draw(img, "RGBA")

    if lang == "en":
        title = "Automated Causal Inference Atlas"
        subtitle = "Auto-Empirical Research Skills · one agent instruction from data to defensible estimates"
        panels = [
            ("Quasi-Experimental ID", ["DID / Event Study", "Staggered DID", "IV / 2SLS / GMM", "RDD: sharp/fuzzy/kink", "SCM / SDID", "Bunching / Shift-share"], COLORS["teal"]),
            ("Observational & Selection", ["OLS / GLM", "Panel FE / RE / FD", "PSM / IPW / EB", "AIPW / TMLE", "Heckman", "Quantile / PPML"], COLORS["blue"]),
            ("ML Causal", ["DML / DoubleML", "Causal Forest / CATE", "Meta-Learners", "TARNet / CFRNet", "DragonNet", "Text Causal"], COLORS["verm"]),
            ("Robustness & Output", ["Spec curve", "Placebo / permutation", "Wild cluster bootstrap", "HonestDID / E-value", "Balance / overlap", "Word · Excel · LaTeX"], COLORS["plum"]),
        ]
        badges = ["900+ StatsPAI functions", "20 methodology skills", "119 repos / 23,000+ Skills"]
        pipeline = ["Clean", "Diagnose", "Identify", "Estimate", "Stress-test", "Publish"]
        title_key, subtitle_key = "display", "sans"
    else:
        title = "自动化因果推断模型图谱"
        subtitle = "Auto-Empirical Research Skills · 一句话从数据到可辩护估计"
        panels = [
            ("准实验识别策略", ["DID / 事件研究", "交错 DID", "IV / 2SLS / GMM", "RDD：sharp/fuzzy/kink", "SCM / SDID", "Bunching / Shift-share"], COLORS["teal"]),
            ("观察数据与选择偏误", ["OLS / GLM", "面板 FE / RE / FD", "PSM / IPW / EB", "AIPW / TMLE", "Heckman 两阶段", "分位数 / PPML"], COLORS["blue"]),
            ("机器学习因果", ["DML / DoubleML", "因果森林 / CATE", "Meta-Learners", "TARNet / CFRNet", "DragonNet", "文本因果"], COLORS["verm"]),
            ("稳健性与发表输出", ["规范曲线", "安慰剂 / 随机置换", "Wild cluster bootstrap", "HonestDID / E-value", "平衡性 / 重叠性", "Word · Excel · LaTeX"], COLORS["plum"]),
        ]
        badges = ["StatsPAI 900+ 函数", "20 个方法论 Skills", "119 个仓库 / 23,000+ Skills"]
        pipeline = ["清洗", "诊断", "识别", "估计", "压力测试", "发表输出"]
        title_key, subtitle_key = "zh_bold", "zh_sans"

    title_font = fit_font(draw, title, title_key, 78 if lang == "en" else 70, 1660)
    subtitle_font = fit_font(draw, subtitle, subtitle_key, 31, 1500)
    centered_text(draw, (120, 48, W - 120, 126), title, title_font, COLORS["ink"])
    centered_text(draw, (120, 132, W - 120, 180), subtitle, subtitle_font, COLORS["muted"])

    badge_x = 475 if lang == "en" else 500
    badge_y = 201
    for i, badge in enumerate(badges):
        badge_x = draw_badge(draw, badge_x, badge_y, badge, [COLORS["amber"], COLORS["teal"], COLORS["blue"]][i], lang) + 18

    draw_connectors(draw)
    draw_panel(draw, 120, 288, 730, 350, *panels[0], lang)
    draw_panel(draw, 1550, 288, 730, 350, *panels[1], lang)
    draw_panel(draw, 120, 758, 730, 350, *panels[2], lang)
    draw_panel(draw, 1550, 758, 730, 350, *panels[3], lang)
    draw_center_engine(draw, lang)
    draw_pipeline(draw, pipeline, lang)

    return img.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lang, name in [
        ("en", "aers-causal-models-poster-en.png"),
        ("zh", "aers-causal-models-poster-cn.png"),
    ]:
        img = poster(lang)
        img.save(OUT_DIR / name, optimize=True, quality=95)
        print(f"wrote {OUT_DIR / name}")


if __name__ == "__main__":
    main()
