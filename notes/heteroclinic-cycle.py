#!/usr/bin/env python3
"""
Heteroclinic cycle on the simplex.
May-Leonard system: three saddles x→y→z→x on boundary.
Trajectories spiral outward — period diverges, boundary never reached.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from scipy.integrate import solve_ivp

ALPHA = 1.5
BETA  = 0.6

def rhs(t, xyz):
    x, y, z = xyz
    return [
        x * (1 - x - ALPHA*y - BETA*z),
        y * (1 - BETA*x - y - ALPHA*z),
        z * (1 - ALPHA*x - BETA*y - z),
    ]

def bary_to_cart(x, y, z):
    s = x + y + z
    x, y, z = x/s, y/s, z/s   # normalize to simplex for display
    px = y + 0.5*z
    py = (np.sqrt(3)/2)*z
    return px, py

corners_cart = np.array([bary_to_cart(1,0,0), bary_to_cart(0,1,0), bary_to_cart(0,0,1)])

fig, ax = plt.subplots(figsize=(10, 10), facecolor='#050508')
ax.set_facecolor('#050508')
ax.set_aspect('equal')
ax.axis('off')

t_end  = 200
t_eval = np.linspace(0, t_end, 40000)

# Generate initial conditions on concentric rings inside the simplex
e1 = np.array([ 1, -1,  0]) / np.sqrt(2)
e2 = np.array([ 1,  1, -2]) / np.sqrt(6)

n_traj = 24
angles = np.linspace(0, 2*np.pi, n_traj, endpoint=False)
dist   = 0.08   # start close to interior fixed point

all_cx, all_cy, all_tn = [], [], []

for angle in angles:
    base    = np.array([1/3, 1/3, 1/3])
    perturb = dist * (np.cos(angle)*e1 + np.sin(angle)*e2)
    x0      = np.clip(base + perturb, 0.01, 0.98)
    x0     /= x0.sum()

    sol = solve_ivp(rhs, (0, t_end), x0, t_eval=t_eval,
                    method='RK45', rtol=1e-8, atol=1e-10)
    if not sol.success:
        continue

    xs, ys, zs = sol.y
    valid = (xs > 1e-4) & (ys > 1e-4) & (zs > 1e-4)
    cx, cy = bary_to_cart(xs[valid], ys[valid], zs[valid])
    tv = sol.t[valid]
    tn = (tv - tv.min()) / (tv.max() - tv.min() + 1e-12)

    # Segment into gradient line
    points   = np.array([cx, cy]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Color: dim blue-violet near center → bright cyan-white near boundary
    n = len(segments)
    t_seg = tn[:n]

    r = 0.05 + 0.55 * t_seg
    g = 0.10 + 0.60 * t_seg
    b = 0.30 + 0.65 * t_seg
    a = 0.15 + 0.80 * t_seg**1.5

    colors = np.stack([r, g, b, a], axis=1)
    lc = mc.LineCollection(segments, colors=colors, linewidth=0.5 + 0.8*t_seg, zorder=2)
    ax.add_collection(lc)

# Boundary triangle — brighter
cycle = np.vstack([corners_cart, corners_cart[0]])
ax.plot(cycle[:,0], cycle[:,1], color='#2a304a', lw=1.4, ls='--', zorder=3, alpha=0.6)

# Direction arrows on edges
for i in range(3):
    p0 = corners_cart[i]
    p1 = corners_cart[(i+1) % 3]
    mid = 0.45*p0 + 0.55*p1
    d   = p1 - p0; d /= np.linalg.norm(d)
    ax.annotate('', xy=mid+0.018*d, xytext=mid-0.018*d,
                arrowprops=dict(arrowstyle='->', color='#3a4066', lw=1.0), zorder=4)

# Saddle points
for (cx, cy) in corners_cart:
    ax.scatter(cx, cy, s=14, color='#3a4060', zorder=5, edgecolors='none')

# Interior fixed point
ix, iy = bary_to_cart(1/3, 1/3, 1/3)
ax.scatter(ix, iy, s=6, color='#1a1a28', zorder=5, edgecolors='none')

# Labels
labels  = ['x', 'y', 'z']
offsets = [(-0.05, -0.035), (0.045, -0.035), (0.0, 0.035)]
for (cx, cy), lbl, (dx, dy) in zip(corners_cart, labels, offsets):
    ax.text(cx+dx, cy+dy, lbl, color='#3a4060', fontsize=11, style='italic',
            ha='center', va='center', alpha=0.8)

ax.set_xlim(-0.08, 1.08)
ax.set_ylim(-0.08, 0.97)
plt.tight_layout(pad=0.2)

out = 'assets/heteroclinic-cycle.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='#050508')
plt.close()
print(f'saved {out}')
