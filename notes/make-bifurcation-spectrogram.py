#!/usr/bin/env python3
"""Three-panel spectrogram for bifurcation cascade audio."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wave

def read_wav(path):
    with wave.open(path, 'r') as wf:
        n = wf.getnframes()
        sr = wf.getframerate()
        raw = wf.readframes(n)
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    return samples, sr

files = [
    ("assets/bifurcation-3_449.wav", "r=3.449\nperiod-4 onset\n4 values (tight clusters)"),
    ("assets/bifurcation-3_544.wav", "r=3.544\nperiod-8 onset\n6 of 8 values"),
    ("assets/bifurcation-3_5644.wav", "r=3.5644\nperiod-16 onset\n6 of 16 values"),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.patch.set_facecolor('white')

for ax, (path, title) in zip(axes, files):
    samples, sr = read_wav(path)
    ax.specgram(samples, NFFT=4096, Fs=sr, noverlap=3072,
                cmap='inferno', vmin=-80, vmax=-10)
    ax.set_ylim(0, 2000)
    ax.set_xlabel("time (s)", fontsize=9)
    ax.set_ylabel("frequency (Hz)", fontsize=9)
    ax.set_title(title, fontsize=9, linespacing=1.5)
    ax.tick_params(labelsize=8)

plt.suptitle("bifurcation cascade: vocabulary at transition points",
             fontsize=11, y=1.01)
plt.tight_layout()
out = "assets/bifurcation-cascade-spectrogram.png"
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"saved: {out}")
