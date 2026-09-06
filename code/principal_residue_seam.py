from math import floor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1600, 1000
STEP_DEG = 13.0
OUT = Path("assets/principal-residue-seam.png")


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(52, True)
F_HEAD = font(30, True)
F_TEXT = font(22)
F_SMALL = font(17)
F_TINY = font(14)


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def draw_text(draw, xy, text, fill, fnt, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def principal_residue(angle_deg, spokes):
    period = 360.0 / spokes
    return ((angle_deg + period / 2.0) % period) - period / 2.0


def sign_color(value):
    if value >= 0:
        return (238, 116, 121, 245)
    return (102, 206, 202, 245)


def plot_xy(n, residue, x0, x1, y0, y1):
    x = x0 + (n - 8) / (60 - 8) * (x1 - x0)
    y = y0 + (18.0 - residue) / 36.0 * (y1 - y0)
    return x, y


def draw_axes(draw, x0, y0, x1, y1):
    draw.rectangle((x0, y0, x1, y1), fill=(17, 22, 29, 235), outline=(73, 83, 93, 220), width=2)
    for deg in range(-15, 20, 5):
        _, y = plot_xy(3, deg, x0, x1, y0, y1)
        fill = (236, 229, 207, 170) if deg == 0 else (82, 92, 102, 135)
        draw.line((x0, y, x1, y), fill=fill, width=2 if deg == 0 else 1)
        draw_text(draw, (x0 - 18, y), f"{deg:+d}", (139, 153, 160), F_TINY, "rm")
    for n in [8, 10, 12, 20, 30, 40, 50, 60]:
        x, _ = plot_xy(n, 0, x0, x1, y0, y1)
        draw.line((x, y0, x, y1), fill=(82, 92, 102, 115), width=1)
        draw_text(draw, (x, y1 + 20), str(n), (139, 153, 160), F_TINY, "mm")
    draw_text(draw, ((x0 + x1) / 2, y1 + 58), "spoke count N", (180, 190, 185), F_SMALL, "mm")
    draw_text(draw, (x0 + 22, y0 + 18), "principal residue, degrees", (180, 190, 185), F_TINY)


def draw_window(draw, x0, y0, x1, y1):
    upper = []
    lower = []
    for n in range(10, 61):
        half = 180.0 / n
        upper.append(plot_xy(n, half, x0, x1, y0, y1))
        lower.append(plot_xy(n, -half, x0, x1, y0, y1))
    draw.line(upper, fill=(235, 228, 207, 145), width=2)
    draw.line(lower, fill=(235, 228, 207, 145), width=2)
    for n in [12, 20]:
        half = 180.0 / n
        x, yu = plot_xy(n, half, x0, x1, y0, y1)
        _, yl = plot_xy(n, -half, x0, x1, y0, y1)
        draw.line((x, yu, x, yl), fill=(235, 228, 207, 170), width=2)


def draw_residue_curve(draw, x0, y0, x1, y1):
    previous = None
    for n in range(8, 61):
        r = principal_residue(STEP_DEG, n)
        point = plot_xy(n, r, x0, x1, y0, y1)
        if previous:
            draw.line((previous[0], previous[1], point[0], point[1]), fill=(120, 132, 142, 120), width=2)
        color = sign_color(r)
        radius = 7 if n not in (12, 20) else 13
        draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), fill=color)
        if n in (12, 20):
            label = f"N={n}: {r:+.0f} deg"
            draw_text(draw, (point[0] + 18, point[1] - 8), label, color, F_SMALL)
        previous = point


def draw_branch_strips(draw, x, y):
    for n, color, label in [
        (12, (238, 116, 121, 245), "12 spokes"),
        (20, (102, 206, 202, 245), "20 spokes"),
    ]:
        period = 360.0 / n
        half = period / 2.0
        r = principal_residue(STEP_DEG, n)
        draw.rounded_rectangle((x, y, x + 430, y + 112), radius=6, fill=(18, 23, 30, 240), outline=(72, 82, 92, 220), width=2)
        draw_text(draw, (x + 24, y + 20), label, (227, 231, 222), F_TEXT)
        draw_text(draw, (x + 406, y + 20), f"window +/-{half:.0f} deg", (139, 153, 160), F_TINY, "ra")
        track_x0, track_x1 = x + 54, x + 376
        track_y = y + 72
        draw.line((track_x0, track_y, track_x1, track_y), fill=(80, 90, 101, 220), width=2)
        draw.line((x + 215, track_y - 16, x + 215, track_y + 16), fill=(233, 229, 212, 210), width=2)
        px = x + 215 + (r / half) * 150
        draw.ellipse((px - 11, track_y - 11, px + 11, track_y + 11), fill=color)
        draw_text(draw, (px, track_y + 28), f"{r:+.0f}", color, F_SMALL, "mm")
        y += 142


def main():
    img = Image.new("RGB", (W, H), (10, 13, 18))
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        draw.line((0, y, W, y), fill=blend((10, 13, 18), (28, 31, 35), y / (H - 1)))

    draw_text(draw, (96, 72), "THE SEAM IS CHOSEN", (235, 229, 210), F_TITLE)
    draw_text(draw, (100, 128), "one positive step, many quotient clocks; direction appears at the nearest-lift cut", (150, 165, 171), F_TEXT)

    x0, y0, x1, y1 = 132, 232, 1080, 798
    draw_axes(draw, x0, y0, x1, y1)
    draw_window(draw, x0, y0, x1, y1)
    draw_residue_curve(draw, x0, y0, x1, y1)

    draw.rounded_rectangle((1135, 232, 1495, 506), radius=6, fill=(18, 23, 30, 238), outline=(72, 82, 92, 220), width=2)
    draw_text(draw, (1165, 274), "rule", (235, 229, 210), F_HEAD)
    draw_text(draw, (1165, 326), "period = 360 / N", (188, 198, 192), F_TEXT)
    draw_text(draw, (1165, 366), "keep the residue inside", (188, 198, 192), F_TEXT)
    draw_text(draw, (1165, 406), "(-period/2, period/2]", (188, 198, 192), F_TEXT)
    draw_text(draw, (1165, 462), f"fixed step = +{STEP_DEG:.0f} deg", (235, 229, 210), F_TEXT)

    draw_branch_strips(draw, 1135, 560)

    boundary = floor(180.0 / STEP_DEG)
    draw_text(draw, (132, 874), f"At N={boundary + 1}, the half-window falls below the step.", (235, 229, 210), F_HEAD)
    draw_text(draw, (132, 916), f"The motor still turns +{STEP_DEG:.0f}; the representative crosses the cut.", (235, 229, 210), F_HEAD)
    draw_text(draw, (132, 958), "Exploratory move: direction is assigned by the section, not recovered from the quotient.", (137, 151, 158), F_SMALL)

    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(OUT)
    for n in (12, 20):
        print(f"N={n} residue={principal_residue(STEP_DEG, n):.6f}")


if __name__ == "__main__":
    main()
