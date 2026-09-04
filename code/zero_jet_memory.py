from pathlib import Path
from math import exp

from PIL import Image, ImageDraw, ImageFont


W, H = 1600, 1000
OUT = Path("assets/zero-jet-memory.png")


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
F_TEXT = font(23)
F_SMALL = font(18)
F_TINY = font(15)


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def bump(u):
    if u <= 0 or u >= 1:
        return 0.0
    return exp(-1.0 / (u * (1 - u)))


def draw_text(draw, xy, text, fill, fnt, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def polyline(draw, pts, fill, width=3):
    if len(pts) > 1:
        draw.line(pts, fill=fill, width=width, joint="curve")


def main():
    img = Image.new("RGB", (W, H), (13, 16, 22))
    draw = ImageDraw.Draw(img, "RGBA")

    # Subtle paper grain and room bands.
    for y in range(H):
        t = y / (H - 1)
        col = blend((15, 18, 25), (26, 29, 34), t)
        draw.line([(0, y), (W, y)], fill=col)

    draw.rectangle((110, 170, 1490, 790), fill=(21, 25, 32, 230), outline=(78, 84, 95, 180), width=2)
    draw.rectangle((110, 170, 520, 790), fill=(34, 42, 54, 135))
    draw.rectangle((1080, 170, 1490, 790), fill=(34, 42, 54, 135))
    draw.rectangle((520, 170, 1080, 790), fill=(39, 50, 45, 95))

    draw_text(draw, (110, 70), "ZERO-JET CROSSING", (232, 225, 204), F_TITLE)
    draw_text(draw, (111, 123), "the room contains the event; the doors read zero", (165, 177, 184), F_TEXT)

    left_x, right_x = 520, 1080
    draw.line([(left_x, 170), (left_x, 790)], fill=(225, 216, 190, 180), width=2)
    draw.line([(right_x, 170), (right_x, 790)], fill=(225, 216, 190, 180), width=2)
    draw_text(draw, (left_x, 825), "door A", (214, 205, 181), F_SMALL, "mm")
    draw_text(draw, (right_x, 825), "door B", (214, 205, 181), F_SMALL, "mm")

    # Main path: baseline plus compactly supported smooth bump inside the room.
    xs = [160 + i * (1280 / 520) for i in range(521)]
    base = 510
    pts = []
    area_pts = []
    for x in xs:
        if left_x < x < right_x:
            u = (x - left_x) / (right_x - left_x)
            y = base - 5600 * bump(u)
        else:
            y = base
        pts.append((x, y))
        area_pts.append((x, y))
    fill_poly = [(left_x, base)] + [p for p in pts if left_x <= p[0] <= right_x] + [(right_x, base)]
    draw.polygon(fill_poly, fill=(80, 169, 139, 44))
    polyline(draw, [(160, base), (1440, base)], (104, 112, 119, 150), 2)
    polyline(draw, pts, (232, 226, 202, 255), 7)
    polyline(draw, pts, (39, 47, 54, 90), 13)

    # Interior samples: derivatives visibly spend themselves in support.
    for k, x in enumerate([650, 760, 870, 980]):
        u = (x - left_x) / (right_x - left_x)
        y = base - 5600 * bump(u)
        amp = [70, 95, 95, 70][k]
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(237, 167, 88, 245))
        draw.line([(x, y), (x + 36, y - amp)], fill=(237, 167, 88, 180), width=3)
        draw.arc((x - 42, y - 42, x + 42, y + 42), 210, 315, fill=(237, 167, 88, 110), width=2)

    # Boundary zero witnesses.
    for x in [left_x, right_x]:
        y = base
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(17, 20, 25, 255), outline=(232, 226, 202, 255), width=3)
        draw.line([(x - 76, y), (x + 76, y)], fill=(118, 191, 176, 230), width=5)
        draw.line([(x, y - 78), (x, y + 78)], fill=(118, 191, 176, 130), width=1)
        draw_text(draw, (x, y + 105), "position = slope = curvature = 0", (142, 207, 190), F_TINY, "mm")

    # Integral memory track below.
    y0 = 705
    draw.line([(260, y0), (1340, y0)], fill=(75, 82, 91, 220), width=2)
    mem_pts = []
    accum = 0.0
    last = None
    for x in xs:
        if left_x < x < right_x:
            u = (x - left_x) / (right_x - left_x)
            accum += bump(u)
        if last is None:
            last = accum
        norm = accum / 3.04
        mem_pts.append((x, y0 - min(1.0, norm) * 115))
    polyline(draw, mem_pts, (210, 94, 102, 255), 5)
    draw_text(draw, (255, y0 + 35), "observer integral", (210, 94, 102), F_SMALL)
    draw_text(draw, (1338, y0 - 130), "nonzero memory", (210, 94, 102), F_SMALL, "ra")

    # Captions inside the piece.
    draw_text(draw, (180, 215), "before", (201, 209, 210), F_HEAD)
    draw_text(draw, (610, 215), "compact support", (201, 209, 210), F_HEAD)
    draw_text(draw, (1160, 215), "after", (201, 209, 210), F_HEAD)
    draw_text(draw, (188, 258), "nothing owed", (139, 150, 158), F_TEXT)
    draw_text(draw, (624, 258), "all debt spent inside", (139, 150, 158), F_TEXT)
    draw_text(draw, (1168, 258), "nothing owed", (139, 150, 158), F_TEXT)

    draw_text(draw, (110, 910), "The local witness is zero. The path-memory is not.", (232, 225, 204), F_HEAD)
    draw_text(draw, (110, 950), "exploratory move: borrowed basis becomes compact support", (132, 145, 154), F_SMALL)

    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
