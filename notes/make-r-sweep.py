#!/usr/bin/env python3
"""
r-sweep: logistic map attractor sonified as r sweeps 2.8 → 4.0.
The spectrogram of this piece should look like the bifurcation diagram.

Design:
- Duration: 54 seconds
- r sweeps from 2.8 (stable fixed point) to 4.0 (full chaos)
- Every 0.2s, compute attractor for current r, synthesize as sine tones
- In chaos regime, sample 12 attractor values rather than all unique ones

Expected audio shape:
- 0-6s: single steady tone (fixed point)
- 6s: first bifurcation (pitch splits to dyad)
- ~18s: period-4 (chord of 4)
- ~22s: period-8 (dense chord)
- ~25s+: cascade accelerates, then chaos (dense texture)
"""

import numpy as np
from scipy.io import wavfile
import subprocess

SR = 44100
DURATION = 54   # seconds
SEG = 0.2       # seconds per r step
FADE = 0.03     # crossfade at segment edges

r_start = 2.8
r_end = 4.0
n_segs = int(DURATION / SEG)
r_values = np.linspace(r_start, r_end, n_segs)

def get_attractor(r, seed=0.37, transient=3000, collect=256, max_tones=12):
    """Run logistic map to attractor, return unique values (capped at max_tones)."""
    x = seed
    for _ in range(transient):
        x = r * x * (1 - x)

    # collect values, find unique ones (rounded to distinguish)
    vals = []
    for _ in range(collect):
        x = r * x * (1 - x)
        vals.append(x)

    vals = np.array(vals)
    # round to find distinct attractor points
    rounded = np.round(vals, 3)
    unique_rounded = np.unique(rounded)

    # map back to original (unrounded) values
    result = []
    for ur in unique_rounded:
        # find the first val close to this rounded value
        idx = np.argmin(np.abs(rounded - ur))
        result.append(vals[idx])

    result = np.array(result)

    # in chaos: too many unique values — sample evenly
    if len(result) > max_tones:
        indices = np.linspace(0, len(result)-1, max_tones, dtype=int)
        result = result[indices]

    return result


def make_segment(freqs, n_samples, sr, fade_samps):
    """Synthesize sine waves at given frequencies."""
    if len(freqs) == 0:
        return np.zeros(n_samples, dtype=np.float32)

    t = np.arange(n_samples) / sr
    seg = np.zeros(n_samples)
    for f in freqs:
        seg += np.sin(2 * np.pi * f * t)
    seg /= len(freqs)

    # fade in/out to avoid clicks
    fade_in = np.linspace(0, 1, fade_samps)
    fade_out = np.linspace(1, 0, fade_samps)
    seg[:fade_samps] *= fade_in
    seg[-fade_samps:] *= fade_out

    return seg.astype(np.float32)


seg_samples = int(SEG * SR)
fade_samples = int(FADE * SR)
audio = np.zeros(int(DURATION * SR), dtype=np.float32)

print(f"Generating {n_segs} segments, r: {r_start:.2f} → {r_end:.2f}")

for i, r in enumerate(r_values):
    if i % 50 == 0:
        print(f"  segment {i}/{n_segs}, r={r:.4f}")

    attractor = get_attractor(r)
    # map [0,1] attractor values to [200, 1100] Hz
    freqs = 200 + attractor * 900

    seg = make_segment(freqs, seg_samples, SR, fade_samples)

    start = i * seg_samples
    end = start + seg_samples
    if end <= len(audio):
        audio[start:end] += seg

# normalize
peak = np.max(np.abs(audio))
if peak > 0:
    audio = audio / peak * 0.8

out_path = 'assets/r-sweep-bifurcation.wav'
wavfile.write(out_path, SR, audio)
print(f"\nWrote {DURATION}s audio → {out_path}")
print(f"r range: {r_start} → {r_end}")
print(f"First bifurcation at r=3.0: t ≈ {(3.0-r_start)/(r_end-r_start)*DURATION:.1f}s")
print(f"Chaos onset r≈3.57: t ≈ {(3.57-r_start)/(r_end-r_start)*DURATION:.1f}s")

# Generate spectrogram
print("\nGenerating spectrogram...")
spec_script = """
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

sr, audio = wavfile.read('assets/r-sweep-bifurcation.wav')
if audio.ndim > 1:
    audio = audio[:, 0]
audio = audio.astype(np.float32)

fig, ax = plt.subplots(figsize=(12, 5), facecolor='white')

f, t, Sxx = signal.spectrogram(audio, sr, nperseg=4096, noverlap=3072)

# limit to 200-1200 Hz
freq_mask = (f >= 150) & (f <= 1200)
f_plot = f[freq_mask]
Sxx_plot = Sxx[freq_mask, :]

Sxx_db = 10 * np.log10(Sxx_plot + 1e-12)
vmin = np.percentile(Sxx_db, 40)
vmax = np.percentile(Sxx_db, 99.5)

ax.pcolormesh(t, f_plot, Sxx_db, shading='gouraud', cmap='inferno', vmin=vmin, vmax=vmax)
ax.set_xlabel('time (s)', fontsize=10)
ax.set_ylabel('frequency (Hz)', fontsize=10)
ax.set_title('r-sweep: logistic map attractor, r = 2.8 → 4.0', fontsize=11)

# mark bifurcation times
r_start, r_end, dur = 2.8, 4.0, 54.0
bifurcations = [(3.0, 'r=3.0'), (3.449, 'r=3.449'), (3.544, 'r=3.544'), (3.57, 'r≈3.57')]
for r_val, label in bifurcations:
    t_mark = (r_val - r_start) / (r_end - r_start) * dur
    ax.axvline(t_mark, color='white', alpha=0.4, linewidth=0.8, linestyle='--')
    ax.text(t_mark+0.3, 1150, label, color='white', fontsize=7, alpha=0.7)

plt.tight_layout()
plt.savefig('assets/r-sweep-spectrogram.png', dpi=150, bbox_inches='tight')
print("Saved assets/r-sweep-spectrogram.png")
"""
import tempfile, os
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(spec_script)
    tmp = f.name

os.system(f'python3 {tmp}')
os.unlink(tmp)
