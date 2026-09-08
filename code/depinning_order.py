from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path("assets/depinning-order")
FRAMES = OUT / "frames"
W, H = 1280, 720
FPS = 12
DURATION = 40.0
SR = 44100


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


def paper() -> np.ndarray:
    rng = np.random.default_rng(83)
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
    fiber = 0.5 + 0.5 * np.sin(65 * y + 10 * np.sin(9 * x))
    return 0.76 * base + 0.24 * fiber


def release_schedule(kind: str) -> list[float]:
    if kind == "even":
        return [7.0, 12.0, 17.0, 22.0, 27.0, 32.0]
    return [8.2, 11.7, 16.5, 25.8, 30.9, 33.2]


def panel_state(t: float, kind: str) -> tuple[list[float], float]:
    releases = release_schedule(kind)
    opened = [smoothstep((t - r) / 0.75) for r in releases]
    load = smoothstep(t / 34.0)
    carried = 1.0 - sum(opened) / len(opened)
    return opened, load * carried


def draw_panel(draw: ImageDraw.ImageDraw, x0: int, y0: int, ww: int, hh: int, t: float, kind: str) -> None:
    opened, carried = panel_state(t, kind)
    releases = release_schedule(kind)

    draw.rounded_rectangle((x0, y0, x0 + ww, y0 + hh), radius=4, fill=(222, 210, 186, 90), outline=(46, 42, 38, 180), width=2)
    seam_y = y0 + int(0.50 * hh)
    draw.line((x0 + 42, seam_y, x0 + ww - 42, seam_y), fill=(54, 43, 38, 210), width=5)

    label = "six equal pins" if kind == "even" else "one late pin"
    draw.text((x0 + 28, y0 + 24), label, fill=(34, 36, 35, 235), font=BODY)

    for i, amount in enumerate(opened):
        px = x0 + 84 + i * ((ww - 168) / 5)
        threshold = releases[i] / 34.0
        pull = 34 + 64 * threshold
        top = seam_y - pull * (1.0 - amount) - 18 * math.sin(0.5 * t + i)
        bottom = seam_y + 58 * amount
        color = (33, 93, 117, 230) if amount > 0.85 else (172, 62, 48, 230)
        alpha = int(230 - 115 * amount)
        draw.line((px, top, px, bottom), fill=(26, 72, 93, alpha), width=3)
        draw.ellipse((px - 9, top - 9, px + 9, top + 9), fill=color)
        draw.ellipse((px - 5, bottom - 5, px + 5, bottom + 5), fill=(44, 37, 33, 210))
        if 0.0 < amount < 1.0:
            r = 26 + 78 * amount
            draw.ellipse((px - r, seam_y - r, px + r, seam_y + r), outline=(233, 175, 75, int(180 * (1.0 - amount))), width=3)

    if kind == "stuck":
        q = smoothstep((t - 17.0) / 9.0) * (1.0 - smoothstep((t - 31.0) / 2.0))
        draw.arc((x0 + 250, seam_y - 165, x0 + ww - 250, seam_y + 165), 190, 350, fill=(164, 45, 48, int(210 * q)), width=5)
        draw.text((x0 + 278, seam_y + 118), "load waits", fill=(108, 36, 35, int(225 * q)), font=SMALL)

    bar_x = x0 + 48
    bar_y = y0 + hh - 52
    draw.rectangle((bar_x, bar_y, x0 + ww - 48, bar_y + 8), fill=(44, 39, 36, 95))
    draw.rectangle((bar_x, bar_y, bar_x + int((ww - 96) * carried), bar_y + 8), fill=(180, 62, 48, 210))
    draw.text((bar_x, bar_y + 16), f"held load {carried:0.2f}", fill=(52, 51, 48, 210), font=SMALL)


def render_frame(idx: int, grain: np.ndarray) -> None:
    u = idx / max(1, int(DURATION * FPS) - 1)
    t = u * DURATION
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    bg = np.dstack([196 + 40 * grain, 188 + 35 * grain, 170 + 30 * grain])
    bg *= (0.92 + 0.06 * x + 0.03 * np.sin(2 * np.pi * y))[..., None]
    im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    draw.rectangle((0, 0, W, H), outline=(28, 26, 24, 255), width=10)
    draw.text((40, 34), "PINNING ORDER", fill=(32, 34, 33, 245), font=TITLE)
    draw.text((42, 66), "same final release; different bookkeeping in the medium", fill=(48, 49, 47, 220), font=BODY)

    draw_panel(draw, 58, 130, 548, 470, t, "even")
    draw_panel(draw, 674, 130, 548, 470, t, "stuck")

    for r in release_schedule("even"):
        if 0 <= t - r <= 0.55:
            x0 = 58 + 84 + release_schedule("even").index(r) * ((548 - 168) / 5)
            draw.ellipse((x0 - 34, 588, x0 + 34, 656), outline=(35, 105, 125, 170), width=4)
    for r in release_schedule("stuck"):
        if 0 <= t - r <= 0.55:
            x0 = 674 + 84 + release_schedule("stuck").index(r) * ((548 - 168) / 5)
            draw.ellipse((x0 - 34, 588, x0 + 34, 656), outline=(175, 61, 49, 170), width=4)

    draw.text((72, 642), "each pin has a threshold", fill=(45, 45, 43, 225), font=BODY)
    draw.text((710, 642), "the last pin changes the order", fill=(45, 45, 43, 225), font=BODY)

    im = Image.alpha_composite(im.convert("RGBA"), overlay)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=65, threshold=4))
    im.save(FRAMES / f"frame_{idx:04d}.png")


def click_train(times: list[float], n: int, side: float) -> np.ndarray:
    rng = np.random.default_rng(int(1000 * side) + 7)
    out = np.zeros(n)
    for i, ct in enumerate(times):
        start = int(ct * SR)
        length = int((0.13 + 0.015 * (i % 2)) * SR)
        if start + length >= n:
            continue
        env = np.exp(-np.linspace(0, 9.5, length))
        noise = rng.normal(0, 1, length)
        tone = np.sin(2 * np.pi * (430 + 70 * i + 40 * side) * np.arange(length) / SR)
        amp = 0.12 + 0.025 * i
        if i == len(times) - 1:
            amp *= 1.9
        out[start : start + length] += amp * (0.65 * noise + 0.35 * tone) * env
    return out


def synth_audio() -> None:
    n = int(DURATION * SR)
    tt = np.arange(n) / SR
    center = 0.10 * np.sin(2 * np.pi * 55 * tt) + 0.055 * np.sin(2 * np.pi * 110 * tt)
    pressure = 0.035 * np.sin(2 * np.pi * (72 + 14 * smoothstep(tt / DURATION)) * tt)
    even = click_train(release_schedule("even"), n, 0.0)
    stuck = click_train(release_schedule("stuck"), n, 1.0)
    late_hum = 0.10 * np.sin(2 * np.pi * 143 * tt) * smoothstep((tt - 17.0) / 8.5) * (1.0 - smoothstep((tt - 31.5) / 3.0))

    left = center + pressure + even - 0.45 * stuck
    right = center + pressure + stuck + late_hum - 0.35 * even
    stereo = np.column_stack([left, right])
    stereo *= 0.88 / max(0.01, np.max(np.abs(stereo)))
    with wave.open(str(OUT / "depinning-order.wav"), "wb") as wf:
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
        "ffmpeg -y -framerate 12 -i assets/depinning-order/frames/frame_%04d.png "
        "-i assets/depinning-order/depinning-order.wav "
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "
        "assets/depinning-order/depinning-order.mp4"
    )
    raise SystemExit(os.system(cmd))


if __name__ == "__main__":
    main()
