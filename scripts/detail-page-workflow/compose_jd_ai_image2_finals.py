#!/usr/bin/env python3
"""Composite JD-AI image2 visual bases with fixed copy and real screenshots."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "cases/jd_ai_material_microapp").exists():
            return path
    raise RuntimeError("Cannot find repo root with cases/jd_ai_material_microapp")


ROOT = find_repo_root(Path(__file__).resolve())
CASE = ROOT / "cases/jd_ai_material_microapp"
BASE_DIR = CASE / "05_assets/image2_bases"
SCREEN_DIR = CASE / "05_assets/screenshots"
MASK_JSON = CASE / "05_assets/mask_plan.jd_ai_material.json"
FINAL_DIR = CASE / "06_output/final_comps"
SKETCH_DIR = CASE / "06_output/sketches"

BLUE = "#2652f6"
TEXT = "#222529"
MUTED = "#687485"
LIGHT = "#fafbfc"


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc" if weight == "bold" else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for item in candidates:
        p = Path(item)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    src_w, src_h = image.size
    scale = max(width / src_w, height / src_h)
    new_size = (round(src_w * scale), round(src_h * scale))
    image = image.resize(new_size, Image.LANCZOS)
    left = (image.width - width) // 2
    top = (image.height - height) // 2
    return image.crop((left, top, left + width, top + height))


def rounded_mask(width: int, height: int, radius: int) -> Image.Image:
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
    return mask


def soft_shadow(base: Image.Image, box, radius: int, alpha=70, blur=20, offset=(0, 10)) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    dx, dy = offset
    d.rounded_rectangle((x0 + dx, y0 + dy, x1 + dx, y1 + dy), radius=radius, fill=(31, 43, 77, alpha))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def paste_screenshot(base: Image.Image, slot: dict) -> None:
    x, y = int(slot["x"]), int(slot["y"])
    w, h = int(slot["width"]), int(slot["height"])
    radius = int(slot.get("corner_radius", 16))
    shot = Image.open(CASE / "05_assets" / slot["asset"]).convert("RGBA")
    shot = cover_crop(shot, w, h)
    mask = rounded_mask(w, h, radius)
    soft_shadow(base, (x, y, x + w, y + h), radius, alpha=72, blur=18, offset=(0, 9))
    shot.putalpha(mask)
    base.alpha_composite(shot, (x, y))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x, y, x + w, y + h), radius=radius, outline=(255, 255, 255, 230), width=2)


def draw_center(d: ImageDraw.ImageDraw, x: int, y: int, text: str, fnt, fill) -> None:
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((x - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


def pill(d: ImageDraw.ImageDraw, box, text: str, fill=(255, 255, 255, 238), outline=None, text_fill=BLUE, size=18) -> None:
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=1)
    draw_center(d, (box[0] + box[2]) // 2, box[1] + max(3, (box[3] - box[1] - size) // 2 - 1), text, font(size, "bold"), text_fill)


def fit_base(name: str, size: tuple[int, int]) -> Image.Image:
    path = BASE_DIR / f"{name}_image2_base.png"
    return cover_crop(Image.open(path).convert("RGBA"), *size)


def paint_text_clear(d: ImageDraw.ImageDraw, box, alpha=238) -> None:
    d.rounded_rectangle(box, radius=10, fill=(250, 251, 252, alpha))


def part1(slots: list[dict]) -> Image.Image:
    im = fit_base("part1-hero", (816, 1054))
    d = ImageDraw.Draw(im)
    pill(d, (70, 58, 200, 92), "欢乐逛出品", size=15)
    paint_text_clear(d, (54, 122, 412, 286), alpha=236)
    d.text((70, 146), "AI商品素材", font=font(39, "bold"), fill=BLUE)
    d.text((70, 208), "对话生成  批量生成商品素材", font=font(22, "bold"), fill=TEXT)
    d.text((70, 252), "京东商家素材生成新方式", font=font(18), fill=MUTED)
    tags = ["主图", "白底图", "透图", "场景图", "卖点图"]
    x = 70
    for tag in tags:
        d.rounded_rectangle((x, 306, x + 58, 330), radius=12, fill=(250, 251, 252, 205), outline=(38, 82, 246, 90))
        draw_center(d, x + 29, 309, tag, font(13), BLUE)
        x += 72
    paint_text_clear(d, (52, 340, 520, 386), alpha=212)
    for slot in slots:
        paste_screenshot(im, slot)
    paint_text_clear(d, (252, 904, 564, 948), alpha=190)
    draw_center(d, 408, 912, "覆盖对话生成 / 批量生成 / 结果确认", font(18), MUTED)
    return im


def part2() -> Image.Image:
    im = fit_base("part2-summary", (816, 1054))
    d = ImageDraw.Draw(im)
    pill(d, (316, 64, 500, 110), "欢乐逛出品", size=22)
    d.rounded_rectangle((132, 138, 612, 286), radius=16, fill=(38, 82, 246, 246))
    d.text((202, 154), "商品素材生产闭环", font=font(48, "bold"), fill="#ffffff")
    d.text((222, 238), "选图提要求  批量出图  失败可重试", font=font(23), fill="#eef4ff")
    d.rounded_rectangle((96, 356, 720, 420), radius=18, fill=(250, 251, 252, 235))
    draw_center(d, 408, 374, "从商品图开始  生成多类经营素材", font(31, "bold"), TEXT)
    d.rounded_rectangle((238, 420, 578, 450), radius=8, fill="#fff2a8")
    draw_center(d, 408, 424, "不用反复下载上传  不满意继续修改", font(19), "#434b57")
    cards = [
        ("多来源选图", ["本地上传", "图片空间", "商品图"]),
        ("对话改图", ["换背景", "换模特", "改颜色"]),
        ("套图生成", ["主图", "搜索图", "规格图"]),
        ("批量生图", ["多商品", "批量提交", "计划生成"]),
        ("多类覆盖", ["白底图", "透图", "场景图", "卖点图"]),
        ("结果可控", ["成功失败", "查看原因", "重新生成"]),
    ]
    x0, y0 = 94, 500
    cw, ch, gx, gy = 188, 156, 34, 31
    for i, (title, tags) in enumerate(cards):
        row, col = divmod(i, 3)
        x, y = x0 + col * (cw + gx), y0 + row * (ch + gy)
        d.rounded_rectangle((x + 18, y + 70, x + cw - 18, y + 126), radius=10, fill=(250, 251, 252, 215))
        draw_center(d, x + cw // 2, y + 74, title, font(23, "bold"), BLUE)
        if len(tags) == 4:
            positions = [(x + 22, y + 108), (x + 98, y + 108), (x + 22, y + 132), (x + 98, y + 132)]
        else:
            positions = [(x + 22, y + 108), (x + 98, y + 108), (x + 60, y + 132)]
        for tag, (tx, ty) in zip(tags, positions):
            d.rounded_rectangle((tx, ty, tx + 68, ty + 21), radius=6, fill=(255, 255, 255, 235))
            draw_center(d, tx + 34, ty + 3, tag, font(12), "#667081")
    d.rounded_rectangle((260, 920, 556, 952), radius=10, fill=(250, 251, 252, 205))
    draw_center(d, 408, 925, "覆盖商品素材从生成到确认的关键步骤", font(17), MUTED)
    return im


def part3(name: str, title: str, subtitle: str, bullets: list[str], note: str, slots: list[dict]) -> Image.Image:
    im = fit_base(name, (816, 982))
    d = ImageDraw.Draw(im)
    pill(d, (70, 58, 184, 88), "欢乐逛出品", size=13)
    paint_text_clear(d, (66, 124, 492, 322), alpha=232)
    d.text((70, 140), title, font=font(31, "bold"), fill=BLUE)
    d.text((70, 188), subtitle, font=font(17), fill="#566275")
    y = 236
    for item in bullets:
        d.ellipse((72, y + 5, 82, y + 15), fill=BLUE)
        d.text((94, y), item, font=font(12), fill="#303846")
        y += 27
    for slot in slots:
        paste_screenshot(im, slot)
    d.rounded_rectangle((210, 890, 606, 925), radius=10, fill=(250, 251, 252, 205))
    draw_center(d, 408, 898, note, font(15), MUTED)
    return im


def contact_sheet(subdir: Path, suffix: str, title: str) -> None:
    files = [
        subdir / f"part1-hero{suffix}.png",
        subdir / f"part2-summary{suffix}.png",
        subdir / f"part3-01-agent{suffix}.png",
        subdir / f"part3-02-batch{suffix}.png",
        subdir / f"part3-03-confirm{suffix}.png",
    ]
    sheet = Image.new("RGB", (960, 800), "#f4f7fb")
    d = ImageDraw.Draw(sheet)
    d.text((38, 24), title, font=font(34, "bold"), fill="#1d2433")
    d.text((38, 76), "全部视觉已走 image2 底稿  真实截图按 mask 合成", font=font(20), fill="#617088")
    positions = [(30, 110), (318, 110), (606, 110), (30, 485), (318, 485)]
    labels = ["part1-hero", "part2-summary", "part3-01-agent", "part3-02-batch", "part3-03-confirm"]
    for path, (x, y), label in zip(files, positions, labels):
        thumb = Image.open(path).convert("RGBA")
        thumb.thumbnail((274, 354), Image.LANCZOS)
        sheet.paste(thumb, (x, y), thumb)
        d.text((x + 4, y + thumb.height + 14), label + suffix, font=font(18), fill="#5f6b83")
    sheet.save(subdir / "contact_sheet.png")


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    SKETCH_DIR.mkdir(parents=True, exist_ok=True)
    slots = json.loads(MASK_JSON.read_text(encoding="utf-8"))["slots"]
    by_id: dict[str, list[dict]] = {}
    for slot in slots:
        by_id.setdefault(slot["image_id"], []).append(slot)
    outputs = {
        "part1-hero": part1(by_id["part1-hero"]),
        "part2-summary": part2(),
        "part3-01-agent": part3(
            "part3-01-agent",
            "对话生图",
            "选图提要求  快速生成商品素材",
            [
                "多来源选图｜本地 / 图片空间 / 商品图都能用",
                "对话式修改｜换背景 / 换模特 / 换颜色",
                "结果可回用｜引用结果 / 继续修改",
            ],
            "主体图 / 场景参考 / 比例选择 / 重新生成",
            by_id["part3-01-agent"],
        ),
        "part3-02-batch": part3(
            "part3-02-batch",
            "批量生图",
            "一次选择商品  多类素材批量生成",
            [
                "多类型覆盖｜白底图 / 透图 / 场景图",
                "商品范围可选｜筛选商品后批量提交计划",
                "原图处理可控｜支持跳过或覆盖原商品图片",
            ],
            "选择商品 / 素材类型 / 提交计划",
            by_id["part3-02-batch"],
        ),
        "part3-03-confirm": part3(
            "part3-03-confirm",
            "结果确认",
            "结果按状态管理  失败可重试",
            [
                "结果分状态｜成功 / 失败 / 跳过 / 执行中",
                "失败可处理｜查看原因 / 单个重试 / 全部重试",
                "结果可查看｜按商品维度查看生成图片",
            ],
            "成功 / 失败 / 执行中 / 重新生成",
            by_id["part3-03-confirm"],
        ),
    }
    for name, image in outputs.items():
        image.save(FINAL_DIR / f"{name}_final.png")
        image.save(SKETCH_DIR / f"{name}_sketch.png")
    contact_sheet(FINAL_DIR, "_final", "JD-AI商品素材微应用 详情页完成稿总览")
    contact_sheet(SKETCH_DIR, "_sketch", "JD-AI商品素材微应用 详情页草图总览")
    for path in sorted(FINAL_DIR.glob("*_final.png")):
        print(path)


if __name__ == "__main__":
    main()
