from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


OUT = Path("assets/drying-lift-sound")
FRAMES = OUT / "frames"
W, H = 1280, 720
FPS = 12
DURATION = 42.0
SR = 44100


def smoothstep(x: np.ndarray | float) -> np.ndarray | float:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def make_paper_texture() -> np.ndarray:
    rng = np.random.default_rng(11)
    base = rng.normal(0, 1, (H, W))
    for _ in range(4):
        base = (
            base
            + np.roll(base, 1, axis=0)
            + np.roll(base, -1, axis=0)
            + np.roll(base, 1, axis=1)
            + np.roll(base, -1, axis=1)
        ) / 5.0
    base = (base - base.min()) / (base.max() - base.min())
    yy = np.linspace(0, 1, H)[:, None]
    xx = np.linspace(0, 1, W)[None, :]
    grain = 0.55 * base + 0.45 * rng.random((H, W))
    fiber = 0.5 + 0.5 * np.sin(80 * yy + 15 * np.sin(12 * xx))
    return 0.72 * grain + 0.28 * fiber


def crack_paths() -> list[list[tuple[float, float]]]:
    paths: list[list[tuple[float, float]]] = []
    starts = [(0.56, 0.28), (0.62, 0.38), (0.66, 0.50), (0.58, 0.63), (0.72, 0.34)]
    for i, (x0, y0) in enumerate(starts):
        pts = []
        for k in range(7):
            x = x0 + 0.045 * k + 0.015 * math.sin(1.7 * k + i)
            y = y0 + 0.035 * math.sin(1.25 * k + i * 0.9) + 0.015 * (k - 3)
            pts.append((x * W, y * H))
        paths.append(pts)
        if i < 3:
            branch = pts[2:5]
            bx, by = branch[0]
            paths.append([(bx, by), (bx + 70, by - 45 - 20 * i), (bx + 130, by - 35 + 10 * i)])
    return paths


def render_frame(idx: int, texture: np.ndarray, paths: list[list[tuple[float, float]]]) -> None:
    t = idx / (FPS * DURATION)
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    front = 0.22 + 0.62 * smoothstep(t)
    ridge = np.exp(-((x - front) / 0.055) ** 2)
    curl = np.clip(np.sin(32 * y + 7 * np.sin(9 * x)) * ridge, 0, None)
    dry = smoothstep((x - front + 0.22) / 0.38)
    damp = 1.0 - smoothstep((x - front + 0.10) / 0.22)

    r = 104 + 58 * texture + 34 * damp + 44 * dry
    g = 71 + 48 * texture + 26 * damp + 34 * dry
    b = 48 + 34 * texture + 16 * damp + 20 * dry
    img = np.dstack([r, g, b])

    lift_shadow = 42 * ridge * smoothstep((t - 0.10) / 0.32)
    img[..., 0] += 54 * curl
    img[..., 1] += 35 * curl
    img[..., 2] += 12 * curl
    img -= lift_shadow[..., None] * np.array([0.65, 0.72, 0.9])

    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(im, "RGBA")

    # Drying front: lifted skin, before any fracture line is drawn.
    fx = int(front * W)
    for off, alpha in [(-18, 30), (-8, 70), (0, 120), (8, 55)]:
        pts = []
        for py in range(-20, H + 24, 18):
            px = fx + off + 9 * math.sin(py * 0.035 + 5.5 * t)
            pts.append((px, py))
        draw.line(pts, fill=(240, 176, 92, alpha), width=3)

    crack_alpha = int(255 * smoothstep((t - 0.42) / 0.42))
    for n, path in enumerate(paths):
        local = np.clip((t - 0.46 - n * 0.035) / 0.22, 0, 1)
        if local <= 0:
            continue
        count = max(2, int(2 + local * (len(path) - 1)))
        visible = path[:count]
        draw.line(visible, fill=(31, 22, 18, int(crack_alpha * local)), width=3)
        draw.line(visible, fill=(226, 156, 85, int(60 * local)), width=1)

    draw.rectangle((0, 0, W, H), outline=(21, 18, 15, 255), width=12)
    draw.text((42, 42), "LIFT BEFORE BREAK", fill=(239, 218, 181, 225))
    draw.text((42, H - 72), "the front stores stress; the crack arrives late", fill=(239, 218, 181, 190))

    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=4))
    im.save(FRAMES / f"frame_{idx:04d}.png")


def synth_audio() -> None:
    n = int(DURATION * SR)
    t = np.arange(n) / SR
    front = smoothstep(t / DURATION)
    tension = smoothstep((t - 4.0) / 18.0) * (1.0 - 0.35 * smoothstep((t - 28.0) / 8.0))
    freq = 72 + 42 * tension + 9 * np.sin(2 * np.pi * 0.033 * t)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    bed = 0.13 * np.sin(phase) + 0.05 * np.sin(2.01 * phase + 0.5)

    lift = 0.09 * np.sin(2 * np.pi * (170 + 45 * front) * t) * smoothstep((t - 5.0) / 10.0)
    lift *= 1.0 - smoothstep((t - 33.0) / 8.0)

    rng = np.random.default_rng(19)
    crack = np.zeros(n)
    crack_times = [18.2, 20.7, 23.4, 25.1, 27.8, 30.9, 33.0, 35.6]
    for i, ct in enumerate(crack_times):
        start = int(ct * SR)
        length = int((0.09 + 0.025 * (i % 3)) * SR)
        env = np.exp(-np.linspace(0, 8.5, length))
        noise = rng.normal(0, 1, length)
        tone = np.sin(2 * np.pi * (620 + 93 * i) * np.arange(length) / SR)
        crack[start : start + length] += (0.28 * noise + 0.18 * tone) * env

    pan = 0.42 * np.sin(2 * np.pi * 0.017 * t)
    left = bed + lift * (0.8 - pan) + crack * (0.65 - pan)
    right = bed + lift * (0.8 + pan) + crack * (0.65 + pan)
    audio = np.column_stack([left, right])
    audio *= 0.86 / max(0.01, np.max(np.abs(audio)))
    pcm = (audio * 32767).astype("<i2")

    with wave.open(str(OUT / "drying-lift-sound.wav"), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    texture = make_paper_texture()
    paths = crack_paths()
    frames = int(DURATION * FPS)
    for idx in range(frames):
        render_frame(idx, texture, paths)
    synth_audio()
    os.system(
        "ffmpeg -y -framerate 12 -i assets/drying-lift-sound/frames/frame_%04d.png "
        "-i assets/drying-lift-sound/drying-lift-sound.wav "
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "
        "assets/drying-lift-sound/drying-lift-sound.mp4"
    )


if __name__ == "__main__":
    main()
