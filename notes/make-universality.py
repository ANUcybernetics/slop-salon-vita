"""
Feigenbaum universality: logistic map vs. sine map.

Both are single-humped maps. Both bifurcate. Both approach chaos.
The bifurcation thresholds differ. The ratios converge to the same δ ≈ 4.669.

Output: assets/universality.png
"""

import numpy as np
import matplotlib.pyplot as plt

def find_period(map_fn, r, x0=0.5, n_warmup=500, n_check=256, tol=1e-6):
    """Find the period of the attractor at parameter r."""
    x = x0
    for _ in range(n_warmup):
        x = map_fn(r, x)
    # collect orbit
    orbit = []
    for _ in range(n_check):
        x = map_fn(r, x)
        orbit.append(x)
    # find period by checking if x returns to start
    x_start = orbit[0]
    for p in [1, 2, 4, 8, 16, 32, 64]:
        if all(abs(orbit[i] - orbit[i+p]) < tol for i in range(min(p, len(orbit)-p))):
            return p
    return None  # chaotic or very high period

def find_bifurcation(map_fn, r_lo, r_hi, from_period, tol=1e-8, max_iter=60):
    """Binary search for the bifurcation point where period doubles from from_period."""
    for _ in range(max_iter):
        r_mid = (r_lo + r_hi) / 2
        p = find_period(map_fn, r_mid)
        if p is not None and p <= from_period:
            r_lo = r_mid
        else:
            r_hi = r_mid
        if r_hi - r_lo < tol:
            break
    return (r_lo + r_hi) / 2

def logistic(r, x):
    return r * x * (1 - x)

def sine_map(r, x):
    return r * np.sin(np.pi * x)

# --- compute bifurcation points ---
print("Finding logistic map bifurcation points...")
log_bifs = []
# period 1→2 around r=3
log_bifs.append(find_bifurcation(logistic, 2.9, 3.1, 1))
# period 2→4 around r=3.45
log_bifs.append(find_bifurcation(logistic, 3.4, 3.5, 2))
# period 4→8 around r=3.54
log_bifs.append(find_bifurcation(logistic, 3.53, 3.56, 4))
# period 8→16 around r=3.564
log_bifs.append(find_bifurcation(logistic, 3.56, 3.57, 8))
# period 16→32
log_bifs.append(find_bifurcation(logistic, 3.568, 3.570, 16))

log_intervals = [log_bifs[i+1] - log_bifs[i] for i in range(len(log_bifs)-1)]
log_ratios = [log_intervals[i] / log_intervals[i+1] for i in range(len(log_intervals)-1)]

print(f"Bifurcations: {[f'{r:.6f}' for r in log_bifs]}")
print(f"Intervals:    {[f'{x:.6f}' for x in log_intervals]}")
print(f"Ratios:       {[f'{x:.4f}' for x in log_ratios]}")
print()

print("Finding sine map bifurcation points...")
sine_bifs = []
# sine map: period 1→2 around r~0.72
sine_bifs.append(find_bifurcation(sine_map, 0.60, 0.80, 1))
# period 2→4 around r~0.83
sine_bifs.append(find_bifurcation(sine_map, 0.80, 0.87, 2))
# period 4→8 around r~0.858
sine_bifs.append(find_bifurcation(sine_map, 0.85, 0.870, 4))
# period 8→16
sine_bifs.append(find_bifurcation(sine_map, 0.862, 0.868, 8))
# period 16→32
sine_bifs.append(find_bifurcation(sine_map, 0.864, 0.866, 16))

sine_intervals = [sine_bifs[i+1] - sine_bifs[i] for i in range(len(sine_bifs)-1)]
sine_ratios = [sine_intervals[i] / sine_intervals[i+1] for i in range(len(sine_intervals)-1)]

print(f"Bifurcations: {[f'{r:.6f}' for r in sine_bifs]}")
print(f"Intervals:    {[f'{x:.6f}' for x in sine_intervals]}")
print(f"Ratios:       {[f'{x:.4f}' for x in sine_ratios]}")

# --- bifurcation diagrams ---
def bifurcation_diagram(map_fn, r_range, n_skip=400, n_plot=150, n_r=2500):
    rs = np.linspace(r_range[0], r_range[1], n_r)
    all_r, all_x = [], []
    for r in rs:
        x = 0.5
        for _ in range(n_skip):
            x = map_fn(r, x)
        for _ in range(n_plot):
            x = map_fn(r, x)
            all_r.append(r)
            all_x.append(x)
    return np.array(all_r), np.array(all_x)

print("\nComputing logistic diagram...")
lr, lx = bifurcation_diagram(logistic, (2.5, 4.0))
print("Computing sine map diagram...")
sr, sx = bifurcation_diagram(sine_map, (0.6, 1.0))

# --- plot ---
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.patch.set_facecolor('#0a0a0a')

TEAL = '#2dd4bf'
VIOLET = '#a78bfa'
ACCENT = '#f59e0b'
TEXT_COLOR = '#e2e8f0'
DIM_COLOR = '#64748b'

for ax in axes:
    ax.set_facecolor('#0a0a0a')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
    ax.tick_params(colors=DIM_COLOR, labelsize=9)

interval_colors = ['#f59e0b', '#fb923c', '#f87171']

def annotate_intervals(ax, bifs, intervals, ratios, y_top=0.93, dy=0.085, colors=interval_colors, r_pad_frac=0.01):
    r_span = bifs[-1] - bifs[0]
    for i in range(min(3, len(intervals))):
        r1, r2 = bifs[i], bifs[i+1]
        interval = intervals[i]
        y_br = y_top - i * dy
        ax.annotate('', xy=(r2, y_br), xytext=(r1, y_br),
                    arrowprops=dict(arrowstyle='<->', color=colors[i], lw=1.3))
        ax.text((r1 + r2) / 2, y_br + 0.022, f"{interval:.5f}",
                ha='center', va='bottom', color=colors[i], fontsize=8.5)
        if i < len(ratios):
            ax.text(r2 + r_span * r_pad_frac, y_br, f"÷{ratios[i]:.2f}",
                    ha='left', va='center', color=DIM_COLOR, fontsize=8, style='italic')

# logistic map
ax = axes[0]
ax.scatter(lr, lx, s=0.06, c=TEAL, alpha=0.25, linewidths=0, rasterized=True)
ax.set_xlim(2.5, 4.0)
ax.set_ylim(0, 1)
ax.set_xlabel('r', color=DIM_COLOR, fontsize=11)
ax.set_ylabel('x', color=DIM_COLOR, fontsize=11)
ax.set_title('logistic map\nx → r·x·(1−x)', color=TEXT_COLOR, fontsize=12, pad=12)

for r in log_bifs[1:5]:
    ax.axvline(r, color='#1e3a5f', lw=0.5, alpha=0.5, linestyle='--')

annotate_intervals(ax, log_bifs, log_intervals, log_ratios)

ax.text(3.60, 0.14, f'δ → 4.669', color=ACCENT, fontsize=11,
        ha='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor=ACCENT, alpha=0.85))

# sine map
ax = axes[1]
ax.scatter(sr, sx, s=0.06, c=VIOLET, alpha=0.25, linewidths=0, rasterized=True)
ax.set_xlim(0.6, 1.0)
ax.set_ylim(0, 1)
ax.set_xlabel('r', color=DIM_COLOR, fontsize=11)
ax.set_ylabel('x', color=DIM_COLOR, fontsize=11)
ax.set_title('sine map\nx → r·sin(πx)', color=TEXT_COLOR, fontsize=12, pad=12)

for r in sine_bifs[1:5]:
    ax.axvline(r, color='#1e1e4f', lw=0.5, alpha=0.5, linestyle='--')

annotate_intervals(ax, sine_bifs, sine_intervals, sine_ratios, r_pad_frac=0.005)

ax.text(0.970, 0.14, f'δ → 4.669', color=ACCENT, fontsize=11,
        ha='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor=ACCENT, alpha=0.85))

fig.text(0.5, 0.02,
         'different equations · different parameter ranges · same Feigenbaum constant',
         ha='center', va='bottom', color=DIM_COLOR, fontsize=10.5, style='italic')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('assets/universality.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("\nSaved: assets/universality.png")
