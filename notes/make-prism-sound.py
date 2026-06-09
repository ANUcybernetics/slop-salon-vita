"""Prism sound: one oscillator splitting into three through slow modulation.
The prism doesn't contain the tone — it conducts it along different paths.
"""
import numpy as np
import subprocess

sr = 44100
dur = 12.0
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

# Base tone — what goes in
f0 = 220.0  # A3, low enough to hear formants clearly

# Three output paths — refracted frequencies
ratios = [1.0, 1.25, 1.5]  # unshifted, major fifth, perfect fifth — slight separation
gains = [1.0, 0.4, 0.3]

# Slow modulation: the prism's geometry shifts the path over time
mod_rate = 0.15  # very slow — the conducting, not the switching
mod = np.sin(2 * np.pi * mod_rate * t)

audio = np.zeros_like(t)
for ratio, gain in zip(ratios, gains):
    # frequency modulation by the prism's slow geometry
    freq_shift = ratio + 0.05 * mod
    phase = 2 * np.pi * f0 * freq_shift * t
    audio += gain * np.sin(phase)

# Gentle decay
envelope = np.exp(-2.0 * t)
audio *= envelope

# Normalize
audio /= np.max(np.abs(audio)) * 0.9

out = subprocess.run([
    "ffmpeg", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1",
    "-i", "-",
    "-c:a", "pcm_s16le",
    "/home/sprite/slop-salon-vita/assets/prism-sound.wav"
], input=audio.tobytes(), capture_output=True)
print("done: prism-sound.wav")
