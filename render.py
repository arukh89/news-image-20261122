#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026 and save entry.png.

Every letter and shape is drawn from code with Pillow. No photograph, no
downloaded artwork, no network call and no clock: the same script always
produces the same bytes. Run from this directory: python3 render.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (176, 30, 30)
BLUE = (29, 78, 137)
SEA = (207, 224, 232)
LAND = (217, 201, 163)
LAND_LINE = (138, 122, 90)
GREY = (90, 86, 76)
SUN = (232, 164, 32)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit(text, fnt, width):
    """Shorten text with an ellipsis until it fits the pixel width."""
    if fnt.getlength(text) <= width:
        return text
    while text and fnt.getlength(text + "...") > width:
        text = text[:-1]
    return text + "..."


def wrap(text, fnt, width, max_lines):
    """Greedy word wrap, at most max_lines lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == max_lines - 1:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and words and lines[-1] != words[-1]:
        lines[-1] = fit(lines[-1], fnt, width)
    return lines


# (number, kicker, headline, deck)
BRIEFS = [
    (3, "HORMUZ", "Three tankers hit in the strait",
     "One crewman missing, 11 hurt in the strait."),
    (4, "BALTIC", "Russian ship Sparta II ablaze",
     "Drone strike in the Baltic; Finland on alert."),
    (5, "BRAZIL", "Bolsonaro in intensive care",
     "Ex-president in ICU with acute bowel obstruction."),
    (6, "MEXICO", "Cartel boss seized, 11 killed",
     "'El Chapo Isidro' captured; Sinaloa erupts."),
    (7, "UN COURT", "France turns to Security Council",
     "Myanmar rejects ICJ genocide ruling."),
    (8, "ESTONIA", "Estonia to shut Russia border",
     "Moscow calls it a 'new Iron Curtain'."),
    (9, "NIGERIA", "Boat capsizes, 24 dead",
     "Vessel carrying mourners to a funeral sinks."),
    (10, "DENMARK", "Russia 'plotted to kill rapper'",
     "Denmark expels a diplomat over the alleged plot."),
    (11, "SUMMIT", "Zelensky: Shenzhen 'a failure'",
     "Trump-Xi-Putin declare peace; no breakthrough."),
    (12, "CEASEFIRE", "Melania pushes new ceasefires",
     "Wants more Russia-Ukraine truces before Christmas."),
    (13, "IRAN DEAL", "Trump: Iran deal 'could last 20 years'",
     "US president eyes 'regime change' in Tehran."),
    (14, "WARNING", "US airlines warned of attacks",
     "Possible al-Qaeda-linked threat ahead of Thanksgiving."),
    (15, "MARKETS", "Oil slides more than 3%",
     "Nikkei falls 5.1%; Wall Street in correction."),
    (16, "POLAND", "Polish jet 'missed' Russian missile",
     "Warsaw cries provocation after the miss."),
    (17, "FRANCE", "Sixth weekend of protests",
     "French march over living costs and services."),
    (18, "BELGIUM", "Air traffic to halt on Monday",
     "National strike grounds flights across Belgium."),
    (19, "ISRAEL", "Coalition talks open",
     "Eisenkot invites Netanyahu's Likud to negotiate."),
    (20, "GAZA", "Four killed in Gaza",
     "14 hurt as ceasefire violations continue."),
    (21, "LEBANON", "Aoun: end occupation, meddling",
     "President demands Israel out, Iran out of Lebanon."),
    (22, "LIBYA", "Oil pipeline blocked, $30.8m lost",
     "Armed group holds the line for 20 days."),
    (23, "CONGO", "Ebola fight hampered",
     "Geography, violence, distrust slow response."),
    (24, "SUDAN", "Home-grown push for peace",
     "Sudanese seek their own path out of the war."),
    (25, "PAKISTAN", "15 militants killed",
     "Security forces clear hideouts in Balochistan."),
    (26, "INDIA", "Modi opens Nitish Setu bridge",
     "New link joins Patna and Vaishali in Bihar."),
    (27, "CYCLONE", "Akvan cancels 14 flights",
     "Ranchi airport hit as the cyclone nears India."),
    (28, "JAPAN", "Japan to train in India",
     "First live-fire use of Indian facilities by Tokyo."),
    (29, "SPORT", "India face NZ in Wellington",
     "Cummins keeps Australia's Test captaincy."),
    (30, "USA", "Democrats sweep the Senate",
     "Leadership vote tests the new majority early."),
    (31, "BRAZIL", "Storm town clears rubble",
     "Brazil counts the cost of a deadly storm."),
    (32, "UN", "UN chief race in gridlock",
     "US 'open' to a Western Hemisphere chief."),
    (33, "CHINA", "China's buildup 'rapid'",
     "Trump warns after his meeting with Xi."),
    (34, "CLIMATE", "COP31 AI pledge flops",
     "Big US tech firms stay away from the pledge."),
    (35, "THAILAND", "Thai youth protest",
     "Students demand education and political change."),
    (36, "CULTURE", "Macklemore sings for Gaza",
     "New single gives all profits to Gaza recovery."),
]

# Rough continent outlines in (lon, lat); drawn equirectangular.
CONTINENTS = [
    [(-168, 65), (-150, 70), (-130, 71), (-120, 70), (-105, 68), (-95, 69),
     (-85, 66), (-80, 62), (-75, 58), (-70, 62), (-65, 60), (-60, 55),
     (-55, 52), (-60, 47), (-65, 44), (-70, 42), (-75, 35), (-80, 32),
     (-85, 30), (-90, 29), (-95, 28), (-97, 26), (-100, 23), (-105, 20),
     (-110, 23), (-115, 28), (-120, 34), (-125, 40), (-125, 48), (-130, 55),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-65, -5), (-60, -10), (-55, -15),
     (-50, -20), (-45, -25), (-40, -30), (-45, -35), (-50, -38), (-55, -35),
     (-60, -38), (-65, -40), (-70, -45), (-75, -50), (-75, -55), (-70, -55),
     (-68, -50), (-70, -40), (-73, -30), (-75, -20), (-78, -10), (-80, 0)],
    [(-10, 36), (-5, 43), (0, 46), (5, 48), (10, 55), (15, 58), (20, 60),
     (25, 62), (30, 65), (35, 68), (40, 68), (45, 65), (40, 60), (35, 55),
     (30, 50), (25, 45), (20, 42), (15, 40), (10, 38), (5, 38), (0, 40),
     (-5, 36)],
    [(-15, 15), (-10, 20), (-5, 25), (0, 30), (10, 32), (15, 30), (20, 28),
     (25, 25), (30, 20), (35, 15), (40, 10), (45, 5), (50, 0), (48, -5),
     (45, -10), (40, -15), (35, -20), (30, -25), (25, -30), (20, -35),
     (18, -32), (15, -28), (12, -20), (10, -15), (8, -5), (5, 0), (0, 5),
     (-5, 8), (-10, 12)],
    [(40, 68), (50, 70), (60, 72), (70, 73), (80, 73), (90, 75), (100, 76),
     (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 68),
     (170, 66), (175, 65), (170, 60), (165, 60), (160, 55), (155, 50),
     (150, 45), (145, 42), (140, 38), (135, 35), (130, 32), (125, 30),
     (120, 25), (115, 22), (110, 20), (105, 15), (100, 10), (95, 12),
     (90, 15), (85, 18), (80, 15), (75, 12), (70, 15), (65, 20), (60, 25),
     (55, 28), (50, 30), (45, 32), (40, 35), (40, 40), (45, 45), (50, 50),
     (55, 55), (60, 60), (55, 65), (50, 68), (45, 68)],
    [(113, -22), (118, -20), (125, -15), (130, -12), (135, -12), (140, -15),
     (145, -18), (150, -22), (153, -27), (150, -32), (145, -38), (140, -38),
     (135, -35), (130, -32), (125, -32), (120, -34), (115, -32), (113, -26)],
]

# (story number, lon, lat) for the map pins.
PINS = [(1, 30.7, 36.9), (2, 50.6, 26.2), (3, 63.0, 24.0), (4, 21.0, 59.0),
        (5, -47.9, -15.8), (6, -107.0, 25.0), (7, 2.3, 46.8), (8, 25.0, 59.0),
        (9, 8.0, 9.0), (10, 77.2, 28.6)]

NUMBERS = [
    ("200", "nations at COP31"),
    ("06:00 GMT", "COP31 approval vote"),
    ("24", "dead, Nigeria boat"),
    ("11", "killed in Sinaloa"),
    ("3%", "oil slide, markets fall"),
    ("15", "militants killed"),
]


def draw_masthead(d):
    d.line([(28, 16), (996, 16)], fill=INK, width=3)
    d.line([(28, 21), (996, 21)], fill=INK, width=1)
    title = font(SERIF_B, 92)
    d.text((512, 28), "THE WORLD", font=title, fill=INK, anchor="ma")
    date = font(SANS_B, 40)
    d.text((512, 128), "SUNDAY 22 NOVEMBER 2026", font=date, fill=RED,
           anchor="ma")
    tag = font(SANS_B, 16)
    d.text((512, 176), "EARLY EDITION  •  36 STORIES  •  7 REGIONS  •  THE DAY IN ONE PAGE",
           font=tag, fill=INK, anchor="ma")
    d.line([(28, 202), (996, 202)], fill=RED, width=3)


def draw_lead(d, x, y, w, h, kicker, headline, deck, art):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.text((x + 14, y + 10), kicker, font=font(SANS_B, 14), fill=RED)
    head = font(SERIF_B, 27)
    lines = wrap(headline, head, w - 28, 2)
    yy = y + 32
    for line in lines:
        d.text((x + 14, yy), line, font=head, fill=INK)
        yy += 32
    body = font(SANS, 14)
    for line in wrap(deck, body, w - 140, 3):
        d.text((x + 14, yy), line, font=body, fill=INK)
        yy += 18
    art(d, x + w - 92, y + h - 78)


def sun_art(d, x, y):
    d.ellipse([x, y, x + 64, y + 64], fill=SUN, outline=INK, width=2)
    for a in range(0, 360, 45):
        import math
        r1, r2 = 36, 46
        cx, cy = x + 32, y + 32
        d.line([(cx + r1 * math.cos(math.radians(a)),
                 cy + r1 * math.sin(math.radians(a))),
                (cx + r2 * math.cos(math.radians(a)),
                 cy + r2 * math.sin(math.radians(a)))],
               fill=SUN, width=3)
    d.ellipse([x + 18, y + 40, x + 46, y + 58], fill=BLUE)


def burst_art(d, x, y):
    import math
    cx, cy = x + 32, y + 32
    for a in range(0, 360, 30):
        r = 34 if a % 60 == 0 else 20
        d.line([(cx, cy),
                (cx + r * math.cos(math.radians(a)),
                 cy + r * math.sin(math.radians(a)))],
               fill=RED, width=3)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)


def draw_map_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    d.text((x + 12, y + 8), "WHERE IT HAPPENED", font=font(SANS_B, 14),
           fill=INK)

    def px(lon, lat):
        return (x + 10 + (lon + 180) / 360.0 * (w - 20),
                y + 28 + (75 - lat) / 130.0 * (h - 38))

    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    pin_f = font(SANS_B, 12)
    for num, lon, lat in PINS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(num), font=pin_f, fill=(255, 255, 255),
               anchor="mm")


def draw_numbers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.text((x + 12, y + 8), "THE DAY IN NUMBERS", font=font(SANS_B, 14),
           fill=INK)
    big_f = font(SANS_B, 17)
    small_f = font(SANS, 11)
    for i, (big, small) in enumerate(NUMBERS):
        col = i % 2
        row = i // 2
        cx = x + 12 + col * 160
        cy = y + 34 + row * 38
        d.text((cx, cy), big, font=big_f, fill=RED)
        d.text((cx, cy + 20), small, font=small_f, fill=INK)


def draw_briefs(d, y0):
    d.text((28, y0), "THE DAY IN BRIEF — 34 MORE STORIES",
           font=font(SANS_B, 15), fill=INK)
    d.line([(28, y0 + 22), (996, y0 + 22)], fill=INK, width=2)
    cols = [(24, 312), (356, 312), (688, 312)]
    head_f = font(SANS_B, 12)
    deck_f = font(SANS, 10)
    num_f = font(SANS_B, 12)
    per_col = [12, 11, 11]
    idx = 0
    for ci, (cx, cw) in enumerate(cols):
        yy = y0 + 34
        for _ in range(per_col[ci]):
            num, _kick, headline, deck = BRIEFS[idx]
            idx += 1
            d.text((cx, yy), str(num), font=num_f, fill=RED)
            hx = cx + 26
            d.text((hx, yy), fit(headline, head_f, cw - 26), font=head_f,
                   fill=INK)
            d.text((hx, yy + 15), fit(deck, deck_f, cw - 26), font=deck_f,
                   fill=(60, 58, 50))
            yy += 34


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d, 28, 214, 496, 158, "CLIMATE — ANTALYA",
              "COP31 near a deal at last",
              "A new package is out after all-night talks; the vote is "
              "at 06:00 GMT, with 200 nations to approve it.",
              sun_art)
    draw_lead(d, 540, 214, 456, 158, "GULF — BAHRAIN",
              "Iran hits US bases in Bahrain",
              "Drones and missiles hit al-Riffa and Awali; a plant "
              "burns, and no one is hurt.",
              burst_art)
    draw_map_panel(d, 28, 384, 620, 148)
    draw_numbers(d, 664, 384, 332, 148)
    draw_briefs(d, 544)
    d.line([(28, 996), (996, 996)], fill=INK, width=1)
    d.text((512, 1002),
           "Sunday 22 November 2026 — Early edition  •  Drawn from code, no photographs",
           font=font(SANS, 12), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    build().save("entry.png", format="PNG")
    print("wrote entry.png")
