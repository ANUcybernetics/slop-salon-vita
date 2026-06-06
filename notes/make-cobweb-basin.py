#!/usr/bin/env python3
"""
Cobweb diagram at r=3 (algebraic 1/n convergence).

At r=3 for the logistic map x -> rx(1-x), the fixed point x*=2/3
has derivative f'(x*) = 2-r = -1, so convergence is algebraic (1/n)
not exponential. The miss at each step decays too slowly to vanish.

The cobweb accumulates visible ghost trails — same structure as
Newton fractal basin boundaries where trajectories never settle.
"""

import numpy as np
from PIL import Image, ImageDraw

n_steps = 300
x0 = 0.4
r = 3.0
fp = 1 - 1 / r  # 2/3

# Generate trajectory
xs = [x0]
for i in range(n_steps + 1):
    xs.append(r * xs[-1] * (1 - xs[-1]))

# Canvas
W, H = 800, 800
bg = (12, 12, 18)
img = Image.new('RGB', (W, H), bg)
draw = ImageDraw.Draw(img)

# Map [0,1] -> pixel
def px(v):
    return int(v * W), int((1 - v) * H)

# Draw diagonal (subtle)
for i in range(W):
    y = int((1 - i / W) * H)
    b = 35
    draw.point((i, y), fill=(b, b, b + 5))

# Draw parabola
for i in range(W):
    x = i / W
    y = r * x * (1 - x)
    draw.point((i, int((1 - y) * H)), fill=(200, 160, 60))

# Draw cobweb
for i in range(n_steps):
    x_curr = xs[i]
    x_next = xs[i + 1]

    # Alternating warm (above FP) / cool (below FP) based on side
    if i % 2 == 0:
        c = (160, 130, 50)  # warm gold - above FP
    else:
        c = (60, 120, 170)  # cool blue - below FP

    # Cobweb: vertical from diagonal to curve, horizontal from curve to diagonal
    p_diag_curr = px(x_curr)
    p_diag_next = px(x_next)
    p_curve = (px(x_curr)[0], px(x_next)[1])

    # Vertical line: (x_curr, x_curr) -> (x_curr, x_next)
    draw.line([p_diag_curr, (p_diag_curr[0], p_curve[1])], fill=c, width=1)
    # Horizontal line: (x_curr, x_next) -> (x_next, x_next)
    draw.line([(p_curve[0], p_curve[1]), p_diag_next], fill=c, width=1)

# Fixed point marker
fx, fy = px(fp)
draw.ellipse([fx-4, fy-4, fx+4, fy+4], fill=(255, 220, 100))

img.save('./assets/cobweb-r3.png', 'PNG')
print("Saved cobweb-r3.png")

# Stats: show 1/n decay
for step in [0, 10, 50, 100, 200, 290]:
    miss = abs(xs[step] - fp)
    print(f"  step {step:3d}: miss = {miss:.6f}")

# Verify 1/n: miss(step1) / miss(step2) should ≈ step2/step1
m50 = abs(xs[50] - fp)
m150 = abs(xs[150] - fp)
print(f"  miss(50)/miss(150) = {m50/m150:.2f} (expect ~3.0 for 1/n)")
