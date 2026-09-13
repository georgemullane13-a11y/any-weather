#!/usr/bin/env python3
"""
Generates the raster images the site needs (Open Graph card + Apple touch icon).

Only needed when the branding changes:  pip install pillow && python3 tools/make_images.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
FONT_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

NAVY = (14, 27, 39)
NAVY_2 = (23, 54, 79)
EMBER = (226, 113, 29)
EMBER_L = (244, 162, 92)
SKY = (140, 195, 228)
CREAM = (251, 248, 244)


def font(path, size):
    return ImageFont.truetype(path, size)


def vertical_gradient(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize(size, Image.BILINEAR)


def radial_glow(size, centre, radius, colour, strength=110):
    w, h = size
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    steps = 44
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(strength * (1 - i / steps) ** 2)
        d.ellipse([centre[0] - r, centre[1] - r, centre[0] + r, centre[1] + r], fill=a)
    tint = Image.new("RGB", (w, h), colour)
    return tint, layer


def og_image():
    W, H = 1200, 630
    img = vertical_gradient((W, H), NAVY, NAVY_2)
    for centre, radius, colour, s in (((110, 40), 520, (62, 143, 196), 120),
                                      ((1110, 560), 470, EMBER, 105)):
        tint, mask = radial_glow((W, H), centre, radius, colour, s)
        img = Image.composite(tint, img, mask.point(lambda v: min(v, 96)))

    d = ImageDraw.Draw(img, "RGBA")

    # --- roof illustration, right-hand side -------------------------------- #
    ox, oy = 908, 292
    d.polygon([(ox, oy - 126), (ox + 184, oy + 38), (ox - 184, oy + 38)],
              fill=(29, 59, 85))
    for row in range(5):                      # laid tiles
        y = oy - 84 + row * 25
        half = int((y - (oy - 126)) * (184 / 164))
        x = ox - half + 8
        while x + 44 < ox + half:
            tone = (43, 84, 120) if (row + x) % 3 else (23, 47, 69)
            d.rounded_rectangle([x, y, x + 40, y + 21], 5, fill=tone)
            x += 46
    d.line([(ox - 184, oy + 38), (ox, oy - 126), (ox + 184, oy + 38)],
           fill=EMBER, width=9, joint="curve")
    d.rounded_rectangle([ox - 150, oy + 38, ox + 150, oy + 186], 8, fill=(238, 232, 222))
    d.rounded_rectangle([ox - 192, oy + 30, ox + 192, oy + 48], 9, fill=(10, 20, 29))
    for wx in (ox - 114, ox + 26):            # windows
        d.rounded_rectangle([wx, oy + 74, wx + 88, oy + 142], 6, fill=(29, 59, 85))
        d.line([(wx + 44, oy + 74), (wx + 44, oy + 142)], fill=(238, 232, 222), width=6)
        d.line([(wx, oy + 108), (wx + 88, oy + 108)], fill=(238, 232, 222), width=6)
    d.ellipse([ox + 142, oy - 246, ox + 240, oy - 148], fill=EMBER_L)   # sun

    # --- type, left-hand side ---------------------------------------------- #
    d.text((80, 96), "ANY WEATHER", font=font(FONT_B, 40), fill=SKY)
    d.text((80, 144), "ROOFING", font=font(FONT_B, 94), fill=(255, 255, 255))
    d.rounded_rectangle([80, 262, 188, 270], 4, fill=EMBER)

    d.text((80, 308), "New roofs  ·  Repairs", font=font(FONT_B, 34),
           fill=(214, 230, 242))
    d.text((80, 356), "Flat roofs  ·  Guttering  ·  Chimneys", font=font(FONT_B, 34),
           fill=(214, 230, 242))

    d.rounded_rectangle([80, 434, 476, 506], 36, fill=EMBER)
    d.text((112, 454), "07745 364 538", font=font(FONT_B, 38), fill=(255, 255, 255))

    d.text((82, 538), "Plymouth  ·  24-hour call-out  ·  Free quotes",
           font=font(FONT_R, 28), fill=(150, 178, 200))

    img.save(os.path.join(OUT, "og-image.png"), optimize=True)
    print("wrote assets/img/og-image.png")


def touch_icon():
    S = 720                       # drawn large, downsampled for clean edges
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S, S], S * 0.22, fill=NAVY)
    d.line([(S * .19, S * .55), (S * .5, S * .27), (S * .81, S * .55)],
           fill=EMBER, width=int(S * .085), joint="curve")
    d.line([(S * .285, S * .52), (S * .285, S * .755), (S * .715, S * .755), (S * .715, S * .52)],
           fill=SKY, width=int(S * .062), joint="curve")
    img = img.resize((180, 180), Image.LANCZOS)
    img.save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
    print("wrote assets/img/apple-touch-icon.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    og_image()
    touch_icon()
