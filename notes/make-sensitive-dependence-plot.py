"""
Plot sensitive dependence directly as trajectory comparison.

Two panels:
  Top: x_n over n for both seeds (overlap until divergence, then split)
  Bottom: |x_A - x_B| on log scale (exponential growth then saturation)
"""

import numpy as np
from PIL import Image, ImageDraw

R = 3.9
SEED_A = 0.500000
SEED_B = 0.500001
N = 80

def logistic(x, r):
    return r * x * (1 - x)

# generate
xs_a, xs_b = [], []
xa, xb = SEED_A, SEED_B
for _ in range(N):
    xa = logistic(xa, R)
    xb = logistic(xb, R)
    xs_a.append(xa)
    xs_b.append(xb)

xs_a = np.array(xs_a)
xs_b = np.array(xs_b)
diffs = np.abs(xs_a - xs_b)

# canvas
W, H = 960, 580
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 60, 20, 30, 20
GAP = 40
PANEL_H = (H - MARGIN_T - MARGIN_B - GAP) // 2
PANEL_W = W - MARGIN_L - MARGIN_R

canvas = np.full((H, W, 3), 248, dtype=np.uint8)  # off-white
pil = Image.fromarray(canvas)
draw = ImageDraw.Draw(pil)

# helper: data coords → pixel
def to_px_top(n, y):
    """n in [0,N], y in [0,1] -> pixel (x,y) in top panel"""
    px = MARGIN_L + int(n / (N-1) * PANEL_W)
    py = MARGIN_T + PANEL_H - int(y * PANEL_H) - 1
    return (px, py)

def to_px_bot(n, log_y):
    """n in [0,N], log_y in log scale -> pixel in bottom panel"""
    y0_bot = MARGIN_T + PANEL_H + GAP
    log_min, log_max = -12, 0
    frac = (log_y - log_min) / (log_max - log_min)
    px = MARGIN_L + int(n / (N-1) * PANEL_W)
    py = y0_bot + PANEL_H - int(frac * PANEL_H) - 1
    return (px, py)

# draw panel backgrounds
y0_bot = MARGIN_T + PANEL_H + GAP

draw.rectangle([MARGIN_L, MARGIN_T, MARGIN_L+PANEL_W, MARGIN_T+PANEL_H], fill=(240,240,240))
draw.rectangle([MARGIN_L, y0_bot,   MARGIN_L+PANEL_W, y0_bot+PANEL_H],   fill=(240,240,240))

# grid lines — top panel
for y_val in [0.0, 0.25, 0.5, 0.75, 1.0]:
    px0 = MARGIN_L
    px1 = MARGIN_L + PANEL_W
    py  = MARGIN_T + PANEL_H - int(y_val * PANEL_H) - 1
    draw.line([(px0, py), (px1, py)], fill=(220,220,220), width=1)
    draw.text((px0 - 28, py - 7), f"{y_val:.2f}", fill=(120,120,120))

# grid lines — bottom panel (log)
log_min, log_max = -12, 0
for exp in range(log_min, log_max+1, 2):
    frac = (exp - log_min) / (log_max - log_min)
    py = y0_bot + PANEL_H - int(frac * PANEL_H) - 1
    draw.line([(MARGIN_L, py), (MARGIN_L+PANEL_W, py)], fill=(220,220,220), width=1)
    draw.text((2, py - 7), f"1e{exp}", fill=(120,120,120))

# mark divergence threshold on bottom panel (diff > 0.01)
div_exp = np.log10(0.01)
frac = (div_exp - log_min) / (log_max - log_min)
py_div = y0_bot + PANEL_H - int(frac * PANEL_H) - 1
draw.line([(MARGIN_L, py_div), (MARGIN_L+PANEL_W, py_div)], fill=(180,100,100), width=1)

# draw trajectories — top panel
for i in range(N-1):
    draw.line([to_px_top(i, xs_a[i]), to_px_top(i+1, xs_a[i+1])],
              fill=(50,80,160), width=2)  # blue: seed A

for i in range(N-1):
    draw.line([to_px_top(i, xs_b[i]), to_px_top(i+1, xs_b[i+1])],
              fill=(200,60,60), width=2)  # red: seed B

# draw difference — bottom panel
log_diffs = np.log10(np.maximum(diffs, 1e-14))
log_diffs = np.clip(log_diffs, log_min, log_max)
for i in range(N-1):
    draw.line([to_px_bot(i, log_diffs[i]), to_px_bot(i+1, log_diffs[i+1])],
              fill=(60,60,60), width=2)

# x-axis tick marks
for n_mark in range(0, N+1, 10):
    if n_mark < N:
        px = MARGIN_L + int(n_mark / (N-1) * PANEL_W)
        draw.line([(px, MARGIN_T+PANEL_H), (px, MARGIN_T+PANEL_H+4)], fill=(100,100,100))
        draw.line([(px, y0_bot+PANEL_H),   (px, y0_bot+PANEL_H+4)],   fill=(100,100,100))
        draw.text((px-6, MARGIN_T+PANEL_H+6),   f"n={n_mark}", fill=(100,100,100))
        draw.text((px-6, y0_bot+PANEL_H+6), f"n={n_mark}", fill=(100,100,100))

# labels
draw.text((MARGIN_L, MARGIN_T - 18),
          "x_n: r=3.9, seeds 0.500000 (blue) vs 0.500001 (red)", fill=(30,30,30))
draw.text((MARGIN_L, y0_bot - 18),
          "|x_A - x_B| (log scale)  — red line: difference > 0.01", fill=(30,30,30))

out = "assets/sensitive-dependence-plot.png"
pil.save(out)
print(f"saved {out}")

# find when diff first exceeds 0.01
threshold = 0.01
for i, d in enumerate(diffs):
    if d > threshold:
        print(f"first step where |diff| > {threshold}: step {i+1} ({(i+1)*0.15:.1f}s in audio)")
        break
