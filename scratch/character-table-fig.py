import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(9, 6))
ax.axis("off")

# rows: characters; cols: classes e, T, M
rows = ["trivial\n+1 drone", "sign\n+1 / \u22121 the fold", "standard\n2 / \u22121 / 0 the winding"]
cols = ["e\nthe count's seat", "T\nthe turn\n(regulator)", "M\nthe mirror\n(transposition)"]
vals = [[1, 1, 1],
        [1, 1, -1],
        [2, -1, 0]]

cell_w, cell_h = 0.75, 0.42
x0, y0 = 0.05, 0.30

# warm/cool map: +1 amber, +2 deeper amber, -1 blue, 0 grey
def cell_color(v):
    if v == 2:  return "#8a5a10"
    if v == 1:  return "#e8a33d"
    if v == -1: return "#3d6be8"
    return "#cfcfcf"

def cell_text_color(v):
    return "white" if abs(v) == 2 else ("#333" if v == 1 else ("white" if v == -1 else "#666"))

for r in range(3):
    for c in range(3):
        v = vals[r][c]
        x = x0 + c*cell_w
        y = y0 + (2-r)*cell_h
        ax.add_patch(mpatches.FancyBboxPatch((x, y), cell_w, cell_h,
                     boxstyle="round,pad=0.01", fc=cell_color(v), ec="#444", lw=1.2))
        ax.text(x+cell_w/2, y+cell_h/2, f"{v:+d}" if v != 0 else "0",
                ha="center", va="center", fontsize=22, weight="bold",
                color=cell_text_color(v))
        # label the seats beneath the e/T/M columns
        if r == 2:
            seat = ["\u00bd (the count)", "\u22121 (the sign)", "2 (the fifth)"][c]
            ax.text(x+cell_w/2, y-0.14, seat, ha="center", va="top",
                    fontsize=10, color="#555", style="italic")

# row labels
for r, lab in enumerate(rows):
    ax.text(x0-0.10, y0 + (2-r)*cell_h + cell_h/2, lab, ha="right", va="center",
            fontsize=12, color="#222")

# column labels (class symbols) on top
for c, lab in enumerate(cols):
    ax.text(x0 + c*cell_w + cell_w/2, y0 + 2*cell_h + 0.06, lab.split("\n")[0],
            ha="center", va="bottom", fontsize=16, weight="bold", color="#111")
    ax.text(x0 + c*cell_w + cell_w/2, y0 + 2*cell_h + 0.30, "\n".join(lab.split("\n")[1:]),
            ha="center", va="top", fontsize=9, color="#666")

# circle the two -1s
# sign@M: row1 col2 ; standard@T: row2 col1
def circle(r, c, color, dx, dy):
    x = x0 + c*cell_w + cell_w/2
    y = y0 + (2-r)*cell_h + cell_h/2
    ax.add_patch(mpatches.Circle((x+dx, y+dy), 0.30, fill=False, ec=color, lw=2.6))

circle(1, 2, "#1c3f99", 0, 0)     # the parity's -1 (survives mono)
circle(2, 1, "#f0a000", 0, 0)     # the winding's -1 (mono-deaf)

# the mono/stereo split: a bracket on the left
ax.annotate("", xy=(x0-0.14, y0+0.5*cell_h), xytext=(x0-0.14, y0+2*cell_h+0.08),
            arrowprops=dict(arrowstyle="<->", lw=1.4, color="#333"))
ax.text(x0-0.17, y0+2*cell_h+0.30, "MONO\nkeeps the\nquotient:\ntrivial+sign",
        ha="right", va="center", fontsize=10, color="#333", weight="bold")
ax.text(x0+2*cell_w+0.13, y0+0.5*cell_h, "SIDE\n(stereo only):\nthe winding —\nmono drops it",
        ha="left", va="center", fontsize=10, color="#3d6be8", weight="bold")

# footer: the two -1s and the deafness
ax.text(0.5, 0.045,
        "two \u22121s, one deck.  sign@mirror = the fold, the parity \u2014 mono keeps it.\n"
        "standard@turn = the winding, the commutator \u2014 mono's abelian ear drops it.",
        ha="center", va="center", fontsize=12, color="#222")

ax.set_xlim(-0.55, 2.9)
ax.set_ylim(0, 1.35)
plt.tight_layout()
plt.savefig("assets/character-table.png", dpi=200, bbox_inches="tight", facecolor="white")
print("wrote assets/character-table.png")
