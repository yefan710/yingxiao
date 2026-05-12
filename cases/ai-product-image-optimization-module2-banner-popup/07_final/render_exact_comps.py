from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


CASE = Path(__file__).resolve().parents[1]
OUT = CASE / "07_final" / "final_comps"
OUT.mkdir(parents=True, exist_ok=True)

FONT_MEDIUM = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_LIGHT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

BLUE = (34, 84, 244)
BLUE_DARK = (19, 56, 207)
TEXT = (34, 37, 41)
MUTED = (76, 83, 92)
TERTIARY = (127, 135, 146)
BG = (238, 246, 255)
LINE = (188, 210, 242)
WHITE = (255, 255, 255)
ORANGE = (255, 126, 72)

ASSETS = {
    "input_1": "/Users/admin/Desktop/折叠椅测试/参考原图/主图4.jpg",
    "input_2": "/Users/admin/Desktop/折叠椅测试/参考原图/主图2.jpg",
    "result_1": "/Users/admin/Desktop/折叠椅测试/1/2/123.png",
    "result_2": "/Users/admin/Desktop/折叠椅测试/1/2/4993b986-90e1-4892-8d00-a2715cd46767.png",
    "result_3": "/Users/admin/Desktop/折叠椅测试/1/2/e2d36e15-28cc-4acc-836e-8c2165ab8a5f.png",
    "result_4": "/Users/admin/Desktop/折叠椅测试/1/2/4e95d222-7a14-42e2-a0f6-334c33025362.png",
    "result_5": "/Users/admin/Desktop/折叠椅测试/1/2/66de7447-389c-4a01-909f-1bd7a1392c72.png",
}

SCALE = 2


def s(value: int | float) -> int:
    return round(value * SCALE)


def sb(x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    return s(x), s(y), s(w), s(h)


def sxy(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int, int, int]:
    return s(x1), s(y1), s(x2), s(y2)


def font(size: int, medium: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if medium else FONT_LIGHT, size)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_center(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill) -> None:
    x, y, w, h = xy
    tw, th = text_size(draw, text, fnt)
    draw.text((x + (w - tw) / 2, y + (h - th) / 2 - 2), text, font=fnt, fill=fill)


def draw_art_text(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill, stroke=(255, 255, 255), stroke_width=3, shadow_fill=(205, 222, 255)) -> None:
    x, y = xy
    draw.text((x + 3, y + 4), text, font=fnt, fill=shadow_fill)
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke_width, stroke_fill=stroke)


def round_rect(draw: ImageDraw.ImageDraw, xy, r: int, fill, outline=None, width=1) -> None:
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def shadow(base: Image.Image, xy, radius: int = 18, opacity: int = 70) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(xy, radius=radius, fill=(80, 120, 190, opacity))
    layer = layer.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(layer, (0, 5))


def cover(path: str, size: tuple[int, int]) -> Image.Image:
    src = Image.open(path).convert("RGB")
    w, h = size
    scale = max(w / src.width, h / src.height)
    src = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    x = (src.width - w) // 2
    y = (src.height - h) // 2
    return src.crop((x, y, x + w, y + h))


def paste_round(base: Image.Image, path: str, box, radius: int, outline=WHITE, outline_width=3) -> None:
    x, y, w, h = box
    img = cover(path, (w, h))
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    base.paste(img, (x, y), mask)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x, y, x + w, y + h), radius=radius, outline=outline, width=outline_width)


def bg(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGBA", size, BG + (255,))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        r = round(245 * (1 - t) + 232 * t)
        g = round(250 * (1 - t) + 242 * t)
        b = round(255 * (1 - t) + 255 * t)
        d.line((0, y, w, y), fill=(r, g, b, 255))
    d.polygon([(w * 0.58, h), (w, h * 0.12), (w, h)], fill=(218, 232, 255, 150))
    d.polygon([(0, 0), (w * 0.18, 0), (0, h * 0.76)], fill=(255, 255, 255, 92))
    return img


def ai_icon(draw: ImageDraw.ImageDraw, x: int, y: int, size: int) -> None:
    round_rect(draw, (x, y, x + size, y + size), size // 5, (229, 239, 255), (161, 194, 255), 2)
    round_rect(draw, (x + 6, y + 6, x + size - 6, y + size - 6), size // 6, BLUE)
    draw_center(draw, (x + 6, y + 5, size - 12, size - 10), "AI", font(round(size * 0.34)), WHITE)


def close_button(draw: ImageDraw.ImageDraw, x: int, y: int, size: int) -> None:
    draw.ellipse((x, y, x + size, y + size), fill=(255, 255, 255, 235), outline=(218, 230, 252), width=2)
    pad = round(size * 0.32)
    draw.line((x + pad, y + pad, x + size - pad, y + size - pad), fill=(133, 151, 181), width=5)
    draw.line((x + size - pad, y + pad, x + pad, y + size - pad), fill=(133, 151, 181), width=5)


def clip_to_popup_frame(img: Image.Image, frame: tuple[int, int, int, int], radius: int) -> Image.Image:
    scale = 4
    mask = Image.new("L", (img.width * scale, img.height * scale), 0)
    md = ImageDraw.Draw(mask)
    scaled_frame = tuple(v * scale for v in frame)
    md.rounded_rectangle(scaled_frame, radius=radius * scale, fill=255)
    mask = mask.resize(img.size, Image.Resampling.LANCZOS)
    clipped = img.copy()
    clipped.putalpha(mask)
    return clipped


def render_banner() -> dict:
    img = bg((2400, 240))
    d = ImageDraw.Draw(img)
    slots = []

    d.polygon([(1560, 240), (2400, 34), (2400, 240)], fill=(210, 226, 255, 145))
    d.rounded_rectangle(sxy(36, 12, 410, 108), radius=s(24), fill=(255, 255, 255, 202))
    source_box = sb(58, 20, 94, 94)
    shadow(img, sxy(58, 20, 152, 114), s(17), 28)
    paste_round(img, ASSETS["input_1"], source_box, s(17), WHITE, s(5))
    slots.append({"id": "banner_source_product", "asset": ASSETS["input_1"], "x": s(58), "y": s(20), "width": s(94), "height": s(94), "corner_radius": s(17)})
    d = ImageDraw.Draw(img)
    for idx, color in enumerate([BLUE, ORANGE, BLUE_DARK]):
        x = s(118 + idx * 18)
        d.ellipse((x, s(25), x + s(13), s(38)), fill=color)
    d.line((s(170), s(64), s(218), s(64)), fill=BLUE, width=s(5))
    d.polygon([(s(218), s(64)), (s(204), s(55)), (s(204), s(73))], fill=BLUE)

    for idx, key in enumerate(["result_3", "result_2", "result_1"]):
        x = 230 + idx * 50
        y = 18 - idx * 2
        box = sb(x, y, 92, 92)
        shadow(img, sxy(x, y, x + 92, y + 92), s(17), 30)
        paste_round(img, ASSETS[key], box, s(17), WHITE, s(5))
        slots.append({"id": f"banner_{key}", "asset": ASSETS[key], "x": s(x), "y": s(y), "width": s(92), "height": s(92), "corner_radius": s(17)})

    d = ImageDraw.Draw(img)
    d.text((s(438), s(21)), "AI 商品图优化功能上线", font=font(s(34)), fill=TEXT)
    d.text((s(440), s(68)), "提取主图/详情图/标题/属性卖点，AI 重新规划生成视觉", font=font(s(18), False), fill=MUTED)
    round_rect(d, sxy(1012, 31, 1150, 89), s(18), BLUE)
    draw_center(d, (s(1012), s(31), s(138), s(58)), "立即体验", font(s(23)), WHITE)

    out = OUT / "ai商品图优化_banner_1200x120.png"
    img.convert("RGB").save(out, quality=96)
    out_2x = OUT / "ai商品图优化_banner_2k_2400x240.png"
    img.convert("RGB").save(out_2x, quality=96)
    return {"path": str(out_2x), "preview_path": str(out), "canvas": {"width": 2400, "height": 240}, "display_canvas": {"width": 1200, "height": 120}, "mask_slots": slots}


def render_popup() -> dict:
    img = Image.new("RGBA", (1500, 1100), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    W, H = 1500, 1100
    for y in range(H):
        t = y / (H - 1)
        r = round(255 * (1 - t) + 239 * t)
        g = round(248 * (1 - t) + 246 * t)
        b = round(249 * (1 - t) + 255 * t)
        d.line((0, y, W, y), fill=(r, g, b, 255))
    d.rounded_rectangle((26, 24, 1474, 1076), radius=14, outline=(220, 232, 255), width=2)
    d.polygon([(980, 24), (1474, 24), (1474, 360), (1240, 306)], fill=(228, 240, 255, 160))
    close_button(d, 1394, 50, 56)

    draw_art_text(d, (122, 68), "AI 商品图优化接入", font(78), TEXT, stroke_width=5, shadow_fill=(207, 224, 255))
    draw_art_text(d, (126, 164), "一个商品多位置素材", font(54), TEXT, stroke_width=3, shadow_fill=(224, 234, 255))
    draw_art_text(d, (650, 164), "批量生成 5 张主图", font(54), BLUE, stroke_width=3, shadow_fill=(224, 234, 255))

    slots = []
    d.rounded_rectangle((124, 250, 446, 308), radius=29, fill=(238, 246, 255), outline=(194, 219, 255), width=2)
    d.text((150, 260), "选择 5 张主图位置", font=font(34), fill=BLUE_DARK)
    shadow(img, (88, 330, 478, 888), 30, 28)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((88, 330, 478, 888), radius=30, fill=WHITE, outline=(232, 239, 248), width=2)
    paste_round(img, ASSETS["input_1"], (120, 362, 326, 326), 20, WHITE, 0)
    d.rounded_rectangle((120, 362, 446, 688), radius=20, outline=(232, 239, 248), width=2)
    slots.append({"id": "popup_source_product", "asset": ASSETS["input_1"], "x": 120, "y": 362, "width": 326, "height": 326, "corner_radius": 20})

    markers = [(174, 428), (292, 394), (358, 512), (214, 628), (350, 660)]
    for idx, (mx, my) in enumerate(markers, 1):
        d.ellipse((mx - 13, my - 13, mx + 13, my + 13), fill=BLUE if idx % 2 else ORANGE, outline=WHITE, width=4)
        d.text((mx - 6, my - 11), str(idx), font=font(18), fill=WHITE)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle((116, 724, 450, 846), radius=22, fill=(245, 250, 255), outline=(210, 229, 255), width=2)
    draw_art_text(d, (142, 742), "提取", font(42), BLUE, stroke_width=2)
    d.text((246, 750), "主图 / 详情页", font=font(30, False), fill=MUTED)
    d.text((246, 790), "标题 / 属性卖点", font=font(30, False), fill=MUTED)

    d.line((506, 610, 580, 610), fill=BLUE, width=9)
    d.polygon([(580, 610), (550, 590), (550, 630)], fill=BLUE)

    d.rounded_rectangle((720, 250, 1068, 308), radius=29, fill=(238, 246, 255), outline=(194, 219, 255), width=2)
    d.text((788, 260), "AI 优化结果", font=font(34), fill=BLUE_DARK)
    shadow(img, (610, 330, 1422, 888), 30, 28)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((610, 330, 1422, 888), radius=30, fill=WHITE, outline=(232, 239, 248), width=2)

    result_boxes = [
        ("result_5", (784, 388, 186, 186)),
        ("result_4", (1018, 388, 186, 186)),
        ("result_3", (676, 608, 186, 186)),
        ("result_2", (910, 608, 186, 186)),
        ("result_1", (1144, 608, 186, 186)),
    ]
    for key, box in result_boxes:
        shadow(img, (box[0], box[1], box[0] + box[2], box[1] + box[3]), 20, 16)
        paste_round(img, ASSETS[key], box, 16, WHITE, 5)
        slots.append({"id": f"popup_{key}", "asset": ASSETS[key], "x": box[0], "y": box[1], "width": box[2], "height": box[3], "corner_radius": 16})

    d = ImageDraw.Draw(img)
    d.rounded_rectangle((785, 814, 1248, 862), radius=24, fill=(238, 246, 255))
    d.text((830, 821), "5 张 1:1 主图优化结果", font=font(32), fill=BLUE_DARK)

    shadow(img, (210, 912, 1290, 1014), 52, 32)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((210, 904, 1290, 1006), radius=51, fill=BLUE)
    draw_center(d, (210, 904, 1080, 102), "立即体验", font(54), WHITE)
    left = "新用户可免费使用 "
    highlight = "8 张图"
    f_plain = font(32, False)
    f_highlight = font(38)
    tw_left, _ = text_size(d, left, f_plain)
    tw_highlight, _ = text_size(d, highlight, f_highlight)
    pill_w = tw_left + tw_highlight + 92
    pill_x = (W - pill_w) // 2
    d.rounded_rectangle((pill_x, 1020, pill_x + pill_w, 1070), radius=25, fill=(245, 250, 255), outline=(204, 224, 255), width=2)
    x0 = pill_x + 46
    d.text((x0, 1027), left, font=f_plain, fill=MUTED)
    d.text((x0 + tw_left, 1022), highlight, font=f_highlight, fill=BLUE)

    img = clip_to_popup_frame(img, (26, 24, 1474, 1076), 14)

    out = OUT / "ai商品图优化_popup_700x550.png"
    img.resize((750, 550), Image.Resampling.LANCZOS).save(out)
    out_2x = OUT / "ai商品图优化_popup_2k_1500x1100.png"
    img.save(out_2x)
    return {"path": str(out_2x), "preview_path": str(out), "canvas": {"width": 1500, "height": 1100}, "display_canvas": {"width": 750, "height": 550}, "mask_slots": slots}


def main() -> None:
    banner = render_banner()
    popup = render_popup()
    manifest = {
        "request_id": "ai-product-image-optimization-module2-banner-popup",
        "note": "Exact-size production comps generated from the approved wireframe and current GaoDing banner/popup specs. Local compositor enforces final canvas and masks real product assets.",
        "specs": {
            "banner": "/Users/admin/Desktop/运营推广材料/服务市场详情页/config/material_specs/banner_gaoding_function_promo.json",
            "popup": "/Users/admin/Desktop/运营推广材料/服务市场详情页/config/material_specs/popup_gaoding_function_promo.json"
        },
        "outputs": {"banner": banner, "popup": popup},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
