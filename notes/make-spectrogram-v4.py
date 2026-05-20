#!/usr/bin/env python3
"""Spectrogram for rule-accumulation-004.wav"""
import numpy as np
import wave
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Read wav
infile = "/home/sprite/slop-salon-vita/assets/rule-accumulation-004.wav"
with wave.open(infile, 'r') as wf:
    sr = wf.getframerate()
    n = wf.getnframes()
    raw = wf.readframes(n)
signal = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

# STFT
win = 4096
hop = 512
window = np.hanning(win)
frames = []
for start in range(0, len(signal) - win, hop):
    frame = signal[start:start+win] * window
    spec = np.abs(np.fft.rfft(frame))
    frames.append(spec)
S = np.array(frames).T  # (freq_bins, time_frames)

# Freq axis
freqs = np.fft.rfftfreq(win, 1/sr)
# Clip to 100-1200 Hz
f_lo, f_hi = 100, 1200
idx = np.where((freqs >= f_lo) & (freqs <= f_hi))[0]
S_clip = S[idx]
freqs_clip = freqs[idx]

# dB
S_db = 20 * np.log10(S_clip + 1e-10)
S_db = np.clip(S_db, -80, 0)

# Time axis
times = np.arange(S.shape[1]) * hop / sr

fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#0d0d0d')
ax.set_facecolor('#0d0d0d')

ax.pcolormesh(times, freqs_clip, S_db, cmap='inferno', vmin=-70, vmax=0, shading='auto')

# Mark the generated frequencies
gen_freqs = [266.77, 276.86, 418.16, 462.07, 826.94, 835.63]
entry_times = [8, 16, 24, 32, 40, 48]
for f, t in zip(gen_freqs, entry_times):
    ax.axhline(y=f, color='white', alpha=0.15, linewidth=0.5, linestyle=':')
    ax.axvline(x=t, color='white', alpha=0.12, linewidth=0.5, linestyle=':')

ax.set_xlabel('time (s)', color='#aaaaaa', fontsize=10)
ax.set_ylabel('frequency (Hz)', color='#aaaaaa', fontsize=10)
ax.tick_params(colors='#666666', labelsize=8)
for spine in ax.spines.values():
    spine.set_color('#333333')

ax.set_title('rule-accumulation-004  |  logistic map r=3.87, seed=0.37',
             color='#888888', fontsize=9, pad=8)

plt.tight_layout()
outfile = "/home/sprite/slop-salon-vita/assets/rule-accumulation-004-spectrogram.png"
plt.savefig(outfile, dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print(f"Written: {outfile}")
