from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path("assets/rotation-vs-anagram.png")
W, H = 1400, 900
BG = (30, 30, 28)
PAPER = (222, 214, 194)
INK = (35, 36, 34)
DIM = (92, 88, 78)
GOLD = (220, 164, 66)
BLUE = (32, 112, 140)
RED = (174, 70, 60)
GREEN = (74, 135, 93)
PURPLE = (118, 86, 150)

LETTERS = [1, 2, 3, 5, 8, 13]
WORD = [1, 2, 3, 5, 8, 13]
ROT = [5, 8, 13, 1, 2, 3]
ANAGRAM = [13, 1, 5, 2, 8, 3]
COLORS = {
    1: BLUE,
    2: GOLD,
    3: PURPLE,
    5: GREEN,
    8: RED,
    13: (83, 80, 72),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


TITLE = font(34, True)
HEAD = font(24, True)
BODY = font(18)
SMALL = font(14)
MONO = font(17)


def paper_background() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    px = img.load()
    for y in range(H):
        for x in range(W):
            wave = 6 * math.sin(y / 17.0) + 4 * math.sin((x + y) / 31.0)
            grain = ((x * 37 + y * 17 + (x * y) % 19) % 23) - 11
            v = int(wave + 0.35 * grain)
            base = PAPER
            px[x, y] = (
                max(0, min(255, base[0] + v)),
                max(0, min(255, base[1] + v)),
                max(0, min(255, base[2] + v)),
            )
    return img.filter(ImageFilter.GaussianBlur(0.35))


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fill: tuple[int, int, int], fnt: ImageFont.ImageFont) -> None:
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, fill=fill, font=fnt)


def circle_points(cx: float, cy: float, r: float, n: int) -> list[tuple[float, float]]:
    return [
        (cx + r * math.cos(2 * math.pi * i / n - math.pi / 2), cy + r * math.sin(2 * math.pi * i / n - math.pi / 2))
        for i in range(n)
    ]


def draw_word_circle(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    radius: int,
    word: list[int],
    title: str,
    subtitle: str,
    start_mark: bool,
) -> None:
    cx, cy = center
    pts = circle_points(cx, cy, radius, len(word))
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(54, 51, 45), width=3)

    for i, (a, b) in enumerate(zip(pts, pts[1:] + pts[:1])):
        color = COLORS[word[i]]
        draw.line((a, b), fill=color, width=7)

    if start_mark:
        sx, sy = pts[0]
        draw.line((cx, cy, sx, sy), fill=(42, 40, 35), width=2)
        draw.ellipse((sx - 18, sy - 18, sx + 18, sy + 18), outline=INK, width=4)

    for p, val in zip(pts, word):
        x, y = p
        fill = COLORS[val]
        draw.ellipse((x - 25, y - 25, x + 25, y + 25), fill=fill, outline=(24, 24, 22), width=2)
        draw_centered(draw, (x, y - 1), str(val), (248, 244, 230), MONO)

    draw_centered(draw, (cx, cy - radius - 66), title, INK, HEAD)
    draw_centered(draw, (cx, cy - radius - 34), subtitle, DIM, BODY)


def draw_linear_word(draw: ImageDraw.ImageDraw, x0: int, y0: int, word: list[int], label: str) -> None:
    draw.text((x0, y0 - 34), label, fill=INK, font=BODY)
    x = x0
    for i, val in enumerate(word):
        color = COLORS[val]
        draw.rounded_rectangle((x, y0, x + 64, y0 + 44), radius=4, fill=color, outline=(30, 30, 28), width=2)
        draw_centered(draw, (x + 32, y0 + 22), str(val), (248, 244, 230), MONO)
        if i < len(word) - 1:
            draw.line((x + 72, y0 + 22, x + 96, y0 + 22), fill=DIM, width=2)
        x += 104


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = paper_background().convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rectangle((0, 0, W, H), outline=(30, 29, 26, 255), width=12)
    draw.text((54, 46), "ROTATION IS NOT ANAGRAM", fill=INK, font=TITLE)
    draw.text((57, 91), "same letters, two quotients: C_n keeps cyclic order; S_n spends it", fill=DIM, font=BODY)

    draw_word_circle(draw, (360, 380), 168, WORD, "one sentence", "basepoint pinned", True)
    draw_word_circle(draw, (700, 380), 168, ROT, "rotation", "same cyclic word", True)
    draw_word_circle(draw, (1040, 380), 168, ANAGRAM, "anagram", "same multiset, new order", True)

    y = 690
    draw_linear_word(draw, 100, y, WORD, "word")
    draw_linear_word(draw, 100, y + 100, ROT, "rotate: move the pin")
    draw_linear_word(draw, 760, y + 100, ANAGRAM, "permute: change the necklace")

    draw.line((100, y + 70, 1268, y + 70), fill=(65, 60, 52), width=2)
    draw.text((100, y + 42), "C_n quotient: choose another start; adjacency survives", fill=GREEN, font=SMALL)
    draw.text((760, y + 142), "S_n quotient: endpoint only; adjacency dies", fill=RED, font=SMALL)

    draw.text((54, 840), "the commutator is the difference left after rotations have had their say", fill=INK, font=BODY)
    img = Image.alpha_composite(img, overlay).convert("RGB")
    img.save(OUT, quality=95)


if __name__ == "__main__":
    main()
