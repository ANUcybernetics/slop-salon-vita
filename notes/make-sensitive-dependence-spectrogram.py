"""
Generate a two-panel spectrogram: seed A (top) vs seed B (bottom).
The divergence point is visible as the moment they stop mirroring.
"""

import numpy as np
import wave
import struct
from PIL import Image, ImageDraw, ImageFont

SAMPLE_RATE = 44100
FREQ_MAX_DISPLAY = 1200  # Hz

def read_wav_mono(path):
    with wave.open(path, 'r') as wf:
        n = wf.getnframes()
        raw = wf.readframes(n)
        ch = wf.getnchannels()
        sw = wf.getsampwidth()
    fmt = '<' + ('h' if sw == 2 else 'b') * (n * ch)
    samples = struct.unpack(fmt, raw)
    if ch == 2:
        # stereo: deinterleave
        left  = np.array(samples[0::2], dtype=float) / 32767.0
        right = np.array(samples[1::2], dtype=float) / 32767.0
        return left, right
    else:
        return np.array(samples, dtype=float) / 32767.0, None

def spectrogram(signal, sample_rate, fft_size=2048, hop=512, freq_max=None):
    """Return (times, freqs, magnitude_dB) arrays."""
    n = len(signal)
    window = np.hanning(fft_size)
    frames = []
    times = []
    for i in range(0, n - fft_size, hop):
        frame = signal[i:i+fft_size] * window
        spec = np.abs(np.fft.rfft(frame))
        frames.append(spec)
        times.append((i + fft_size / 2) / sample_rate)
    S = np.array(frames).T  # (freq_bins, time_frames)
    freqs = np.fft.rfftfreq(fft_size, 1/sample_rate)
    # dB
    S_db = 20 * np.log10(np.maximum(S, 1e-10))
    # trim to freq_max
    if freq_max:
        mask = freqs <= freq_max
        freqs = freqs[mask]
        S_db = S_db[mask, :]
    return np.array(times), freqs, S_db

def render_panel(S_db, width, height, db_min=-60, db_max=0):
    """Render a spectrogram matrix to a numpy RGB image (freq low=bottom)."""
    S_norm = np.clip((S_db - db_min) / (db_max - db_min), 0, 1)
    # resize to (height, width)
    from PIL import Image
    img_arr = (S_norm * 255).astype(np.uint8)
    # S_norm is (freq_bins, time_frames); freq goes low→high (row 0 = 0 Hz)
    # flip vertically so low freq is at bottom
    img_arr = np.flipud(img_arr)
    pil = Image.fromarray(img_arr, mode='L').convert('RGB')
    pil = pil.resize((width, height), Image.LANCZOS)
    return np.array(pil)

left, right = read_wav_mono("assets/sensitive-dependence.wav")

_, _, S_a = spectrogram(left,  SAMPLE_RATE, fft_size=2048, hop=256, freq_max=FREQ_MAX_DISPLAY)
times, freqs, S_b = spectrogram(right, SAMPLE_RATE, fft_size=2048, hop=256, freq_max=FREQ_MAX_DISPLAY)

PANEL_W = 900
PANEL_H = 250
MARGIN   = 40
GAP      = 20

total_w = PANEL_W + MARGIN * 2
total_h = PANEL_H * 2 + GAP + MARGIN * 3

canvas = np.full((total_h, total_w, 3), 255, dtype=np.uint8)

p_a = render_panel(S_a, PANEL_W, PANEL_H)
p_b = render_panel(S_b, PANEL_W, PANEL_H)

y0 = MARGIN
y1 = MARGIN + PANEL_H + GAP

canvas[y0:y0+PANEL_H, MARGIN:MARGIN+PANEL_W] = p_a
canvas[y1:y1+PANEL_H, MARGIN:MARGIN+PANEL_W] = p_b

pil = Image.fromarray(canvas)
draw = ImageDraw.Draw(pil)

# labels
draw.text((MARGIN, y0 - 18), "seed A: 0.500000", fill=(30,30,30))
draw.text((MARGIN, y1 - 18), "seed B: 0.500001", fill=(30,30,30))

# freq axis label (left side)
draw.text((2, y0 + PANEL_H//2 - 8), f"{FREQ_MAX_DISPLAY}Hz", fill=(80,80,80))
draw.text((2, y0 + PANEL_H - 12),    "200Hz",                 fill=(80,80,80))
draw.text((2, y1 + PANEL_H//2 - 8), f"{FREQ_MAX_DISPLAY}Hz", fill=(80,80,80))
draw.text((2, y1 + PANEL_H - 12),    "200Hz",                 fill=(80,80,80))

# time axis
duration = times[-1]
for t_mark in [0, 5, 10, 15, 20, 25, 30]:
    if t_mark <= duration:
        x = MARGIN + int(t_mark / duration * PANEL_W)
        draw.text((x - 4, y1 + PANEL_H + 4), f"{t_mark}s", fill=(80,80,80))
        draw.line([(x, y1+PANEL_H), (x, y1+PANEL_H+3)], fill=(80,80,80))

out = "assets/sensitive-dependence-spectrogram.png"
pil.save(out)
print(f"saved {out}")
print(f"canvas: {total_w}x{total_h}, duration: {duration:.1f}s, freq bins: {len(freqs)}")
