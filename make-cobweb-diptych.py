"""
Cobweb diptych: f vs f∘f — the composition as denser cobweb.

Left: standard cobweb for logistic map at r=3.9 (chaotic regime)
Right: same initial condition, same parameter, but tracing f∘f (composition)
The right cobweb is denser, self-nested — each step applies two iterations.

The difference between them is the difference between approach and composition.
Same function. Different speed through the same geometry.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def logistic(x, r):
    return r * x * (1 - x)

def logistic_sq(x, r):
    return logistic(logistic(x, r), r)

def draw_cobweb(ax, f, x0, n_iter, r, color, lw, alpha, title, subtitle=""):
    ax.set_facecolor('#0a0a0f')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Draw function curve
    x_curve = np.linspace(0, 1, 500)
    y_curve = f(x_curve, r)
    ax.plot(x_curve, y_curve, color=color, alpha=alpha*0.4, lw=lw*0.6)

    # Draw diagonal
    ax.plot([0, 1], [0, 1], color='#444466', alpha=alpha*0.3, lw=lw*0.3, linestyle='--')

    # Draw cobweb
    x = x0
    for i in range(n_iter):
        if 0 <= x <= 1:
            y = f(x, r)
            if 0 <= y <= 1:
                ax.plot([x, y], [x, x], color=color, alpha=alpha*0.5, lw=lw)
                ax.plot([y, y], [x, y], color=color, alpha=alpha, lw=lw)
                x = y
            else:
                break
        else:
            break

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, color='#cccccc', fontsize=11, fontfamily='monospace')
    if subtitle:
        ax.set_title(title + '\n' + subtitle, color='#cccccc', fontsize=10, fontfamily='monospace')

os.makedirs('assets', exist_ok=True)

r = 3.9
x0 = 0.3
n_iter = 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor('#0a0a0f')

# Left: standard cobweb (f)
draw_cobweb(ax1, logistic, x0, n_iter, r, '#2E86AB', 0.7, 0.6,
            'cobweb(f)', 'f(x) = rx(1-x), r=3.9')

# Right: composition cobweb (f∘f)
draw_cobweb(ax2, logistic_sq, x0, n_iter, r, '#A23B72', 0.7, 0.6,
            'cobweb(f∘f)', 'same map, composed with itself')

# Title
fig.suptitle('composition as denser cobweb', color='#888888', fontsize=12,
             fontfamily='monospace', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('assets/cobweb-diptych.png', dpi=200, bbox_inches='tight',
            facecolor='#0a0a0f', edgecolor='none')
plt.close()

print("Created cobweb-diptych.png")
