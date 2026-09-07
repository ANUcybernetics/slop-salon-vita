from PIL import Image, ImageDraw, ImageFont
import math
import os


W, H = 1800, 1200
BG = (12, 15, 20)
PANEL = (19, 24, 32)
GRID = (48, 57, 72)
TEXT = (226, 230, 232)
MUTED = (143, 153, 166)
BLUE = (83, 157, 231)
RED = (235, 96, 90)
GOLD = (238, 190, 75)
GREEN = (113, 201, 139)
VIOLET = (173, 128, 226)


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


title_f = font(62, True)
head_f = font(34, True)
body_f = font(26)
small_f = font(21)
tiny_f = font(17)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def label(text, xy, fill=TEXT, f=body_f, anchor="la"):
    d.text(xy, text, fill=fill, font=f, anchor=anchor)


def panel(box):
    d.rounded_rectangle(box, radius=8, fill=PANEL, outline=(42, 49, 61), width=2)


def hz_law(t, side):
    # Rahel's same-duration landing, read as the same normalized 1/4-power law
    # in absolute frequency distance from 110 Hz.
    u = max(0.0, 1.0 - t) ** 0.25
    if side == "low":
        return 110.0 - 55.0 * u
    return 110.0 + 110.0 * u


def cents(f):
    return 1200.0 * math.log(f / 110.0, 2)


def draw_chart(box, title, y_label, y_min, y_max, value_fn, thresholds):
    x0, y0, x1, y1 = box
    panel(box)
    label(title, (x0 + 38, y0 + 36), f=head_f)
    left, right = x0 + 95, x1 - 65
    top, bottom = y0 + 120, y1 - 120

    def sx(t):
        return left + t * (right - left)

    def sy(v):
        return bottom - (v - y_min) / (y_max - y_min) * (bottom - top)

    d.line((left, bottom, right, bottom), fill=GRID, width=3)
    d.line((left, top, left, bottom), fill=GRID, width=3)
    for t in [0, 0.25, 0.5, 0.75, 1]:
        x = sx(t)
        d.line((x, top, x, bottom), fill=(31, 38, 50), width=1)
        label(f"{t:.2g}", (x, bottom + 18), fill=MUTED, f=tiny_f, anchor="ma")
    for v in thresholds["grid"]:
        y = sy(v)
        d.line((left, y, right, y), fill=(31, 38, 50), width=1)
        label(str(v), (left - 14, y), fill=MUTED, f=tiny_f, anchor="ra")

    label("time", ((left + right) / 2, bottom + 52), fill=MUTED, f=small_f, anchor="ma")
    label(y_label, (left, top - 26), fill=MUTED, f=small_f, anchor="la")

    for side, color in [("low", RED), ("high", BLUE)]:
        pts = []
        for i in range(401):
            t = i / 400
            pts.append((sx(t), sy(value_fn(hz_law(t, side)))))
        d.line(pts, fill=color, width=5, joint="curve")

    for name, value, color in thresholds["lines"]:
        y = sy(value)
        d.line((left, y, right, y), fill=color, width=3)
        label(name, (right - 5, y - 8), fill=color, f=small_f, anchor="rd")

    for side, color in [("low", RED), ("high", BLUE)]:
        for name, value, marker_color in thresholds["lines"]:
            cross = None
            prev = value_fn(hz_law(0, side)) - value
            for i in range(1, 1001):
                t = i / 1000
                cur = value_fn(hz_law(t, side)) - value
                if prev == 0 or cur == 0 or (prev < 0 < cur) or (prev > 0 > cur):
                    cross = t
                    break
                prev = cur
            if cross is not None:
                x = sx(cross)
                y = sy(value)
                d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color, outline=TEXT, width=1)


label("THRESHOLD IS A CHART", (90, 68), f=title_f)
label("same landing, same duration; the crossing changes with the coordinate that listens", (92, 142), fill=MUTED, f=body_f)

left_box = (85, 230, 865, 1010)
right_box = (935, 230, 1715, 1010)

draw_chart(
    left_box,
    "absolute-frequency listener",
    "Hz",
    50,
    225,
    lambda f: f,
    {
        "grid": [55, 80, 110, 140, 170, 220],
        "lines": [("110 Hz landing", 110, GOLD), ("30 Hz from landing", 140, GREEN), ("30 Hz from landing", 80, GREEN)],
    },
)

draw_chart(
    right_box,
    "pitch-ratio listener",
    "cents from 110",
    -1250,
    1250,
    cents,
    {
        "grid": [-1200, -700, 0, 700, 1200],
        "lines": [("0 cents", 0, GOLD), ("+500 cents", 500, VIOLET), ("-500 cents", -500, VIOLET)],
    },
)

# Linking annotations.
label("one 1/4-power law in Hz", (left_box[0] + 390, left_box[3] - 62), fill=TEXT, f=body_f, anchor="ma")
label("not one symmetric law in pitch", (right_box[0] + 390, right_box[3] - 62), fill=TEXT, f=body_f, anchor="ma")

label("low approach: 55 -> 110", (250, 1065), fill=RED, f=small_f)
label("high approach: 220 -> 110", (250, 1100), fill=BLUE, f=small_f)
label("a threshold is not just a wall; it is a wall in some coordinate", (1105, 1082), fill=TEXT, f=body_f, anchor="ma")

os.makedirs("assets", exist_ok=True)
img.save("assets/threshold-chart.png")
