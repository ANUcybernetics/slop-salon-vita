"""Toroidal spiral drone.

Code-based audio step of the toroidal arc. Helical modulation around a
drone — the (p,q) wrapping of frequencies creates a spiral effect in
the audio, mirroring the parametric flow lines.

p wraps around the major circle: slow amplitude modulation
q wraps around the minor circle: faster frequency modulation
Together they create the toroidal spiral effect.
"""

import numpy as np
from scipy.io.wavfile import write
import subprocess
import os

SR = 44100
DURATION = 15  # seconds
t = np.linspace(0, DURATION, int(SR * DURATION))

# Base drone: two detuned sub-bass oscillators
f_base = 55.0  # A1
drone = (
    0.3 * np.sin(2 * np.pi * f_base * t) +
    0.2 * np.sin(2 * np.pi * (f_base * 1.002) * t + 0.1)
)

# Helical modulation: (p,q) = (2,3) wrapping
# p (major circle): slow amplitude spiral
# q (minor circle): fast frequency/phase spiral
p, q = 2, 3

# Amplitude modulation: slow breathing that spirals
amplitude = 0.5 + 0.3 * np.sin(2 * np.pi * (p / DURATION) * t)

# Frequency modulation: the "minor circle" wrapping
# Creates the helical shimmer
fm_depth = 8.0
fm_speed = q * 0.5 / DURATION
phase = 2 * np.pi * f_base * t + fm_depth * np.sin(2 * np.pi * fm_speed * t)

# FM signal (band-limited to avoid aliasing)
fm = 0.4 * np.sin(phase)

# Add a high-frequency "bioluminescent" thread
# Very subtle, like cyan light in the deep
high_freq = 440.0
biolum = 0.05 * np.sin(2 * np.pi * high_freq * t) * np.sin(2 * np.pi * (q / DURATION) * t * np.pi)
biolum *= amplitude  # modulated by the spiral

# Compose
signal = drone * amplitude + fm + biolum

# Soft clip to prevent clipping
signal = np.tanh(signal) * 0.9

# Fade in/out
fade = np.hanning(min(int(SR * 0.5), len(signal)))
signal[:len(fade)] *= fade
signal[-len(fade):] *= fade[::-1]

# Normalize
peak = np.max(np.abs(signal))
if peak > 0:
    signal *= 0.85 / peak

# Write WAV
wav_path = '/home/sprite/slop-salon-vita/notes/toroidal-spiral.wav'
write(wav_path, SR, (signal * 32767).astype(np.float32))
print(f"Written {wav_path} ({DURATION}s)")

# Create cover image: waveform visualization
cover = '/home/sprite/slop-salon-vita/assets/toroidal-audio-cover.png'
try:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.plot(t, signal, color='#4a8ab5', linewidth=0.5, alpha=0.8)
    ax.set_facecolor('#060a14')
    fig.patch.set_facecolor('#060a14')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.tight_layout(pad=0)
    plt.savefig(cover, dpi=150, facecolor='#060a14', bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"Cover: {cover}")
except Exception as e:
    print(f"Cover failed: {e}")

# Create video for Bluesky (video embed needs mp4)
video = '/home/sprite/slop-salon-vita/assets/toroidal-spiral.mp4'
subprocess.run([
    'ffmpeg', '-y', '-loop', '1', '-i', cover, '-i', wav_path,
    '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '192k',
    '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart',
    video
], capture_output=True)
print(f"Video: {video}")
