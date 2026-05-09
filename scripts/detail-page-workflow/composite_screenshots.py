#!/usr/bin/env python3
"""Paste real screenshots into a detail-page layout draft by mask coordinates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError as exc:
        raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc
    return Image, ImageDraw, ImageFilter


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_asset(asset: str, assets_dir: Path) -> Path:
    path = Path(asset)
    if path.is_absolute():
        return path
    return assets_dir / path


def cover_crop(image, width: int, height: int):
    src_w, src_h = image.size
    scale = max(width / src_w, height / src_h)
    new_size = (round(src_w * scale), round(src_h * scale))
    image = image.resize(new_size)
    left = (image.width - width) // 2
    top = (image.height - height) // 2
    return image.crop((left, top, left + width, top + height))


def contain_pad(image, width: int, height: int, background=(255, 255, 255, 0)):
    src_w, src_h = image.size
    scale = min(width / src_w, height / src_h)
    new_size = (round(src_w * scale), round(src_h * scale))
    image = image.resize(new_size)
    canvas = image.__class__.new("RGBA", (width, height), background)
    left = (width - image.width) // 2
    top = (height - image.height) // 2
    canvas.alpha_composite(image, (left, top))
    return canvas


def rounded_mask(width: int, height: int, radius: int):
    Image, ImageDraw, _ = load_pillow()
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
    return mask


def paste_slot(base, slot: dict, assets_dir: Path):
    Image, ImageDraw, ImageFilter = load_pillow()
    x = int(slot["x"])
    y = int(slot["y"])
    width = int(slot["width"])
    height = int(slot["height"])
    radius = int(slot.get("corner_radius", 0))
    fit_mode = slot.get("fit_mode", "cover_crop")
    asset_path = resolve_asset(slot["asset"], assets_dir)
    if not asset_path.exists():
        raise SystemExit(f"Missing asset for slot {slot.get('slot', '')}: {asset_path}")

    shot = Image.open(asset_path).convert("RGBA")
    if fit_mode == "cover_crop":
        shot = cover_crop(shot, width, height)
    elif fit_mode == "contain_pad":
        shot = contain_pad(shot, width, height)
    elif fit_mode == "native_scale":
        shot = shot.resize((width, height))
    else:
        raise SystemExit(f"Unknown fit_mode: {fit_mode}")

    mask = rounded_mask(width, height, radius)

    shadow = slot.get("shadow")
    if shadow:
        blur = int(shadow.get("blur", 18))
        offset_x = int(shadow.get("offset_x", 0))
        offset_y = int(shadow.get("offset_y", 8))
        alpha = int(shadow.get("alpha", 40))
        shadow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        shadow_shape = Image.new("RGBA", (width, height), (0, 0, 0, alpha))
        shadow_shape.putalpha(mask)
        shadow_layer.alpha_composite(shadow_shape, (x + offset_x, y + offset_y))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur))
        base.alpha_composite(shadow_layer)

    shot.putalpha(mask)
    base.alpha_composite(shot, (x, y))

    stroke = slot.get("stroke")
    if stroke:
        draw = ImageDraw.Draw(base)
        color = stroke.get("color", "#1b44f0")
        stroke_width = int(stroke.get("width", 2))
        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=radius,
            outline=color,
            width=stroke_width,
        )


def composite(args: argparse.Namespace) -> None:
    Image, _, _ = load_pillow()
    draft = Path(args.draft).resolve()
    mask_json = Path(args.mask_json).resolve()
    out = Path(args.out).resolve()
    assets_dir = Path(args.assets_dir).resolve()

    spec = read_json(mask_json)
    base = Image.open(draft).convert("RGBA")
    slots = sorted(spec.get("slots", []), key=lambda item: int(item.get("z_index", 0)))
    for slot in slots:
        paste_slot(base, slot, assets_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    base.save(out)
    print(f"Composited: {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Paste real screenshots into a draft image.")
    parser.add_argument("--draft", required=True, help="Layout draft image path")
    parser.add_argument("--mask-json", required=True, help="Mask coordinate JSON path")
    parser.add_argument("--assets-dir", required=True, help="Directory containing real screenshots")
    parser.add_argument("--out", required=True, help="Output image path")
    composite(parser.parse_args())


if __name__ == "__main__":
    main()
