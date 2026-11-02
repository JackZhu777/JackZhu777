"""Generate the profile's original GIF banner and reduced-motion PNG.

Requires Pillow. Run from any directory: python scripts/build_header.py
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def font(size, bold=False, mono=False):
    names = (["C:/Windows/Fonts/consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
             if mono else ["C:/Windows/Fonts/segoeui.ttf" if not bold else "C:/Windows/Fonts/segoeuib.ttf",
                           "/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if bold else "") + ".ttf"])
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default(size=size)


def draw_frame(index, still=False):
    image = Image.new("RGB", (960, 300), "#0d1117")
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((1, 1, 958, 298), radius=22, fill="#111923", outline="#283648", width=2)
    d.line((24, 42, 936, 42), fill="#283648")
    for x, color in [(28, "#f97583"), (46, "#e3b341"), (64, "#56d4a0")]:
        d.ellipse((x, 19, x + 8, 27), fill=color)
    d.text((86, 13), "jackzhu777 / about-me", font=font(14, mono=True), fill="#93a4b8")
    d.text((38, 66), "HELLO, WORLD", font=font(15, mono=True), fill="#6ee7ce")
    d.text((36, 91), "Zhuowei Zhu", font=font(49, bold=True), fill="#f0f6fc")
    d.text((39, 158), "UCL  /  Scientific & Data Intensive Computing", font=font(18), fill="#acbdd0")
    phrases = ["Building with Java & Python", "Exploring machine learning", "Designing useful products"]
    phrase = phrases[(index // 36) % 3]
    count = len(phrase) if still else min(len(phrase), (index % 36) * 2)
    d.text((39, 202), "> " + phrase[:count], font=font(21, mono=True), fill="#7dd3fc")
    if not still and index % 8 < 5:
        x = 39 + d.textlength("> " + phrase[:count], font=font(21, mono=True))
        d.rectangle((x + 3, 208, x + 12, 228), fill="#7dd3fc")
    d.text((39, 260), "RESEARCH  /  ENGINEERING  /  PRODUCT", font=font(13, mono=True), fill="#7b8fa9")
    cx, cy = 807, 167
    d.ellipse((cx-86, cy-86, cx+86, cy+86), outline="#2a3c51", width=2)
    points = [(cx + 81*math.cos(a), cy + 81*math.sin(a)) for a in [-math.pi/2, math.pi/6, 5*math.pi/6]]
    for n, (x, y) in enumerate(points):
        d.line((cx, cy, x, y), fill="#35485f", width=2)
        phase = .5 if still else (index % 36) / 36
        px, py = cx + (x-cx)*phase, cy + (y-cy)*phase
        d.ellipse((px-3, py-3, px+3, py+3), fill="#6ee7ce")
        d.rounded_rectangle((x-28, y-17, x+28, y+17), radius=10, fill="#1c2d40", outline="#41617e")
        label = ["ML", "DEV", "UX"][n]
        width = d.textlength(label, font=font(16, mono=True))
        d.text((x-width/2, y-11), label, font=font(16, mono=True), fill="#b4f5e5")
    d.ellipse((cx-38, cy-38, cx+38, cy+38), fill="#1a3343", outline="#6ee7ce", width=2)
    d.text((cx, cy), "Zhuowei", font=font(16, bold=True), fill="#ecfdf5", anchor="mm")
    return image


frames = [draw_frame(i) for i in range(108)]
frames[0].save(ASSETS / "header-zhuowei-v2.gif", save_all=True, append_images=frames[1:],
               duration=100, loop=0, optimize=True, disposal=1)
draw_frame(18, still=True).save(ASSETS / "header-zhuowei-v2.png")
print(f"Generated 108 frames; GIF size: {(ASSETS / 'header-zhuowei-v2.gif').stat().st_size:,} bytes")
