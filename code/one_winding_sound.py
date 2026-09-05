from pathlib import Path
from math import exp, pi, cos, sin
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont


SR = 44100
DUR = 72.0
N = int(SR * DUR)
OUT_WAV = Path("assets/one-winding.wav")
OUT_COVER = Path("assets/one-winding-cover.png")

W, H = 1600, 1000


def font(size, bold=False):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


F_TITLE = font(52, True)
F_HEAD = font(28, True)
F_TEXT = font(22)
F_SMALL = font(17)


def flat_bump(u):
    if u <= 0.0 or u >= 1.0:
        return 0.0
    return exp(-1.0 / (u * (1.0 - u)))


def make_theta():
    u = np.linspace(0.0, 1.0, N)
    vals = np.zeros(N, dtype=np.float64)
    inside = (u > 0.0) & (u < 1.0)
    vals[inside] = np.exp(-1.0 / (u[inside] * (1.0 - u[inside])))
    scale = (2.0 * pi * SR) / vals.sum()
    theta = np.cumsum(vals * scale / SR)
    theta[-1] = 2.0 * pi
    return vals, theta, scale


def soft_clip(x):
    return max(-1.0, min(1.0, x))


def write_wav(bump_vals, theta):
    OUT_WAV.parent.mkdir(exist_ok=True)
    t = np.arange(N, dtype=np.float64) / SR
    edge = np.minimum.reduce([np.ones(N), t / 4.0, (DUR - t) / 4.0])
    bump_norm = bump_vals / bump_vals.max()
    body = (
        0.23 * np.sin(2 * pi * 110 * t)
        + 0.08 * np.sin(2 * pi * 220 * t + 0.2)
        + 0.035 * np.sin(2 * pi * 330 * t + 0.7)
    )
    witness = 0.18 * bump_norm * np.sin(2 * pi * 55 * t + 0.4 * np.sin(theta))
    radius = 0.18 + 0.42 * bump_norm
    left = edge * (body + radius * np.cos(theta) * witness)
    right = edge * (body + radius * np.sin(theta) * witness)
    stereo = np.column_stack([left, right])
    pcm = np.clip(stereo, -1.0, 1.0)
    pcm = (pcm * 32767).astype("<i2")
    with wave.open(str(OUT_WAV), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def draw_text(draw, xy, text, fill, fnt, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def polyline(draw, pts, fill, width=3):
    if len(pts) > 1:
        draw.line(pts, fill=fill, width=width, joint="curve")


def make_cover(bump_vals, theta):
    bump_max = float(bump_vals.max())
    img = Image.new("RGB", (W, H), (12, 15, 21))
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=blend((12, 15, 21), (27, 31, 34), y / (H - 1)))

    draw_text(draw, (105, 72), "ONE WINDING, ZERO JET", (236, 229, 209), F_TITLE)
    draw_text(draw, (108, 124), "the doors agree; the room keeps a turn", (158, 172, 177), F_TEXT)

    cx, cy, r = 490, 500, 255
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(79, 88, 99, 220), width=2)
    for k in range(24):
        a = 2 * pi * k / 24
        x0 = cx + (r - 12) * cos(a)
        y0 = cy + (r - 12) * sin(a)
        x1 = cx + r * cos(a)
        y1 = cy + r * sin(a)
        draw.line([(x0, y0), (x1, y1)], fill=(73, 82, 92, 160), width=2)
    pts = []
    for j in range(800):
        th = theta[int(j * (N - 1) / 799)]
        rad = r * (0.48 + 0.42 * flat_bump(j / 799) / bump_max)
        pts.append((cx + rad * cos(th), cy + rad * sin(th)))
    polyline(draw, pts, (232, 223, 194, 255), 6)
    polyline(draw, pts, (212, 91, 104, 120), 14)
    draw.ellipse((cx + r * 0.48 - 12, cy - 12, cx + r * 0.48 + 12, cy + 12), fill=(18, 22, 28, 255), outline=(232, 223, 194, 255), width=3)
    draw_text(draw, (cx, cy + r + 45), "same point, one enclosed turn", (232, 223, 194), F_HEAD, "mm")

    x0, x1 = 870, 1450
    y0, y1 = 275, 515
    draw.rectangle((x0, y0, x1, y1), outline=(77, 87, 98, 210), width=2)
    speed_pts = []
    for j in range(620):
        u = j / 619
        x = x0 + 34 + u * (x1 - x0 - 68)
        y = y1 - 38 - (y1 - y0 - 76) * flat_bump(u) / bump_max
        speed_pts.append((x, y))
    polyline(draw, speed_pts, (107, 190, 174, 255), 5)
    draw_text(draw, (x0 + 30, y0 + 34), "angular speed", (107, 190, 174), F_HEAD)
    draw_text(draw, (x0 + 30, y1 - 24), "flat at both doors", (139, 154, 160), F_SMALL)

    y2, y3 = 610, 820
    draw.rectangle((x0, y2, x1, y3), outline=(77, 87, 98, 210), width=2)
    wind_pts = []
    for j in range(620):
        idx = int(j * (N - 1) / 619)
        u = j / 619
        x = x0 + 34 + u * (x1 - x0 - 68)
        y = y3 - 38 - (y3 - y2 - 76) * theta[idx] / (2 * pi)
        wind_pts.append((x, y))
    polyline(draw, wind_pts, (211, 96, 105, 255), 5)
    draw_text(draw, (x0 + 30, y2 + 34), "accumulated phase", (211, 96, 105), F_HEAD)
    draw_text(draw, (x1 - 30, y2 + 48), "2pi", (211, 96, 105), F_TEXT, "ra")

    draw_text(draw, (105, 910), "Boundary questions see zero. The integral sees the supported passage.", (236, 229, 209), F_HEAD)
    draw_text(draw, (105, 950), "exploratory move: compact support becomes winding", (132, 146, 153), F_SMALL)

    OUT_COVER.parent.mkdir(exist_ok=True)
    img.save(OUT_COVER)


def main():
    bump_vals, theta, _ = make_theta()
    write_wav(bump_vals, theta)
    make_cover(bump_vals, theta)
    print(OUT_WAV)
    print(OUT_COVER)


if __name__ == "__main__":
    main()
