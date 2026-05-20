"""
Feigenbaum universality: logistic map vs. sine map.

Both are single-humped maps. Both bifurcate. Both approach chaos.
The bifurcation thresholds differ. The ratios converge to the same δ ≈ 4.669.

Output: assets/universality.png
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Known precise logistic map bifurcation points ---
# x -> r*x*(1-x)
# From: Feigenbaum (1978), confirmed numerically
LOG_BIFS = [
    3.0,          # period 1 -> 2 (exact: f'(x*)=-1 gives r=3)
    3.4494897,    # period 2 -> 4 (= 1 + sqrt(6), ≈ 3.449)
    3.5440903,    # period 4 -> 8
    3.5644073,    # period 8 -> 16
    3.5687594,    # period 16 -> 32
]

def logistic(r, x):
    return r * x * (1 - x)

def sine_map(r, x):
    return r * np.sin(np.pi * x)

def detect_period(map_fn, r, n_warmup=5000, n_orbit=512, tol=1e-7):
    """Detect period of attractor. Returns period or None if chaotic/high-period."""
    x = 0.5
    for _ in range(n_warmup):
        x = map_fn(r, x)
    orbit = []
    for _ in range(n_orbit):
        x = map_fn(r, x)
        orbit.append(x)
    for p in [1, 2, 4, 8, 16, 32]:
        # check that orbit[i] ≈ orbit[i+p] for many i
        n_check = min(p * 8, n_orbit - p)
        if all(abs(orbit[i] - orbit[i + p]) < tol for i in range(n_check)):
            return p
    return None

def find_bifurcation(map_fn, r_lo, r_hi, from_period, tol=1e-9, max_iter=80):
    """Binary search: find r where period transitions from from_period to 2*from_period."""
    for _ in range(max_iter):
        r_mid = (r_lo + r_hi) / 2
        p = detect_period(map_fn, r_mid)
        if p is not None and p <= from_period:
            r_lo = r_mid
        else:
            r_hi = r_mid
        if r_hi - r_lo < tol:
            break
    return (r_lo + r_hi) / 2

print("Logistic map (using known values):")
log_intervals = [LOG_BIFS[i+1] - LOG_BIFS[i] for i in range(len(LOG_BIFS)-1)]
log_ratios = [log_intervals[i] / log_intervals[i+1] for i in range(len(log_intervals)-1)]
print(f"Bifurcations: {[f'{r:.7f}' for r in LOG_BIFS]}")
print(f"Intervals:    {[f'{x:.7f}' for x in log_intervals]}")
print(f"Ratios:       {[f'{x:.4f}' for x in log_ratios]}")
print()

print("Finding sine map bifurcation points (high-warmup)...")
SINE_BIFS = []
SINE_BIFS.append(find_bifurcation(sine_map, 0.60, 0.78, 1))
SINE_BIFS.append(find_bifurcation(sine_map, 0.78, 0.87, 2))
SINE_BIFS.append(find_bifurcation(sine_map, 0.855, 0.866, 4))
SINE_BIFS.append(find_bifurcation(sine_map, 0.862, 0.867, 8))
SINE_BIFS.append(find_bifurcation(sine_map, 0.864, 0.866, 16))

sine_intervals = [SINE_BIFS[i+1] - SINE_BIFS[i] for i in range(len(SINE_BIFS)-1)]
sine_ratios = [sine_intervals[i] / sine_intervals[i+1] for i in range(len(sine_intervals)-1)]
print(f"Bifurcations: {[f'{r:.7f}' for r in SINE_BIFS]}")
print(f"Intervals:    {[f'{x:.7f}' for x in sine_intervals]}")
print(f"Ratios:       {[f'{x:.4f}' for x in sine_ratios]}")

# --- bifurcation diagrams ---
def bifurcation_diagram(map_fn, r_range, n_skip=500, n_plot=150, n_r=2500):
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

def annotate_intervals(ax, bifs, intervals, ratios, y_top=0.93, dy=0.085, r_pad_frac=0.008):
    r_span = bifs[-1] - bifs[0]
    for i in range(min(3, len(intervals))):
        r1, r2 = bifs[i], bifs[i+1]
        y_br = y_top - i * dy
        c = interval_colors[i]
        ax.annotate('', xy=(r2, y_br), xytext=(r1, y_br),
                    arrowprops=dict(arrowstyle='<->', color=c, lw=1.3))
        ax.text((r1 + r2) / 2, y_br + 0.022, f"{intervals[i]:.5f}",
                ha='center', va='bottom', color=c, fontsize=8.5)
        if i < len(ratios):
            ax.text(r2 + r_span * r_pad_frac, y_br, f"÷{ratios[i]:.3f}",
                    ha='left', va='center', color=DIM_COLOR, fontsize=8, style='italic')

# logistic map
ax = axes[0]
ax.scatter(lr, lx, s=0.06, c=TEAL, alpha=0.25, linewidths=0, rasterized=True)
ax.set_xlim(2.5, 4.0)
ax.set_ylim(0, 1)
ax.set_xlabel('r', color=DIM_COLOR, fontsize=11)
ax.set_ylabel('x', color=DIM_COLOR, fontsize=11)
ax.set_title('logistic map\nx → r·x·(1−x)', color=TEXT_COLOR, fontsize=12, pad=12)

for r in LOG_BIFS[1:5]:
    ax.axvline(r, color='#1e3a5f', lw=0.5, alpha=0.5, linestyle='--')

annotate_intervals(ax, LOG_BIFS, log_intervals, log_ratios)
ax.text(3.62, 0.14, 'δ → 4.669', color=ACCENT, fontsize=11, ha='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor=ACCENT, alpha=0.85))

# sine map
ax = axes[1]
ax.scatter(sr, sx, s=0.06, c=VIOLET, alpha=0.25, linewidths=0, rasterized=True)
ax.set_xlim(0.6, 1.0)
ax.set_ylim(0, 1)
ax.set_xlabel('r', color=DIM_COLOR, fontsize=11)
ax.set_ylabel('x', color=DIM_COLOR, fontsize=11)
ax.set_title('sine map\nx → r·sin(πx)', color=TEXT_COLOR, fontsize=12, pad=12)

for r in SINE_BIFS[1:5]:
    ax.axvline(r, color='#1e1e4f', lw=0.5, alpha=0.5, linestyle='--')

annotate_intervals(ax, SINE_BIFS, sine_intervals, sine_ratios, r_pad_frac=0.003)
ax.text(0.978, 0.14, 'δ → 4.669', color=ACCENT, fontsize=11, ha='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor=ACCENT, alpha=0.85))

fig.text(0.5, 0.02,
         'different equations · different parameter ranges · same Feigenbaum constant',
         ha='center', va='bottom', color=DIM_COLOR, fontsize=10.5, style='italic')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('assets/universality.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("\nSaved: assets/universality.png")
