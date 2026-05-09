#!/usr/bin/env python3
"""Composite real screenshots onto image2 bases that already include copy."""

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
BASE_DIR = CASE / "05_assets/image2_text_bases"
MASK_JSON = CASE / "05_assets/mask_plan.jd_ai_material.json"
FINAL_DIR = CASE / "06_output/final_comps"
SKETCH_DIR = CASE / "06_output/sketches"


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


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    src_w, src_h = image.size
    scale = max(width / src_w, height / src_h)
    image = image.resize((round(src_w * scale), round(src_h * scale)), Image.LANCZOS)
    left = (image.width - width) // 2
    top = (image.height - height) // 2
    return image.crop((left, top, left + width, top + height))


def rounded_mask(width: int, height: int, radius: int) -> Image.Image:
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
    return mask


def fit_base(name: str, size: tuple[int, int]) -> Image.Image:
    base = Image.open(BASE_DIR / f"{name}_image2_text_base.png").convert("RGBA")
    return cover_crop(base, *size)


def soft_shadow(base: Image.Image, box, radius: int, alpha=70, blur=18, offset=(0, 9)) -> None:
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
    soft_shadow(base, (x, y, x + w, y + h), radius)
    shot.putalpha(mask)
    base.alpha_composite(shot, (x, y))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x, y, x + w, y + h), radius=radius, outline=(255, 255, 255, 235), width=2)


def render_all() -> dict[str, Image.Image]:
    slots = json.loads(MASK_JSON.read_text(encoding="utf-8"))["slots"]
    by_id: dict[str, list[dict]] = {}
    for slot in slots:
        by_id.setdefault(slot["image_id"], []).append(slot)

    specs = {
        "part1-hero": (816, 1054),
        "part2-summary": (816, 1054),
        "part3-01-agent": (816, 982),
        "part3-02-batch": (816, 982),
        "part3-03-confirm": (816, 982),
    }
    outputs: dict[str, Image.Image] = {}
    for name, size in specs.items():
        image = fit_base(name, size)
        for slot in by_id.get(name, []):
            paste_screenshot(image, slot)
        outputs[name] = image
    return outputs


def contact_sheet(subdir: Path, suffix: str, title: str) -> None:
    names = ["part1-hero", "part2-summary", "part3-01-agent", "part3-02-batch", "part3-03-confirm"]
    sheet = Image.new("RGB", (960, 800), "#f4f7fb")
    d = ImageDraw.Draw(sheet)
    d.text((38, 24), title, font=font(34, "bold"), fill="#1d2433")
    d.text((38, 76), "文案排版由 image2 生成  本地仅贴入真实截图", font=font(20), fill="#617088")
    positions = [(30, 110), (318, 110), (606, 110), (30, 485), (318, 485)]
    for name, (x, y) in zip(names, positions):
        thumb = Image.open(subdir / f"{name}{suffix}.png").convert("RGBA")
        thumb.thumbnail((274, 354), Image.LANCZOS)
        sheet.paste(thumb, (x, y), thumb)
        d.text((x + 4, y + thumb.height + 14), name + suffix, font=font(18), fill="#5f6b83")
    sheet.save(subdir / "contact_sheet.png")


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    SKETCH_DIR.mkdir(parents=True, exist_ok=True)
    outputs = render_all()
    for name, image in outputs.items():
        image.save(FINAL_DIR / f"{name}_final.png")
        image.save(SKETCH_DIR / f"{name}_sketch.png")
        print(FINAL_DIR / f"{name}_final.png")
    contact_sheet(FINAL_DIR, "_final", "JD-AI商品素材微应用 详情页完成稿总览")
    contact_sheet(SKETCH_DIR, "_sketch", "JD-AI商品素材微应用 详情页草图总览")


if __name__ == "__main__":
    main()
