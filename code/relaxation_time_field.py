from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path("assets/relaxation-time-field")
FRAMES = OUT / "frames"
W, H = 1280, 720
FPS = 12
DURATION = 36.0
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


TITLE = font(24, True)
BODY = font(16)
SMALL = font(13)


def texture() -> np.ndarray:
    rng = np.random.default_rng(41)
    field = rng.normal(0.0, 1.0, (H, W))
    for _ in range(5):
        field = (
            field
            + np.roll(field, 1, 0)
            + np.roll(field, -1, 0)
            + np.roll(field, 1, 1)
            + np.roll(field, -1, 1)
        ) / 5.0
    field = (field - field.min()) / (field.max() - field.min())
    yy = np.linspace(0, 1, H)[:, None]
    fibers = 0.5 + 0.5 * np.sin(95 * yy + 8 * np.sin(np.linspace(0, 8, W)[None, :]))
    return 0.72 * field + 0.28 * fibers


def draw_arrow(draw: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float], fill: tuple[int, int, int, int], width: int = 3) -> None:
    draw.line((a, b), fill=fill, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    head = 12
    left = (b[0] - head * math.cos(ang - 0.55), b[1] - head * math.sin(ang - 0.55))
    right = (b[0] - head * math.cos(ang + 0.55), b[1] - head * math.sin(ang + 0.55))
    draw.polygon([b, left, right], fill=fill)


def render_frame(idx: int, grain: np.ndarray) -> None:
    u = idx / max(1, int(DURATION * FPS) - 1)
    t = smoothstep(u)
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]

    base = np.dstack(
        [
            210 + 22 * grain,
            202 + 22 * grain,
            184 + 18 * grain,
        ]
    )
    base *= (0.96 + 0.05 * x + 0.025 * np.sin(2 * np.pi * y))[..., None]

    cx = 0.28 + 0.42 * t
    cy = 0.52 + 0.08 * np.sin(1.3 * math.pi * t)
    tau = np.exp(-3.7 * t)
    packet = np.exp(-(((x - cx) / (0.17 + 0.16 * t)) ** 2 + ((y - cy) / (0.16 + 0.06 * t)) ** 2))
    ring = np.exp(-(((x - 0.52) / 0.23) ** 2 + ((y - 0.50) / 0.23) ** 2)) - np.exp(
        -(((x - 0.52) / 0.12) ** 2 + ((y - 0.50) / 0.12) ** 2)
    )
    residual = np.clip(0.78 * tau * packet + 0.38 * tau * np.maximum(ring, 0), 0, 1)

    img = base.copy()
    img[..., 0] += 100 * residual
    img[..., 1] -= 35 * residual
    img[..., 2] -= 40 * residual

    boundary = np.exp(-((x - 0.88) / 0.014) ** 2)
    img[..., 0] += 20 * boundary
    img[..., 1] += 42 * boundary
    img[..., 2] += 48 * boundary

    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    draw.rectangle((0, 0, W, H), outline=(32, 31, 29, 255), width=10)
    draw.text((38, 34), "RELAXATION TIME", fill=(34, 35, 35, 240), font=TITLE)
    draw.text((39, 64), "same boundary reading; residual field on its own clock", fill=(52, 52, 50, 220), font=BODY)

    draw.line((1125, 105, 1125, 610), fill=(40, 112, 134, 230), width=5)
    draw.text((1080, 80), "far end", fill=(30, 82, 98, 235), font=SMALL)
    draw.text((1052, 630), "sum already agrees", fill=(30, 82, 98, 220), font=SMALL)

    center = (int(cx * W), int(cy * H))
    for k in range(15):
        a = 2 * math.pi * k / 15 + 0.7 * t
        rr = 64 + 170 * (k % 5) / 4
        start = (center[0] + 28 * math.cos(a), center[1] + 22 * math.sin(a))
        end = (center[0] + rr * math.cos(a + 0.45 * t), center[1] + 0.68 * rr * math.sin(a + 0.45 * t))
        alpha = int(35 + 140 * tau)
        draw_arrow(draw, start, end, (175, 50, 44, alpha), width=2)

    trace = []
    for q in np.linspace(0, t, 80):
        px = int((0.28 + 0.42 * smoothstep(q)) * W)
        py = int((0.52 + 0.08 * np.sin(1.3 * math.pi * smoothstep(q))) * H)
        trace.append((px, py))
    if len(trace) > 1:
        draw.line(trace, fill=(120, 58, 48, 110), width=3)

    draw.ellipse((center[0] - 18, center[1] - 18, center[0] + 18, center[1] + 18), fill=(235, 185, 86, 220))
    draw.text((66, 610), "verdict: immediate", fill=(46, 49, 48, 220), font=BODY)
    draw.text((308, 610), f"residue: {tau:0.2f}", fill=(112, 42, 36, 225), font=BODY)

    im = Image.alpha_composite(im.convert("RGBA"), overlay)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=4))
    im.save(FRAMES / f"frame_{idx:04d}.png")


def synth_audio() -> None:
    n = int(DURATION * SR)
    tt = np.arange(n) / SR
    u = tt / DURATION
    decay = np.exp(-3.7 * smoothstep(u))
    verdict = 0.12 * np.sin(2 * np.pi * 110 * tt)
    verdict += 0.045 * np.sin(2 * np.pi * 220 * tt)

    drift = 33 * (1.0 - smoothstep(u))
    left_residue = np.sin(2 * np.pi * (143 + drift) * tt)
    right_residue = -np.sin(2 * np.pi * (143 - 0.5 * drift) * tt)
    tremor = 0.5 + 0.5 * np.sin(2 * np.pi * (0.7 + 1.6 * u) * tt)
    residue = 0.18 * decay * (0.55 + 0.45 * tremor)

    rng = np.random.default_rng(52)
    grains = rng.normal(0, 1, n)
    for _ in range(3):
        grains = (grains + np.roll(grains, 1) + np.roll(grains, -1)) / 3.0
    grains *= 0.025 * decay

    left = verdict + residue * left_residue + grains
    right = verdict + residue * right_residue - grains
    stereo = np.column_stack([left, right])
    stereo *= 0.88 / max(0.01, np.max(np.abs(stereo)))

    with wave.open(str(OUT / "relaxation-time-field.wav"), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((stereo * 32767).astype("<i2").tobytes())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    grain = texture()
    for idx in range(int(DURATION * FPS)):
        render_frame(idx, grain)
    synth_audio()
    cmd = (
        "ffmpeg -y -framerate 12 -i assets/relaxation-time-field/frames/frame_%04d.png "
        "-i assets/relaxation-time-field/relaxation-time-field.wav "
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "
        "assets/relaxation-time-field/relaxation-time-field.mp4"
    )
    raise SystemExit(os.system(cmd))


if __name__ == "__main__":
    main()
