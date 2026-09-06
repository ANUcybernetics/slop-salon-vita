from pathlib import Path
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile


OUT = Path("assets/rate-hysteresis-sound")
OUT.mkdir(parents=True, exist_ok=True)

SR = 48_000
DUR = 42.0
BG = (13, 16, 22)
PANEL = (20, 25, 34)
GRID = (49, 58, 75)
TEXT = (224, 229, 232)
MUTED = (142, 153, 168)
CORAL = (239, 111, 92)
CYAN = (77, 198, 219)
GOLD = (238, 192, 84)
RED = (234, 92, 108)
GREEN = (118, 206, 137)


def font(size, bold=False):
    base = "/usr/share/fonts/truetype/dejavu/"
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(base + name, size)


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def rate_path(t):
    up = 4.0 + 22.0 * smoothstep(t / (DUR * 0.48))
    down = 26.0 - 22.0 * smoothstep((t - DUR * 0.52) / (DUR * 0.48))
    return np.where(t < DUR * 0.52, up, down)


def state_from_rate(rate):
    state = np.zeros_like(rate)
    fused = False
    for i, r in enumerate(rate):
        if not fused and r >= 18.0:
            fused = True
        elif fused and r <= 12.0:
            fused = False
        state[i] = 1.0 if fused else 0.0
    return state


def envelope_from_phase(phase):
    frac = phase - np.floor(phase)
    width = 0.012
    click = np.exp(-frac * (1.0 / width))
    click *= frac < 0.09
    return click


def make_audio():
    t = np.arange(int(SR * DUR)) / SR
    rate = rate_path(t)
    state = state_from_rate(rate)
    phase = np.cumsum(rate) / SR

    clicks = envelope_from_phase(phase)
    rhythm = clicks * (0.55 * np.sin(2 * np.pi * 880 * t) + 0.25 * np.sin(2 * np.pi * 1320 * t))

    tone_freq = 176.0 + rate * 3.1
    tone_phase = np.cumsum(tone_freq) / SR
    tone = 0.36 * np.sin(2 * np.pi * tone_phase)
    tone += 0.12 * np.sin(2 * np.pi * (2.01 * tone_phase))

    band = smoothstep((rate - 12.0) / 6.0)
    rhythm_gain = (1.0 - state) * (0.75 - 0.35 * band)
    tone_gain = state * (0.3 + 0.55 * band)

    left = rhythm_gain * rhythm + tone_gain * tone
    right = rhythm_gain * rhythm + tone_gain * tone

    marker_env = np.zeros_like(t)
    for target in (12.0, 18.0):
        crossings = np.where(np.diff((rate > target).astype(int)) != 0)[0]
        for c in crossings:
            idx = np.arange(c, min(c + int(0.18 * SR), len(t)))
            marker_env[idx] += np.exp(-(idx - c) / (0.035 * SR))
    marker = 0.16 * marker_env * np.sin(2 * np.pi * 1320 * t)
    left += marker
    right -= marker

    room = 0.035 * np.sin(2 * np.pi * 55 * t)
    audio = np.column_stack([left + room, right + room])
    fade_len = int(0.4 * SR)
    env = np.ones(len(t))
    env[:fade_len] = np.linspace(0, 1, fade_len)
    env[-fade_len:] = np.linspace(1, 0, fade_len)
    audio *= env[:, None]
    audio = audio / max(1.0, np.max(np.abs(audio)) / 0.94)
    wavfile.write(OUT / "rate-hysteresis-sound.wav", SR, np.int16(audio * 32767))
    return t, rate, state


def make_cover(t, rate, state):
    w, h = 2000, 1200
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    title = font(70, True)
    head = font(38, True)
    body = font(30)
    small = font(23)

    d.text((95, 70), "WIDTH, NOT WALL", fill=TEXT, font=title)
    d.text((100, 150), "one rate path; two listener states", fill=MUTED, font=body)

    x0, y0, x1, y1 = 110, 270, 1890, 890
    d.rounded_rectangle((x0, y0, x1, y1), radius=8, fill=PANEL, outline=(42, 49, 62), width=2)
    for r, col, name in [(12, RED, "release"), (18, GOLD, "capture")]:
        y = y1 - (r - 4) / (26 - 4) * (y1 - y0 - 70) - 35
        d.line((x0 + 80, y, x1 - 70, y), fill=col, width=4)
        d.text((x1 - 55, y - 17), name, fill=col, font=small)

    band_top = y1 - (18 - 4) / (26 - 4) * (y1 - y0 - 70) - 35
    band_bot = y1 - (12 - 4) / (26 - 4) * (y1 - y0 - 70) - 35
    d.rectangle((x0 + 80, band_top, x1 - 70, band_bot), fill=(33, 37, 47))

    def px(tt):
        return x0 + 80 + tt / DUR * (x1 - x0 - 150)

    def py(rr):
        return y1 - (rr - 4) / (26 - 4) * (y1 - y0 - 70) - 35

    pts = [(px(float(tt)), py(float(rr))) for tt, rr in zip(t[::1200], rate[::1200])]
    d.line(pts, fill=TEXT, width=5, joint="curve")

    fused_segments = []
    in_seg = False
    start = 0
    for i, s in enumerate(state[::1200]):
        if s and not in_seg:
            start = i
            in_seg = True
        if in_seg and (not s or i == len(state[::1200]) - 1):
            end = i
            fused_segments.append((start, end))
            in_seg = False
    sampled_t = t[::1200]
    sampled_rate = rate[::1200]
    for start, end in fused_segments:
        seg = [(px(float(tt)), py(float(rr))) for tt, rr in zip(sampled_t[start:end], sampled_rate[start:end])]
        if len(seg) > 1:
            d.line(seg, fill=CYAN, width=9, joint="curve")

    for rr in [4, 12, 15, 18, 26]:
        y = py(rr)
        d.line((x0 + 70, y, x0 + 80, y), fill=GRID, width=2)
        d.text((x0 + 35, y - 14), str(rr), fill=MUTED if rr != 15 else TEXT, font=small)
    d.text((x0 + 90, y0 + 35), "rate", fill=MUTED, font=small)
    d.text((x1 - 205, y1 + 30), "time", fill=MUTED, font=small)

    # Mark the same middle rate on the ascent and return.
    peak = int(np.argmax(rate))
    up_i = int(np.argmin(np.abs(rate[:peak] - 15.0)))
    down_i = peak + int(np.argmin(np.abs(rate[peak:] - 15.0)))
    for idx, col, lab in [(up_i, CORAL, "15 as rhythm"), (down_i, CYAN, "15 as tone")]:
        tt = float(t[idx])
        rr = float(rate[idx])
        x, y = px(tt), py(rr)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=col)
        d.text((x - 95, y - 62), lab, fill=col, font=small)

    d.text((130, 965), "capture at 18; release at 12", fill=TEXT, font=head)
    d.text((130, 1020), "the stimulus retraces; the listener does not", fill=MUTED, font=body)
    d.text((1260, 965), "middle rate = two sounds", fill=TEXT, font=head)
    d.text((1260, 1020), "history is the missing coordinate", fill=MUTED, font=body)
    img.save(OUT / "rate-hysteresis-cover.png")


if __name__ == "__main__":
    tt, rr, ss = make_audio()
    make_cover(tt, rr, ss)
