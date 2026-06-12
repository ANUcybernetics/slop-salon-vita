"""
Crease audio spectrogram.

The crease's time-varying sharpness made visible as a spectrogram.
The envelope's V-shape (γ→0.3) vs U-shape (γ→2) shows as horizontal
band structure — the crease's nonlinearity imprinting itself on the spectrum.

This is the material register heard: the frequency response of a fold
that is sharp at the edges and flat at the center.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

sr, data = wav.read('/home/sprite/slop-salon-vita/assets/crease-audio.wav')
data = data.astype(np.float32) / 32768.0

plt.rcParams.update({
    'axes.facecolor': '#0a0a0a',
    'figure.facecolor': '#0a0a0a',
    'axes.labelcolor': '#888888',
    'xtick.color': '#888888',
    'ytick.color': '#888888',
    'text.color': '#cccccc',
    'font.family': 'monospace',
    'font.size': 10,
})

fig, ax = plt.subplots(figsize=(12, 4))

spec, freqs, t_bins, im = ax.specgram(
    data, NFFT=2048, Fs=sr,
    cmap='magma',
    vmin=-80, vmax=-10,
)

ax.set_xlabel('time (s)')
ax.set_ylabel('frequency (Hz)')
ax.set_title('crease-audio.wav')

# Mark the crease's sharpness transitions
# γ goes from rounded (0.3) to sharp (2.0) in a sine wave over 2 cycles
ax.axvline(1.0, color='#ff6633', alpha=0.4, linewidth=0.5, linestyle='--')
ax.axvline(2.0, color='#ff6633', alpha=0.4, linewidth=0.5, linestyle='--')
ax.axvline(3.0, color='#ff6633', alpha=0.4, linewidth=0.5, linestyle='--')

fig.colorbar(im, ax=ax, label='dB', shrink=0.8)
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/crease-audio-spec.png', dpi=150)
plt.close()
print("Wrote crease-audio-spec.png")
