from math import exp
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


W, H = 1600, 1000
OUT = Path("assets/same-area-quotient.png")


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
F_HEAD = font(29, True)
F_TEXT = font(22)
F_SMALL = font(17)
F_TINY = font(14)


def bump(u):
    if u <= 0.0 or u >= 1.0:
        return 0.0
    return exp(-1.0 / (u * (1.0 - u)))


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def draw_text(draw, xy, text, fill, fnt, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def polyline(draw, pts, fill, width=3):
    if len(pts) > 1:
        draw.line(pts, fill=fill, width=width, joint="curve")


def shape_a(u):
    return bump(u)


def shape_b(u):
    return 0.78 * bump(u) + 0.56 * bump((u - 0.08) / 0.42) + 0.42 * bump((u - 0.52) / 0.34)


def make_scaled_paths():
    xs = np.linspace(0.0, 1.0, 900)
    ya = np.array([shape_a(float(x)) for x in xs])
    yb = np.array([shape_b(float(x)) for x in xs])
    area_a = float(np.trapezoid(ya, xs))
    area_b = float(np.trapezoid(yb, xs))
    yb *= area_a / area_b
    return xs, ya, yb, area_a, float(np.trapezoid(yb, xs))


def path_points(xs, ys, x0, x1, base, amp):
    pts = []
    for x, y in zip(xs, ys):
        pts.append((x0 + float(x) * (x1 - x0), base - float(y) * amp))
    return pts


def draw_area_bar(draw, x, y, w, h, label, value, fill):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=6, fill=(18, 22, 29, 240), outline=(75, 84, 94, 220), width=2)
    draw.rectangle((x + 18, y + h - 32, x + w - 18, y + h - 18), fill=(49, 57, 64, 255))
    draw.rectangle((x + 18, y + h - 32, x + w - 18, y + h - 18), outline=(104, 112, 120, 210), width=1)
    draw.rectangle((x + 18, y + h - 32, x + w - 18, y + h - 18), fill=fill)
    draw_text(draw, (x + 20, y + 20), label, (221, 226, 218), F_SMALL)
    draw_text(draw, (x + w - 20, y + 20), value, fill, F_SMALL, "ra")


def main():
    xs, ya, yb, area_a, area_b = make_scaled_paths()
    img = Image.new("RGB", (W, H), (12, 15, 21))
    draw = ImageDraw.Draw(img, "RGBA")

    for y in range(H):
        draw.line([(0, y), (W, y)], fill=blend((12, 15, 21), (28, 30, 34), y / (H - 1)))

    draw_text(draw, (102, 70), "SAME WITNESS, DIFFERENT CROSSING", (235, 228, 207), F_TITLE)
    draw_text(draw, (105, 124), "signed area keeps one quotient; the path itself is lost", (154, 170, 176), F_TEXT)

    x0, x1 = 190, 1265
    top_base, bot_base = 355, 675
    amp = 9000
    door_a, door_b = x0, x1
    room = (105, 185, 1495, 820)
    draw.rectangle(room, fill=(20, 24, 31, 225), outline=(78, 86, 96, 210), width=2)

    for x in (door_a, door_b):
        draw.line([(x, 185), (x, 820)], fill=(224, 216, 190, 130), width=2)
    draw_text(draw, (door_a, 850), "door A", (206, 199, 180), F_SMALL, "mm")
    draw_text(draw, (door_b, 850), "door B", (206, 199, 180), F_SMALL, "mm")

    pts_a = path_points(xs, ya, x0, x1, top_base, amp)
    pts_b = path_points(xs, yb, x0, x1, bot_base, amp)

    for base, pts, fill, stroke, label, sub in [
        (top_base, pts_a, (208, 92, 105, 42), (229, 104, 117, 255), "crossing A", "one smooth debt"),
        (bot_base, pts_b, (93, 184, 169, 42), (112, 204, 188, 255), "crossing B", "two smaller debts"),
    ]:
        fill_poly = [(x0, base)] + pts + [(x1, base)]
        draw.polygon(fill_poly, fill=fill)
        draw.line([(x0 - 45, base), (x1 + 45, base)], fill=(91, 99, 108, 160), width=2)
        polyline(draw, pts, stroke, 6)
        for x in (x0, x1):
            draw.ellipse((x - 10, base - 10, x + 10, base + 10), fill=(14, 18, 24, 255), outline=(235, 228, 207, 240), width=3)
        draw_text(draw, (132, base - 108), label, (225, 229, 220), F_HEAD)
        draw_text(draw, (132, base - 72), sub, (137, 151, 158), F_TEXT)
        draw_text(draw, (x1 + 34, base + 22), "local state = 0", (153, 168, 171), F_TINY)

    # The equality mark is the work: visibly different curves, identical area readout.
    draw.line([(1350, 262), (1456, 262)], fill=(235, 228, 207, 220), width=5)
    draw.line([(1350, 293), (1456, 293)], fill=(235, 228, 207, 220), width=5)
    draw_text(draw, (1403, 334), "same quotient", (235, 228, 207), F_SMALL, "mm")

    draw_area_bar(draw, 1285, 430, 210, 96, "area A", f"{area_a:.6f}", (229, 104, 117, 235))
    draw_area_bar(draw, 1285, 552, 210, 96, "area B", f"{area_b:.6f}", (112, 204, 188, 235))

    draw_text(draw, (112, 908), "The witness does not preserve the event. It preserves the relation: equal signed area.", (235, 228, 207), F_HEAD)
    draw_text(draw, (112, 950), "exploratory move: path-memory becomes a quotient map", (132, 146, 153), F_SMALL)

    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(OUT)
    print(f"area_a={area_a:.12f}")
    print(f"area_b={area_b:.12f}")


if __name__ == "__main__":
    main()
