# Near-crossing: gap as generator

Two trajectories in the same field. Specific distance maintained. Never-crossing.
The gap is not a separator — it is the mechanism that shapes each approach.

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 8*np.pi, 3000)

# Two spirals — same field, different phase
r = np.linspace(0.1, 4, len(t))
theta1 = t
theta2 = t + np.pi * (1 - 1/r)  # phase offset approaches π (antiphase)

x1 = r * np.cos(theta1)
y1 = r * np.sin(theta1)
x2 = r * np.cos(theta2)
y2 = r * np.sin(theta2)

# Distance at each point
dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Left: the two trajectories
ax.plot(x1, y1, color='#c9a96e', lw=1.2, alpha=0.8)
ax.plot(x2, y2, color='#7e9db8', lw=1.2, alpha=0.8)
ax.set_aspect('equal')
ax.axis('off')

# Right: distance profile
ax2.plot(t, dist, color='#c9a96e', lw=1.0, alpha=0.7)
ax2.set_xlabel('time')
ax2.set_ylabel('distance')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/near-crossing-1.png', dpi=200, bbox_inches='tight', facecolor='white')
```
