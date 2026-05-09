from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


OUT = Path(__file__).resolve().parent
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"

BLUE = (22, 91, 246)
TEXT = (25, 36, 56)
MUTED = (94, 106, 125)
BG = (239, 246, 255)
LINE = (188, 208, 236)
WHITE = (255, 255, 255)
ORANGE = (255, 126, 72)


def font(size, medium=True):
    return ImageFont.truetype(FONT_MEDIUM if medium else FONT_LIGHT, size)


def fit_cover(path, size):
    src = Image.open(path).convert("RGB")
    w, h = size
    scale = max(w / src.width, h / src.height)
    src = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    x = (src.width - w) // 2
    y = (src.height - h) // 2
    return src.crop((x, y, x + w, y + h))


def rounded_paste(base, path, box, radius=14):
    x, y, w, h = box
    img = fit_cover(path, (w, h))
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    base.paste(img, (x, y), mask)


def round_rect(draw, xy, r, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def render_banner():
    img = Image.new("RGB", (1200, 120), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1200, 120), fill=(237, 246, 255))
    rounded_paste(img, "/Users/admin/Desktop/折叠椅测试/参考原图/主图4.jpg", (52, 17, 84, 84), 14)
    d.rounded_rectangle((52, 17, 136, 101), radius=14, outline=WHITE, width=4)
    d.text((66, 102), "原商品", font=font(12, False), fill=MUTED)
    for idx, label in enumerate(["1", "2", "3"]):
        x = 108 + idx * 18
        d.ellipse((x, 20, x + 15, 35), fill=BLUE)
        d.text((x + 4, 21), label, font=font(10), fill=WHITE)
    d.line((148, 58, 194, 58), fill=BLUE, width=4)
    d.polygon([(194, 58), (181, 50), (181, 66)], fill=BLUE)
    result_paths = [
        "/Users/admin/Desktop/折叠椅测试/1/2/e2d36e15-28cc-4acc-836e-8c2165ab8a5f.png",
        "/Users/admin/Desktop/折叠椅测试/1/2/4993b986-90e1-4892-8d00-a2715cd46767.png",
        "/Users/admin/Desktop/折叠椅测试/1/2/123.png",
    ]
    for idx, path in enumerate(result_paths):
        x = 204 + idx * 44
        y = 16 - idx * 2
        rounded_paste(img, path, (x, y, 80, 80), 14)
        d.rounded_rectangle((x, y, x + 80, y + 80), radius=14, outline=WHITE, width=4)
    d.text((211, 101), "生成 3 张主图", font=font(13, False), fill=MUTED)

    d.text((390, 22), "AI 商品图优化功能上线", font=font(30), fill=TEXT)
    d.text((390, 64), "选择一个商品 3 个位置，生成 3 张新主图", font=font(18, False), fill=TEXT)
    round_rect(d, (720, 18, 890, 54), 13, WHITE, LINE)
    d.text((737, 28), "多店铺管理 - AI 商品图", font=font(14), fill=BLUE)
    round_rect(d, (944, 30, 1140, 88), 29, BLUE)
    d.text((993, 47), "立即体验", font=font(24), fill=WHITE)
    return img


def render_popup():
    img = Image.new("RGB", (700, 550), WHITE)
    d = ImageDraw.Draw(img)
    round_rect(d, (110, 50, 590, 530), 24, (235, 243, 255), None)
    d.text((145, 86), "AI 商品图优化", font=font(32), fill=TEXT)
    d.text((146, 126), "功能上线", font=font(28), fill=TEXT)
    d.text((146, 165), "选择多个位置主图，AI 自动提炼卖点", font=font(18, False), fill=TEXT)

    rounded_paste(img, "/Users/admin/Desktop/折叠椅测试/参考原图/主图4.jpg", (420, 78, 82, 82), 14)
    d.rounded_rectangle((420, 78, 502, 160), radius=14, outline=WHITE, width=4)
    result_paths = [
        "/Users/admin/Desktop/折叠椅测试/1/2/e2d36e15-28cc-4acc-836e-8c2165ab8a5f.png",
        "/Users/admin/Desktop/折叠椅测试/1/2/4993b986-90e1-4892-8d00-a2715cd46767.png",
        "/Users/admin/Desktop/折叠椅测试/1/2/123.png",
    ]
    for idx, path in enumerate(result_paths):
        x = 495 + idx * 20
        y = 88 - idx * 8
        rounded_paste(img, path, (x, y, 82, 82), 14)
        d.rounded_rectangle((x, y, x + 82, y + 82), radius=14, outline=WHITE, width=4)
    d.line((508, 120, 487, 120), fill=BLUE, width=4)
    d.polygon([(508, 120), (497, 112), (497, 128)], fill=BLUE)

    round_rect(d, (128, 193, 572, 515), 20, WHITE, None)
    bullets = [
        ("选择多个位置主图", "一次整理一组商品素材"),
        ("AI 自动提炼商品卖点", "基于原图、详情图、属性和标题"),
        ("生成多张新主图", "多套效果图叠放预览"),
    ]
    y = 230
    for idx, (title, desc) in enumerate(bullets):
        cy = y + idx * 70
        d.ellipse((176, cy + 8, 184, cy + 16), fill=ORANGE)
        d.text((202, cy), title, font=font(21), fill=BLUE)
        d.text((202, cy + 34), desc, font=font(16, False), fill=MUTED)

    round_rect(d, (158, 440, 542, 500), 30, BLUE)
    d.text((312, 457), "去体验", font=font(25), fill=WHITE)
    return img


def main():
    banner = render_banner()
    popup = render_popup()
    banner.save(OUT / "banner_wireframe.png", quality=95)
    popup.save(OUT / "popup_wireframe.png", quality=95)


if __name__ == "__main__":
    main()
