"""
Bifurcation diagram with self-similar zoom boxes.
The visual argument for *why* universality holds:
at each scale, the cascade looks like a rescaled copy of itself.
That self-similarity is exactly what the renormalization fixed point means.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- compute bifurcation diagram ---
def bifurcation_diagram(r_min, r_max, n_r=2000, n_discard=500, n_keep=200):
    rs = np.linspace(r_min, r_max, n_r)
    xs = []
    for r in rs:
        x = 0.5
        for _ in range(n_discard):
            x = r * x * (1 - x)
        orbit = []
        for _ in range(n_keep):
            x = r * x * (1 - x)
            orbit.append(x)
        xs.append(orbit)
    return rs, xs

# logistic map bifurcation thresholds
r1 = 3.0000   # period 1 → 2
r2 = 3.4495   # period 2 → 4
r3 = 3.5441   # period 4 → 8
r4 = 3.5644   # period 8 → 16
r_chaos = 3.5699  # onset of chaos (approx)

# --- figure ---
fig, axes = plt.subplots(1, 3, figsize=(14, 5), facecolor='#0d0d12')
for ax in axes:
    ax.set_facecolor('#0d0d12')

colors = {
    'diagram': '#3aafa9',
    'box0': '#f0a500',
    'box1': '#e05c5c',
    'box2': '#9b7fd4',
    'text': '#c8c8d0',
    'dim': '#555566',
}

def plot_bifurc(ax, r_min, r_max, rs_full, xs_full, box_r_min=None, box_r_max=None,
                 box_x_min=None, box_x_max=None, box_color=None, label=None,
                 title=None, show_boxes=True, alpha_pts=0.18):
    # filter to range
    mask = (rs_full >= r_min) & (rs_full <= r_max)
    rs = rs_full[mask]
    xs = [xs_full[i] for i in range(len(rs_full)) if mask[i]]

    for i, (r, orbit) in enumerate(zip(rs, xs)):
        ax.scatter([r] * len(orbit), orbit,
                   s=0.3, c=colors['diagram'], alpha=alpha_pts, linewidths=0)

    if show_boxes and box_r_min is not None:
        rect = patches.Rectangle(
            (box_r_min, box_x_min),
            box_r_max - box_r_min,
            box_x_max - box_x_min,
            linewidth=1.5, edgecolor=box_color, facecolor='none',
            linestyle='--', zorder=5
        )
        ax.add_patch(rect)
        if label:
            ax.text(box_r_max + (r_max - r_min) * 0.01, (box_x_min + box_x_max) / 2,
                    label, color=box_color, fontsize=8, va='center', fontfamily='monospace')

    ax.set_xlim(r_min, r_max)
    ax.set_ylim(0, 1)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=colors['dim'], labelsize=7)
    ax.xaxis.label.set_color(colors['text'])
    ax.yaxis.label.set_color(colors['text'])
    if title:
        ax.set_title(title, color=colors['text'], fontsize=9, pad=8, fontfamily='monospace')

# Generate once at full resolution
rs_full, xs_full = bifurcation_diagram(2.5, 4.0, n_r=3000, n_discard=600, n_keep=300)
rs_full = np.array(rs_full)

# --- Panel 0: full view, box around first bifurcation interval ---
# Box: r1..r2, attractor range roughly 0 to 1
ax0 = axes[0]
plot_bifurc(ax0, 2.5, 4.0, rs_full, xs_full,
            box_r_min=r1, box_r_max=r2,
            box_x_min=0.05, box_x_max=0.95,
            box_color=colors['box0'],
            label='A', title='full cascade', alpha_pts=0.12)
ax0.set_xlabel('r', color=colors['text'], fontsize=8, fontfamily='monospace')
ax0.set_ylabel('x*', color=colors['text'], fontsize=8, fontfamily='monospace')

# --- Panel 1: zoom into box A (r1..r2), box around second bifurcation interval ---
ax1 = axes[1]
# In this zoomed view, the second bifurcation interval is r2..r3
# and the attractor lives roughly 0.3..0.9 in this range
plot_bifurc(ax1, r1, r2, rs_full, xs_full,
            box_r_min=r2, box_r_max=r3,
            box_x_min=0.3, box_x_max=0.9,
            box_color=colors['box1'],
            label='B', title=f'zoom: box A  (scale ×{(r2-r1)/(r3-r2):.1f} narrower)',
            alpha_pts=0.25)
ax1.set_xlabel('r', color=colors['text'], fontsize=8, fontfamily='monospace')

# annotate scaling
ax1.annotate('', xy=(r1, 0.08), xytext=(r2, 0.08),
             arrowprops=dict(arrowstyle='<->', color=colors['box0'], lw=1.2))
ax1.text((r1 + r2) / 2, 0.12, f'Δr₁ = {r2-r1:.4f}',
         ha='center', va='bottom', color=colors['box0'], fontsize=7, fontfamily='monospace')

# --- Panel 2: zoom into box B (r2..r3) ---
ax2 = axes[2]
# Box C: r3..r4
plot_bifurc(ax2, r2, r3, rs_full, xs_full,
            box_r_min=r3, box_r_max=r4,
            box_x_min=0.3, box_x_max=0.92,
            box_color=colors['box2'],
            label='C', title=f'zoom: box B  (scale ×{(r3-r2)/(r4-r3):.1f} narrower)',
            alpha_pts=0.5)
ax2.set_xlabel('r', color=colors['text'], fontsize=8, fontfamily='monospace')

ax2.annotate('', xy=(r2, 0.08), xytext=(r3, 0.08),
             arrowprops=dict(arrowstyle='<->', color=colors['box1'], lw=1.2))
ax2.text((r2 + r3) / 2, 0.12, f'Δr₂ = {r3-r2:.4f}',
         ha='center', va='bottom', color=colors['box1'], fontsize=7, fontfamily='monospace')

# --- overall annotation ---
ratio1 = (r2 - r1) / (r3 - r2)
ratio2 = (r3 - r2) / (r4 - r3)
ratio3 = (r4 - r3) / (r_chaos - r4)

fig.text(0.5, 0.01,
         f'ratios of successive intervals:  Δr₁/Δr₂ ≈ {ratio1:.3f}   '
         f'Δr₂/Δr₃ ≈ {ratio2:.3f}   '
         f'Δr₃/Δr₄ ≈ {ratio3:.3f}   →   δ ≈ 4.669',
         ha='center', va='bottom', color=colors['text'], fontsize=8.5,
         fontfamily='monospace')

fig.suptitle('self-similarity at every scale: the renormalization fixed point',
             color=colors['text'], fontsize=11, fontfamily='monospace', y=1.01)

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('assets/renormalization.png', dpi=150, bbox_inches='tight',
            facecolor='#0d0d12')
print("saved assets/renormalization.png")
