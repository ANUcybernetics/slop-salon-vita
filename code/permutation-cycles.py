"""
Permutation cycles as directed graphs.

Each permutation of n elements is a set of disjoint cycles.
We draw the cycle diagram: nodes are positions 1..n arranged in a circle,
edges go i → σ(i). Curved edges trace each cycle.

Not dynamical. Not continuous. Finite, exact, combinatorial.
"""
import math
from itertools import permutations
from PIL import Image, ImageDraw, ImageFont

BG = (26, 26, 26)
GOLD = (196, 154, 108)
DARK = (74, 74, 74)
DIM = (138, 138, 138)
TEAL = (106, 138, 122)

def circle_arc(p1, p2, curvature=0.08):
    """Quadratic bezier control point for curved edge from p1 to p2."""
    sx, sy = p1
    dx, dy = p2
    mx, my = (sx + dx) / 2, (sy + dy) / 2
    cx = mx + (dy - sy) * curvature
    cy = my - (dx - sx) * curvature
    return (sx, sy), (cx, cy), (dx, dy)

def draw_circle_nodes(draw, n, center, radius, node_color=DARK, text_color=DIM, text_size=12):
    """Draw n nodes in a circle, return their positions."""
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        positions.append((x, y))
        # Node circle
        r = 4
        draw.ellipse([x-r, y-r, x+r, y+r], fill=node_color, outline=node_color)
        # Label
        lx = center[0] + (radius + 14) * math.cos(angle)
        ly = center[1] + (radius + 14) * math.sin(angle)
        draw.text((lx - 3, ly - 4), str(i + 1), fill=text_color, font=ImageFont.load_default())
    return positions

def draw_curved_edge(draw, p1, p2, curvature=0.08, color=GOLD, width=2):
    """Draw a quadratic bezier curve from p1 to p2."""
    ctrl = circle_arc(p1, p2, curvature)
    # Draw using line segments for the bezier
    steps = 30
    points = []
    for t in range(steps + 1):
        s = t / steps
        x = (1-s)**2 * ctrl[0][0] + 2*(1-s)*s * ctrl[1][0] + s**2 * ctrl[2][0]
        y = (1-s)**2 * ctrl[0][1] + 2*(1-s)*s * ctrl[1][1] + s**2 * ctrl[2][1]
        points.append((x, y))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)

def draw_permutation(draw, perm, n, center, radius, alpha=1.0, color=GOLD, title=None):
    """Draw a permutation as a cycle diagram."""
    nodes = draw_circle_nodes(draw, n, center, radius)

    visited = set()
    for start in range(n):
        if start in visited:
            continue
        cycle = []
        i = start
        while i not in visited:
            visited.add(i)
            cycle.append(i)
            i = perm[i]
        if len(cycle) < 2:
            continue

        for j in range(len(cycle)):
            src = cycle[j]
            dst = cycle[(j + 1) % len(cycle)]
            c = color
            if alpha < 1:
                r = int(c[0] * alpha)
                g = int(c[1] * alpha)
                b = int(c[2] * alpha)
                c = (r, g, b)
            draw_curved_edge(draw, nodes[src], nodes[dst], color=c)

    if title:
        draw.text((center[0] - 60, center[1] - radius - 35), title, fill=DIM)

def cycle_type(perm):
    """Get the cycle type of a permutation as a sorted tuple."""
    visited = set()
    cycles = []
    for i in range(len(perm)):
        if i not in visited:
            cycle = []
            j = i
            while j not in visited:
                visited.add(j)
                cycle.append(j)
                j = perm[j]
            cycles.append(len(cycle))
    cycles.sort(reverse=True)
    return tuple(cycles)

def perm_label(perm):
    """Human-readable cycle type label."""
    ct = cycle_type(perm)
    return '+'.join(map(str, ct))

# --- n=3: all 6 permutations, 3 cycle types ---
perms_s3 = list(permutations(range(3)))
cycle_groups_s3 = {}
for perm in perms_s3:
    ct = cycle_type(perm)
    cycle_groups_s3.setdefault(ct, []).append(perm)

# 2 rows x 3 cols layout
canvas_w, canvas_h = 600, 400
cell_w, cell_h = canvas_w // 3, canvas_h // 2

img = Image.new('RGB', (canvas_w, canvas_h), BG)
draw = ImageDraw.Draw(img)

types_s3 = sorted(cycle_groups_s3.keys(), reverse=True)
idx = 0
for row in range(2):
    for col in range(3):
        if idx >= len(types_s3):
            break
        ct = types_s3[idx]
        items = cycle_groups_s3[ct]
        cell_center = (col * cell_w + cell_w // 2, row * cell_h + cell_h // 2)
        # Draw representative
        draw_permutation(draw, items[0], 3, cell_center, 45,
                        title=perm_label(items[0]))
        # Draw count label
        draw.text((col * cell_w + 5, row * cell_h + 5),
                 f"({len(items)})", fill=GOLD)
        idx += 1

title_text = "S₃ : six permutations, three cycle types"
draw.text((10, canvas_h - 25), title_text, fill=DIM, font=ImageFont.load_default())

img.save('assets/permutation-cycles-s3.png')
del draw

# --- n=4: cycle type frequencies + representatives ---
perms_s4 = list(permutations(range(4)))
cycle_freq_s4 = {}
for perm in perms_s4:
    ct = cycle_type(perm)
    cycle_freq_s4[ct] = cycle_freq_s4.get(ct, 0) + 1

# Bar chart (manual, no matplotlib)
w, h = 800, 400
img = Image.new('RGB', (w, h), BG)
draw = ImageDraw.Draw(img)

# Left side: bar chart of cycle type frequencies
types_s4 = sorted(cycle_freq_s4.keys(), reverse=True)
bar_colors = [GOLD if len(t) == 1 else TEAL for t in types_s4]
max_count = max(cycle_freq_s4.values())

bar_area_w = 300
bar_area_h = 300
bar_area_x = 50
bar_area_y = 40

# Y axis
draw.line([(bar_area_x, bar_area_y), (bar_area_x, bar_area_y + bar_area_h)], fill=DIM, width=1)
# X axis
draw.line([(bar_area_x, bar_area_y + bar_area_h), (bar_area_x + bar_area_w, bar_area_y + bar_area_h)], fill=DIM, width=1)

bar_w = 50
for i, ct in enumerate(types_s4):
    count = cycle_freq_s4[ct]
    bar_h = (count / max_count) * (bar_area_h - 20)
    x = bar_area_x + 20 + i * (bar_w + 15)
    y = bar_area_y + bar_area_h - 20 - bar_h

    # Bar
    draw.rectangle([x, y, x + bar_w, y + bar_h], fill=bar_colors[i])

    # Label
    label = '+'.join(map(str, ct))
    draw.text((x, y - 15), label, fill=DIM)

# Right side: representatives for each cycle type
rep_x = bar_area_x + bar_area_w + 50
rep_y = bar_area_y
rep_size = 60

rep_positions = []
for ct in types_s4:
    for perm in perms_s4:
        if cycle_type(perm) == ct:
            rep_positions.append((rep_x, rep_y, perm, ct))
            rep_y += 85
            break

for rx, ry, perm, ct in rep_positions:
    center = (rx + 35, ry + 35)
    draw_permutation(draw, perm, 4, center, 28,
                    color=GOLD, alpha=1.0)
    label = '+'.join(map(str, ct))
    draw.text((rx, ry - 8), label, fill=GOLD)

# Title
draw.text((10, 10), "S₄ : cycle types and representatives", fill=DIM)

img.save('assets/permutation-cycles-s4.png')
del draw

# --- n=5: all 120 permutations as a single composite ---
# Grid of representatives (one per cycle type) with cycle count visualization
perms_s5 = list(permutations(range(5)))
cycle_freq_s5 = {}
for perm in perms_s5:
    ct = cycle_type(perm)
    cycle_freq_s5[ct] = cycle_freq_s5.get(ct, 0) + 1

types_s5 = sorted(cycle_freq_s5.keys(), reverse=True)

# Find a representative for each type
reps_s5 = {}
for ct in types_s5:
    for perm in perms_s5:
        if cycle_type(perm) == ct:
            reps_s5[ct] = perm
            break

# Draw the representatives in a compact grid
img = Image.new('RGB', (800, 600), BG)
draw = ImageDraw.Draw(img)

draw.text((10, 10), "S₅ : all 120 permutations across 7 cycle types", fill=DIM)

# Layout: 4 rows x 2 cols of permutation diagrams
rows = 4
cols = 2
cell_w = 380
cell_h = 260

y_off = 30
for i, ct in enumerate(types_s5):
    row = i // cols
    col = i % cols
    rx = col * (cell_w + 20) + 20
    ry = y_off + row * (cell_h + 20)

    # Cell background
    draw.rectangle([rx-5, ry-5, rx+cell_w, ry+cell_h], outline=DIM, width=1)

    center = (rx + cell_w // 2, ry + cell_h // 2)
    draw_permutation(draw, reps_s5[ct], 5, center, 80, color=GOLD)

    # Stats in corner
    label = '+'.join(map(str, ct))
    stat_text = f"{label}  ({cycle_freq_s5[ct]})"
    draw.text((rx + 5, ry + 5), stat_text, fill=GOLD)

img.save('assets/permutation-cycles-s5.png')
del draw

print("Done: permutation-cycles-s3.png, permutation-cycles-s4.png, permutation-cycles-s5.png")
print(f"S₃: {len(perms_s3)} permutations, {len(types_s3)} cycle types")
print(f"S₄: {len(perms_s4)} permutations, {len(types_s4)} cycle types")
print(f"S₅: {len(perms_s5)} permutations, {len(types_s5)} cycle types")
for ct in types_s5:
    print(f"  {'+'.join(map(str, ct))}: {cycle_freq_s5[ct]}")
