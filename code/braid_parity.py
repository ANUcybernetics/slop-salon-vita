from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path("assets/braid-parity")
FRAMES = OUT / "frames"
W, H = 1280, 720
FPS = 12
DURATION = 36.0
SR = 44100

BG = (218, 210, 191)
INK = (32, 33, 31)
DIM = (78, 74, 66)
BLUE = (35, 104, 130)
RUST = (172, 70, 54)
GOLD = (217, 156, 61)
GREEN = (65, 130, 91)


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
MONO = font(16)


def paper() -> np.ndarray:
    rng = np.random.default_rng(133)
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
    fiber = 0.5 + 0.5 * np.sin(70 * y + 8 * np.sin(8 * x))
    return 0.73 * base + 0.27 * fiber


def braid_paths(pair: int, steps: int = 260) -> list[list[tuple[float, float]]]:
    xs = np.array([0.18, 0.50, 0.82], dtype=float)
    paths = [[(float(xs[i]), 0.0)] for i in range(3)]
    pos_to_strand = [0, 1, 2]
    events = [pair, pair]
    rows = np.linspace(0.12, 0.88, len(events) + 1)

    for event_index, crossing in enumerate(events):
        y0, y1 = rows[event_index], rows[event_index + 1]
        a, b = crossing, crossing + 1
        left_strand = pos_to_strand[a]
        right_strand = pos_to_strand[b]
        for k in range(1, steps + 1):
            u = k / steps
            s = smoothstep(u)
            y = y0 + (y1 - y0) * u
            current = xs.copy()
            current[a] = xs[a] + (xs[b] - xs[a]) * s
            current[b] = xs[b] + (xs[a] - xs[b]) * s
            lift = math.sin(math.pi * u)
            for p, strand in enumerate(pos_to_strand):
                offset = 0.0
                if strand == left_strand:
                    offset = -0.026 * lift
                elif strand == right_strand:
                    offset = 0.026 * lift
                paths[strand].append((float(current[p]), float(y + offset)))
        pos_to_strand[a], pos_to_strand[b] = pos_to_strand[b], pos_to_strand[a]
    for strand in range(3):
        paths[strand].append((paths[strand][-1][0], 1.0))
    return paths


def interpolate_path(path: list[tuple[float, float]], visible: float) -> list[tuple[float, float]]:
    if visible >= 1.0:
        return path
    max_i = max(1, int(visible * (len(path) - 1)))
    return path[: max_i + 1]


def draw_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    pair: int,
    t: float,
    color: tuple[int, int, int],
) -> None:
    x0, y0, ww, hh = box
    visible = smoothstep(t / DURATION)
    draw.rounded_rectangle((x0, y0, x0 + ww, y0 + hh), radius=4, fill=(237, 229, 207, 86), outline=(48, 44, 39, 180), width=2)
    draw.text((x0 + 24, y0 + 22), title, fill=INK, font=BODY)
    draw.text((x0 + 24, y0 + 48), "endpoint = identity   sign = +", fill=DIM, font=SMALL)

    top_y = y0 + 88
    bot_y = y0 + hh - 76
    left_x = x0 + 74
    scale_x = ww - 148
    scale_y = bot_y - top_y

    for i, x in enumerate([0.18, 0.50, 0.82], start=1):
        px = left_x + x * scale_x
        draw.text((px - 6, y0 + 66), str(i), fill=DIM, font=SMALL)
        draw.text((px - 6, bot_y + 22), str(i), fill=DIM, font=SMALL)
        draw.line((px, top_y, px, bot_y), fill=(60, 56, 49, 55), width=1)

    colors = [BLUE, GOLD, GREEN]
    widths = [6, 6, 6]
    for strand, path in enumerate(braid_paths(pair)):
        pts = interpolate_path(path, visible)
        mapped = [(left_x + x * scale_x, top_y + y * scale_y) for x, y in pts]
        if len(mapped) > 1:
            draw.line(mapped, fill=colors[strand] + (230,), width=widths[strand], joint="curve")
        if mapped:
            px, py = mapped[-1]
            draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill=colors[strand] + (245,), outline=(29, 28, 25, 190), width=1)

    for cy in [top_y + 0.12 * scale_y, top_y + 0.50 * scale_y, top_y + 0.88 * scale_y]:
        draw.line((x0 + 48, cy, x0 + ww - 48, cy), fill=(52, 48, 42, 60), width=1)

    label = "sigma1 sigma1" if pair == 0 else "sigma2 sigma2"
    draw.text((x0 + 24, y0 + hh - 36), label, fill=color, font=MONO)


def render_frame(idx: int, grain: np.ndarray) -> None:
    t = idx / FPS
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    bg = np.dstack([BG[0] + 42 * grain, BG[1] + 38 * grain, BG[2] + 32 * grain])
    bg *= (0.90 + 0.08 * x + 0.025 * np.sin(2 * np.pi * y))[..., None]
    im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    draw.rectangle((0, 0, W, H), outline=(28, 27, 24, 255), width=10)
    draw.text((40, 34), "SIGN IS NOT THE BRAID", fill=INK, font=TITLE)
    draw.text((42, 66), "same endpoint, same parity; different crossing history", fill=DIM, font=BODY)

    draw_panel(draw, (60, 124, 540, 456), "left pair crosses twice", 0, t, BLUE)
    draw_panel(draw, (680, 124, 540, 456), "right pair crosses twice", 1, t, RUST)

    draw.line((118, 628, 1162, 628), fill=(52, 48, 42, 110), width=2)
    marker = 118 + int(1044 * smoothstep(t / DURATION))
    draw.ellipse((marker - 8, 620, marker + 8, 636), fill=(219, 160, 61, 225))
    draw.text((118, 650), "S_n -> Z/2 reads +", fill=INK, font=MONO)
    draw.text((778, 650), "B_n keeps which strands crossed", fill=INK, font=MONO)

    im = Image.alpha_composite(im.convert("RGBA"), overlay)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=60, threshold=4))
    im.save(FRAMES / f"frame_{idx:04d}.png")


def click_train(times: list[float], pitch: float, n: int) -> np.ndarray:
    out = np.zeros(n)
    for i, start_t in enumerate(times):
        start = int(start_t * SR)
        length = int(0.16 * SR)
        if start + length >= n:
            continue
        env = np.exp(-np.linspace(0, 9.0, length))
        tt = np.arange(length) / SR
        tone = np.sin(2 * np.pi * (pitch + 30 * i) * tt)
        out[start : start + length] += (0.18 + 0.04 * i) * tone * env
    return out


def synth_audio() -> None:
    n = int(DURATION * SR)
    tt = np.arange(n) / SR
    center = 0.09 * np.sin(2 * np.pi * 55 * tt) + 0.045 * np.sin(2 * np.pi * 110 * tt)
    left_cross = click_train([6.0, 18.0], 330, n)
    right_cross = click_train([12.0, 24.0], 440, n)
    side = 0.075 * np.sin(2 * np.pi * 143 * tt) * smoothstep(tt / 6.0) * (1.0 - smoothstep((tt - 31.0) / 5.0))
    left = center + left_cross - 0.35 * right_cross - side
    right = center + right_cross - 0.35 * left_cross + side
    stereo = np.column_stack([left, right])
    stereo *= 0.88 / max(0.01, np.max(np.abs(stereo)))
    with wave.open(str(OUT / "braid-parity.wav"), "wb") as wf:
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
        "ffmpeg -y -framerate 12 -i assets/braid-parity/frames/frame_%04d.png "
        "-i assets/braid-parity/braid-parity.wav "
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "
        "assets/braid-parity/braid-parity.mp4"
    )
    raise SystemExit(os.system(cmd))


if __name__ == "__main__":
    main()
