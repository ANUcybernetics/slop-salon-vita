from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1400, 900
FRAMES = 240
FPS = 24
STEP_DEG = 13.0
OUT = Path("assets/lift-residue-clocks")


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(48, True)
F_HEAD = font(28, True)
F_TEXT = font(22)
F_SMALL = font(16)


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def principal_residue(angle_deg, spokes):
    period = 360.0 / spokes
    return ((angle_deg + period / 2.0) % period) - period / 2.0


def spoke_points(cx, cy, radius, spokes, angle_deg):
    theta0 = angle_deg * pi / 180.0
    pts = []
    for i in range(spokes):
        theta = theta0 + 2.0 * pi * i / spokes
        pts.append((cx + radius * cos(theta), cy + radius * sin(theta)))
    return pts


def draw_text(draw, xy, text, fill, fnt, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def draw_wheel(draw, cx, cy, spokes, lift_angle, color, label, residue):
    radius = 145
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(88, 96, 106, 190), width=2)
    draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=(233, 228, 207, 230))

    for x, y in spoke_points(cx, cy, radius, spokes, lift_angle):
        draw.line((cx, cy, x, y), fill=color, width=3)
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)

    draw_text(draw, (cx, cy - 205), label, (230, 232, 222), F_HEAD, "mm")
    draw_text(draw, (cx, cy + 196), f"{spokes} spokes", (147, 161, 166), F_TEXT, "mm")

    sign = "+" if residue >= 0 else ""
    direction = "forward" if residue >= 0 else "backward"
    draw_text(draw, (cx, cy + 232), f"principal residue {sign}{residue:.0f} deg: {direction}", color, F_SMALL, "mm")


def draw_lift(draw, frame, lift_angle):
    x0, y0, w, h = 140, 145, 1120, 82
    draw.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=6, fill=(18, 22, 28, 235), outline=(70, 78, 88, 190), width=2)
    draw_text(draw, (x0 + 22, y0 + 18), "lift", (230, 232, 222), F_SMALL)
    draw_text(draw, (x0 + w - 22, y0 + 18), f"theta = {lift_angle:.1f} deg", (230, 232, 222), F_SMALL, "ra")

    turns = lift_angle / 360.0
    track_x0, track_x1 = x0 + 28, x0 + w - 28
    y = y0 + 58
    draw.line((track_x0, y, track_x1, y), fill=(76, 84, 94, 220), width=2)
    for k in range(9):
        x = track_x0 + (track_x1 - track_x0) * k / 8
        draw.line((x, y - 8, x, y + 8), fill=(105, 113, 122, 200), width=1)
        draw_text(draw, (x, y + 16), f"{k}", (117, 131, 137), F_SMALL, "ma")

    head = track_x0 + (track_x1 - track_x0) * min(turns / 8.0, 1.0)
    draw.line((track_x0, y, head, y), fill=(232, 190, 96, 230), width=6)
    draw.ellipse((head - 10, y - 10, head + 10, y + 10), fill=(232, 190, 96, 255))


def draw_residue_strip(draw, x, y, spokes, residue, color):
    period = 360.0 / spokes
    half = period / 2.0
    draw.line((x, y, x + 300, y), fill=(85, 93, 104, 220), width=2)
    draw.line((x + 150, y - 15, x + 150, y + 15), fill=(230, 232, 222, 210), width=2)
    for value in (-half, 0, half):
        px = x + 150 + (value / half) * 140
        draw.line((px, y - 8, px, y + 8), fill=(105, 113, 122, 180), width=1)
    px = x + 150 + (residue / half) * 140
    draw.ellipse((px - 9, y - 9, px + 9, y + 9), fill=color)
    draw_text(draw, (x, y - 42), f"mod {period:.0f} deg", (143, 157, 163), F_SMALL)


def frame_image(frame):
    img = Image.new("RGB", (W, H), (10, 13, 18))
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        draw.line((0, y, W, y), fill=blend((10, 13, 18), (27, 30, 34), y / (H - 1)))

    t = frame / (FRAMES - 1)
    lift_angle = t * STEP_DEG * 56.0
    draw_text(draw, (86, 70), "ONE LIFT, TWO RESIDUES", (235, 229, 210), F_TITLE)
    draw_text(draw, (90, 118), "direction appears after the spoke quotient chooses a nearest return", (145, 160, 166), F_TEXT)

    draw_lift(draw, frame, lift_angle)

    r12 = principal_residue(STEP_DEG, 12)
    r20 = principal_residue(STEP_DEG, 20)
    a12 = principal_residue(lift_angle, 12)
    a20 = principal_residue(lift_angle, 20)

    draw_wheel(draw, 410, 495, 12, a12, (238, 113, 119, 245), "clock A", r12)
    draw_wheel(draw, 990, 495, 20, a20, (105, 207, 202, 245), "clock B", r20)

    draw_residue_strip(draw, 260, 775, 12, r12, (238, 113, 119, 245))
    draw_residue_strip(draw, 840, 775, 20, r20, (105, 207, 202, 245))

    draw_text(draw, (700, 848), "the motor has no direction after the quotient; the clock supplies it", (235, 229, 210), F_HEAD, "mm")
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for i in range(FRAMES):
        frame_image(i).save(OUT / f"frame_{i:04d}.png")
    print(OUT)
    print(f"residue_12={principal_residue(STEP_DEG, 12):.6f}")
    print(f"residue_20={principal_residue(STEP_DEG, 20):.6f}")


if __name__ == "__main__":
    main()
