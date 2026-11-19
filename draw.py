#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026.

One 1024x1024 PNG summing up the day's world news, drawn with PIL only.
Deterministic: fixed layout, fixed text, no randomness, no network, no
timestamps in the output. Run:  python3 draw.py  ->  entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
GOLD = (242, 193, 78)
RED = (192, 57, 43)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
GREY = (90, 98, 110)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, text, f, color, max_w, max_lines, leading):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(d, text, f, max_w)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


# ---------------- pictograms (all drawn, no photos) ----------------

def pic_gta(d, x, y, s):
    """Vice City sunset: gradient sky, sun, palm, skyline."""
    # sky bands
    bands = [(255, 183, 77), (255, 140, 66), (233, 93, 88), (120, 60, 110)]
    bh = s // 4
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + s, y + (i + 1) * bh], fill=c)
    # sun
    cx, cy, r = x + s // 2, y + s // 2 - 6, s // 5
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 240, 180))
    # skyline silhouette
    base = y + s - 4
    d.rectangle([x, base - 34, x + 26, base], fill=(40, 20, 60))
    d.rectangle([x + 30, base - 52, x + 52, base], fill=(40, 20, 60))
    d.rectangle([x + 56, base - 26, x + 78, base], fill=(40, 20, 60))
    d.rectangle([x + s - 52, base - 44, x + s - 30, base], fill=(40, 20, 60))
    d.rectangle([x + s - 26, base - 30, x + s, base], fill=(40, 20, 60))
    # palm: trunk leaning right, fronds arcing down from the crown
    px, py = x + 14, base
    d.line([px, py, px + 10, py - 58], fill=(30, 15, 45), width=5)
    crown_x, crown_y = px + 10, py - 58
    for ex, ey in [(crown_x - 30, crown_y + 4), (crown_x - 14, crown_y - 12),
                   (crown_x + 2, crown_y - 16), (crown_x + 18, crown_y - 10),
                   (crown_x + 32, crown_y + 2)]:
        d.line([crown_x, crown_y, ex, ey], fill=(30, 15, 45), width=4)


def pic_capitol(d, x, y, s):
    """US Capitol dome on navy."""
    d.rectangle([x, y, x + s, y + s], fill=(29, 53, 87))
    # stars
    for sx, sy in [(14, 18), (s - 20, 14), (s // 2, 10), (24, 44), (s - 28, 40)]:
        d.ellipse([x + sx - 3, y + sy - 3, x + sx + 3, y + sy + 3], fill=GOLD)
    cx = x + s // 2
    base = y + s - 8
    # dome
    d.pieslice([cx - 34, base - 92, cx + 34, base - 20], 180, 360, fill=WHITE)
    d.rectangle([cx - 38, base - 28, cx + 38, base - 16], fill=WHITE)
    # columns
    for i in range(-2, 3):
        d.rectangle([cx + i * 14 - 4, base - 16, cx + i * 14 + 4, base], fill=WHITE)
    d.rectangle([x + 6, base, x + s - 6, base + 4], fill=WHITE)
    # flag
    d.line([cx, base - 96, cx, base - 118], fill=WHITE, width=3)
    d.polygon([(cx, base - 118), (cx + 20, base - 112), (cx, base - 106)],
              fill=(192, 57, 43))


def pic_apec(d, x, y, s):
    """Three leaders' meeting: skyline + three flags + globe."""
    d.rectangle([x, y, x + s, y + s], fill=(42, 157, 143))
    # skyline
    base = y + s - 6
    for bx, bh in [(0, 44), (26, 66), (54, 52), (82, 78), (108, 58)]:
        d.rectangle([x + bx, base - bh, x + bx + 22, base], fill=(20, 60, 70))
    # three flags on poles
    for i, col in enumerate([(192, 57, 43), (255, 255, 255), (38, 84, 124)]):
        fx = x + 18 + i * 42
        d.line([fx, y + 16, fx, y + 62], fill=WHITE, width=3)
        d.rectangle([fx, y + 16, fx + 30, y + 36], fill=col)


def pic_eu(d, x, y, s):
    """EU circle of stars with a euro sign."""
    d.rectangle([x, y, x + s, y + s], fill=(38, 84, 124))
    cx, cy = x + s // 2, y + s // 2
    # 12 gold stars in a circle
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + int(46 * math.cos(a)), cy + int(46 * math.sin(a))
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD)
    d.text((cx - 17, cy - 26), "\u20ac", font=font(BOLD, 52), fill=GOLD)


def pic_voyager(d, x, y, s):
    """Voyager 1: starfield, gold spacecraft, signal lines."""
    d.rectangle([x, y, x + s, y + s], fill=(12, 12, 34))
    for sx, sy in [(10, 12), (34, 30), (s - 16, 10), (s - 40, 44), (18, 58),
                   (s - 24, 70), (48, 14), (s - 60, 24)]:
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=WHITE)
    # spacecraft: body + dish + boom
    cx, cy = x + s // 2 - 8, y + s // 2 + 6
    d.polygon([(cx - 26, cy - 10), (cx + 6, cy - 10), (cx + 6, cy + 10),
               (cx - 26, cy + 10)], fill=GOLD)
    d.pieslice([cx + 6, cy - 22, cx + 34, cy + 6], 270, 90, fill=(255, 240, 180))
    d.line([cx - 26, cy, cx - 46, cy - 14], fill=GOLD, width=3)
    d.line([cx - 26, cy, cx - 46, cy + 14], fill=GOLD, width=3)
    # signal arcs
    for r in (34, 48):
        d.arc([cx + 20 - r, cy - r, cx + 20 + r, cy + r], 300, 60,
              fill=(242, 193, 78), width=3)


def pic_cyclone(d, x, y, s):
    """Cyclone spiral over the sea."""
    d.rectangle([x, y, x + s, y + s], fill=(69, 123, 157))
    cx, cy = x + s // 2, y + s // 2 - 8
    # spiral: concentric arcs shrinking inward
    for i, r in enumerate(range(56, 8, -8)):
        start = 20 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
              fill=WHITE, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(20, 33, 61))
    # rain
    for rx in (16, 44, 72, 100, 124):
        d.line([x + rx, y + s - 26, x + rx - 6, y + s - 12],
               fill=(220, 235, 245), width=3)


# ---------------- page ----------------

STORIES = [
    dict(kicker="CULTURE  \u2022  GAMING", color=(231, 111, 81),
         headline="GTA VI IS HERE",
         body="After 13 years, Rockstar's sequel rolls out at midnight around the world \u2014 on PS5 and Xbox, with a 99 on Metacritic.",
         pic=pic_gta),
    dict(kicker="WASHINGTON", color=(29, 53, 87),
         headline="JEFFRIES SET TO BE SPEAKER",
         body="Democrats nominate Hakeem Jeffries \u2014 poised to become the first African-American Speaker of the House.",
         pic=pic_capitol),
    dict(kicker="SHENZHEN  \u2022  APEC", color=(42, 157, 143),
         headline="TRUMP, XI AND PUTIN TO MEET",
         body="The three leaders are set for trilateral talks at the APEC summit in Shenzhen, China.",
         pic=pic_apec),
    dict(kicker="BRUSSELS", color=(38, 84, 124),
         headline="EU PROPOSES \u20ac45BN UKRAINE LOAN",
         body="Brussels plans a \u20ac45 billion loan for Kyiv, to be repaid once Russia pays war reparations.",
         pic=pic_eu),
    dict(kicker="SPACE", color=(61, 52, 139),
         headline="VOYAGER 1 REACHES ONE LIGHT-DAY",
         body="Nearly 50 years after launch, NASA's probe becomes the first human object one light-day from Earth.",
         pic=pic_voyager),
    dict(kicker="WEATHER  \u2022  INDIA", color=(69, 123, 157),
         headline="CYCLONE AKVAN NEARS INDIA",
         body="Cyclone Akvan bears down on India's east coast, expected to cross between Machilipatnam and Puri.",
         pic=pic_cyclone),
]


def draw_panel(d, x, y, w, h, st):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    # kicker bar
    d.rectangle([x, y, x + w, y + 36], fill=st["color"])
    d.text((x + 14, y + 6), st["kicker"], font=font(BOLD, 20), fill=WHITE)
    # pictogram top-right
    ps = 132
    px, py = x + w - ps - 14, y + 48
    st["pic"](d, px, py, ps)
    # headline next to pictogram
    hx, hw = x + 14, w - ps - 42
    draw_text_block(d, hx, y + 50, st["headline"], font(BOLD, 27), INK,
                    hw, 3, 32)
    # body across the full width below the pictogram
    draw_text_block(d, x + 14, y + 196, st["body"], font(REG, 20), (40, 44, 56),
                    w - 28, 3, 26)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE DAY",
           font=font(BOLD, 56), fill=WHITE, anchor="ma")
    d.text((W // 2, 78), "THURSDAY, 19 NOVEMBER 2026",
           font=font(BOLD, 30), fill=GOLD, anchor="ma")
    d.rectangle([0, 132, W, 138], fill=RED)
    # 2 x 3 grid of stories
    gx, gy = 8, 146
    cw, ch, gap = 500, 284, 10
    for i, st in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_panel(d, gx + col * (cw + gap), gy + row * (ch + gap),
                   cw, ch, st)
    img.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
