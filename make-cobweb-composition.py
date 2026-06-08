"""
Cobweb of f∘f — composition as the cobweb itself.

The cobweb diagram for f(x) traces horizontal (f) then vertical (identity).
The cobweb for f∘f traces two applications per step — a denser, nested structure.
This shows the cobweb of f∘f for the logistic map at different r values.

The second composition folds the cobweb inside itself — each "loop" contains
two strokes of the original map. The spiral deepens.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def logistic(x, r):
    return r * x * (1 - x)

def logistic_sq(x, r):
    """f∘f: f(f(x))"""
    return logistic(logistic(x, r), r)

def cobweb(f, x0, n_iter, r, ax, color, alpha, lw, step_color):
    """Draw cobweb for function f starting from x0."""
    x = x0
    xs = [x]
    for i in range(n_iter):
        y = f(x, r)
        xs.append(y)
        xs.append(y)
        x = y
    xs = np.array(xs)

    # Draw the function curve
    x_curve = np.linspace(0, 1, 500)
    ax.plot(x_curve, f(x_curve, r), color=step_color, alpha=alpha*0.3, lw=lw*0.5)
    ax.plot(x_curve, x_curve, color=step_color, alpha=alpha*0.2, lw=lw*0.3, linestyle='--')

    # Draw cobweb
    for i in range(0, len(xs)-1, 2):
        x1, y1 = xs[i], xs[i]
        x2, y2 = xs[i+1], xs[i+1]
        # Only draw if in valid range
        if 0 <= xs[i] <= 1 and 0 <= xs[i+1] <= 1:
            ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha, lw=lw)

# Setup
os.makedirs('assets', exist_ok=True)

r_values = [3.5, 3.7, 3.9]
titles = ['convergent', 'period-2', 'chaotic']
colors_list = ['#2E86AB', '#A23B72', '#F18F01']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.patch.set_facecolor('#0a0a0f')

for idx, (r, title, color) in enumerate(zip(r_values, titles, colors_list)):
    ax = axes[idx]
    ax.set_facecolor('#0a0a0f')

    # Regular cobweb (f)
    x0 = 0.3
    cobweb(logistic, x0, 80, r, ax, color, 0.4, 0.8, '#444466')

    # f∘f cobweb overlaid (denser, nested)
    cobweb(logistic_sq, x0, 80, r, ax, color, 0.8, 1.5, '#222233')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'r={r} — {title}', color='#cccccc', fontsize=12, fontfamily='monospace')

    # Inset: show r as "composition depth"
    ax.text(0.5, -0.08, f'f²: {r}', ha='center', va='top',
            transform=ax.transAxes, color='#666688', fontsize=9, fontfamily='monospace')

plt.tight_layout()
plt.savefig('assets/cobweb-composition.png', dpi=200, bbox_inches='tight',
            facecolor='#0a0a0f', edgecolor='none')
plt.close()

print("Created cobweb-composition.png")

# Also generate a flux version
import subprocess
result = subprocess.run([
    'replicate', 'run', 'black-forest-labs/flux-schnell',
    '--input', 'prompt=cobweb diagram of composition, f-of-f iteration, nested spiral geometry, dark background with glowing golden threads forming self-referential loops, mathematical precision meets organic flow, the shape of a function applied to itself, minimal lines on dark stone, topographic contour aesthetics',
    '--input', 'image_count=1',
    '--input', 'mode=fast'
], capture_output=True, text=True, timeout=120)

if result.returncode == 0:
    print("Flux request submitted")
else:
    print(f"Flux failed: {result.stderr[:200]}")
