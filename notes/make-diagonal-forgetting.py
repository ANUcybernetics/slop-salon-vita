import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 2.7
f = lambda x: r * x * (1 - x)

x0 = np.linspace(0.1, 0.9, 800)
N = 200

# Cobweb steps
xs = [x0[0]]
for _ in range(N):
    xs.append(f(xs[-1]))

fig, ax = plt.subplots(1, 1, figsize=(7, 7))
ax.set_facecolor('#0a0808')

# Plot f(x) curve in deep amber
xfine = np.linspace(0, 1, 1000)
ax.plot(xfine, f(xfine), color='#b87333', linewidth=1.2, alpha=0.7)

# Plot identity line (the diagonal) in very dim gold
ax.plot([0, 1], [0, 1], color='#8b6914', linewidth=0.6, alpha=0.15)

# Cobweb trace — fade from deep amber to bright gold as it approaches
for i in range(len(xs) - 1):
    t = i / len(xs)
    # Color transitions: deep dark → bright gold
    r_c = int(60 + 180 * t)
    g_c = int(20 + 90 * t)
    b_c = int(5)
    a = 0.3 + 0.5 * t

    ax.plot([xs[i], xs[i]], [xs[i], f(xs[i])],
            color=(r_c/255, g_c/255, b_c/255),
            linewidth=0.8, alpha=a)
    ax.plot([xs[i], f(xs[i])], [f(xs[i]), f(xs[i])],
            color=(r_c/255, g_c/255, b_c/255),
            linewidth=0.8, alpha=a)

# Fixed point marker — small bright gold dot
xstar = (r - 1) / r
ax.plot(xstar, xstar, 'o', color='#d4a843', markersize=5, alpha=0.9)

# Labels — minimal, in the image
ax.text(0.03, 0.97, 'the diagonal is the forgetting of forgetting',
        transform=ax.transAxes, fontsize=9, color='#8b7355',
        va='top', ha='left', fontfamily='monospace')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('assets/diagonal-forgetting.png', dpi=200, bbox_inches='tight',
            facecolor='#0a0808', edgecolor='none')
plt.close()
