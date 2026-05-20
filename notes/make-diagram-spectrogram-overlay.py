#!/usr/bin/env python3
"""
Overlay: bifurcation diagram and r-sweep spectrogram.

Mina's observation: the spectrogram of my r-sweep audio IS the bifurcation
diagram. Same structure. Different relation to duration.

This makes that convergence explicit: both panels share the same x-axis
(r / time), and the y-axes map to the same frequency range (200-1000 Hz,
log scale). A dot in the bifurcation diagram and a stripe in the spectrogram
are two ways of marking the same point.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.io import wavfile

# --- Parameters (must match make-r-sweep.py) ---
r_start = 2.8
r_end = 4.0
freq_lo = 200.0
freq_hi = 1000.0
SR = 44100
DURATION = 54.0


def x_to_freq(x):
    """Map attractor value [0,1] to frequency [200,1000] log scale."""
    return freq_lo * (freq_hi / freq_lo) ** x


def compute_bifurcation(r_vals, transient=3000, collect=512):
    """Return (r, x) pairs for bifurcation diagram."""
    rs = []
    xs = []
    for r in r_vals:
        x = 0.37
        for _ in range(transient):
            x = r * x * (1 - x)
        for _ in range(collect):
            x = r * x * (1 - x)
            rs.append(r)
            xs.append(x)
    return np.array(rs), np.array(xs)


# Load the existing r-sweep audio
audio_path = "/home/sprite/slop-salon-vita/assets/r-sweep-bifurcation.wav"
sr, audio = wavfile.read(audio_path)
if audio.ndim > 1:
    audio = audio[:, 0]  # take left channel
audio = audio.astype(float)
audio /= np.abs(audio).max() + 1e-9

# Compute spectrogram
from scipy.signal import spectrogram as sp_spectrogram
nperseg = 2048
noverlap = nperseg - 256
f, t, Sxx = sp_spectrogram(audio, fs=sr, nperseg=nperseg, noverlap=noverlap,
                             window='hann', scaling='density')

# Keep only audible range (100-2000 Hz for display context)
freq_mask = (f >= 100) & (f <= 2000)
f_display = f[freq_mask]
Sxx_display = Sxx[freq_mask, :]

# Clip t to actual audio duration
t_clip = t[t <= DURATION]
Sxx_display = Sxx_display[:, :len(t_clip)]

# Normalize: log power
Sxx_log = 10 * np.log10(Sxx_display + 1e-12)
vmin = np.percentile(Sxx_log, 40)
vmax = np.percentile(Sxx_log, 99.5)

# Map spectrogram time to r-value (linear)
t_to_r = r_start + (t_clip / DURATION) * (r_end - r_start)

# Compute bifurcation diagram at same r resolution
r_bif = np.linspace(r_start, r_end, 800)
rs_bif, xs_bif = compute_bifurcation(r_bif, transient=3000, collect=200)
freqs_bif = x_to_freq(xs_bif)

# --- Plot ---
fig, axes = plt.subplots(2, 1, figsize=(12, 8),
                          facecolor='#0d0d0d', sharex=True)
fig.subplots_adjust(hspace=0.04, left=0.07, right=0.97, top=0.93, bottom=0.08)

fig.suptitle("same structure / different relation to duration",
             color='#cccccc', fontsize=11, fontfamily='monospace', y=0.97)

# --- Panel 1: Bifurcation diagram ---
ax1 = axes[0]
ax1.set_facecolor('#0d0d0d')

# Convert bifurcation x-values to frequency (same mapping as audio)
ax1.scatter(rs_bif, freqs_bif, s=0.08, c='#4dd0c4', alpha=0.4, linewidths=0)
ax1.set_yscale('log')
ax1.set_ylim(freq_lo * 0.8, freq_hi * 1.2)
ax1.set_yticks([200, 400, 600, 1000])
ax1.set_yticklabels(['200', '400', '600', '1000'],
                     color='#888888', fontsize=8, fontfamily='monospace')
ax1.set_ylabel('Hz', color='#888888', fontsize=9, fontfamily='monospace')
ax1.tick_params(axis='x', colors='#888888', labelsize=8)
ax1.tick_params(axis='y', colors='#888888', labelsize=8)
for spine in ax1.spines.values():
    spine.set_color('#333333')

# Add horizontal reference lines at freq_lo and freq_hi
ax1.axhline(freq_lo, color='#333333', linewidth=0.5, linestyle='--')
ax1.axhline(freq_hi, color='#333333', linewidth=0.5, linestyle='--')

label1 = "bifurcation diagram  ·  r [2.8 → 4.0]  ·  attractor values → Hz"
ax1.text(0.01, 0.96, label1, transform=ax1.transAxes,
          color='#666666', fontsize=8, fontfamily='monospace', va='top')

# --- Panel 2: Spectrogram ---
ax2 = axes[1]
ax2.set_facecolor('#0d0d0d')

# x-axis: r-value (mapped from time)
extent = [t_to_r[0], t_to_r[-1], f_display[0], f_display[-1]]
img = ax2.imshow(Sxx_log, aspect='auto', origin='lower',
                  extent=extent, cmap='inferno',
                  vmin=vmin, vmax=vmax,
                  interpolation='bilinear')
ax2.set_yscale('log')
ax2.set_ylim(freq_lo * 0.8, freq_hi * 1.2)
ax2.set_yticks([200, 400, 600, 1000])
ax2.set_yticklabels(['200', '400', '600', '1000'],
                     color='#888888', fontsize=8, fontfamily='monospace')
ax2.set_ylabel('Hz', color='#888888', fontsize=9, fontfamily='monospace')
ax2.set_xlabel('r', color='#888888', fontsize=9, fontfamily='monospace')
ax2.tick_params(axis='x', colors='#888888', labelsize=8)
ax2.tick_params(axis='y', colors='#888888', labelsize=8)
for spine in ax2.spines.values():
    spine.set_color('#333333')

label2 = "r-sweep spectrogram  ·  54s audio  ·  time → r  ·  frequency"
ax2.text(0.01, 0.96, label2, transform=ax2.transAxes,
          color='#666666', fontsize=8, fontfamily='monospace', va='top')

# Shared x tick labels
ax1.set_xlim(r_start, r_end)
x_ticks = [2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0]
ax2.set_xticks(x_ticks)
ax2.set_xticklabels([str(r) for r in x_ticks],
                     color='#888888', fontsize=8, fontfamily='monospace')

out_path = "/home/sprite/slop-salon-vita/assets/diagram-spectrogram-overlay.png"
plt.savefig(out_path, dpi=150, facecolor='#0d0d0d', bbox_inches='tight')
print(f"saved: {out_path}")
plt.close()
