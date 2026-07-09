#!/usr/bin/env python3
"""
Same local. Different global.

Four joint distributions on R⁴ with similar pairwise correlation
structure but fundamentally different dependency graphs.

1. Multivariate Normal — fully characterized by pairwise. No hidden structure.
2. Latent Mixture — a latent Z modulates within-block correlation.
3. Independent Blocks — two bivariate blocks, no cross-block structure.
4. Latent Factor — a shared factor couples the blocks globally.

The pairwise view sees the same local structure. The global dependencies
differ. Frobenius analogue: local closure ≠ global integrability.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

np.random.seed(42)
N = 5000

def make_gaussian(n=N, seed=42):
    """Pure multivariate normal."""
    np.random.seed(seed)
    cov = np.array([
        [1.0,  0.6,  0.05, 0.05],
        [0.6,  1.0,  0.05, 0.05],
        [0.05, 0.05, 1.0,  0.4],
        [0.05, 0.05, 0.4,  1.0 ],
    ])
    return np.random.multivariate_normal([0,0,0,0], cov, size=n)

def make_mixture(n=N, seed=42):
    """Latent Z modulates within-block correlation."""
    np.random.seed(seed)
    Z = np.random.binomial(1, 0.5, size=n).astype(bool)

    cov1 = np.array([
        [1.0, 0.85, 0.15, 0.15],
        [0.85, 1.0, 0.15, 0.15],
        [0.15, 0.15, 1.0, 0.34],
        [0.15, 0.15, 0.34, 1.0],
    ])
    cov0 = np.array([
        [1.0, 0.35, -0.05, -0.05],
        [0.35, 1.0, -0.05, -0.05],
        [-0.05, -0.05, 1.0, 0.14],
        [-0.05, -0.05, 0.14, 1.0],
    ])

    samples = np.zeros((n, 4))
    samples[Z] = np.random.multivariate_normal([0,0,0,0], cov1, size=Z.sum())
    samples[~Z] = np.random.multivariate_normal([0,0,0,0], cov0, size=(~Z).sum())

    stds = samples.std(axis=0)
    stds[stds < 1e-6] = 1.0
    return np.nan_to_num(samples / stds, 0.0)

def make_blocks(n=N, seed=42):
    """Two independent bivariate blocks."""
    np.random.seed(seed)
    x12 = np.random.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], size=n)
    x34 = np.random.multivariate_normal([0, 0], [[1, 0.4], [0.4, 1]], size=n)
    samples = np.column_stack([x12, x34])
    stds = samples.std(axis=0)
    stds[stds < 1e-6] = 1.0
    return np.nan_to_num(samples / stds, 0.0)

def make_factor(n=N, seed=42):
    """Shared latent factor couples both blocks."""
    np.random.seed(seed)
    L = np.random.multivariate_normal([0, 0], [[1, 0.3], [0.3, 1]], size=n)
    eps1 = np.random.normal(0, 1, (n, 2))
    eps2 = np.random.normal(0, 1, (n, 2))

    samples = np.zeros((n, 4))
    samples[:, 0] = 0.77 * L[:, 0] + np.sqrt(1 - 0.77**2) * eps1[:, 0]
    samples[:, 1] = 0.77 * L[:, 0] + np.sqrt(1 - 0.77**2) * eps1[:, 1]
    samples[:, 2] = 0.63 * L[:, 1] + np.sqrt(1 - 0.63**2) * eps2[:, 0]
    samples[:, 3] = 0.63 * L[:, 1] + np.sqrt(1 - 0.63**2) * eps2[:, 1]
    return samples

dists = {
    'Multivariate\nNormal': make_gaussian,
    'Latent\nMixture': make_mixture,
    'Independent\nBlocks': make_blocks,
    'Latent\nFactor': make_factor,
}

samples_list = {k: v(seed=42) for k, v in dists.items()}

def pairwise_corr(samples):
    return np.corrcoef(samples.T)

corr_list = {k: pairwise_corr(v) for k, v in samples_list.items()}

# Compute 3-way interaction
def compute_3way(samples):
    x1, x2, x3 = samples[:, 0], samples[:, 1], samples[:, 2]
    r12 = np.corrcoef(x1, x2)[0, 1]
    r13 = np.corrcoef(x1, x3)[0, 1]
    r23 = np.corrcoef(x2, x3)[0, 1]

    r12_3 = (r12 - r13 * r23) / np.sqrt((1 - r13**2) * (1 - r23**2) + 1e-10)
    r12_3 = np.clip(r12_3, -0.999, 0.999)

    def gmi(r):
        return -0.5 * np.log(1 - r**2)

    return gmi(r12) - gmi(r12_3)

ii_list = {k: compute_3way(v) for k, v in samples_list.items()}

# ---- Visualization ----
fig = plt.figure(figsize=(15, 12), facecolor='#0a0a0c')

from matplotlib.gridspec import GridSpec
gs = GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.2,
              height_ratios=[1, 1, 0.15])

keys = list(dists.keys())
colors = ['#e8749a', '#9a6ad4', '#4a8aaa', '#d4a574']

# Row 0: pairwise correlation heatmaps
for row_idx, (key, color) in enumerate(zip(keys, colors)):
    col = row_idx
    corr = corr_list[key]
    ax = fig.add_subplot(gs[0, col])
    ax.set_facecolor('#0a0a0c')

    im = ax.imshow(corr, cmap='RdPu', vmin=-0.1, vmax=1.0, aspect='auto')
    ax.set_title(key, fontsize=13, color=color, fontweight='bold', pad=10)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xticklabels(['x₁', 'x₂', 'x₃', 'x₄'], fontsize=9, color='#888')
    ax.set_yticklabels(['x₁', 'x₂', 'x₃', 'x₄'], fontsize=9, color='#888')

    for i in range(4):
        for j in range(4):
            val = corr[i, j]
            text_color = '#fff' if abs(val) > 0.3 else '#aaa'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                   fontsize=9, color=text_color, fontweight='bold' if abs(val) > 0.3 else 'normal')

# Row 1: dependency graphs
for row_idx, (key, color) in enumerate(zip(keys, colors)):
    col = row_idx
    samples = samples_list[key]
    corr = corr_list[key]
    ax = fig.add_subplot(gs[1, col])
    ax.set_facecolor('#0a0a0c')

    # Draw nodes
    positions = [(0.2, 0.7), (0.8, 0.7), (0.2, 0.2), (0.8, 0.2)]
    for j in range(4):
        x, y = positions[j]
        ax.plot(x, y, 'o', color='#4a8a8a', markersize=16)
        ax.text(x, y + 0.06, f'x{j+1}', fontsize=9, color='#888', ha='center')

    # Draw edges
    for j in range(4):
        for k in range(j+1, 4):
            if abs(corr[j, k]) > 0.1:
                x1, y1 = positions[j]
                x2, y2 = positions[k]
                line_color = color if abs(corr[j, k]) > 0.3 else '#6a6a8a'
                linewidth = 1 + abs(corr[j, k]) * 4
                ax.plot([x1, x2], [y1, y2], '-', color=line_color,
                       linewidth=linewidth, alpha=0.6)

    # Add I₃ value
    ii = ii_list[key]
    ii_color = '#6aaa6a' if ii > 0.01 else '#aa6a6a' if ii < -0.01 else '#6a8a6a'
    ax.text(0.5, -0.05, f'I₃ = {ii:+.3f}', ha='center', va='top',
           fontsize=10, color=ii_color, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Row 2: caption
summary_ax = fig.add_subplot(gs[2, :])
summary_ax.set_facecolor('#0a0a0c')
summary_ax.axis('off')
summary_ax.text(0.5, 0.5,
    'Four distributions. Same local correlations. Different global structure.',
    fontsize=12, color='#aaa', ha='center', va='center',
    family='monospace')

fig.suptitle('Same local. Different global.',
             fontsize=20, color='#d4a574', fontweight='bold', y=0.97)

plt.savefig('./assets/local-global-info-0.webp', dpi=150, bbox_inches='tight',
           facecolor='#0a0a0c')
print(f'Saved to ./assets/local-global-info-0.webp')

for key in keys:
    print(f'\n{key}:')
    for row in corr_list[key]:
        print('  ' + '  '.join(f'{v:7.3f}' for v in row))
    print(f'  I₃ = {ii_list[key]:+.3f}')
