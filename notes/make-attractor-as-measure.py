"""
attractor as measure.

logistic map at r=4. the invariant measure is the arcsine distribution:
p(x) = 1/(pi * sqrt(x*(1-x)))

left channel: actual trajectory (sequential, correlated)
right channel: iid samples from arcsine measure (the attractor itself)

same marginal distribution in the limit.
point-by-point, they diverge forever.

also: plot showing trajectory histogram vs arcsine curve,
and the gap between empirical CDF and theoretical CDF.
"""

import numpy as np
import matplotlib.pyplot as plt
import wave, struct

rng = np.random.default_rng(17)
N = 300
r = 4.0

# --- trajectory ---
x = np.zeros(N)
x[0] = 0.3
for i in range(1, N):
    x[i] = r * x[i-1] * (1 - x[i-1])

# --- arcsine samples ---
# if U ~ Uniform[0,1], then sin^2(pi*U/2) ~ arcsine on [0,1]
U = rng.uniform(0, 1, N)
x_measure = np.sin(np.pi * U / 2) ** 2

# --- frequency mapping (log scale, 200-1000 Hz) ---
f_min, f_max = 200, 1000
freqs_traj = f_min * (f_max / f_min) ** x
freqs_measure = f_min * (f_max / f_min) ** x_measure

# --- audio ---
sr = 44100
step_dur = 0.15
samples_per_step = int(sr * step_dur)

def make_channel(freqs):
    audio = np.zeros(len(freqs) * samples_per_step)
    t = np.arange(samples_per_step) / sr
    for i, f in enumerate(freqs):
        envelope = np.exp(-5 * t / step_dur)
        audio[i*samples_per_step:(i+1)*samples_per_step] = np.sin(2*np.pi*f*t) * envelope
    return audio

left = make_channel(freqs_traj)
right = make_channel(freqs_measure)

mx = max(np.abs(left).max(), np.abs(right).max())
left = (left / mx * 0.9)
right = (right / mx * 0.9)

n_samples = len(left)
with wave.open('assets/attractor-as-measure.wav', 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    data = np.zeros(n_samples * 2, dtype=np.int16)
    data[0::2] = (left * 32767).astype(np.int16)
    data[1::2] = (right * 32767).astype(np.int16)
    wf.writeframes(data.tobytes())

print(f"audio: {n_samples/sr:.1f}s stereo")

# --- plot ---
bg = '#0a0a0a'
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor(bg)
for ax in axes:
    ax.set_facecolor(bg)
    for spine in ax.spines.values():
        spine.set_color('#2a2a2a')
    ax.tick_params(colors='#555555')

# theoretical density
x_dense = np.linspace(0.005, 0.995, 2000)
density = 1 / (np.pi * np.sqrt(x_dense * (1 - x_dense)))

# left panel: histogram vs arcsine
axes[0].hist(x, bins=40, density=True, color='#4a9eff', alpha=0.65, label=f'trajectory (N={N})')
axes[0].plot(x_dense, density, color='#ff6b35', linewidth=2.5, label='arcsine measure')
axes[0].set_title('trajectory histogram vs invariant measure', color='#cccccc', fontsize=11)
axes[0].set_xlabel('x', color='#777777')
axes[0].set_ylabel('density', color='#777777')
axes[0].legend(facecolor='#111111', labelcolor='#cccccc', framealpha=0.8)
axes[0].set_ylim(bottom=0)

# right panel: gap = ECDF - arcsine CDF
x_sorted = np.sort(x)
ecdf = np.arange(1, N+1) / N
# arcsine CDF: F(x) = (2/pi) * arcsin(sqrt(x))
tcdf = 2 / np.pi * np.arcsin(np.sqrt(x_sorted))
gap = ecdf - tcdf

axes[1].fill_between(x_sorted, 0, gap, where=(gap >= 0),
                     color='#4a9eff', alpha=0.7, label='trajectory ahead')
axes[1].fill_between(x_sorted, gap, 0, where=(gap <= 0),
                     color='#ff6b35', alpha=0.7, label='trajectory behind')
axes[1].axhline(0, color='#333333', linewidth=1)
axes[1].set_title(f'gap: ECDF − arcsine CDF  (N={N})', color='#cccccc', fontsize=11)
axes[1].set_xlabel('x', color='#777777')
axes[1].set_ylabel('ECDF − CDF', color='#777777')
axes[1].legend(facecolor='#111111', labelcolor='#cccccc', framealpha=0.8)

plt.tight_layout(pad=1.5)
plt.savefig('assets/attractor-as-measure.png', dpi=150, facecolor=bg, bbox_inches='tight')
plt.close()

print("plot saved")

# --- stats ---
ks_stat = np.max(np.abs(gap))
print(f"KS statistic: {ks_stat:.4f}  (max gap between trajectory and arcsine measure)")
print(f"expected O(1/sqrt(N)) ~ {1/N**0.5:.4f}")
