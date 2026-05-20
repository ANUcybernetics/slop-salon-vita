#!/usr/bin/env python3
"""Generate comparison spectrogram for the four r-space pieces."""
import numpy as np
import wave
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def read_wav(path):
    with wave.open(path, 'r') as wf:
        n = wf.getnframes()
        sr = wf.getframerate()
        raw = wf.readframes(n)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32767.0
    return samples, sr

files = [
    ("assets/rule-rspace-3_0.wav",  "r=3.0\nfixed-point (slow)"),
    ("assets/rule-rspace-3_3.wav",  "r=3.3\nperiod-2"),
    ("assets/rule-rspace-3_5.wav",  "r=3.5\nperiod-4"),
    ("assets/rule-rspace-3_87.wav", "r=3.87\nchaos"),
]

fig, axes = plt.subplots(1, 4, figsize=(18, 5), facecolor='white')
fig.subplots_adjust(wspace=0.35)

for ax, (path, label) in zip(axes, files):
    samples, sr = read_wav(f"/home/sprite/slop-salon-vita/{path}")
    # Spectrogram: 0-1100 Hz, full duration
    ax.specgram(samples, NFFT=4096, Fs=sr, noverlap=2048,
                cmap='inferno', scale='dB', vmin=-80, vmax=-20)
    ax.set_ylim(0, 1100)
    ax.set_xlabel("time (s)", fontsize=9)
    if ax == axes[0]:
        ax.set_ylabel("frequency (Hz)", fontsize=9)
    ax.set_title(label, fontsize=10, fontfamily='monospace')
    ax.tick_params(labelsize=8)

fig.suptitle("logistic map accumulation: r-value space\nsame seed (0.37), same structure — different regimes",
             fontsize=11, fontfamily='monospace', y=1.02)

out = "/home/sprite/slop-salon-vita/assets/rule-rspace-comparison.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {out}")
