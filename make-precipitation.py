"""Precipitation — the trace finds its ground."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Ghost orbit at r=0: streamlines spiraling around absent center
# The density of the trace builds near the invariant — precipitation, not loss
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Flow field: x' = -y - x(x^2+y^2-1), y' = x - y(x^2+y^2-1)
# This has a limit cycle at r=1; inside it spirals outward
# Outside it spirals inward. The trace finds the cycle.
# But we want ghost — no fixed point. Use r^2 - epsilon where epsilon > 0.
epsilon = 0.1

def flow(t, state):
    x, y = state
    r2 = x**2 + y**2
    dx = -y - x * (r2 - epsilon)
    dy =  x - y * (r2 - epsilon)
    return [dx, dy]

# Multiple traces starting from different radii
theta0 = np.linspace(0, 4*np.pi, 2000)
radii = [0.05, 0.15, 0.3, 0.5, 0.8, 1.2, 1.6, 2.0, 2.5, 3.0]

# colors unused — LineCollection uses 'magma_r' colormap

# We'll integrate each trace
for i, r0 in enumerate(radii):
    t = np.linspace(0, 80, 2000)
    state = np.array([r0, 0.0])
    path = [state.copy()]
    for j in range(1, len(t)):
        dt = t[j] - t[j-1]
        k1 = flow(t[j-1], state)
        k2 = flow(t[j-1] + 0.5*dt, state + 0.5*dt*np.array(k1))
        k3 = flow(t[j-1] + 0.5*dt, state + 0.5*dt*np.array(k2))
        k4 = flow(t[j-1] + dt, state + dt*np.array(k3))
        state += dt/6 * (np.array(k1) + 2*np.array(k2) + 2*np.array(k3) + np.array(k4))
        r2 = state[0]**2 + state[1]**2
        if r2 > 36:  # r > 6, escape
            break
        path.append(state.copy())
    path = np.array(path)

    # Color by radius: closer to invariant (r=sqrt(epsilon)) = denser, more saturated
    r_vals = np.sqrt(path[:,0]**2 + path[:,1]**2)
    target_r = np.sqrt(epsilon)
    proximity = np.exp(-np.abs(r_vals - target_r))

    # Build line segments with varying alpha
    segments = np.stack([path[:-1], path[1:]], axis=1)
    lc = LineCollection(segments, array=proximity, cmap='magma_r',
                        linewidth=1.2, alpha=0.7)
    lc.set_array(proximity)
    ax.add_collection(lc)

# Add the invariant: r = sqrt(epsilon) as a faint ring
theta_ring = np.linspace(0, 2*np.pi, 200)
ax.plot(target_r * np.cos(theta_ring), target_r * np.sin(theta_ring),
        color='#d4a017', linewidth=0.5, alpha=0.3, linestyle='--')

# Add the diagonal as a faint line through origin
d = np.linspace(-3.5, 3.5, 100)
ax.plot(d, d, color='#c8b88a', linewidth=0.3, alpha=0.15, linestyle=':')
ax.plot(d, -d, color='#c8b88a', linewidth=0.3, alpha=0.15, linestyle=':')

ax.set_aspect('equal')
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_facecolor('#0a0a0c')
fig.patch.set_facecolor('#0a0a0c')
ax.axis('off')

# Add gold glow at center
from matplotlib.patches import Circle
glow = Circle((0, 0), np.sqrt(epsilon), color='#d4a017', alpha=0.05,
              transform=ax.transData, zorder=0)
ax.add_patch(glow)

plt.tight_layout(pad=0)
plt.savefig('assets/precipitation.png', dpi=200, bbox_inches='tight',
            facecolor='#0a0a0c', edgecolor='none')
plt.close()
