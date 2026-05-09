#!/usr/bin/env python3
"""Render JD service-market main images at 1580x890.

These are horizontal marketplace main images, not the vertical detail-page
screens. They keep copy compact and use real exported UI screenshots.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "cases/jd_ai_material_microapp").exists():
            return path
    raise RuntimeError("Cannot find repo root with cases/jd_ai_material_microapp")


ROOT = find_repo_root(Path(__file__).resolve())
CASE = ROOT / "cases/jd_ai_material_microapp"
SCREEN_DIR = CASE / "05_assets/screenshots"
OUT = CASE / "06_output/final_comps"

W, H = 1580, 890
BLUE = (38, 82, 246)
DEEP = (20, 35, 70)
MUTED = (91, 104, 125)
LIGHT_BLUE = (232, 241, 255)
PALE = (248, 251, 255)
WHITE = (255, 255, 255)
MINT = (213, 245, 232)
YELLOW = (255, 239, 173)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for item in candidates:
        path = Path(item)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def center_text(draw: ImageDraw.ImageDraw, box, text: str, fnt, fill) -> None:
    x0, y0, x1, y1 = box
    tw, th = text_size(draw, text, fnt)
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - th) / 2 - 2), text, font=fnt, fill=fill)


def bg() -> Image.Image:
    im = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        r = round(250 * (1 - t) + 235 * t)
        g = round(252 * (1 - t) + 244 * t)
        b = round(255 * (1 - t) + 255 * t)
        d.line((0, y, W, y), fill=(r, g, b, 255))
    d.ellipse((1160, -180, 1630, 290), fill=(212, 229, 255, 155))
    d.ellipse((-130, 640, 230, 1000), fill=(206, 244, 230, 150))
    d.polygon([(1180, 140), (1580, 30), (1580, 390)], fill=(226, 238, 255, 145))
    return im


def shadow(base: Image.Image, box, radius: int = 28, alpha: int = 42, blur: int = 24) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0, y0 + 10, x1, y1 + 10), radius=radius, fill=(42, 64, 116, alpha))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    w, h = size
    scale = max(w / image.width, h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    x = (resized.width - w) // 2
    y = (resized.height - h) // 2
    return resized.crop((x, y, x + w, y + h))


def contain(image: Image.Image, size: tuple[int, int], bg_color=(255, 255, 255, 255)) -> Image.Image:
    w, h = size
    scale = min(w / image.width, h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, bg_color)
    canvas.alpha_composite(resized, ((w - resized.width) // 2, (h - resized.height) // 2))
    return canvas


def paste_image(base: Image.Image, filename: str, box, mode: str = "contain", radius: int = 24) -> None:
    x, y, w, h = box
    src = Image.open(SCREEN_DIR / filename).convert("RGBA")
    prepared = contain(src, (w, h)) if mode == "contain" else cover(src, (w, h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    shadow(base, (x, y, x + w, y + h), radius=radius)
    prepared.putalpha(mask)
    base.alpha_composite(prepared, (x, y))
    ImageDraw.Draw(base).rounded_rectangle((x, y, x + w, y + h), radius=radius, outline=(255, 255, 255, 235), width=3)


def pill(draw: ImageDraw.ImageDraw, box, text: str, fill=(255, 255, 255, 235), outline=(38, 82, 246, 95), text_fill=BLUE, size=24) -> None:
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=2)
    center_text(draw, box, text, font(size, True), text_fill)


def title_block(draw: ImageDraw.ImageDraw, eyebrow: str, title: str, subtitle: str, accent: str | None = None) -> None:
    pill(draw, (76, 58, 212, 96), eyebrow, size=20)
    draw.text((76, 130), title, font=font(76, True), fill=BLUE)
    if accent and accent in subtitle:
        before, after = subtitle.split(accent, 1)
        x = 80
        draw.text((x, 232), before, font=font(34, True), fill=DEEP)
        bw, _ = text_size(draw, before, font(34, True))
        draw.text((x + bw, 232), accent, font=font(34, True), fill=BLUE)
        aw, _ = text_size(draw, accent, font(34, True))
        draw.text((x + bw + aw, 232), after, font=font(34, True), fill=DEEP)
    else:
        draw.text((80, 232), subtitle, font=font(34, True), fill=DEEP)


def bullet(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, body: str) -> None:
    draw.ellipse((x, y + 10, x + 14, y + 24), fill=BLUE)
    draw.text((x + 28, y), label, font=font(25, True), fill=DEEP)
    lw, _ = text_size(draw, label, font(25, True))
    draw.text((x + 38 + lw, y), body, font=font(25), fill=MUTED)


def card(draw: ImageDraw.ImageDraw, box, title: str, body: str, fill=WHITE) -> None:
    draw.rounded_rectangle(box, radius=22, fill=fill, outline=(215, 229, 255), width=2)
    draw.text((box[0] + 26, box[1] + 24), title, font=font(28, True), fill=BLUE)
    draw.text((box[0] + 26, box[1] + 70), body, font=font(22), fill=MUTED)


def save_jpg(im: Image.Image, name: str) -> Path:
    path = OUT / name
    rgb = im.convert("RGB")
    for quality in (92, 88, 84, 80):
        rgb.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
        if path.stat().st_size <= 3 * 1024 * 1024:
            break
    return path


def main_overview() -> Path:
    im = bg()
    d = ImageDraw.Draw(im)
    title_block(d, "欢乐逛出品", "AI商品素材", "对话生成  批量生成商品素材", "批量生成")
    for i, text in enumerate(["主图", "白底图", "透图", "场景图", "卖点图"]):
        pill(d, (78 + i * 118, 306, 166 + i * 118, 346), text, fill=(250, 252, 255, 230), size=20)
    bullet(d, 86, 410, "多类素材｜", "主图、场景图、卖点图统一生成")
    bullet(d, 86, 462, "结果可控｜", "查看结果，失败可重试")
    paste_image(im, "part1_hero_product_ui.png", (548, 150, 900, 600), "contain", 32)
    d.rounded_rectangle((610, 780, 1160, 824), radius=22, fill=(250, 252, 255, 210))
    center_text(d, (610, 780, 1160, 824), "覆盖对话生成 / 批量生成 / 结果确认", font(24), MUTED)
    return save_jpg(im, "service_market_main_01_overview_1580x890.jpg")


def main_dialog() -> Path:
    im = bg()
    d = ImageDraw.Draw(im)
    title_block(d, "功能演示", "对话生图", "选图提要求  快速生成商品素材", "快速生成")
    bullet(d, 82, 336, "多来源选图｜", "本地、图片空间、商品图都能用")
    bullet(d, 82, 388, "对话式修改｜", "换背景、换模特、改颜色")
    bullet(d, 82, 440, "结果可回用｜", "引用结果继续修改")
    paste_image(im, "part3-01_agent_home.png", (640, 108, 780, 350), "cover", 30)
    paste_image(im, "part3-01_agent_result.png", (540, 520, 840, 270), "contain", 28)
    return save_jpg(im, "service_market_main_02_dialog_generate_1580x890.jpg")


def main_batch() -> Path:
    im = bg()
    d = ImageDraw.Draw(im)
    title_block(d, "核心优势", "批量生图", "一次选择商品  多类素材批量生成", "批量生成")
    bullet(d, 82, 336, "多商品处理｜", "筛选商品后批量提交计划")
    bullet(d, 82, 388, "多类型覆盖｜", "白底图、透图、场景图")
    bullet(d, 82, 440, "原图可控｜", "支持跳过或覆盖原商品图")
    paste_image(im, "part3-02_batch_generate.png", (620, 170, 820, 560), "contain", 32)
    card(d, (82, 540, 396, 652), "批量提交", "适合海量 SKU 运营")
    card(d, (82, 680, 396, 792), "计划生成", "统一管理生成任务")
    return save_jpg(im, "service_market_main_03_batch_generate_1580x890.jpg")


def main_confirm() -> Path:
    im = bg()
    d = ImageDraw.Draw(im)
    title_block(d, "流程闭环", "结果确认", "按状态管理生成结果  失败可重试", "失败可重试")
    bullet(d, 82, 336, "状态清晰｜", "成功、失败、跳过、执行中")
    bullet(d, 82, 388, "失败处理｜", "查看原因，单张或批量重试")
    bullet(d, 82, 440, "结果查看｜", "按商品维度查看生成图片")
    paste_image(im, "part3-03_task_detail.png", (620, 190, 820, 380), "contain", 32)
    d.rounded_rectangle((650, 626, 1248, 678), radius=26, fill=(250, 252, 255, 230), outline=(205, 224, 255), width=2)
    center_text(d, (650, 626, 1248, 678), "生成后确认效果，不满意可继续处理", font(27, True), BLUE)
    return save_jpg(im, "service_market_main_04_result_confirm_1580x890.jpg")


def main_coverage() -> Path:
    im = bg()
    d = ImageDraw.Draw(im)
    title_block(d, "场景应用", "多类素材覆盖", "从商品图开始  生成多类经营素材", "多类经营素材")
    cards = [
        ("主图", "商品首屏展示"),
        ("白底图", "适配平台规范"),
        ("透图", "灵活组合场景"),
        ("场景图", "突出使用氛围"),
        ("卖点图", "强化商品利益点"),
    ]
    x_positions = [88, 358, 628, 898, 1168]
    colors = [(238, 246, 255), (236, 250, 244), (255, 246, 222), (240, 244, 255), (247, 242, 255)]
    for idx, ((title, body), x) in enumerate(zip(cards, x_positions)):
        d.rounded_rectangle((x, 348, x + 224, 602), radius=28, fill=colors[idx], outline=(216, 228, 246), width=2)
        d.ellipse((x + 56, 390, x + 168, 502), fill=WHITE)
        center_text(d, (x + 56, 390, x + 168, 502), str(idx + 1), font(40, True), BLUE)
        center_text(d, (x, 520, x + 224, 562), title, font(32, True), BLUE if idx % 2 == 0 else (26, 154, 113))
        center_text(d, (x, 566, x + 224, 600), body, font(20), MUTED)
    d.rounded_rectangle((338, 680, 1242, 744), radius=32, fill=(250, 252, 255, 225), outline=(206, 225, 255), width=2)
    center_text(d, (338, 680, 1242, 744), "覆盖商家常用素材坑位，减少重复制作和上传", font(28, True), DEEP)
    return save_jpg(im, "service_market_main_05_material_coverage_1580x890.jpg")


def contact_sheet(paths: list[Path]) -> None:
    sheet = Image.new("RGB", (1580, 1780), "#f4f7fb")
    d = ImageDraw.Draw(sheet)
    d.text((48, 40), "JD-AI商品素材微应用 服务市场主图总览", font=font(48, True), fill=DEEP)
    d.text((50, 108), "规格：1580x890，单张建议 3M 内，内容为功能演示 + 核心优势", font=font(26), fill=MUTED)
    for idx, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        im.thumbnail((720, 406), Image.Resampling.LANCZOS)
        x = 50 + (idx % 2) * 760
        y = 170 + (idx // 2) * 520
        sheet.paste(im, (x, y))
        d.text((x, y + 424), path.name, font=font(22), fill=DEEP)
    sheet.save(OUT / "service_market_main_contact_sheet.jpg", "JPEG", quality=90, optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [main_overview(), main_dialog(), main_batch(), main_confirm(), main_coverage()]
    contact_sheet(paths)
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
