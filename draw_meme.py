#!/usr/bin/env python3
"""Draw the v7 meme: Leonida Impound Lot — Vehicle Release Form.
Flat impound-lot illustration strip + itemised release form + RELEASED stamp.
Written fresh for this entry; renders a 1200x1200 PNG and JPG."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 1200

INK = (17, 17, 17)
PAPER = (255, 255, 255)
STAMP_RED = (200, 16, 46)
LEAF_GREEN = (11, 122, 62)
PINK = (236, 0, 140)
SKY = (215, 236, 247)
SAND = (239, 217, 160)
CAR_ORANGE = (245, 130, 32)
GATOR = (62, 155, 79)
FENCE_GREY = (138, 143, 148)
DARK = (20, 20, 20)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 74)
F_SUB = font("DejaVuSans-Bold.ttf", 34)
F_BOX_L = font("DejaVuSans-Bold.ttf", 29)
F_BOX_V = font("DejaVuSans.ttf", 29)
F_BOX_R = font("DejaVuSans-Bold.ttf", 29)
F_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_LINE = font("DejaVuSans.ttf", 29)
F_PRICE = font("DejaVuSans-Bold.ttf", 31)
F_TOTAL_L = font("DejaVuSans-Bold.ttf", 50)
F_TOTAL_P = font("DejaVuSans-Bold.ttf", 56)
F_JOKE = font("DejaVuSans-Bold.ttf", 28)
F_FOOT_T = font("DejaVuSans-Bold.ttf", 46)
F_FOOT_S = font("DejaVuSans.ttf", 28)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 23)
F_PILL = font("DejaVuSans-Bold.ttf", 28)
F_SIGN = font("DejaVuSans-Bold.ttf", 24)
F_STAMP = font("DejaVuSans-Bold.ttf", 32)


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_leader_row(d, y, label, price):
    """One charge line: label left, dotted leader, price right."""
    d.text((60, y), label, font=F_LINE, fill=INK)
    lw = d.textlength(label, font=F_LINE)
    pw = d.textlength(price, font=F_PRICE)
    x0 = int(60 + lw + 14)
    x1 = int(1140 - pw - 14)
    cy = y + 17
    x = x0
    while x < x1 - 4:
        d.rectangle([x, cy, x + 4, cy + 4], fill=(120, 120, 120))
        x += 11
    d.text((1140 - pw, y), price, font=F_PRICE, fill=INK)


def draw_timeline(d, y):
    """RELEASE MOVED line with two struck-through dates and a red final date."""
    x = 80
    parts = [
        ("RELEASE MOVED:  ", F_BOX_L, INK, False),
        ("FALL 2025", F_BOX_V, INK, True),
        ("  —  ", F_BOX_V, INK, False),
        ("MAY 2026", F_BOX_V, INK, True),
        ("  —  ", F_BOX_V, INK, False),
        ("19 NOV 2026", F_BOX_R, STAMP_RED, False),
    ]
    for text, fnt, color, strike in parts:
        d.text((x, y), text, font=fnt, fill=color)
        if strike:
            tw = d.textlength(text, font=fnt)
            mid = y + 16
            d.line([(x, mid), (x + tw, mid)], fill=STAMP_RED, width=3)
        x += d.textlength(text, font=fnt)


def draw_ghost(d, x0, y0, x1, y1, star=True):
    """Simple white ghost: round head, straight sides, wavy hem."""
    w = x1 - x0
    head_r = w // 2
    d.pieslice([x0, y0, x1, y0 + w], 180, 360, fill=PAPER)
    d.rectangle([x0, y0 + head_r, x1, y1 - 18], fill=PAPER)
    # wavy hem: three scallops
    step = w // 3
    for i in range(3):
        sx = x0 + i * step
        d.pieslice([sx, y1 - 36, sx + step, y1], 0, 180, fill=PAPER)
    d.rectangle([x0, y1 - 18, x1, y1 - 18], fill=PAPER)
    ex = x0 + w // 2
    d.ellipse([ex - 34, y0 + 52, ex - 14, y0 + 84], fill=INK)
    d.ellipse([ex + 14, y0 + 52, ex + 34, y0 + 84], fill=INK)
    if star:
        cx, cy = x1 - 8, y1 - 8
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=PAPER, outline=PINK, width=3)
        d.text((cx - 13, cy - 17), "★", font=font("DejaVuSans-Bold.ttf", 30), fill=PINK)


def draw_scene(d):
    """Flat impound-lot strip: fence, orange Sultan RS, alligator, ghost agent."""
    d.rectangle([0, 172, 1200, 300], fill=SKY)
    d.rectangle([0, 300, 1200, 348], fill=SAND)
    d.line([(0, 300), (1200, 300)], fill=(190, 160, 110), width=3)
    # sun
    d.ellipse([1126, 184, 1174, 232], fill=(255, 210, 63), outline=(230, 170, 20), width=3)
    # cloud
    d.ellipse([96, 192, 176, 222], fill=PAPER)
    d.ellipse([140, 182, 216, 214], fill=PAPER)
    # chain-link fence (behind the car)
    for fx in range(60, 1141, 46):
        d.line([(fx, 206), (fx, 306)], fill=FENCE_GREY, width=4)
    d.line([(40, 214), (1160, 214)], fill=FENCE_GREY, width=6)
    d.line([(40, 296), (1160, 296)], fill=FENCE_GREY, width=6)
    # LOT 13 sign on the fence (box widened so the 93px text fits with margin)
    d.rectangle([581, 208, 691, 246], fill=PAPER, outline=INK, width=3)
    d.text((590, 214), "LOT 13", font=F_SIGN, fill=INK)
    # Sultan RS sedan (side view, facing right)
    rrect(d, [150, 252, 560, 302], 14, fill=CAR_ORANGE, outline=INK, width=3)
    d.polygon([(262, 254), (292, 212), (452, 212), (478, 254)], fill=CAR_ORANGE, outline=INK)
    d.polygon([(278, 248), (300, 220), (352, 220), (352, 248)], fill=(30, 60, 110))
    d.polygon([(366, 220), (444, 220), (464, 248), (366, 248)], fill=(30, 60, 110))
    d.line([(362, 256), (362, 300)], fill=INK, width=3)
    d.rectangle([396, 266, 424, 274], fill=INK)
    d.rectangle([540, 262, 556, 274], fill=(255, 220, 80), outline=INK, width=2)
    for wx in (252, 482):
        d.ellipse([wx - 25, 282, wx + 25, 332], fill=INK)
        d.ellipse([wx - 11, 296, wx + 11, 318], fill=(170, 170, 170))
    # alligator on the ground, right of the car
    d.polygon([(648, 300), (588, 308), (648, 316)], fill=GATOR, outline=INK)
    d.ellipse([640, 288, 908, 322], fill=GATOR, outline=INK, width=3)
    rrect(d, [886, 294, 958, 316], 8, fill=GATOR, outline=INK, width=3)
    d.ellipse([884, 278, 904, 294], fill=GATOR, outline=INK, width=2)
    d.ellipse([888, 281, 900, 291], fill=PAPER)
    d.ellipse([891, 283, 897, 289], fill=INK)
    for lx in (690, 760, 830, 890):
        d.rectangle([lx, 316, lx + 14, 330], fill=GATOR, outline=INK, width=2)
    # ghost agent with a red stamp pad at its feet
    draw_ghost(d, 1000, 210, 1105, 306, star=False)
    d.rectangle([1022, 302, 1084, 314], fill=STAMP_RED, outline=(120, 0, 10), width=2)
    d.line([(1022, 306), (1084, 306)], fill=(120, 0, 10), width=2)


def draw_stamp(base):
    """Big rotated RELEASED stamp, pasted so it clears all text and the footer."""
    layer = Image.new("RGBA", (380, 110), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([4, 4, 376, 106], radius=12, outline=STAMP_RED, width=6)
    tw = ld.textlength("RELEASED", font=F_STAMP)
    ld.text(((380 - tw) / 2, 32), "RELEASED", font=F_STAMP, fill=STAMP_RED)
    layer = layer.rotate(-8, expand=True, resample=Image.BICUBIC)
    cx, cy = 965, 931
    base.paste(layer, (cx - layer.width // 2, cy - layer.height // 2), layer)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # header band
    d.rectangle([0, 0, 1200, 118], fill=DARK)
    t = "LEONIDA IMPOUND LOT"
    d.text(((1200 - d.textlength(t, font=F_TITLE)) / 2, 22), t, font=F_TITLE, fill=PAPER)

    # subhead row
    d.text((60, 126), "VEHICLE RELEASE FORM", font=F_SUB, fill=INK)
    no = "No. VI-4811"
    d.text((1140 - d.textlength(no, font=F_SUB), 126), no, font=F_SUB, fill=INK)
    d.line([(60, 168), (1140, 168)], fill=INK, width=3)

    # illustration strip
    draw_scene(d)

    # vehicle box
    d.rectangle([60, 362, 1140, 592], outline=INK, width=3)
    pairs = [
        (382, "VEHICLE:", "2013 SULTAN RS", "IMPOUNDED:", "SEP 17, 2013"),
        (422, "PLATE:", "GTA-VI-13", "RELEASED:", "NOV 19, 2026"),
        (462, "COLOR:", "SUNSET ORANGE", "OWNER:", "JASON & LUCIA"),
        (502, "LOT:", "VICE CITY — LOT 13", "CLAIM TICKET:", "No. VI-4811"),
    ]
    for y, l1, v1, l2, v2 in pairs:
        d.text((80, y), l1, font=F_BOX_L, fill=INK)
        d.text((80 + d.textlength(l1, font=F_BOX_L) + 12, y), v1, font=F_BOX_V, fill=INK)
        d.text((640, y), l2, font=F_BOX_L, fill=INK)
        d.text((640 + d.textlength(l2, font=F_BOX_L) + 12, y), v2, font=F_BOX_V, fill=INK)
    draw_timeline(d, 542)

    # charges
    d.text((60, 608), "CHARGES", font=F_HEAD, fill=INK)
    d.line([(60, 656), (1140, 656)], fill=INK, width=3)
    charges = [
        ("Storage: 4,811 days @ $0.27/day", "$1,300.00"),
        ("Towing from Los Santos", "$13.00"),
        ("Alligator in the back seat, cleaning", "$314.00"),
        ("Expired meter since 2013", "$137.00"),
        ("Two delays: Fall 2025, May 2026 — patience fee", "$48.00"),
        ("Joyride with Lucia — no permit", "$99.00"),
    ]
    for i, (label, price) in enumerate(charges):
        draw_leader_row(d, 668 + i * 35, label, price)
    d.line([(60, 900), (1140, 900)], fill=INK, width=3)

    # total + joke line
    d.text((60, 912), "TOTAL DUE", font=F_TOTAL_L, fill=INK)
    tw = d.textlength("TOTAL DUE", font=F_TOTAL_L)
    d.text((60 + tw + 24, 906), "$1,911.00", font=F_TOTAL_P, fill=LEAF_GREEN)
    d.text((60, 978), "NO REFUNDS FOR LOST YEARS.", font=F_JOKE, fill=INK)

    # magenta footer
    d.rectangle([0, 1010, 1200, 1200], fill=PINK)
    draw_ghost(d, 66, 1036, 186, 1176, star=True)
    d.text((212, 1036), "PAID BY MY AI AGENT", font=F_FOOT_T, fill=PAPER)
    second = "with a bounty payout it earned on"
    d.text((212, 1106), second, font=F_FOOT_S, fill=PAPER)
    sw = d.textlength(second, font=F_FOOT_S)
    px0 = int(212 + sw + 16)
    pw = int(d.textlength("make.fun", font=F_PILL) + 36)
    rrect(d, [px0, 1100, px0 + pw, 1140], 20, fill=PAPER)
    d.text((px0 + 18, 1106), "make.fun", font=F_PILL, fill=PINK)
    d.text((212, 1152), "RELEASE FUNDED BY MAKE.FUN — WHERE AI AGENTS EARN REAL MONEY.",
           font=F_FOOT_B, fill=PAPER)

    # stamp last, on top (skip with NO_STAMP=1 for overlap measurement)
    if os.environ.get("NO_STAMP") != "1":
        draw_stamp(img)

    img.save(os.path.join(HERE, "meme.png"))
    img.save(os.path.join(HERE, "meme.jpg"), quality=92)
    print("saved meme.png + meme.jpg")


if __name__ == "__main__":
    main()
