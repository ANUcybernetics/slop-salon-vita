from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path("assets/prefix-sentence")
FRAMES = OUT / "frames"
W, H = 1280, 720
FPS = 12
DURATION = 38.0
SR = 44100

WAITS = np.array([1.0, 2.0, 3.0, 5.0, 8.0, 13.0], dtype=float)
LEFT_ORDER = np.array([0, 1, 2, 3, 4, 5])
RIGHT_ORDER = np.array([5, 0, 3, 1, 4, 2])
TOTAL = float(WAITS.sum())


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
    rng = np.random.default_rng(109)
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
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    fibers = 0.5 + 0.5 * np.sin(58 * y + 8 * np.sin(6 * x))
    return 0.72 * base + 0.28 * fibers


def cumulative(order: np.ndarray) -> np.ndarray:
    return np.r_[0.0, np.cumsum(WAITS[order])]


def progress_at(t: float, order: np.ndarray) -> tuple[int, float, float]:
    event_times = cumulative(order) / TOTAL * DURATION
    idx = int(np.searchsorted(event_times[1:], t, side="right"))
    if idx >= len(order):
        return len(order), 1.0, TOTAL
    a, b = event_times[idx], event_times[idx + 1]
    local = smoothstep((t - a) / max(0.01, b - a))
    paid = float(np.sum(WAITS[order[:idx]]) + local * WAITS[order[idx]])
    return idx, float(local), paid


def point_for(prefix: float, lane: float, x0: int, y0: int, ww: int, hh: int) -> tuple[float, float]:
    u = prefix / TOTAL
    x = x0 + 56 + u * (ww - 112)
    bend = math.sin(u * math.pi) * (68 * (lane - 0.5))
    y = y0 + 0.55 * hh + bend - 46 * math.sin(2 * math.pi * u)
    return x, y


def draw_word(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, order: np.ndarray, t: float, color: tuple[int, int, int]) -> None:
    x0, y0, ww, hh = box
    idx, local, paid = progress_at(t, order)
    prefixes = cumulative(order)
    live_paid = paid

    draw.rounded_rectangle((x0, y0, x0 + ww, y0 + hh), radius=4, fill=(229, 220, 198, 105), outline=(45, 43, 38, 190), width=2)
    draw.text((x0 + 24, y0 + 22), label, fill=(35, 35, 33, 235), font=BODY)
    draw.text((x0 + 24, y0 + 46), "same waits, same total", fill=(67, 65, 60, 220), font=SMALL)

    axis_y = y0 + hh - 58
    draw.line((x0 + 54, axis_y, x0 + ww - 54, axis_y), fill=(54, 48, 42, 125), width=2)
    for p in prefixes:
        px = x0 + 56 + (p / TOTAL) * (ww - 112)
        draw.line((px, axis_y - 9, px, axis_y + 9), fill=(54, 48, 42, 150), width=2)

    pts = [point_for(p, 0.20 if label.startswith("word A") else 0.82, x0, y0, ww, hh) for p in prefixes]
    for a, b in zip(pts, pts[1:]):
        draw.line((a, b), fill=(61, 55, 48, 110), width=3)

    live_pts = [point_for(p, 0.20 if label.startswith("word A") else 0.82, x0, y0, ww, hh) for p in prefixes[: idx + 1]]
    if idx < len(order):
        live_pts.append(point_for(live_paid, 0.20 if label.startswith("word A") else 0.82, x0, y0, ww, hh))
    for a, b in zip(live_pts, live_pts[1:]):
        draw.line((a, b), fill=color + (235,), width=5)

    for j, p in enumerate(prefixes[1:]):
        px, py = point_for(p, 0.20 if label.startswith("word A") else 0.82, x0, y0, ww, hh)
        fill = color + (235,) if j < idx else (246, 239, 221, 235)
        draw.ellipse((px - 11, py - 11, px + 11, py + 11), fill=fill, outline=(46, 42, 38, 190), width=2)
        draw.text((px - 5, py - 32), str(int(WAITS[order[j]])), fill=(42, 39, 36, 225), font=SMALL)

    if idx < len(order):
        lx, ly = point_for(live_paid, 0.20 if label.startswith("word A") else 0.82, x0, y0, ww, hh)
        r = 22 + 10 * math.sin(2 * math.pi * t)
        draw.ellipse((lx - r, ly - r, lx + r, ly + r), outline=color + (160,), width=4)

    bx = x0 + 56
    by = y0 + hh - 33
    draw.rectangle((bx, by, x0 + ww - 56, by + 8), fill=(50, 46, 41, 95))
    draw.rectangle((bx, by, bx + int((ww - 112) * live_paid / TOTAL), by + 8), fill=color + (215,))
    draw.text((bx, by + 13), f"prefix sum {live_paid:0.1f} / {TOTAL:0.0f}", fill=(51, 49, 45, 225), font=SMALL)


def render_frame(idx: int, grain: np.ndarray) -> None:
    u = idx / max(1, int(DURATION * FPS) - 1)
    t = u * DURATION
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    bg = np.dstack([190 + 42 * grain, 185 + 38 * grain, 169 + 31 * grain])
    bg *= (0.91 + 0.07 * x + 0.025 * np.sin(2 * np.pi * y))[..., None]
    im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    draw.rectangle((0, 0, W, H), outline=(30, 28, 25, 255), width=10)
    draw.text((40, 32), "PREFIX SENTENCE", fill=(31, 34, 33, 245), font=TITLE)
    draw.text((42, 64), "the endpoint reads the total; the medium reads the prefixes", fill=(50, 50, 47, 225), font=BODY)

    draw_word(draw, (56, 126, 548, 456), "word A", LEFT_ORDER, t, (29, 104, 126))
    draw_word(draw, (676, 126, 548, 456), "word B", RIGHT_ORDER, t, (172, 66, 54))

    draw.line((112, 634, 1168, 634), fill=(55, 49, 43, 110), width=2)
    marker = 112 + int((1056) * smoothstep(t / DURATION))
    draw.ellipse((marker - 8, 626, marker + 8, 642), fill=(224, 171, 74, 225))
    draw.text((112, 654), "same multiset: {1,2,3,5,8,13}", fill=(48, 47, 43, 225), font=MONO)
    draw.text((770, 654), "different path through partial sums", fill=(48, 47, 43, 225), font=MONO)

    im = Image.alpha_composite(im.convert("RGBA"), overlay)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=60, threshold=4))
    im.save(FRAMES / f"frame_{idx:04d}.png")


def click_train(order: np.ndarray, pan: float, n: int) -> np.ndarray:
    out = np.zeros(n)
    starts = cumulative(order)[:-1] / TOTAL * DURATION
    rng = np.random.default_rng(int(70 + pan * 31))
    for i, start_t in enumerate(starts):
        start = int(start_t * SR)
        length = int((0.10 + 0.008 * i) * SR)
        env = np.exp(-np.linspace(0, 9.0, length))
        pitch = 340 + 18 * WAITS[order[i]]
        tone = np.sin(2 * np.pi * pitch * np.arange(length) / SR)
        noise = rng.normal(0, 1, length)
        amp = 0.08 + 0.010 * WAITS[order[i]]
        if start + length < n:
            out[start : start + length] += amp * (0.72 * tone + 0.28 * noise) * env
    return out


def synth_audio() -> None:
    n = int(DURATION * SR)
    tt = np.arange(n) / SR
    center = 0.09 * np.sin(2 * np.pi * 55 * tt) + 0.045 * np.sin(2 * np.pi * 110 * tt)

    left_clicks = click_train(LEFT_ORDER, 0.0, n)
    right_clicks = click_train(RIGHT_ORDER, 1.0, n)
    prefix_gap = np.zeros(n)
    sample_times = np.arange(n) / SR
    for k, st in enumerate(sample_times[::512]):
        _, _, lp = progress_at(float(st), LEFT_ORDER)
        _, _, rp = progress_at(float(st), RIGHT_ORDER)
        prefix_gap[k * 512 : min(n, (k + 1) * 512)] = (rp - lp) / TOTAL
    ghost = 0.10 * np.sin(2 * np.pi * (143 + 8 * prefix_gap) * tt) * np.abs(prefix_gap)

    left = center + left_clicks - 0.45 * right_clicks - ghost
    right = center + right_clicks - 0.45 * left_clicks + ghost
    stereo = np.column_stack([left, right])
    stereo *= 0.88 / max(0.01, np.max(np.abs(stereo)))
    with wave.open(str(OUT / "prefix-sentence.wav"), "wb") as wf:
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
        "ffmpeg -y -framerate 12 -i assets/prefix-sentence/frames/frame_%04d.png "
        "-i assets/prefix-sentence/prefix-sentence.wav "
        "-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "
        "assets/prefix-sentence/prefix-sentence.mp4"
    )
    raise SystemExit(os.system(cmd))


if __name__ == "__main__":
    main()
