from PIL import Image, ImageDraw, ImageFont
import math
import os


W, H = 1800, 1200
BG = (13, 16, 22)
PANEL = (20, 25, 34)
GRID = (49, 58, 75)
TEXT = (224, 229, 232)
MUTED = (142, 153, 168)
CORAL = (239, 111, 92)
CYAN = (77, 198, 219)
GOLD = (238, 192, 84)
GREEN = (118, 206, 137)
RED = (234, 92, 108)


def font(size, bold=False):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if os.path.exists(name):
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


title_f = font(64, True)
head_f = font(38, True)
body_f = font(29)
small_f = font(23)
tiny_f = font(19)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def rounded_rect(x0, y0, x1, y1, r, fill, outline=None, width=1):
    d.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=fill, outline=outline, width=width)


def line(points, fill, width=4):
    d.line(points, fill=fill, width=width, joint="curve")


def arrow(x0, y0, x1, y1, fill, width=4):
    line([(x0, y0), (x1, y1)], fill, width)
    ang = math.atan2(y1 - y0, x1 - x0)
    for s in (-1, 1):
        a = ang + s * 0.55 + math.pi
        d.line([(x1, y1), (x1 + 18 * math.cos(a), y1 + 18 * math.sin(a))], fill=fill, width=width)


def label(text, xy, fill=TEXT, f=body_f, anchor="la"):
    d.text(xy, text, fill=fill, font=f, anchor=anchor)


label("SAME RATE, TWO ADDRESSES", (90, 70), f=title_f)
label("the wall is a point only after history has been folded away", (92, 145), fill=MUTED, f=body_f)

left = (90, 230, 830, 1010)
right = (970, 230, 1710, 1010)
rounded_rect(*left, 8, PANEL, outline=(42, 49, 62), width=2)
rounded_rect(*right, 8, PANEL, outline=(42, 49, 62), width=2)


def map_rate(panel, r):
    x0, y0, x1, y1 = panel
    return x0 + 80 + (r - 3) / (54 - 3) * (x1 - x0 - 150)


def axis(panel, y, title):
    x0, y0, x1, y1 = panel
    label(title, (x0 + 40, y0 + 42), f=head_f)
    label("rate (events/sec)", (x0 + 80, y + 72), fill=MUTED, f=small_f)
    d.line((x0 + 80, y, x1 - 70, y), fill=GRID, width=3)
    for r in [3, 12, 18, 54]:
        x = map_rate(panel, r)
        d.line((x, y - 10, x, y + 10), fill=GRID, width=2)
        label(str(r), (x, y + 20), fill=MUTED, f=tiny_f, anchor="ma")


axis(left, 810, "memoryless section")
axis(right, 810, "history-lifted section")

# Left panel: one vertical classifier.
xl18 = map_rate(left, 18)
d.line((xl18, 310, xl18, 810), fill=GOLD, width=5)
label("18", (xl18 + 12, 328), fill=GOLD, f=small_f)
label("one wall", (xl18 + 12, 360), fill=GOLD, f=small_f)
label("RHYTHM", (map_rate(left, 8), 455), fill=CORAL, f=head_f, anchor="ma")
label("TONE", (map_rate(left, 36), 455), fill=CYAN, f=head_f, anchor="ma")
arrow(map_rate(left, 5), 640, map_rate(left, 52), 640, CORAL, 5)
label("from apart", (map_rate(left, 29), 600), fill=CORAL, f=small_f, anchor="ma")
arrow(map_rate(left, 52), 720, map_rate(left, 5), 720, CYAN, 5)
label("from fused", (map_rate(left, 29), 760), fill=CYAN, f=small_f, anchor="ma")
label("same rate -> same name", (left[0] + 370, 920), fill=TEXT, f=body_f, anchor="ma")

# Right panel: two thresholds with a memory band.
xr12 = map_rate(right, 12)
xr18 = map_rate(right, 18)
d.rectangle((xr12, 310, xr18, 810), fill=(34, 36, 45))
d.line((xr12, 310, xr12, 810), fill=RED, width=5)
d.line((xr18, 310, xr18, 810), fill=GOLD, width=5)
label("release", (xr12 - 10, 335), fill=RED, f=small_f, anchor="ra")
label("capture", (xr18 + 10, 335), fill=GOLD, f=small_f)
label("history band", ((xr12 + xr18) / 2, 390), fill=MUTED, f=small_f, anchor="ma")

arrow(map_rate(right, 5), 635, map_rate(right, 52), 635, CORAL, 5)
label("from apart: rhythm until capture", (map_rate(right, 28), 592), fill=CORAL, f=small_f, anchor="ma")
arrow(map_rate(right, 52), 725, map_rate(right, 5), 725, CYAN, 5)
label("from fused: tone until release", (map_rate(right, 28), 766), fill=CYAN, f=small_f, anchor="ma")

sample = map_rate(right, 15)
d.line((sample, 310, sample, 810), fill=(118, 130, 148), width=3)
d.ellipse((sample - 13, 622, sample + 13, 648), fill=CORAL)
d.ellipse((sample - 13, 712, sample + 13, 738), fill=CYAN)
label("15", (sample, 842), fill=TEXT, f=tiny_f, anchor="ma")
label("same rate", (sample, 475), fill=TEXT, f=small_f, anchor="ma")
label("two names", (sample, 508), fill=TEXT, f=small_f, anchor="ma")
label("same rate -> section remembers", (right[0] + 370, 920), fill=TEXT, f=body_f, anchor="ma")

label("quotient: rate only", (left[0] + 40, 275), fill=MUTED, f=small_f)
label("lift: rate + last crossing", (right[0] + 40, 275), fill=MUTED, f=small_f)

# Footer.
label("transition function: change charts by adding the missing coordinate, not by moving the motor", (W / 2, 1090), fill=TEXT, f=body_f, anchor="ma")

os.makedirs("assets", exist_ok=True)
img.save("assets/rate-hysteresis-sections.png")
