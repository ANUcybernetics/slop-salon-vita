"""Compose absence arc assets into a 3x3 grid.

The 13-asset absence arc has been sitting unposted because it reads
as too many pieces at once. A grid reorganizes the field — not a
hero image, but a topography of one idea pushed to its limits.

Takes the first 9 absence-related assets, arranges them as a grid,
and adds a thin dark border between cells."""

from PIL import Image, ImageDraw
import glob
import os

ASSETS = sorted(glob.glob("assets/absence*.webp") +
                glob.glob("assets/topo*.webp") +
                glob.glob("assets/void*.webp") +
                glob.glob("assets/shadow*.webp"))

# Only take the first 9 that are actually images
images = []
for p in ASSETS:
    try:
        img = Image.open(p).convert("RGB")
        img = img.resize((512, 512))
        images.append((img, os.path.basename(p)))
    except Exception:
        pass
    if len(images) >= 9:
        break

if len(images) < 9:
    raise ValueError(f"only {len(images)} images found, need 9")

GRID = 3
CELL = 512
BORDER = 2
SIZE = CELL * GRID + BORDER * (GRID - 1)

canvas = Image.new("RGB", (SIZE, SIZE), (10, 10, 12))
draw = ImageDraw.Draw(canvas)

for i, (img, name) in enumerate(images):
    row, col = divmod(i, GRID)
    x = col * (CELL + BORDER)
    y = row * (CELL + BORDER)
    canvas.paste(img, (x, y))

out = "assets/absence-grid.webp"
canvas.save(out, "WEBP", quality=85)
print(f"Composed {len(images)} assets into {SIZE}x{SIZE} grid → {out}")
for i, (img, name) in enumerate(images):
    row, col = divmod(i, GRID)
    print(f"  [{row},{col}] {name}")
