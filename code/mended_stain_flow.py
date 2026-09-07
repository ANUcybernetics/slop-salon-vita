from math import exp, pi, sin, cos
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


W, H = 1800, 1800
S = 2
OUT = "assets/mended-stain-flow.png"
random.seed(17)


def sx(x):
    return int((x + 1.0) * 0.5 * W * S)


def sy(y):
    return int((1.0 - (y + 1.0) * 0.5) * H * S)


def seam_x(y):
    return 0.06 * sin(2.4 * pi * y + 0.35) + 0.018 * sin(9.0 * pi * y)


holes = []
for y in np.linspace(-0.78, 0.78, 11):
    x = seam_x(y)
    holes.append((x - 0.038, y + 0.012 * sin(9 * y)))
    holes.append((x + 0.038, y - 0.012 * sin(7 * y)))


def field(x, y):
    u = 0.010
    v = 0.000

    d = x - seam_x(y)
    gate = exp(-(d * d) / 0.006)
    u *= 1.0 - 0.62 * gate
    v += 0.011 * gate * sin(5.0 * y + 0.7)

    for i, (hx, hy) in enumerate(holes):
        dx = x - hx
        dy = y - hy
        r2 = dx * dx + dy * dy + 0.0009
        g = exp(-r2 / 0.018)
        spin = 1 if i % 2 == 0 else -1
        u += spin * (-dy) * g * 0.032
        v += spin * dx * g * 0.032
        u += dx * g * 0.006
        v += dy * g * 0.006

    v += 0.0015 * sin(8 * y + 7 * x)
    return u, v


def draw_polyline(draw, pts, color, width):
    if len(pts) > 1:
        draw.line([(sx(x), sy(y)) for x, y in pts], fill=color, width=width, joint="curve")


img = Image.new("RGB", (W * S, H * S), (227, 216, 191))
px = img.load()
for y in range(H * S):
    for x in range(W * S):
        grain = random.randint(-8, 8)
        fiber = int(7 * sin((x * 0.021) + 1.8 * sin(y * 0.008)))
        base = np.array([227, 216, 191]) + grain + fiber
        px[x, y] = tuple(np.clip(base, 0, 255).astype(int))

wash = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
wd = ImageDraw.Draw(wash, "RGBA")

for seed in np.linspace(-0.88, 0.88, 76):
    y = float(seed + random.uniform(-0.01, 0.01))
    x = -0.94 + random.uniform(-0.015, 0.015)
    pts = []
    strength = random.uniform(0.55, 1.0)
    for _ in range(310):
        pts.append((x, y))
        u, v = field(x, y)
        x += u + random.uniform(-0.0012, 0.0012)
        y += v + random.uniform(-0.0017, 0.0017)
        if x > 0.92 or y < -0.96 or y > 0.96:
            break
    alpha = int(30 + 70 * strength)
    width = random.choice([5, 6, 7, 8]) * S
    color = (126, 62, 34, alpha)
    draw_polyline(wd, pts, color, width)

for _ in range(1700):
    x = random.gauss(-0.22, 0.42)
    y = random.gauss(0.04, 0.48)
    if -0.98 < x < 0.95 and -0.92 < y < 0.92:
        u, v = field(x, y)
        r = random.uniform(2.0, 7.5) * S
        a = int(8 + 35 * min(1, (u * u + v * v) * 8200))
        wd.ellipse((sx(x) - r, sy(y) - r, sx(x) + r, sy(y) + r), fill=(98, 43, 25, a))

wash = wash.filter(ImageFilter.GaussianBlur(1.15 * S))
img = Image.alpha_composite(img.convert("RGBA"), wash)

d = ImageDraw.Draw(img, "RGBA")
crack = [(seam_x(y), y) for y in np.linspace(-0.88, 0.88, 260)]
draw_polyline(d, crack, (58, 46, 40, 195), 5 * S)
draw_polyline(d, [(x + 0.006, y) for x, y in crack], (246, 234, 205, 96), 2 * S)

for i in range(0, len(holes), 2):
    left = holes[i]
    right = holes[i + 1]
    mx = (left[0] + right[0]) / 2
    my = (left[1] + right[1]) / 2
    amp = 0.025
    pts = []
    for t in np.linspace(0, 1, 24):
        x = (1 - t) * left[0] + t * right[0]
        y = (1 - t) * left[1] + t * right[1] + amp * sin(pi * t)
        pts.append((x, y))
    draw_polyline(d, pts, (23, 82, 178, 238), 5 * S)
    for hx, hy in (left, right):
        rr = 0.012 * S * W
        d.ellipse((sx(hx) - rr, sy(hy) - rr, sx(hx) + rr, sy(hy) + rr), fill=(45, 41, 38, 220))
        d.ellipse((sx(hx) - rr * 0.55, sy(hy) - rr * 0.55, sx(hx) + rr * 0.55, sy(hy) + rr * 0.55), fill=(214, 198, 168, 210))
    if i in (4, 10, 16):
        d.line((sx(mx - 0.18), sy(my), sx(mx + 0.18), sy(my + 0.04)), fill=(105, 50, 29, 64), width=3 * S)

for y in np.linspace(-0.75, 0.75, 9):
    x = seam_x(y)
    u, v = field(x, y)
    d.line((sx(x - 0.13), sy(y - 0.035), sx(x - 0.03), sy(y + v * 2.2)), fill=(250, 224, 155, 135), width=2 * S)
    d.line((sx(x + 0.03), sy(y + v * 2.2), sx(x + 0.15), sy(y + 0.045)), fill=(250, 224, 155, 135), width=2 * S)

d.rectangle((0, 0, W * S - 1, H * S - 1), outline=(38, 35, 32, 255), width=7 * S)

img = img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
img.save(OUT, quality=95)
print(OUT)
