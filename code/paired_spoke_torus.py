from math import floor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1600, 1000
OUT = Path("assets/paired-spoke-torus.png")

STEP_MAX = 108.0
SPOKES_A = 12
SPOKES_B = 20


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


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def draw_text(draw, xy, text, fill, fnt, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def residue(angle_deg, spokes):
    period = 360.0 / spokes
    return ((angle_deg + period / 2.0) % period) - period / 2.0


def map_pair(a, b, box):
    x0, y0, x1, y1 = box
    half_a = 180.0 / SPOKES_A
    half_b = 180.0 / SPOKES_B
    x = x0 + (a + half_a) / (2 * half_a) * (x1 - x0)
    y = y1 - (b + half_b) / (2 * half_b) * (y1 - y0)
    return x, y


def map_strip(angle, spokes, box):
    x0, y0, x1, y1 = box
    half = 180.0 / spokes
    r = residue(angle, spokes)
    x = x0 + angle / STEP_MAX * (x1 - x0)
    y = y1 - (r + half) / (2 * half) * (y1 - y0)
    return x, y


def draw_box(draw, box, title, subtitle=None):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 22, 29, 235), outline=(74, 84, 94, 220), width=2)
    draw_text(draw, (x0 + 18, y0 + 18), title, (232, 228, 212), F_SMALL)
    if subtitle:
        draw_text(draw, (x1 - 18, y0 + 18), subtitle, (143, 158, 164), F_TINY, "ra")


def draw_reading_strip(draw, box, spokes, color, label):
    x0, y0, x1, y1 = box
    draw_box(draw, box, label, f"{spokes} spokes")
    half = 180.0 / spokes
    mid_y = (y0 + y1) / 2
    draw.line((x0 + 48, mid_y, x1 - 24, mid_y), fill=(96, 105, 114, 135), width=1)
    for value in (-half, 0, half):
        y = y1 - (value + half) / (2 * half) * (y1 - y0)
        draw.line((x0 + 48, y, x1 - 24, y), fill=(96, 105, 114, 165), width=1)
        draw_text(draw, (x0 + 30, y), f"{value:+.0f}", (136, 151, 157), F_TINY, "rm")
    for angle in range(0, int(STEP_MAX) + 1, 18):
        x = x0 + angle / STEP_MAX * (x1 - x0)
        draw.line((x, y1 - 12, x, y1), fill=(96, 105, 114, 150), width=1)
    pts = [map_strip(i * STEP_MAX / 900, spokes, box) for i in range(901)]
    draw.line(pts, fill=color, width=4, joint="curve")
    period = 360.0 / spokes
    for k in range(1, floor(STEP_MAX / (period / 2.0)) + 1):
        angle = k * period / 2.0
        x = x0 + angle / STEP_MAX * (x1 - x0)
        draw.line((x, y0 + 54, x, y1 - 18), fill=(230, 220, 193, 105), width=2)
    draw_text(draw, (x1 - 24, y1 - 22), "motor angle", (136, 151, 157), F_TINY, "ra")


def draw_torus_chart(draw, box):
    x0, y0, x1, y1 = box
    draw_box(draw, box, "paired residues", "a torus chart, flattened")
    half_a = 180.0 / SPOKES_A
    half_b = 180.0 / SPOKES_B

    for i in range(1, 6):
        x = x0 + i * (x1 - x0) / 6
        draw.line((x, y0 + 62, x, y1 - 54), fill=(70, 80, 90, 150), width=1)
    for i in range(1, 6):
        y = y0 + 62 + i * (y1 - y0 - 116) / 6
        draw.line((x0 + 58, y, x1 - 40, y), fill=(70, 80, 90, 150), width=1)

    inner = (x0 + 58, y0 + 62, x1 - 40, y1 - 54)
    draw.rectangle(inner, outline=(120, 130, 138, 170), width=1)
    draw_text(draw, (inner[0], inner[3] + 24), f"12-clock {-half_a:.0f}", (142, 157, 163), F_TINY)
    draw_text(draw, (inner[2], inner[3] + 24), f"{half_a:.0f}", (142, 157, 163), F_TINY, "ra")
    draw_text(draw, (inner[0] - 18, inner[1]), f"20-clock {half_b:.0f}", (142, 157, 163), F_TINY, "rm")
    draw_text(draw, (inner[0] - 18, inner[3]), f"{-half_b:.0f}", (142, 157, 163), F_TINY, "rm")

    chunks = []
    current = []
    previous = None
    seam_marks = []
    for i in range(1201):
        angle = i * STEP_MAX / 1200
        a = residue(angle, SPOKES_A)
        b = residue(angle, SPOKES_B)
        point = map_pair(a, b, inner)
        if previous and (abs(point[0] - previous[0]) > 260 or abs(point[1] - previous[1]) > 260):
            chunks.append(current)
            current = []
            seam_marks.append(previous)
            seam_marks.append(point)
        current.append(point)
        previous = point
    chunks.append(current)

    for pts in chunks:
        if len(pts) > 1:
            draw.line(pts, fill=(228, 190, 92, 235), width=5, joint="curve")
    for x, y in seam_marks:
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(238, 113, 119, 245))

    for angle, label in [(13, "13"), (18, "18"), (30, "30"), (72, "72"), (90, "90")]:
        a = residue(angle, SPOKES_A)
        b = residue(angle, SPOKES_B)
        x, y = map_pair(a, b, inner)
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=(104, 207, 202, 245))
        draw_text(draw, (x + 13, y - 10), label, (204, 225, 221), F_TINY)


def main():
    img = Image.new("RGB", (W, H), (10, 13, 18))
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        draw.line((0, y, W, y), fill=blend((10, 13, 18), (29, 31, 35), y / (H - 1)))

    draw_text(draw, (96, 70), "THE PAIR KEEPS THE TURN", (235, 229, 210), F_TITLE)
    draw_text(draw, (100, 126), "each clock folds at its own wall; together they mark the seam, not a second motor", (150, 165, 171), F_TEXT)

    draw_reading_strip(draw, (105, 210, 705, 430), SPOKES_A, (238, 113, 119, 245), "clock A reading")
    draw_reading_strip(draw, (105, 492, 705, 712), SPOKES_B, (104, 207, 202, 245), "clock B reading")
    draw_torus_chart(draw, (785, 210, 1495, 812))

    draw_text(draw, (112, 872), "A single coordinate reverses at its cut.", (235, 229, 210), F_HEAD)
    draw_text(draw, (112, 914), "The ordered pair does not add torque; it localizes which section jumped.", (235, 229, 210), F_HEAD)
    draw_text(draw, (112, 956), "Exploratory move: disagreement becomes an atlas for the quotient.", (137, 151, 158), F_SMALL)

    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(OUT)
    for angle in (13, 18, 30, 72, 90):
        print(f"{angle:>3} deg -> ({residue(angle, SPOKES_A):+.1f}, {residue(angle, SPOKES_B):+.1f})")


if __name__ == "__main__":
    main()
