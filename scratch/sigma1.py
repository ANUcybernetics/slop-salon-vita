"""sigma1: one crossing, two readings. Left panel keeps the braid (which
strand passed over); right panel keeps only the endpoints (a swap).
Same endpoints, different memory. First still of Season 2."""
import numpy as np
from PIL import Image, ImageDraw

W, H = 1200, 900
BG = (12, 12, 16)
INK_A = (120, 200, 255)   # strand A, cool
INK_B = (255, 150, 120)   # strand B, warm
FAINT = (70, 70, 84)
TEXT = (200, 200, 205)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def strand_points(x_top, x_bot, n=400, wob=0.0, seed=0):
    t = np.linspace(0, 1, n)
    rng = np.random.default_rng(seed)
    x = x_top + (x_bot - x_top) * t + wob * np.sin(t * np.pi * 3 + seed)
    y = 120 + t * (H - 240)
    return np.stack([x, y], axis=1)

# --- left panel: the braid, one crossing ---
cx = W // 4
top_a, top_b = cx - 130, cx + 130
bot_a, bot_b = cx + 130, cx - 130   # they swap: A ends where B began
pa = strand_points(top_a, bot_a, seed=1)
pb = strand_points(top_b, bot_b, seed=2)

# crossing parameter: where x-order flips
cross_i = int(np.argmin(np.abs(pa[:, 0] - pb[:, 0])))

# draw under-strand (B) full first, then A full, then redraw A's
# over-pass segment with a gap cut in B -> real over/under
for pts, col in ((pb, INK_B), (pa, INK_A)):
    d.line([tuple(p) for p in pts], fill=col, width=7)

# carve the gap: paint BG over B near crossing, redraw A over it
gap = 12
d.line([tuple(p) for p in pb[cross_i-gap:cross_i+gap]], fill=BG, width=13)
d.line([tuple(p) for p in pa[cross_i-gap-8:cross_i+gap+8]], fill=INK_A, width=7)
# small highlight on the over-pass
d.line([tuple(p) for p in pa[cross_i-10:cross_i+10]], fill=(225, 245, 255), width=2)

# endpoint ticks + labels
for x in (top_a, top_b, bot_a, bot_b):
    pass
d.text((cx - 200, 60), "the braid keeps the crossing", fill=TEXT)
d.text((cx - 130, H - 70), "A passes over B", fill=FAINT)

# --- right panel: the quotient, endpoints only ---
qx = 3 * W // 4
d.line([(W//2, 80), (W//2, H-40)], fill=(40, 40, 48), width=2)
for y, tag in ((120, "top:  A   B"), (H-120, "bottom:  B   A")):
    d.ellipse([qx-140-9, y-9, qx-140+9, y+9], fill=INK_A, outline=None)
    d.ellipse([qx+140-9, y-9, qx+140+9, y+9], fill=INK_B, outline=None)
# straight ghost lines: the swap with no crossing memory
d.line([(qx-140, 120), (qx+140, H-120)], fill=(60, 60, 72), width=2)
d.line([(qx+140, 120), (qx-140, H-120)], fill=(60, 60, 72), width=2)
d.text((qx - 200, 60), "the endpoint keeps the swap", fill=TEXT)
d.text((qx - 130, H - 70), "A and B exchanged", fill=FAINT)

img.save("assets/sigma1.png")
print("saved assets/sigma1.png", img.size)
