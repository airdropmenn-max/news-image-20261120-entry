#!/usr/bin/env python3
"""The World in One Day — Friday 20 November 2026.

Draws entry.png (1024x1024, < 1 MiB), a one-page front page summing up
45 verified news stories of Friday 20 November 2026: 3 hero panels with
people/action scenes, 10 small stories with bold glyph icons, a numbered
world map with large pins, and a numbered ALSO ON list (stories 14-45).

Python 3 + PIL only. No network, no randomness. Deterministic output.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette: warm newsprint, one coherent theme ----
PAPER   = (246, 239, 224)   # warm cream paper
PAPER2  = (238, 228, 203)   # slightly deeper cream
INK     = (22, 40, 63)      # dark navy ink
INK2    = (48, 66, 88)      # softer ink
RED     = (179, 39, 30)     # headline red
TEAL    = (15, 118, 110)    # teal accent
MUSTARD = (217, 147, 13)    # mustard accent
SKY     = (191, 217, 232)   # map ocean
LAND    = (227, 201, 143)   # map land sand
LAND_ED = (120, 96, 52)     # land outline
WHITE   = (255, 255, 255)
BLACK   = (16, 16, 16)
CREAMTX = (250, 244, 230)
NIGHT   = (24, 32, 58)      # neon street night
NEONPK  = (255, 92, 168)    # neon pink
NEONCY  = (64, 224, 208)    # neon cyan
SUNSET  = (243, 180, 96)    # bridge sky

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B  = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_DB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max width in px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_center(draw, cx, y, s, fnt, fill):
    draw.text((cx - draw.textlength(s, font=fnt) / 2, y), s, font=fnt, fill=fill)

def draw_wrapped(draw, x, y, lines, fnt, fill, lh=None):
    if lh is None:
        lh = int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

# ---------------------------------------------------------------- masthead
def masthead(d):
    d.rectangle([0, 0, W, 116], fill=PAPER)
    d.rectangle([0, 0, W, 6], fill=RED)
    d.rectangle([0, 112, W, 116], fill=INK)
    f_title = font(SERIF_B, 54)
    text_center(d, W // 2, 6, "THE WORLD IN ONE DAY", f_title, INK)
    f_date = font(SANS_B, 32)
    text_center(d, W // 2, 62, "FRIDAY, 20 NOVEMBER 2026", f_date, RED)
    # thin rules flanking the date
    d.line([(70, 80), (255, 80)], fill=INK, width=2)
    d.line([(769, 80), (954, 80)], fill=INK, width=2)
    f_kick = font(SANS_B, 15)
    text_center(d, W // 2, 94, "45 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
                f_kick, INK2)

# ---------------------------------------------------------------- hero 1: summit
def hero_summit(d, x, y, w, h):
    # warm wood-panelled summit room
    d.rectangle([x, y, x + w, y + h], fill=(141, 74, 52))
    d.rectangle([x, y, x + w, y + 34], fill=(104, 52, 36))
    f_ban = font(SANS_B, 15)
    text_center(d, x + w // 2, y + 8, "SHENZHEN  ·  TRILATERAL SUMMIT", f_ban, (255, 226, 180))
    # back wall flags: three small vertical banners
    for i, c in enumerate([(179, 39, 30), (30, 80, 160), (240, 240, 235)]):
        bx = x + 30 + i * 118
        d.rectangle([bx, y + 40, bx + 56, y + 96], fill=c, outline=INK, width=2)
    # table
    d.rectangle([x + 8, y + 148, x + w - 8, y + 176], fill=(96, 58, 32))
    d.rectangle([x + 8, y + 148, x + w - 8, y + 154], fill=(150, 100, 55))
    # three seated leaders: head + shoulders + name plate
    seats = [(x + 62, (232, 196, 168), (24, 42, 66), "TRUMP"),
             (x + 168, (238, 205, 175), (40, 40, 40), "XI"),
             (x + 274, (228, 190, 160), (70, 70, 78), "PUTIN")]
    for cx, skin, suit, name in seats:
        d.ellipse([cx - 26, y + 96, cx + 26, y + 148], fill=skin, outline=INK, width=2)
        # hair
        d.arc([cx - 26, y + 96, cx + 26, y + 124], 180, 360, fill=(60, 45, 30), width=6)
        # shoulders / suit
        d.pieslice([cx - 34, y + 138, cx + 34, y + 200], 180, 360, fill=suit)
        d.rectangle([cx - 34, y + 150, cx + 34, y + 176], fill=suit)
        # tie
        d.polygon([(cx - 4, y + 150), (cx + 4, y + 150), (cx, y + 172)], fill=RED)
        # name plate on the table
        d.rectangle([cx - 34, y + 156, cx + 34, y + 174], fill=WHITE, outline=INK, width=2)
        f_pl = font(SANS_B, 12)
        text_center(d, cx, y + 159, name, f_pl, INK)
    # microphones on the table
    for mx in (x + 110, x + 216):
        d.line([(mx, y + 148), (mx, y + 132)], fill=INK, width=3)
        d.ellipse([mx - 5, y + 126, mx + 5, y + 136], fill=INK)

# ---------------------------------------------------------------- hero 2: GTA VI neon street
def hero_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # neon signs
    f_neon = font(SANS_B, 22)
    d.rectangle([x + 14, y + 10, x + 128, y + 40], outline=NEONPK, width=3)
    d.text((x + 22, y + 13), "VICE CITY", font=f_neon, fill=NEONPK)
    f_neon2 = font(SANS_B, 15)
    d.rectangle([x + 196, y + 12, x + 306, y + 38], outline=NEONCY, width=3)
    d.text((x + 204, y + 15), "GTA VI", font=f_neon2, fill=NEONCY)
    # buildings silhouettes
    for bx, bh, c in [(x + 8, 60, (38, 48, 84)), (x + 96, 78, (46, 56, 96)),
                      (x + 210, 66, (38, 48, 84)), (x + 288, 84, (46, 56, 96))]:
        d.rectangle([bx, y + 120 - bh, bx + 46, y + 120], fill=c)
        for wy in range(y + 128 - bh, y + 112, 14):
            d.rectangle([bx + 8, wy, bx + 16, wy + 8], fill=(255, 214, 120))
            d.rectangle([bx + 26, wy, bx + 34, wy + 8], fill=(255, 214, 120))
    # road
    d.rectangle([x, y + 120, x + w, y + h], fill=(30, 30, 38))
    for rx in range(x + 6, x + w, 44):
        d.rectangle([rx, y + 168, rx + 26, y + 172], fill=(250, 220, 90))
    # the car: detailed, windows, wheels, headlights
    cx, cy = x + 168, y + 128
    # body
    d.rounded_rectangle([cx - 118, cy - 8, cx + 118, cy + 26], radius=12,
                        fill=(214, 48, 96), outline=INK, width=3)
    d.polygon([(cx - 78, cy - 8), (cx - 58, cy - 38), (cx + 62, cy - 38),
               (cx + 84, cy - 8)], fill=(214, 48, 96), outline=INK, width=3)
    # windows
    d.polygon([(cx - 66, cy - 12), (cx - 52, cy - 34), (cx - 8, cy - 34),
               (cx - 8, cy - 12)], fill=(170, 225, 240), outline=INK, width=2)
    d.polygon([(cx + 2, cy - 12), (cx + 2, cy - 34), (cx + 54, cy - 34),
               (cx + 70, cy - 12)], fill=(170, 225, 240), outline=INK, width=2)
    # door lines + handle
    d.line([(cx - 6, cy - 6), (cx - 6, cy + 24)], fill=INK, width=2)
    d.rectangle([cx + 18, cy + 2, cx + 34, cy + 6], fill=INK)
    # headlights + beams
    d.ellipse([cx + 102, cy + 2, cx + 116, cy + 14], fill=(255, 240, 150), outline=INK, width=2)
    d.polygon([(cx + 116, cy + 4), (x + w - 2, cy - 6), (x + w - 2, cy + 18)],
              fill=(255, 240, 150, 90))
    d.ellipse([cx - 116, cy + 2, cx - 102, cy + 14], fill=(255, 120, 120), outline=INK, width=2)
    # wheels with hubs
    for wx in (cx - 76, cx + 76):
        d.ellipse([wx - 22, cy + 12, wx + 22, cy + 40], fill=BLACK, outline=INK, width=3)
        d.ellipse([wx - 9, cy + 21, wx + 9, cy + 33], fill=(200, 200, 210), outline=INK, width=2)
    # crowd silhouettes behind the car
    for px, pc in [(x + 30, (255, 214, 120)), (x + 66, (120, 220, 255)),
                   (x + 268, (150, 255, 180)), (x + 300, (255, 180, 120))]:
        d.ellipse([px - 8, y + 96, px + 8, y + 112], fill=pc, outline=INK, width=2)
        d.pieslice([px - 12, y + 110, px + 12, y + 132], 180, 360, fill=pc)

# ---------------------------------------------------------------- hero 3: bridge strike
def hero_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SUNSET)
    # sun
    d.ellipse([x + 262, y + 12, x + 296, y + 46], fill=(255, 226, 130), outline=INK, width=2)
    # sea
    d.rectangle([x, y + 128, x + w, y + h], fill=(52, 110, 150))
    for wy in range(y + 138, y + h - 4, 12):
        d.line([(x + 8 + (wy % 24), wy), (x + 60 + (wy % 24), wy)], fill=(140, 190, 220), width=2)
    # bridge deck: left span, broken middle, right span
    d.rectangle([x + 6, y + 96, x + 132, y + 108], fill=(90, 90, 100), outline=INK, width=2)
    d.rectangle([x + 200, y + 96, x + w - 6, y + 108], fill=(90, 90, 100), outline=INK, width=2)
    # fallen middle span tilted into the water
    d.polygon([(x + 132, y + 100), (x + 176, y + 104), (x + 168, y + 140),
               (x + 138, y + 138)], fill=(110, 110, 120), outline=INK, width=2)
    # towers
    for tx in (x + 40, x + 252):
        d.rectangle([tx - 5, y + 40, tx + 5, y + 100], fill=(70, 70, 80), outline=INK, width=2)
        d.rectangle([tx - 16, y + 36, tx + 16, y + 44], fill=(70, 70, 80), outline=INK, width=2)
    # cables
    d.line([(x + 40, y + 40), (x + 132, y + 96)], fill=INK, width=2)
    d.line([(x + 252, y + 40), (x + 200, y + 96)], fill=INK, width=2)
    # explosion burst at the break: spiky starburst, not concentric rings
    ex, ey = x + 166, y + 92
    for r_out, r_in, c in [(36, 20, (255, 120, 30)), (26, 14, (255, 170, 40)),
                           (16, 8, (255, 230, 120))]:
        pts = []
        for k in range(24):
            ang = math.pi * k / 12
            r = r_out if k % 2 == 0 else r_in
            pts.append((ex + r * math.cos(ang), ey + r * math.sin(ang)))
        d.polygon(pts, fill=c, outline=INK, width=2)
    # debris dots
    for dx, dy in [(-30, -18), (28, -24), (34, 10), (-24, 14)]:
        d.ellipse([ex + dx - 3, ey + dy - 3, ex + dx + 3, ey + dy + 3], fill=INK)
    # smoke puffs
    for sx, sy, sr in [(x + 138, y + 52, 14), (x + 162, y + 38, 17), (x + 190, y + 54, 13)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 125),
                  outline=INK, width=2)
    # small boat
    d.polygon([(x + 236, y + 150), (x + 282, y + 150), (x + 272, y + 162),
               (x + 246, y + 162)], fill=(240, 240, 235), outline=INK, width=2)
    d.line([(x + 259, y + 150), (x + 259, y + 134)], fill=INK, width=2)
    d.polygon([(x + 259, y + 134), (x + 274, y + 148), (x + 259, y + 148)],
              fill=RED, outline=INK, width=1)

def hero_strip(d, x, y, w, headline, sub):
    """Dark headline strip under a hero illustration."""
    d.rectangle([x, y, x + w, y + 56], fill=INK)
    f_h = font(SANS_B, 17)
    f_s = font(SANS_R, 13)
    hl = wrap(d, headline, f_h, w - 16)
    yy = y + 4
    for ln in hl[:1]:
        d.text((x + 8, yy), ln, font=f_h, fill=WHITE)
        yy += 20
    d.text((x + 8, yy), sub, font=f_s, fill=(200, 210, 225))
    return y + 56

# ---------------------------------------------------------------- glyphs (bold, few strokes)
def glyph_gavel(d, cx, cy, s, c):
    # handle: diagonal bar; head: thick bar across the top end; base bar
    d.line([(cx - s * 0.9, cy + s * 0.9), (cx + s * 0.55, cy - s * 0.55)],
           fill=c, width=8)
    d.line([(cx + s * 0.1, cy - s * 1.0), (cx + s * 1.05, cy - s * 0.05)],
           fill=c, width=13)
    d.rectangle([cx - s * 1.0, cy + s * 0.75, cx + s * 0.7, cy + s * 0.95], fill=c)

def glyph_cyclone(d, cx, cy, s, c):
    for i, r in enumerate([s * 1.0, s * 0.72, s * 0.45]):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + i * 70, 300 + i * 70,
              fill=c, width=7)

def glyph_chart(d, cx, cy, s, c):
    d.line([(cx - s, cy + s * 0.8), (cx - s, cy - s * 0.8)], fill=c, width=7)
    d.line([(cx - s, cy + s * 0.8), (cx + s, cy + s * 0.8)], fill=c, width=7)
    d.line([(cx - s * 0.85, cy + s * 0.45), (cx - s * 0.2, cy - s * 0.1),
            (cx + s * 0.25, cy + s * 0.25), (cx + s * 0.85, cy - s * 0.6)],
           fill=c, width=7, joint="curve")
    d.polygon([(cx + s * 0.85, cy - s * 0.6), (cx + s * 0.45, cy - s * 0.6),
               (cx + s * 0.85, cy - s * 0.2)], fill=c)

def glyph_ballot(d, cx, cy, s, c):
    d.rectangle([cx - s * 0.9, cy - s * 0.2, cx + s * 0.9, cy + s * 0.9],
                fill=None, outline=c, width=7)
    d.line([(cx - s * 0.9, cy - s * 0.2), (cx - s * 0.55, cy - s * 0.9),
            (cx + s * 0.9, cy - s * 0.9)], fill=c, width=7)
    d.line([(cx - s * 0.55, cy + s * 0.35), (cx - s * 0.1, cy + s * 0.7),
            (cx + s * 0.65, cy - s * 0.25)], fill=c, width=8, joint="curve")

def glyph_euro(d, cx, cy, s, c):
    f = font(SANS_DB, int(s * 2.1))
    d.text((cx - d.textlength("€", font=f) / 2, cy - s * 1.05), "€", font=f, fill=c)

def glyph_line(d, cx, cy, s, c):
    d.line([(cx - s, cy + s * 0.7), (cx + s, cy - s * 0.7)], fill=c, width=6)
    for t in (0.25, 0.5, 0.75):
        px = cx - s + 2 * s * t
        py = cy + s * 0.7 - 2 * s * 0.7 * t
        d.line([(px - 8, py), (px + 8, py)], fill=c, width=5)
    d.ellipse([cx - s * 1.05, cy - s * 1.05, cx - s * 0.55, cy - s * 0.55], fill=c)
    d.ellipse([cx + s * 0.55, cy + s * 0.55, cx + s * 1.05, cy + s * 1.05], fill=c)

def glyph_pact(d, cx, cy, s, c):
    d.rectangle([cx - s * 0.8, cy - s * 0.9, cx + s * 0.8, cy + s * 0.6],
                fill=None, outline=c, width=7)
    d.line([(cx - s * 0.55, cy - s * 0.5), (cx + s * 0.55, cy - s * 0.5)], fill=c, width=5)
    d.line([(cx - s * 0.55, cy - s * 0.1), (cx + s * 0.55, cy - s * 0.1)], fill=c, width=5)
    d.line([(cx - s * 0.55, cy + s * 0.3), (cx + s * 0.1, cy + s * 0.3)], fill=c, width=5)
    d.ellipse([cx + s * 0.35, cy + s * 0.45, cx + s * 0.95, cy + s * 1.05],
              fill=c, outline=c)
    d.text((cx + s * 0.55, cy + s * 0.52), "★", font=font(SANS_DB, 16), fill=WHITE)

def glyph_leaf(d, cx, cy, s, c):
    # pointed-oval leaf, tilted, with a vein and a stem
    d.polygon([(cx, cy - s), (cx + s * 0.75, cy - s * 0.1),
               (cx + s * 0.35, cy + s * 0.8), (cx - s * 0.55, cy + s * 0.35),
               (cx - s * 0.6, cy - s * 0.45)], fill=c)
    d.line([(cx - s * 0.1, cy - s * 0.6), (cx + s * 0.15, cy + s * 0.55)],
           fill=WHITE, width=3)
    d.line([(cx + s * 0.15, cy + s * 0.55), (cx + s * 0.55, cy + s * 0.95)],
           fill=c, width=4)

def glyph_atom(d, cx, cy, s, c):
    # radiation trefoil: three blades + centre dot
    for a0 in (270, 30, 150):
        d.pieslice([cx - s, cy - s, cx + s, cy + s], a0 - 28, a0 + 28, fill=c)
    d.ellipse([cx - s * 0.32, cy - s * 0.32, cx + s * 0.32, cy + s * 0.32],
              fill=c)

def glyph_droplet(d, cx, cy, s, c):
    d.polygon([(cx, cy - s), (cx + s * 0.8, cy + s * 0.1), (cx, cy + s),
               (cx - s * 0.8, cy + s * 0.1)], fill=c)
    d.ellipse([cx - s * 0.8, cy - s * 0.1, cx + s * 0.8, cy + s], fill=c)
    d.line([(cx - s * 0.4, cy + s * 0.5), (cx + s * 0.4, cy - s * 0.3)], fill=WHITE, width=5)

SMALL = [
    # (num, glyph, tag, headline, summary) — headlines/summaries fit 2 lines
    (4, glyph_gavel, "ASIA · JUSTICE", "World Court: Myanmar guilty",
     "ICJ rules 9–6; restitution ordered."),
    (5, glyph_cyclone, "ASIA · WEATHER", "Cyclone Akvan makes landfall",
     "Storm hits Odisha coast; schools shut."),
    (6, glyph_chart, "TECH · BUSINESS", "Anthropic's Nasdaq debut soars",
     "Shares indicated 33% above $83 IPO price."),
    (7, glyph_ballot, "AMERICAS", "Senate rejects Iran war-powers bid",
     "Vote 51–48 against curbing strikes on Iran."),
    (8, glyph_euro, "EUROPE", "EU proposes €45bn loan for Ukraine",
     "Von der Leyen puts 2027 aid for Kyiv to 27 states."),
    (9, glyph_line, "MIDDLE EAST", "Israel pushes past the 'yellow line'",
     "Rare ground operation in central Gaza."),
    (10, glyph_pact, "AMERICAS", "US and Venezuela sign military pact",
     "Hegseth's Caracas visit seals the deal."),
    (11, glyph_leaf, "CLIMATE", "COP31 ministers race to unblock the text",
     "Antalya talks aim to break deadlock."),
    (12, glyph_atom, "ASIA", "North Korea expands uranium enrichment",
     "UN watchdog: Yongbyon site is growing."),
    (13, glyph_droplet, "OCEANIA", "Fiji declares a national disaster",
     "Drought and water shortages under El Niño."),
]

def small_stories(d, x0, y0, cols=5, cw=200, ch=112):
    f_tag = font(SANS_B, 11)
    f_h = font(SANS_B, 14)
    f_s = font(SANS_R, 11)
    for i, (num, glyph, tag, head, summ) in enumerate(SMALL):
        col, row = i % cols, i // cols
        x = x0 + col * cw
        y = y0 + row * ch
        # tinted tile + number chip
        d.rectangle([x + 3, y + 3, x + cw - 4, y + ch - 4], fill=PAPER2,
                    outline=(200, 182, 140), width=1)
        d.ellipse([x + 10, y + 10, x + 46, y + 46], fill=TEAL)
        glyph(d, x + 28, y + 28, 13, WHITE)
        d.ellipse([x + 40, y + 40, x + 60, y + 60], fill=RED, outline=WHITE, width=2)
        f_n = font(SANS_B, 13)
        text_center(d, x + 50, y + 43, str(num), f_n, WHITE)
        tx = x + 68
        d.text((tx, y + 8), tag, font=f_tag, fill=RED)
        # story 8 headline needs 13pt to fit "Ukraine" in 2 lines
        f_hl = font(SANS_B, 13) if num == 8 else f_h
        hl = wrap(d, head, f_hl, cw - 76)
        yy = draw_wrapped(d, tx, y + 24, hl[:2], f_hl, INK, lh=16)
        sl = wrap(d, summ, f_s, cw - 76)
        draw_wrapped(d, tx, yy + 1, sl[:2], f_s, INK2, lh=13)

# ---------------------------------------------------------------- world map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
           (-75, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
           (-80, 32), (-81, 26), (-90, 21), (-97, 16), (-94, 17), (-105, 20),
           (-110, 23), (-114, 29), (-120, 34), (-125, 40), (-124, 48),
           (-135, 58), (-155, 58), (-165, 60)],
    "SA": [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
           (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52),
           (-66, -55), (-62, -48), (-57, -38), (-48, -28), (-41, -22),
           (-35, -8), (-40, -3), (-50, 0), (-53, 5), (-60, 8), (-70, 11),
           (-75, 10)],
    "AF": [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (10, 37), (20, 32),
           (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11),
           (51, 10), (44, 0), (40, -10), (36, -18), (32, -26), (28, -33),
           (20, -35), (16, -28), (12, -18), (9, -1), (9, 4), (-8, 4),
           (-13, 8)],
    "EU": [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50),
           (3, 51), (8, 54), (8, 57), (10, 59), (5, 60), (5, 62),
           (12, 65), (18, 69), (25, 71), (30, 70), (32, 68), (40, 68),
           (44, 66), (48, 62), (50, 60), (48, 58), (44, 55), (40, 52),
           (35, 50), (30, 46), (28, 44), (23, 40), (19, 42), (15, 44),
           (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36)],
    "AS": [(30, 36), (35, 36), (36, 36), (40, 38), (44, 39), (48, 38),
           (50, 40), (54, 38), (57, 37), (60, 37), (63, 40), (66, 42),
           (70, 42), (74, 40), (77, 38), (80, 35), (85, 33), (88, 28),
           (92, 22), (95, 16), (98, 10), (100, 8), (103, 2), (104, 9),
           (106, 11), (109, 13), (108, 18), (106, 20), (105, 21), (103, 23),
           (100, 25), (97, 28), (94, 29), (90, 22), (88, 22), (86, 20),
           (82, 17), (80, 13), (77, 8), (76, 10), (73, 16), (70, 20),
           (66, 25), (62, 25), (58, 26), (56, 27), (52, 28), (50, 29),
           (48, 30), (44, 29), (40, 30), (36, 36)],
    "AU": [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
           (132, -32), (136, -35), (140, -38), (145, -38), (150, -37),
           (153, -32), (153, -27), (150, -22), (146, -19), (142, -11),
           (137, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
    "JP": [(130, 31), (132, 33), (135, 34), (137, 35), (139, 38), (141, 41),
           (143, 42), (144, 44), (142, 44), (140, 39), (137, 37), (133, 35),
           (131, 33)],
    "ID": [(95, 5), (98, 3), (101, 0), (104, -3), (107, -7), (110, -7),
           (114, -8), (118, -9), (120, -10), (119, -5), (115, -2), (112, 0),
           (108, 2), (104, 3), (100, 5)],
}

# (story, lon, lat, dx, dy) — dx/dy nudge the pin so neighbours don't collide
PINS = [
    (1, 114.0, 22.5, 0, 0),      # Shenzhen
    (2, -80.2, 25.8, -30, 26),  # Miami / GTA VI
    (3, 36.5, 45.3, 0, 0),      # Kerch Bridge
    (4, 96.0, 21.9, 0, 0),      # Myanmar
    (5, 85.8, 20.3, -16, 22),   # Odisha
    (6, -74.0, 40.7, 12, -16),  # New York (Nasdaq)
    (7, -77.0, 38.9, -16, 18),  # Washington DC
    (8, 4.35, 50.85, 0, 0),     # Brussels
    (9, 34.45, 31.5, 18, 16),   # Gaza
    (10, -66.9, 10.5, 0, 0),    # Caracas
    (11, 30.7, 36.9, -24, 24),  # Antalya
    (12, 125.75, 39.8, 0, 0),   # Yongbyon
    (13, 178.1, -17.7, -26, 0), # Fiji
]

def world_map(d, x0, y0, mw, mh):
    d.rectangle([x0, y0, x0 + mw, y0 + mh], fill=SKY, outline=INK, width=2)
    # graticule
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * mw
        d.line([(gx, y0), (gx, y0 + mh)], fill=(255, 255, 255), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y0 + (78 - lat) / 136 * mh
        d.line([(x0, gy), (x0 + mw, gy)], fill=(255, 255, 255), width=1)
    # continents
    for pts in CONTINENTS.values():
        xy = [(x0 + (lon + 180) / 360 * mw, y0 + (78 - lat) / 136 * mh)
              for lon, lat in pts]
        d.polygon(xy, fill=LAND, outline=LAND_ED, width=2)
    # pins
    f_pin = font(SANS_B, 15)
    for num, lon, lat, dx, dy in PINS:
        px = x0 + (lon + 180) / 360 * mw
        py = y0 + (78 - lat) / 136 * mh
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (qx, qy)], fill=INK, width=2)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
        d.ellipse([qx - 16, qy - 16, qx + 16, qy + 16], fill=WHITE)
        d.ellipse([qx - 13, qy - 13, qx + 13, qy + 13], fill=RED, outline=WHITE, width=1)
        s = str(num)
        tw = d.textlength(s, font=f_pin)
        d.text((qx - tw / 2, qy - 10), s, font=f_pin, fill=WHITE)

# ---------------------------------------------------------------- ALSO ON list
ALSO_ON = [
    (14, "APEC adopts Shenzhen Outlook"),
    (15, "Kuwait repels Iranian attack"),
    (16, "Yunus's home torched in Bangladesh"),
    (17, "S. Korea court clears ex-PM Han"),
    (18, "Somalia expels UAE ambassador"),
    (19, "47 French nationals on trial in Iraq"),
    (20, "Serbia elects student speaker Cupic"),
    (21, "EU Commission hit by AI cyberattack"),
    (22, "UK, Norway fund Ukraine naval craft"),
    (23, "Denmark OKs Greenland defence deal"),
    (24, "Indonesia passes asset-forfeiture bill"),
    (25, "589m children lived in conflict in 2025"),
    (26, "ASEAN closes with digital trade deal"),
    (27, "Quad leaders meet in Philippines"),
    (28, "US envoys meet Putin, brief Zelenskyy"),
    (29, "Haiti OKs Salvadoran troop deal"),
    (30, "Netanyahu alleges election fraud"),
    (31, "Iran still holds 2,500+ missiles *"),
    (32, "Saudi: Yemen war may last 6 more months"),
    (33, "Modi meets Prince & Princess of Wales"),
    (34, "Nicholls 113* as NZ face India"),
    (35, "Sensex jumps 1.2%, Nifty tops 25,500"),
    (36, "Gemini computer use comes to Mac"),
    (37, "Google opens Genie 4 to developers"),
    (38, "Chrome builds synthetic web for AI tests"),
    (39, "20,000 US flights cancelled in ATC crisis"),
    (40, "California hit by 60-foot waves"),
    (41, "South Sudan election postponed"),
    (42, "Pattinson named the next James Bond"),
    (43, "SS United States sunk as reef"),
    (44, "Ebola response hampered in DR Congo"),
    (45, "Bangkok protest leader calls off march"),
]

def also_on(d, x0, y0, w):
    f_h = font(SANS_B, 15)
    d.text((x0, y0), "ALSO ON THIS DAY — 14–45", font=f_h, fill=INK)
    d.line([(x0 + 250, y0 + 9), (x0 + w, y0 + 9)], fill=RED, width=2)
    f_n = font(SANS_B, 12)
    f_t = font(SANS_R, 12)
    col_w = w // 4
    for i, (num, txt) in enumerate(ALSO_ON):
        col, row = i // 8, i % 8
        x = x0 + col * col_w
        y = y0 + 24 + row * 15
        d.text((x, y), str(num), font=f_n, fill=RED)
        d.text((x + 22, y), txt, font=f_t, fill=INK)

# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    masthead(d)

    # hero row: illustration + headline strip
    hy, hh, strip = 120, 176, 56
    hx = [12, 348, 684]
    hw = 328
    hero_summit(d, hx[0], hy, hw, hh)
    hero_gta(d, hx[1], hy, hw, hh)
    hero_bridge(d, hx[2], hy, hw, hh)
    hero_strip(d, hx[0], hy + hh, hw, "Three nuclear powers, one table",
               "Trump, Xi and Putin meet in Shenzhen")
    hero_strip(d, hx[1], hy + hh, hw, "Vice City opens its doors",
               "GTA VI launches to record crowds")
    hero_strip(d, hx[2], hy + hh, hw, "Crimean Bridge hit a third time",
               "Rail halted as span falls; Putin vows reply")

    # small stories: 2 rows x 5
    small_stories(d, 12, 356)

    # map (narrower than full width so the continents keep their shape)
    f_map = font(SANS_B, 15)
    d.text((82, 584), "WHERE IT HAPPENED — STORIES 1–13", font=f_map, fill=INK)
    d.line([(382, 593), (942, 593)], fill=RED, width=2)
    world_map(d, 82, 604, 860, 210)

    # ALSO ON
    also_on(d, 12, 818, 1000)

    # footer
    d.rectangle([0, 962, W, H], fill=INK)
    f_f = font(SANS_R, 13)
    f_fb = font(SANS_B, 13)
    text_center(d, W // 2, 968,
                "Sources: Reuters · AP · AFP · BBC · Al Jazeera · The Times of India · AI-Newsdesk",
                f_f, CREAMTX)
    text_center(d, W // 2, 990,
                "* Contested claims are marked as claims.  ·  FRIDAY, 20 NOVEMBER 2026",
                f_fb, (200, 210, 225))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
