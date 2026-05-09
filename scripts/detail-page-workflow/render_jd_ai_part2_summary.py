#!/usr/bin/env python3
"""Render the JD-AI part2 summary comp with the summary-header palette."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "cases/jd_ai_material_microapp").exists():
            return path
    raise RuntimeError("Cannot find repo root with cases/jd_ai_material_microapp")


ROOT = find_repo_root(Path(__file__).resolve())
FINAL_DIR = ROOT / "cases/jd_ai_material_microapp/06_output/final_comps"
SKETCH_DIR = ROOT / "cases/jd_ai_material_microapp/06_output/sketches"

W, H = 816, 1054
BLUE = "#2652f6"
BLUE_DARK = "#2148da"
BLUE_GRAY = "#c3d3e4"
WARM_GRAY = "#e3e2db"
MINT = "#e1f6eb"
NEAR_WHITE = "#fafbfc"
TEXT = "#222529"
MUTED = "#687485"


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc" if weight == "bold" else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for item in candidates:
        path = Path(item)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def mix(a: str, b: str, t: float) -> tuple[int, int, int]:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return (
        round(ar * (1 - t) + br * t),
        round(ag * (1 - t) + bg * t),
        round(ab * (1 - t) + bb * t),
    )


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_center(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - (bbox[2] - bbox[0]) / 2, y), text, font=fnt, fill=fill)


def soft_shadow(size: tuple[int, int], box, radius: int, alpha: int = 70, blur: int = 24, offset=(0, 12)):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    dx, dy = offset
    d.rounded_rectangle((x0 + dx, y0 + dy, x1 + dx, y1 + dy), radius=radius, fill=(23, 37, 84, alpha))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def draw_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, kind: str, color: str):
    draw.ellipse((cx - 31, cy - 31, cx + 31, cy + 31), fill=color)
    white = "#ffffff"
    if kind == "upload":
        draw.rounded_rectangle((cx - 15, cy - 6, cx + 15, cy + 18), radius=5, outline=white, width=4)
        draw.line((cx, cy - 19, cx, cy + 8), fill=white, width=4)
        draw.polygon([(cx, cy - 21), (cx - 11, cy - 8), (cx + 11, cy - 8)], fill=white)
    elif kind == "chat":
        draw.rounded_rectangle((cx - 18, cy - 13, cx + 18, cy + 10), radius=7, outline=white, width=4)
        draw.polygon([(cx - 5, cy + 10), (cx - 14, cy + 20), (cx + 7, cy + 10)], fill=white)
    elif kind == "tiles":
        for ox, oy in [(-14, -14), (5, -14), (-14, 5), (5, 5)]:
            draw.rounded_rectangle((cx + ox, cy + oy, cx + ox + 12, cy + oy + 12), radius=3, fill=white)
    elif kind == "batch":
        for i in range(3):
            draw.rounded_rectangle((cx - 18 + i * 9, cy - 16 + i * 8, cx + 8 + i * 9, cy + 10 + i * 8), radius=4, outline=white, width=3)
    elif kind == "cover":
        draw.rounded_rectangle((cx - 19, cy - 16, cx + 19, cy + 16), radius=5, outline=white, width=4)
        draw.line((cx - 11, cy - 3, cx + 11, cy - 3), fill=white, width=4)
        draw.line((cx - 11, cy + 8, cx + 6, cy + 8), fill=white, width=4)
    else:
        draw.rounded_rectangle((cx - 17, cy - 17, cx + 17, cy + 17), radius=7, outline=white, width=4)
        draw.line((cx - 9, cy + 2, cx - 1, cy + 10), fill=white, width=4)
        draw.line((cx - 1, cy + 10, cx + 13, cy - 10), fill=white, width=4)


def render() -> Image.Image:
    img = Image.new("RGBA", (W, H), NEAR_WHITE)
    draw = ImageDraw.Draw(img)

    for y in range(420):
        t = y / 419
        color = mix(BLUE, BLUE_DARK, t * 0.65)
        draw.line((0, y, W, y), fill=color)

    # Low-saturation reference shapes from the approved head-image palette.
    draw.ellipse((-70, -120, 170, 155), outline=(195, 211, 228, 135), width=3)
    draw.ellipse((580, 40, 900, 380), outline=(195, 211, 228, 165), width=3)
    draw.ellipse((652, 94, 836, 278), fill=(250, 251, 252, 248))
    draw.ellipse((632, 190, 785, 345), outline=(250, 251, 252, 205), width=3)
    draw.polygon([(585, 250), (795, 380), (585, 380)], fill=(195, 211, 228, 180))

    rounded(draw, (315, 58, 501, 112), 28, NEAR_WHITE)
    text_center(draw, (408, 72), "欢乐逛出品", font(24, "bold"), BLUE)
    text_center(draw, (408, 154), "商品素材生产闭环", font(50, "bold"), "#ffffff")
    text_center(draw, (408, 244), "选图提要求  批量出图  失败可重试", font(25), "#eef4ff")

    panel = (46, 356, 770, 1002)
    img.alpha_composite(soft_shadow((W, H), panel, 24, alpha=65, blur=24, offset=(0, 18)))
    rounded(draw, panel, 24, (250, 251, 252, 248), outline=(255, 255, 255, 220), width=2)
    text_center(draw, (408, 394), "从商品图开始  生成多类经营素材", font(33, "bold"), TEXT)
    rounded(draw, (236, 438, 580, 470), 7, "#fff3a8")
    text_center(draw, (408, 441), "不用反复下载上传  不满意继续修改", font(21), "#3f4855")

    cards = [
        ("1", "多来源选图", ["本地上传", "图片空间", "商品图"], "upload", "#eef4fb", BLUE),
        ("2", "对话改图", ["换背景", "换模特", "改颜色"], "chat", MINT, BLUE),
        ("3", "套图生成", ["主图", "搜索图", "规格图"], "tiles", WARM_GRAY, BLUE),
        ("4", "批量生图", ["多商品", "批量提交", "计划生成"], "batch", MINT, BLUE),
        ("5", "多类覆盖", ["白底图", "透图", "场景图", "卖点图"], "cover", "#f4f0e8", BLUE),
        ("6", "结果可控", ["成功失败", "查看原因", "重新生成"], "check", "#eef4fb", BLUE),
    ]
    start_x, start_y = 78, 520
    card_w, card_h = 202, 174
    gap_x, gap_y = 28, 22
    for idx, (num, title, tags, icon, bg, accent) in enumerate(cards):
        row, col = divmod(idx, 3)
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        img.alpha_composite(soft_shadow((W, H), (x, y, x + card_w, y + card_h), 14, alpha=45, blur=14, offset=(0, 9)))
        rounded(draw, (x, y, x + card_w, y + card_h), 14, bg, outline=(255, 255, 255, 235), width=2)
        draw.ellipse((x + 18, y + 18, x + 52, y + 52), fill="#ffffff")
        text_center(draw, (x + 35, y + 24), num, font(15, "bold"), accent)
        draw_icon(draw, x + card_w // 2, y + 58, icon, accent)
        text_center(draw, (x + card_w // 2, y + 101), title, font(25, "bold"), accent)
        if len(tags) == 4:
            tag_positions = [(x + 24, y + 124), (x + 108, y + 124), (x + 24, y + 148), (x + 108, y + 148)]
            tag_w = 72
        else:
            tag_positions = [(x + 24, y + 124), (x + 108, y + 124), (x + 66, y + 148)]
            tag_w = 72
        for text, (tx, ty) in zip(tags, tag_positions):
            rounded(draw, (tx, ty, tx + tag_w, ty + 24), 6, (255, 255, 255, 235))
            text_center(draw, (tx + tag_w / 2, ty + 4), text, font(13), "#5c6674")

    text_center(draw, (408, 946), "覆盖商品素材从生成到确认的关键步骤", font(19), MUTED)
    return img


def main() -> None:
    img = render()
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    SKETCH_DIR.mkdir(parents=True, exist_ok=True)
    for path in [
        FINAL_DIR / "part2-summary_final.png",
        SKETCH_DIR / "part2-summary_sketch.png",
    ]:
        img.save(path)
        print(path)


if __name__ == "__main__":
    main()
