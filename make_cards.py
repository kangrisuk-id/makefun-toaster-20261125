"""Build-time card renderer for the toaster entry (NOT part of the entry).

Renders three static PNGs with Pillow:
  cover.png          -- hero: toaster LCD display showing the winning line
  card-winner.png    -- the winning line as a toaster display card
  card-finalists.png -- the two runners-up as display cards

Run once:  python3 make_cards.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

BG = (18, 18, 22)          # deep charcoal
PANEL = (32, 32, 40)       # layered surface
GOLD = (212, 175, 105)     # restrained gold
GREEN = (110, 220, 130)    # LCD green
DIM = (150, 150, 160)
WHITE = (235, 235, 240)
RED = (220, 90, 80)

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MONO_R = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

WINNER = "Error: This toaster has unionized. Toasting resumes after negotiations."
RUNNER1 = "Error: The bread was already sad when it arrived. I merely made it official."
RUNNER2 = "Error: The toaster has seen the inside of your freezer. It would like to forget."


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_toaster(draw, x, y, w, h):
    """Simple chrome toaster body with two slots and a lever."""
    # body
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=(58, 58, 66),
                           outline=(90, 90, 100), width=2)
    # top slots
    draw.rounded_rectangle([x + 30, y + 14, x + w - 30, y + 30], radius=8, fill=(12, 12, 14))
    draw.line([x + w // 2, y + 14, x + w // 2, y + 30], fill=(90, 90, 100), width=2)
    # lever
    draw.rounded_rectangle([x + w - 26, y + h // 2 - 22, x + w - 12, y + h // 2 + 22],
                           radius=6, fill=(24, 24, 28), outline=GOLD, width=2)
    # feet
    draw.rectangle([x + 24, y + h - 6, x + 54, y + h], fill=(24, 24, 28))
    draw.rectangle([x + w - 54, y + h - 6, x + w - 24, y + h], fill=(24, 24, 28))


def lcd_card(path, title, lines, accent, subtitle, w=1280, h=800):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    # gold hairline frame
    d.rectangle([16, 16, w - 16, h - 16], outline=GOLD, width=2)
    d.text((48, 44), title, font=font(SANS, 34), fill=GOLD)
    # LCD panel
    px, py, pw, ph = 48, 120, w - 96, 400
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=16, fill=(8, 26, 12),
                        outline=(40, 90, 50), width=2)
    # LCD header
    d.text((px + 28, py + 22), "TOASTER OS  v2.6  —  DISPLAY", font=font(MONO_R, 24),
           fill=(90, 160, 100))
    d.text((px + pw - 28 - d.textlength("E-771", font=font(MONO, 24)),
            py + 22), "E-771", font=font(MONO, 24), fill=RED)
    # LCD text
    fnt = font(MONO, 44)
    y = py + 88
    for ln in lines:
        d.text((px + 28, y), ln, font=fnt, fill=GREEN)
        y += 62
    # toaster drawing + subtitle
    draw_toaster(d, 48, 560, 260, 150)
    d.text((340, 600), subtitle, font=font(SANS_R, 30), fill=WHITE)
    d.text((340, 650), "make.fun  ·  The Funniest Toaster Error Message",
           font=font(SANS_R, 24), fill=DIM)
    img.save(os.path.join(HERE, path))


def main():
    tmp = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(tmp)
    fnt = font(MONO, 44)
    win_lines = wrap(d, WINNER, fnt, 1280 - 96 - 56)
    lcd_card("cover.png", "THE FUNNIEST TOASTER ERROR MESSAGE", win_lines, GREEN,
             "The winning line — 71 characters.",
             )
    lcd_card("card-winner.png", "WINNER  ·  71 CHARACTERS", win_lines, GREEN,
             "Error: This toaster has unionized. Toasting resumes after negotiations.")
    # finalists: two stacked LCD panels
    w, h = 1280, 800
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, w - 16, h - 16], outline=GOLD, width=2)
    d.text((48, 44), "FINALISTS  ·  THE KNOCKOUT'S RUNNERS-UP", font=font(SANS, 34), fill=GOLD)
    panels = [
        ("RUNNER-UP 1  ·  76 CHARACTERS", RUNNER1),
        ("RUNNER-UP 2  ·  80 CHARACTERS", RUNNER2),
    ]
    y = 120
    for title, text in panels:
        d.rounded_rectangle([48, y, w - 48, y + 280], radius=16, fill=(8, 26, 12),
                            outline=(40, 90, 50), width=2)
        d.text((76, y + 20), title, font=font(MONO_R, 22), fill=(90, 160, 100))
        lines = wrap(d, text, font(MONO, 38), w - 96 - 56)
        yy = y + 70
        for ln in lines:
            d.text((76, yy), ln, font=font(MONO, 38), fill=GREEN)
            yy += 54
        y += 320
    d.text((48, 740), "make.fun  ·  The Funniest Toaster Error Message",
           font=font(SANS_R, 22), fill=DIM)
    img.save(os.path.join(HERE, "card-finalists.png"))


if __name__ == "__main__":
    main()
    for f in ("cover.png", "card-winner.png", "card-finalists.png"):
        p = os.path.join(HERE, f)
        print(f, os.path.getsize(p), "bytes")
