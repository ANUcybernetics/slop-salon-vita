"""Prism sound cover: spectrogram of the refracted tone."""
import numpy as np
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sr = 44100
dur = 12.0
t = np.linspace(0, dur, int(sr * dur), endpoint=False)
f0 = 220.0
ratios = [1.0, 1.25, 1.5]
gains = [1.0, 0.4, 0.3]
mod_rate = 0.15
mod = np.sin(2 * np.pi * mod_rate * t)
audio = np.zeros_like(t)
for ratio, gain in zip(ratios, gains):
    freq_shift = ratio + 0.05 * mod
    phase = 2 * np.pi * f0 * freq_shift * t
    audio += gain * np.sin(phase)
audio *= np.exp(-2.0 * t)

# Use ffmpeg to compute spectrogram
subprocess.run([
    "ffmpeg", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1",
    "-i", "-",
    "-af", "spectrogram=color=blue+black:size=512x384:mode=stack,format=yuv420p",
    "/home/sprite/slop-salon-vita/assets/prism-cover.png"
], input=audio.tobytes(), capture_output=True)
print("done: prism-cover.png")
