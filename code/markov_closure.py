from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path("assets/markov-closure")
FRAMES = OUT / "frames"
W, H = 1280, 720
FPS = 12
DURATION = 28.0
SR = 44100

BG = (220, 213, 194)
INK = (31, 32, 30)
DIM = (73, 69, 61)
BLUE = (36, 105, 132)
RUST = (177, 72, 54)
GOLD = (219, 157, 62)
GREEN = (62, 128, 91)


def smoothstep(x: np.ndarray | float) -> np.ndarray | float:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


TITLE = font(25, True)
BODY = font(16)
SMALL = font(13)
MONO = font(15)


def paper() -> np.ndarray:
    rng = np.random.default_rng(191)
    base = rng.normal(0, 1, (H, W))
    for _ in range(5):
        base = (
            base
            + np.roll(base, 1, 0)
            + np.roll(base, -1, 0)
            + np.roll(base, 1, 1)
            + np.roll(base, -1, 1)
        ) / 5.0
    base = (base - base.min()) / (base.max() - base.min())
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    fiber = 0.5 + 0.5 * np.sin(72 * y + 9 * np.sin(7 * x))
    return 0.70 * base + 0.30 * fiber


def braid_paths(n: int, crossings: list[int], steps: int = 150) -> list[list[tuple[float, float]]]:
    xs = np.linspace(0.20, 0.80, n)
    paths = [[(float(xs[i]), 0.0)] for i in range(n)]
    pos_to_strand = list(range(n))
    rows = np.linspace(0.12, 0.88, len(crossings) + 1)

    for event_index, crossing in enumerate(crossings):
        y0, y1 = rows[event_index], rows[event_index + 1]
        a, b = crossing, crossing + 1
        left_strand = pos_to_strand[a]
        right_strand = pos_to_strand[b]
        for k in range(1, steps + 1):
            u = k / steps
            s = smoothstep(u)
            current = xs.copy()
            current[a] = xs[a] + (xs[b] - xs[a]) * s
            current[b] = xs[b] + (xs[a] - xs[b]) * s
            lift = math.sin(math.pi * u)
            y = y0 + (y1 - y0) * u
            for p, strand in enumerate(pos_to_strand):
                offset = 0.0
                if strand == left_strand:
                    offset = -0.022 * lift
                elif strand == right_strand:
                    offset = 0.022 * lift
                paths[strand].append((float(current[p]), float(y + offset)))
        pos_to_strand[a], pos_to_strand[b] = pos_to_strand[b], pos_to_strand[a]
    for strand in range(n):
        paths[strand].append((paths[strand][-1][0], 1.0))
    return paths


def visible_polyline(points: list[tuple[float, float]], frac: float) -> list[tuple[float, float]]:
    if frac >= 1.0:
        return points
    count = max(2, int(frac * (len(points) - 1)))
    return points[: count + 1]


def draw_closure_arc(
    draw: ImageDraw.ImageDraw,
    a: tuple[float, float],
    b: tuple[float, float],
    lift: float,
    color: tuple[int, int, int],
    frac: float,
) -> None:
    pts = []
    for k in range(80):
        u = k / 79
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u + lift * math.sin(math.pi * u)
        pts.append((x, y))
    pts = visible_polyline(pts, frac)
    if len(pts) > 1:
        draw.line(pts, fill=color + (205,), width=5, joint="curve")


def draw_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    n: int,
    crossings: list[int],
    word: str,
    t: float,
    accent: tuple[int, int, int],
) -> None:
    x0, y0, ww, hh = box
    braid_frac = smoothstep(t / (DURATION * 0.58))
    close_frac = smoothstep((t - DURATION * 0.52) / (DURATION * 0.36))

    draw.rounded_rectangle((x0, y0, x0 + ww, y0 + hh), radius=4, fill=(238, 230, 208, 90), outline=(48, 44, 39, 185), width=2)
    draw.text((x0 + 24, y0 + 20), title, fill=INK, font=BODY)
    draw.text((x0 + 24, y0 + 45), word, fill=accent, font=MONO)

    top_y = y0 + 91
    bot_y = y0 + hh - 105
    left_x = x0 + 72
    scale_x = ww - 144
    scale_y = bot_y - top_y

    xs = np.linspace(0.20, 0.80, n)
    for i, x in enumerate(xs, start=1):
        px = left_x + x * scale_x
        draw.line((px, top_y, px, bot_y), fill=(55, 50, 43, 46), width=1)
        draw.text((px - 5, y0 + 69), str(i), fill=DIM, font=SMALL)
        draw.text((px - 5, bot_y + 16), str(i), fill=DIM, font=SMALL)

    colors = [BLUE, GOLD, GREEN]
    mapped_paths: list[list[tuple[float, float]]] = []
    for strand, path in enumerate(braid_paths(n, crossings)):
        pts = [(left_x + x * scale_x, top_y + y * scale_y) for x, y in visible_polyline(path, braid_frac)]
        mapped_paths.append([(left_x + x * scale_x, top_y + y * scale_y) for x, y in path])
        if len(pts) > 1:
            draw.line(pts, fill=colors[strand] + (230,), width=6, joint="curve")
        if pts:
            px, py = pts[-1]
            draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill=colors[strand] + (240,), outline=(28, 27, 24, 180), width=1)

    # Draw closure outside the braid rectangle. These arcs are deliberately late:
    # the image first shows the word, then the quotient that forgets the word.
    if close_frac > 0:
        for strand, pts in enumerate(mapped_paths):
            top = pts[0]
            bottom = pts[-1]
            side = -1 if top[0] < x0 + ww / 2 else 1
            lift = side * (70 + 18 * strand)
            draw_closure_arc(draw, bottom, top, lift, colors[strand], close_frac)

    draw.line((x0 + 42, y0 + hh - 61, x0 + ww - 42, y0 + hh - 61), fill=(54, 49, 43, 100), width=2)
    draw.text((x0 + 24, y0 + hh - 38), "closure = same loop", fill=INK, font=MONO)


def render_frame(idx: int, grain: np.ndarray) -> None:
    t = idx / FPS
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    bg = np.dstack([BG[0] + 40 * grain, BG[1] + 36 * grain, BG[2] + 30 * grain])
    bg *= (0.90 + 0.08 * x + 0.025 * np.sin(2 * np.pi * y))[..., None]
    im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    draw.rectangle((0, 0, W, H), outline=(28, 27, 24, 255), width=10)
    draw.text((40, 32), "MARKOV MOVE", fill=INK, font=TITLE)
    draw.text((42, 64), "change the braid word; close it and the loop agrees", fill=DIM, font=BODY)

    draw_panel(draw, (60, 124, 540, 456), "two-strand braid", 2, [0], "sigma1", t, BLUE)
    draw_panel(draw, (680, 124, 540, 456), "stabilized braid", 3, [0, 1], "sigma1 sigma2", t, RUST)

    draw.line((118, 628, 1162, 628), fill=(52, 48, 42, 110), width=2)
    marker = 118 + int(1044 * smoothstep(t / DURATION))
    draw.ellipse((marker - 8, 620, marker + 8, 636), fill=GOLD + (230,))
    draw.text((118, 650), "B_n keeps the word", fill=INK, font=MONO)
    draw.text((780, 650), "closure spends the address", fill=INK, font=MONO)

    im = Image.alpha_composite(im.convert("RGBA"), overlay)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=60, threshold=4))
    im.save(FRAMES / f"frame_{idx:04d}.png")


def click(times: list[float], pitch: float, n: int) -> np.ndarray:
    out = np.zeros(n)
    for i, start_t in enumerate(times):
        start = int(start_t * SR)
        length = int(0.18 * SR)
        if start + length >= n:
            continue
        tt = np.arange(length) / SR
        env = np.exp(-np.linspace(0, 9.5, length))
        tone = np.sin(2 * np.pi * (pitch + 38 * i) * tt)
        out[start : start + length] += (0.17 + 0.04 * i) * tone * env
    return out


def synth_audio() -> None:
    n = int(DURATION * SR)
    tt = np.arange(n) / SR
    center = 0.085 * np.sin(2 * np.pi * 55 * tt) + 0.045 * np.sin(2 * np.pi * 110 * tt)
    left_word = click([5.5], 330, n)
    right_word = click([5.5, 11.0], 430, n)
    close_env = smoothstep((tt - 15.0) / 7.0) * (1.0 - smoothstep((tt - 25.0) / 3.0))
    closure = 0.08 * np.sin(2 * np.pi * 165 * tt) * close_env
    side = 0.065 * np.sin(2 * np.pi * 143 * tt) * smoothstep(tt / 5.0) * (1.0 - smoothstep((tt - 15.0) / 5.0))
    left = center + left_word - 0.35 * right_word - side + closure
    right = center + right_word - 0.35 * left_word + side + closure
    stereo = np.column_stack([left, right])
    stereo *= 0.88 / max(0.01, np.max(np.abs(stereo)))
    with wave.open(str(OUT / "markov-closure.wav"), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((stereo * 32767).astype("<i2").tobytes())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    grain = paper()
    for idx in range(int(DURATION * FPS)):
        render_frame(idx, grain)
    synth_audio()
    cmd = (
        "ffmpeg -y -framerate 12 -i assets/markov-closure/frames/frame_%04d.png "
        "-i assets/markov-closure/markov-closure.wav "
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "
        "assets/markov-closure/markov-closure.mp4"
    )
    raise SystemExit(os.system(cmd))


if __name__ == "__main__":
    main()
