from math import cos, exp, pi, sin
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


W, H = 1800, 1200
S = 2
OUT = "assets/residual-frustration-medium.png"
random.seed(29)

BG = (16, 18, 20)
PAPER = (218, 211, 193)
INK = (37, 40, 42)
MUTED = (116, 124, 128)
GOLD = (231, 181, 83)
BLUE = (72, 142, 210)
RED = (207, 80, 70)
GREEN = (96, 175, 121)


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


title_f = font(58, True)
head_f = font(30, True)
body_f = font(24)
small_f = font(18)


img = Image.new("RGB", (W * S, H * S), BG)
px = img.load()
for y in range(H * S):
    for x in range(W * S):
        grain = random.randint(-5, 5)
        fiber = int(5 * sin(x * 0.018 + 0.7 * sin(y * 0.011)))
        shade = np.array(PAPER) + grain + fiber
        if x < W * S * 0.5:
            shade = shade * np.array([0.93, 0.96, 1.02])
        else:
            shade = shade * np.array([1.0, 0.96, 0.91])
        px[x, y] = tuple(np.clip(shade, 0, 255).astype(int))

veil = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil, "RGBA")
vd.rectangle((0, 0, W * S, H * S), fill=(0, 0, 0, 32))
vd.line((W * S // 2, 120 * S, W * S // 2, (H - 100) * S), fill=(35, 34, 32, 180), width=4 * S)


def scale(box, x, y):
    x0, y0, x1, y1 = box
    return (x0 + x * (x1 - x0), y0 + y * (y1 - y0))


def draw_text(draw, xy, text, fill=INK, f=body_f, anchor="la"):
    draw.text(xy, text, fill=fill, font=f, anchor=anchor)


left = (105 * S, 205 * S, 825 * S, 1045 * S)
right = (975 * S, 205 * S, 1695 * S, 1045 * S)

for box, tint in [(left, (220, 232, 242, 34)), (right, (242, 222, 200, 34))]:
    vd.rounded_rectangle(box, radius=10 * S, fill=tint, outline=(44, 45, 43, 185), width=2 * S)

# Left: the quotient closes cleanly.
cx, cy = scale(left, 0.5, 0.5)
r = 236 * S
for k in range(6):
    a = 2 * pi * k / 6 - pi / 2
    b = 2 * pi * (k + 1) / 6 - pi / 2
    x1, y1 = cx + r * cos(a), cy + r * sin(a)
    x2, y2 = cx + r * cos(b), cy + r * sin(b)
    vd.line((x1, y1, x2, y2), fill=(*BLUE, 175), width=6 * S)
    vd.ellipse((x1 - 15 * S, y1 - 15 * S, x1 + 15 * S, y1 + 15 * S), fill=(*BLUE, 230))
vd.ellipse((cx - 88 * S, cy - 88 * S, cx + 88 * S, cy + 88 * S), fill=(*GOLD, 225), outline=(75, 55, 30, 230), width=5 * S)
for k in range(12):
    a = 2 * pi * k / 12
    x1, y1 = cx + 104 * S * cos(a), cy + 104 * S * sin(a)
    x2, y2 = cx + 170 * S * cos(a), cy + 170 * S * sin(a)
    vd.line((x1, y1, x2, y2), fill=(70, 87, 96, 115), width=2 * S)

# Right: the same closure leaves a frustrated material state.
cx, cy = scale(right, 0.5, 0.5)
r = 236 * S
for k in range(6):
    a = 2 * pi * k / 6 - pi / 2
    b = 2 * pi * (k + 1) / 6 - pi / 2
    x1, y1 = cx + r * cos(a), cy + r * sin(a)
    x2, y2 = cx + r * cos(b), cy + r * sin(b)
    sag = 35 * S * sin(k * 1.7)
    mx, my = (x1 + x2) / 2 + sag * cos((a + b) / 2), (y1 + y2) / 2 + sag * sin((a + b) / 2)
    vd.line((x1, y1, mx, my, x2, y2), fill=(*BLUE, 92), width=5 * S, joint="curve")

field = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
fd = ImageDraw.Draw(field, "RGBA")
for seed in np.linspace(0, 2 * pi, 150):
    pts = []
    phase = random.uniform(-0.09, 0.09)
    for i in range(130):
        t = i / 129
        a = seed + 2.9 * pi * t + phase * sin(8 * t)
        rr = (70 + 210 * t + 18 * sin(5 * a)) * S
        x = cx + rr * cos(a)
        y = cy + rr * sin(a) * 0.78
        pull = exp(-((t - 0.48) ** 2) / 0.052)
        x += 38 * S * pull * cos(seed * 3)
        y += 28 * S * pull * sin(seed * 2)
        pts.append((x, y))
    alpha = random.randint(22, 58)
    fd.line(pts, fill=(*RED, alpha), width=random.choice([2, 3, 4]) * S, joint="curve")

for k in range(16):
    a = 2 * pi * k / 16 + 0.15
    x1 = cx + 82 * S * cos(a)
    y1 = cy + 64 * S * sin(a)
    x2 = cx + 292 * S * cos(a + 0.18 * sin(k))
    y2 = cy + 228 * S * sin(a + 0.18 * sin(k))
    fd.line((x1, y1, x2, y2), fill=(*RED, 105), width=3 * S)

field = field.filter(ImageFilter.GaussianBlur(0.55 * S))
veil = Image.alpha_composite(veil, field)

d = ImageDraw.Draw(veil, "RGBA")
draw_text(d, (W * S // 2, 80 * S), "RESIDUAL STATE", fill=(35, 37, 39, 255), f=title_f, anchor="ma")
draw_text(d, scale(left, 0.08, 0.08), "simulation", fill=(42, 54, 62, 255), f=head_f)
draw_text(d, scale(left, 0.08, 0.93), "quotient closes", fill=(48, 57, 60, 255), f=body_f)
draw_text(d, scale(right, 0.08, 0.08), "medium", fill=(67, 43, 35, 255), f=head_f)
draw_text(d, scale(right, 0.08, 0.93), "path remains", fill=(72, 45, 36, 255), f=body_f)

draw_text(d, scale(left, 0.5, 0.5), "verdict", fill=(52, 38, 20, 255), f=head_f, anchor="mm")
draw_text(d, scale(right, 0.5, 0.5), "defect", fill=(92, 28, 24, 255), f=head_f, anchor="mm")

for i, text in enumerate(["fold to mono", "same answer"]):
    y = 1085 * S + i * 34 * S
    draw_text(d, (275 * S, y), text, fill=(58, 64, 65, 245), f=small_f)
for i, text in enumerate(["side keeps the path", "frustration has a lifetime"]):
    y = 1085 * S + i * 34 * S
    draw_text(d, (1110 * S, y), text, fill=(82, 48, 41, 245), f=small_f)

img = Image.alpha_composite(img.convert("RGBA"), veil)
img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")
os.makedirs("assets", exist_ok=True)
img.save(OUT, quality=95)
print(OUT)
