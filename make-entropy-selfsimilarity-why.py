#!/usr/bin/env python3
"""
Why entropy is self-similar: the renormalization fixed point g.

Row 1: R operator, delta, and the scaling connection.
Row 2: Cascade at 3 zoom levels.
Row 3: Entropy at 3 zoom levels (period-3 window, r ≈ 3.83).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

alpha = 2.502907875
delta = 4.669201609

G_COEFFS = [-1.50949980969, -0.2722213765, -0.0647674147, -0.0157485259,
            -0.0044391279, -0.0013182371, -0.0003889423, -0.0001134149]

def feigenbaum_g(x):
    result = np.zeros_like(x, dtype=float)
    for c, p in zip(G_COEFFS, range(2, 2*len(G_COEFFS)+1, 2)):
        result += c * x**p
    return result

def logistic_cascade(r_vals, n_iter=600, n_transient=200, n_extra=20):
    rs, xs = [], []
    for r in r_vals:
        x = 0.5
        for _ in range(n_iter):
            x = r * x * (1 - x)
        for _ in range(n_extra):
            x = r * x * (1 - x)
            rs.append(r)
            xs.append(x)
    return rs, xs

def compute_entropy(r_vals, n_iter=4000, n_skip=1000):
    h = np.zeros(len(r_vals))
    for i, r in enumerate(r_vals):
        if r < 3.0:
            h[i] = 0.0
            continue
        x = 0.5
        for _ in range(n_skip):
            x = r * x * (1 - x)
        lyap = 0.0
        for _ in range(n_iter - n_skip):
            x = r * x * (1 - x)
            lyap += np.log(abs(r - 2 * r * x))
        lyap /= (n_iter - n_skip)
        h[i] = max(0, lyap)
    return h

# ===== Layout: 3x3 =====
fig = plt.figure(figsize=(16, 8), dpi=150)
palette = ['#1a1a2e', '#e74c3c', '#d35400', '#27ae60', '#8e44ad']

# Panel 1: g(x)
ax_g = plt.subplot(3, 3, 1)
gx = np.linspace(-1, 1, 2000)
gy = feigenbaum_g(gx)
ax_g.plot(gx, gy, color=palette[0], linewidth=2.0)
ax_g.axhline(0, color='gray', linewidth=0.5, alpha=0.4)
ax_g.axvline(0, color='gray', linewidth=0.5, alpha=0.4)
ax_g.plot(0, 0, 'o', color=palette[1], markersize=8, label='critical point')
ax_g.set_title('Feigenbaum-Cvitanovic fixed point g(x)', fontsize=9, fontweight='bold')
ax_g.set_xlabel('x')
ax_g.set_ylabel('g(x)')
ax_g.legend(fontsize=7, framealpha=0.9)
ax_g.grid(True, alpha=0.2)

# Panel 2: R operator
ax_op = plt.subplot(3, 3, 2)
ax_op.axis('off')
ax_op.set_xlim(0, 1)
ax_op.set_ylim(0, 1)
op_text = (
    "R[f](x) = −α · f(f(x/α))\n\n"
    "Maps a unimodal map to a rescaled\n"
    "double-composition of itself.\n\n"
    "Fixed point: R[g] = g\n"
    "Unique shape invariant under R.\n"
    "All unimodal maps converge to g.\n\n"
    "This is why δ is universal:"
)
ax_op.text(0.5, 0.5, op_text, fontsize=9, ha='center', va='center',
           family='monospace', transform=ax_op.transAxes, color=palette[0],
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f4e8', alpha=0.95))

# Panel 3: δ
ax_d = plt.subplot(3, 3, 3)
ax_d.axis('off')
ax_d.set_xlim(0, 1)
ax_d.set_ylim(0, 1)
delta_text = (
    "δ = 4.669201609...\n\n"
    "Eigenvalue of Dᵣ at g.\n\n"
    "Governs three things:\n"
    "  1. rₙ → r∞: ratio → δ\n"
    "  2. Cascade width: α⁻ⁿ\n"
    "  3. Entropy scaling: hₙ/δ\n\n"
    "One number, three roles."
)
ax_d.text(0.5, 0.5, delta_text, fontsize=9, ha='center', va='center',
          family='monospace', transform=ax_d.transAxes, color=palette[0],
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#fdf6e3', alpha=0.95))

# Panels 4-6: Cascade at 3 zoom levels
r_inf = 3.56994567
zoom_levels = [
    (r_inf - 0.6, 0.6, 600, 20, 1.0, 'broad'),
    (r_inf - 0.10, 0.10, 800, 15, 0.4, '×α'),
    (r_inf - 0.015, 0.015, 1200, 12, 0.15, '×α²'),
]

for level in range(3):
    r_start, r_span, n_iter, n_pts, scale, label = zoom_levels[level]
    r_vals = np.linspace(r_start, r_start + r_span, 1500)

    ax = plt.subplot(3, 3, 4 + level)
    rs, xs = logistic_cascade(r_vals, n_iter=n_iter, n_extra=n_pts)
    ax.scatter(rs, xs, s=0.2, c=palette[0], alpha=0.35)
    ax.set_title(f'cascade — {label}', fontsize=9, fontweight='bold')
    if level == 0:
        ax.set_ylabel('x')
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.12)
    if level == 0:
        ax.set_xlabel('r')

# Panels 7-9: Entropy at 3 zoom levels (period-3 window)
p3_center = 3.8284
p3_spans = [0.15, 0.03, 0.005]
p3_labels = ['broad', '×α', '×α²']
p3_scales = [1.0, 0.4, 0.15]

for level in range(3):
    ax = plt.subplot(3, 3, 7 + level)
    r_start = p3_center - p3_spans[level]
    r_span = 2 * p3_spans[level]
    r_vals = np.linspace(r_start, r_start + r_span, 1500)
    h_vals = compute_entropy(r_vals, n_iter=5000, n_skip=1000)
    ax.fill_between(r_vals, 0, h_vals * p3_scales[level], color='#d35400', alpha=0.4)
    ax.plot(r_vals, h_vals * p3_scales[level], color='#d35400', linewidth=0.6)
    ax.set_title(f'entropy h(r) — {p3_labels[level]}', fontsize=9, fontweight='bold')
    if level == 0:
        ax.set_ylabel('h')
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.12)
    if level >= 1:
        ax.set_xlabel('r')

fig.suptitle('The Fixed Point g Produces Both Cascade and Entropy Self-Similarity',
             fontsize=13, fontweight='bold', y=0.97)
fig.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('assets/entropy-selfsimilarity-why.webp', format='webp', dpi=150)
print("Saved")
