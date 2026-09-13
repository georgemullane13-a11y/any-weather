#!/usr/bin/env python3
"""
Generates the raster assets: the Open Graph card, the Apple touch icon, and
PLACEHOLDER photography for the hero slideshow, before/after sliders and the
work gallery.

    pip install pillow && python3 tools/make_images.py

Replacing the placeholders with real photos is a straight file swap — keep the
filenames and the aspect ratios listed in PHOTOS below and nothing else has to
change. See README.md.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
PHOTO = os.path.join(IMG, "photos")
FONT_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

NAVY = (10, 31, 51)
NAVY_2 = (18, 58, 94)
BLUE = (30, 139, 255)
BLUE_D = (11, 111, 214)
WHITE = (255, 255, 255)
MIST = (241, 245, 249)


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient(size, top, bottom):
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return strip.resize(size, Image.BILINEAR)


def grain(img, amount=7):
    """A little luminance noise so the placeholders read as photography."""
    w, h = img.size
    rnd = random.Random(7)
    noise = Image.new("L", (w // 2, h // 2))
    noise.putdata([128 + rnd.randint(-amount * 4, amount * 4) for _ in range(
        (w // 2) * (h // 2))])
    noise = noise.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
    return Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.06)


def vignette(img, strength=0.26):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.40, -h * 0.48, w * 1.40, h * 1.48], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.12))
    dark = Image.new("RGB", (w, h), (6, 16, 28))
    return Image.composite(img, Image.blend(img, dark, strength), mask)


# --------------------------------------------------------------------------- #
#  Roof scene — the placeholder "photograph"
# --------------------------------------------------------------------------- #

def roof_scene(w, h, after, seed=1):
    """A stylised hip-roof scene. `after` swaps a tired roof for a finished one."""
    rnd = random.Random(seed)
    sky = ((78, 134, 184), (196, 218, 234)) if after else ((124, 136, 148), (196, 203, 210))
    img = gradient((w, h), *sky)
    d = ImageDraw.Draw(img, "RGBA")

    horizon = int(h * 0.46)

    # cloud banks
    for i in range(5):
        cx = rnd.randint(0, w); cy = rnd.randint(int(h * .05), int(h * .32))
        rx = rnd.randint(int(w * .12), int(w * .26)); ry = rnd.randint(int(h * .03), int(h * .07))
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                  fill=(255, 255, 255, 54 if after else 92))

    # distant rooftops and treeline
    for i in range(9):
        bx = int(w * (i / 9.0)) - rnd.randint(0, 40)
        bw = rnd.randint(int(w * .10), int(w * .18))
        bh = rnd.randint(int(h * .05), int(h * .11))
        tone = (108, 122, 136) if after else (116, 124, 132)
        d.rectangle([bx, horizon - bh, bx + bw, horizon + 8], fill=tone + (200,))
        d.polygon([(bx - 8, horizon - bh), (bx + bw // 2, horizon - bh - int(h * .035)),
                   (bx + bw + 8, horizon - bh)], fill=(86, 98, 112, 210))
    for i in range(14):
        tx = rnd.randint(0, w); tr = rnd.randint(int(h * .03), int(h * .06))
        d.ellipse([tx - tr, horizon - tr * 2, tx + tr, horizon + tr // 2],
                  fill=(58, 82, 62, 190) if after else (64, 78, 64, 190))

    # ---- the main roof: two planes meeting at a ridge ---------------------- #
    ridge_y = int(h * 0.50)
    eave_y = int(h * 0.96)
    ridge_l, ridge_r = int(w * 0.30), int(w * 0.72)
    eave_l, eave_r = int(w * -0.06), int(w * 1.06)

    base = (58, 64, 70) if after else (96, 98, 88)
    d.polygon([(ridge_l, ridge_y), (ridge_r, ridge_y), (eave_r, eave_y), (eave_l, eave_y)],
              fill=base)

    rows = 22
    for r in range(rows):
        t0 = r / rows
        t1 = (r + 1) / rows
        y0 = ridge_y + (eave_y - ridge_y) * t0
        y1 = ridge_y + (eave_y - ridge_y) * t1
        x0 = ridge_l + (eave_l - ridge_l) * t0
        x1 = ridge_r + (eave_r - ridge_r) * t0
        tile_w = (x1 - x0) / (12 + r * 0.9)
        offset = (tile_w / 2) if r % 2 else 0
        x = x0 - offset
        while x < x1:
            if after:
                shade = rnd.randint(-10, 10)
                col = (52 + shade, 58 + shade, 66 + shade)
            else:
                shade = rnd.randint(-22, 22)
                col = (104 + shade, 104 + shade, 92 + shade)
            d.rounded_rectangle([x, y0, x + tile_w * 0.93, y1 + 2],
                                radius=max(2, int(tile_w * 0.12)), fill=col)
            x += tile_w

        if not after and r > 3 and rnd.random() < 0.30:      # missing / slipped tiles
            gx = rnd.uniform(x0, x1 - tile_w * 2)
            d.rectangle([gx, y0, gx + tile_w * rnd.uniform(1, 2.2), y1], fill=(48, 42, 36))
        if not after and rnd.random() < 0.85:                 # moss
            for _ in range(rnd.randint(2, 7)):
                mx = rnd.uniform(x0, x1); my = rnd.uniform(y0, y1)
                mr = rnd.uniform(tile_w * .3, tile_w * 1.1)
                d.ellipse([mx - mr, my - mr * .5, mx + mr, my + mr * .5],
                          fill=(96 + rnd.randint(-14, 14), 112 + rnd.randint(-14, 14), 62, 205))

    # ridge capping
    d.rounded_rectangle([ridge_l - 10, ridge_y - int(h * .022), ridge_r + 10,
                         ridge_y + int(h * .012)], radius=int(h * .014),
                        fill=(44, 50, 58) if after else (118, 114, 100))

    # chimney
    cx0, cx1 = int(w * 0.60), int(w * 0.72)
    cy0, cy1 = int(h * 0.24), int(h * 0.60)
    brick = (150, 96, 78) if after else (132, 96, 82)
    d.rectangle([cx0, cy0, cx1, cy1], fill=brick)
    for by in range(cy0, cy1, max(6, int(h * .016))):
        d.line([(cx0, by), (cx1, by)], fill=(brick[0] - 22, brick[1] - 18, brick[2] - 16), width=2)
    d.rectangle([cx0 - 8, cy0 - int(h * .018), cx1 + 8, cy0], fill=(96, 102, 110))
    d.rectangle([cx0 + 8, cy0 - int(h * .05), cx0 + 30, cy0 - int(h * .016)], fill=(70, 74, 80))
    if after:                                                  # crisp new lead flashing
        d.polygon([(cx0 - 6, cy1), (cx1 + 6, cy1), (cx1 + 22, cy1 + int(h * .05)),
                   (cx0 - 22, cy1 + int(h * .05))], fill=(152, 160, 170))
    else:
        d.polygon([(cx0 - 6, cy1), (cx1 + 6, cy1), (cx1 + 18, cy1 + int(h * .04)),
                   (cx0 - 18, cy1 + int(h * .04))], fill=(126, 122, 112))

    # scaffolding
    pole = (176, 180, 186, 235)
    for px in (int(w * 0.06), int(w * 0.92)):
        d.rectangle([px, int(h * .30), px + max(4, int(w * .006)), h], fill=pole)
    d.rectangle([0, int(h * .885), w, int(h * .885) + max(5, int(h * .012))], fill=pole)

    return vignette(grain(img))


def flat_scene(w, h, after, seed=1):
    """A single-storey flat roof seen from the scaffold — the other placeholder."""
    rnd = random.Random(seed)
    sky = ((86, 142, 190), (198, 220, 236)) if after else ((126, 138, 150), (198, 205, 212))
    img = gradient((w, h), *sky)
    d = ImageDraw.Draw(img, "RGBA")
    horizon = int(h * 0.30)

    for i in range(4):
        cx = rnd.randint(0, w); cy = rnd.randint(int(h * .03), int(h * .20))
        rx = rnd.randint(int(w * .14), int(w * .28)); ry = rnd.randint(int(h * .03), int(h * .06))
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 255, 255, 56 if after else 96))

    # terrace behind, with chimney stacks
    for x in range(0, w, max(40, int(w * .22))):
        d.rectangle([x + int(w * .04), int(h * .06), x + int(w * .10), int(h * .17)],
                    fill=(148, 104, 88))
    d.rectangle([0, int(h * .16), w, int(h * .40)], fill=(196, 184, 168))
    d.rectangle([0, int(h * .38), w, int(h * .41)], fill=(84, 92, 100))

    # rear wall of the host building
    d.rectangle([0, int(h * .41), w, int(h * .57)], fill=(216, 206, 192))
    d.rectangle([int(w * .12), int(h * .44), int(w * .30), int(h * .545)], fill=(238, 241, 244),
                outline=(252, 252, 252), width=max(3, int(w * .006)))
    d.rectangle([int(w * .58), int(h * .46), int(w * .74), int(h * .545)], fill=(228, 232, 237))

    # the flat roof deck in perspective
    deck_top = int(h * 0.56)
    pts = [(int(w * .04), h), (int(w * .96), h), (int(w * .84), deck_top), (int(w * .16), deck_top)]
    if after:
        d.polygon(pts, fill=(38, 42, 47))
        for i in range(3):                                 # soft sheen bands
            y = deck_top + int((h - deck_top) * (.24 + i * .26))
            d.line([(int(w * .13), y), (int(w * .87), y)], fill=(58, 64, 70, 130), width=3)
        d.polygon([(int(w * .16), deck_top), (int(w * .84), deck_top),
                   (int(w * .845), deck_top + 12), (int(w * .155), deck_top + 12)],
                  fill=(150, 158, 166))                    # new edge trim
        d.ellipse([int(w * .70), int(h * .80), int(w * .76), int(h * .86)], fill=(24, 26, 30))
    else:
        d.polygon(pts, fill=(96, 96, 92))
        for _ in range(26):                                # patchy felt
            px = rnd.randint(int(w * .1), int(w * .9)); py = rnd.randint(deck_top, h)
            pw = rnd.randint(int(w * .05), int(w * .16)); ph = rnd.randint(int(h * .03), int(h * .08))
            d.rectangle([px, py, px + pw, py + ph],
                        fill=(86 + rnd.randint(-14, 14), 86 + rnd.randint(-14, 14), 80, 210))
        for _ in range(5):                                 # ponding
            px = rnd.randint(int(w * .2), int(w * .7)); py = rnd.randint(int(h * .70), int(h * .94))
            pw = rnd.randint(int(w * .10), int(w * .26))
            d.ellipse([px, py, px + pw, py + int(h * .05)], fill=(120, 132, 128, 190))
        for _ in range(16):                                # algae
            px = rnd.randint(int(w * .08), int(w * .92)); py = rnd.randint(deck_top, h)
            r = rnd.randint(int(w * .01), int(w * .035))
            d.ellipse([px - r, py - r // 2, px + r, py + r // 2], fill=(104, 118, 70, 190))
        d.line([(int(w * .16), deck_top + 6), (int(w * .84), deck_top + 6)],
               fill=(74, 70, 64), width=max(4, int(h * .012)))

    pole = (176, 180, 186, 230)
    for px in (int(w * 0.03), int(w * 0.95)):
        d.rectangle([px, int(h * .12), px + max(4, int(w * .006)), h], fill=pole)
    d.rectangle([0, int(h * .50), w, int(h * .50) + max(4, int(h * .01))], fill=(176, 180, 186, 120))

    return vignette(grain(img))


def badge(img, text):
    """Small corner mark so a placeholder is never mistaken for a real photo."""
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    f = font(FONT_B, max(13, int(h * 0.026)))
    tw = d.textlength(text, font=f)
    pad = int(h * 0.02)
    bw = tw + pad * 2
    bh = f.size + pad * 1.2
    x0, y0 = w - bw - pad, h - bh - pad
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=int(h * .01),
                        fill=(8, 20, 34, 175))
    d.text((x0 + pad, y0 + pad * .55), text, font=f, fill=(150, 190, 235))
    return img


# --------------------------------------------------------------------------- #
#  Brand assets
# --------------------------------------------------------------------------- #

def logo_mark(d, cx, cy, scale, colour, stroke):
    """The Any Weather arc-over-roofline mark, drawn to match the SVG logo."""
    s = scale
    d.arc([cx - 2.0 * s, cy - 1.75 * s, cx + 2.0 * s, cy + 1.35 * s],
          start=196, end=344, fill=colour, width=max(2, int(.16 * s)))
    d.line([(cx - 1.55 * s, cy + .62 * s), (cx - .48 * s, cy - .42 * s),
            (cx + .12 * s, cy + .16 * s)], fill=colour,
           width=max(2, int(.17 * s)), joint="curve")
    d.line([(cx + .12 * s, cy + .16 * s), (cx + .78 * s, cy - .52 * s),
            (cx + 1.55 * s, cy + .28 * s)], fill=colour,
           width=max(2, int(.17 * s)), joint="curve")
    d.line([(cx + 1.55 * s, cy + .28 * s), (cx + 1.55 * s, cy + .62 * s)],
           fill=colour, width=max(2, int(.17 * s)))
    q = .17 * s
    for dx, dy in ((-.30, -.12), (.06, -.12), (-.30, .16), (.06, .16)):
        d.rectangle([cx + .70 * s + dx * s, cy + dy * s,
                     cx + .70 * s + dx * s + q, cy + dy * s + q], fill=colour)


def og_image():
    W, H = 1200, 630
    img = gradient((W, H), (8, 25, 42), (18, 58, 94))
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(26):                                   # faint tile lattice
        d.line([(0, i * 26), (W, i * 26 - 180)], fill=(255, 255, 255, 8), width=1)
    d.ellipse([W - 460, -220, W + 240, 480], fill=(30, 139, 255, 34))

    logo_mark(d, 118, 108, 38, WHITE, 5)
    d.text((216, 76), "ANY WEATHER", font=font(FONT_B, 36), fill=WHITE)
    d.text((218, 118), "R O O F I N G   L T D", font=font(FONT_R, 19), fill=(150, 190, 235))

    d.text((78, 224), "P L Y M O U T H", font=font(FONT_R, 46), fill=(186, 210, 232))
    d.text((78, 290), "ROOFING DONE", font=font(FONT_B, 82), fill=WHITE)
    d.text((78, 374), "PROPERLY.", font=font(FONT_B, 82), fill=BLUE)

    d.rounded_rectangle([78, 492, 470, 566], 37, fill=BLUE)
    d.text((112, 512), "07745 364 538", font=font(FONT_B, 36), fill=WHITE)
    d.text((500, 520), "Free quotes · Fully insured", font=font(FONT_R, 26), fill=(168, 196, 222))

    img.save(os.path.join(IMG, "og-image.png"), optimize=True)
    print("wrote assets/img/og-image.png")


def touch_icon():
    S = 720
    img = Image.new("RGB", (S, S), NAVY)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S, S], S * .22, fill=NAVY)
    logo_mark(d, S // 2, int(S * .52), S * .21, WHITE, 10)
    img = img.resize((180, 180), Image.LANCZOS)
    img.save(os.path.join(IMG, "apple-touch-icon.png"), optimize=True)
    print("wrote assets/img/apple-touch-icon.png")


# filename, width, height, is_after, caption badge
PHOTOS = [
    ("hero-1.jpg", 1800, 1100, True, "PLACEHOLDER"),
    ("hero-2.jpg", 1800, 1100, False, "PLACEHOLDER"),
    ("hero-3.jpg", 1800, 1100, True, "PLACEHOLDER"),
    ("ba-pitched-before.jpg", 1400, 1000, False, "PLACEHOLDER"),
    ("ba-pitched-after.jpg", 1400, 1000, True, "PLACEHOLDER"),
    ("ba-flat-before.jpg", 1400, 1000, False, "PLACEHOLDER", "flat"),
    ("ba-flat-after.jpg", 1400, 1000, True, "PLACEHOLDER", "flat"),
    ("work-1.jpg", 1200, 900, True, "PLACEHOLDER"),
    ("work-2.jpg", 1200, 900, False, "PLACEHOLDER"),
    ("work-3.jpg", 1200, 900, True, "PLACEHOLDER"),
    ("work-4.jpg", 1200, 900, True, "PLACEHOLDER"),
    ("work-5.jpg", 1200, 900, False, "PLACEHOLDER"),
    ("work-6.jpg", 1200, 900, True, "PLACEHOLDER"),
]


def photos():
    os.makedirs(PHOTO, exist_ok=True)
    for i, entry in enumerate(PHOTOS):
        name, w, h, after, mark = entry[:5]
        kind = entry[5] if len(entry) > 5 else "pitched"
        draw = flat_scene if kind == "flat" else roof_scene
        img = draw(w, h, after, seed=i * 13 + 3)
        img = badge(img, mark)
        img.save(os.path.join(PHOTO, name), quality=78, optimize=True, progressive=True)
        print("wrote assets/img/photos/%s" % name)


if __name__ == "__main__":
    os.makedirs(IMG, exist_ok=True)
    og_image()
    touch_icon()
    photos()
