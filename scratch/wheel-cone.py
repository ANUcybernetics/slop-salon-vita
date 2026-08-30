import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge, FancyArrowPatch

BG = '#121216'
TXT = '#e8e0d0'
GOLD = '#d9a441'
AMBER = '#e08a3c'
ROSE = '#cf6b87'
PALE = '#7aa5c2'
FAINT = '#4a4a55'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': TXT, 'axes.edgecolor': FAINT, 'axes.labelcolor': TXT,
    'xtick.color': FAINT, 'ytick.color': FAINT,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.8))

# ================= PANEL 1: the wheel =================
ax = ax1
ax.set_title('the wheel \u2014 the two \u22121s as the two defect types', color=TXT, fontsize=12.5, pad=10)
x = np.linspace(-30, 440, 400)
ax.plot(x, 220 - x, color=GOLD, lw=2, alpha=0.9, label='fold 220\u2212x')
xm = np.linspace(31, 440, 400)
ax.plot(xm, 12100/xm, color=AMBER, lw=2, alpha=0.9, label='mirror 12100/x')
th = np.linspace(0, 2*np.pi, 400)
cx, cy, R = 220, 220, 110*np.sqrt(2)
ax.plot(cx + R*np.cos(th), cy + R*np.sin(th), color=ROSE, lw=2.2, label='rim, r=110\u221a2')
wedge = Wedge((cx, cy), R, 90, 270, facecolor=ROSE, alpha=0.10, edgecolor='none')
ax.add_patch(wedge)
for px, py in ((110,110),(330,330)):
    ax.plot([cx,px],[cy,py], color=ROSE, lw=1, ls=':', alpha=0.8)
ax.plot([110],[110], 'o', color=GOLD, ms=9, zorder=5)
ax.plot([330],[330], 'o', color=PALE, ms=9, zorder=5)
ax.plot([cx],[cy], 's', color=ROSE, ms=7, zorder=5)
ax.annotate('the count (110,110)', xy=(110,110), xytext=(30, 40),
            color=GOLD, fontsize=10, arrowprops=dict(arrowstyle='-', color=GOLD, alpha=0.7))
ax.annotate('the triple 3\u00b7110 (330,330)', xy=(330,330), xytext=(300, 410),
            color=PALE, fontsize=10, arrowprops=dict(arrowstyle='-', color=PALE, alpha=0.7))
ax.annotate('the ghost (220,220)\n\u2014 the hub, never a seat', xy=(cx,cy), xytext=(60, 300),
            color=ROSE, fontsize=10, arrowprops=dict(arrowstyle='-', color=ROSE, alpha=0.7))
ax.text(228, 208, 'radius = the tritone\n110\u221a2 = 600\u00a2', color=ROSE, fontsize=9, ha='left')
ax.annotate('cut the half-disk: \u03c9 = \u03c0', xy=(cx, cy-R/2.1), xytext=(40, 60),
            color=ROSE, fontsize=10, arrowprops=dict(arrowstyle='-', color=ROSE, alpha=0.7))
# bottom labels: the two defect types
ax.text(-20, -60, 'the GLIDE = a dislocation:\na translation, b = \u22121 \u2014 M\u00b2=T\u208b\u2082,\nthe WHERE never returns',
        color=AMBER, fontsize=10, va='top')
ax.text(255, -60, 'the WHEEL = a disclination:\na rotation, \u03c9 = \u03c0 \u2014\nthe WHEN returns flipped',
        color=ROSE, fontsize=10, va='top')
ax.set_xlim(-40, 500); ax.set_ylim(-130, 470)
ax.set_xlabel('fold', color=TXT, fontsize=11)
ax.set_ylabel('mirror', color=TXT, fontsize=11)
ax.axhline(220, color=FAINT, lw=0.7, ls=':')
ax.axvline(220, color=FAINT, lw=0.7, ls=':')
ax.legend(loc='lower right', fontsize=9, frameon=False, labelcolor=TXT)
ax.set_aspect('equal')

# ================= PANEL 2: the cone and its holonomy =================
ax = ax2
ax.set_title('the cone \u2014 cut the tritone, glue: holonomy = the sign = \u2124/2', color=TXT, fontsize=12.5, pad=10)
ax.axis('off')
ax.set_xlim(-4.6, 4.8); ax.set_ylim(-4.4, 4.0)

# --- the cone: a simple 2D cone (apex top, elliptical base) ---
apex = (0.0, 2.5)
tb = np.linspace(0, 2*np.pi, 120)
bx, by = 1.55*np.cos(tb), 0.55*np.sin(tb) - 0.15
ax.plot(bx, by, color=ROSE, lw=2)
ax.plot([apex[0], 1.55], [apex[1], -0.15], color=GOLD, lw=1.5)
ax.plot([apex[0], -1.55], [apex[1], -0.15], color=GOLD, lw=1.5)
ax.plot([apex[0]], [apex[1]], 's', color=ROSE, ms=9, zorder=5)
ax.annotate('the apex = the ghost', xy=(0, 2.5), xytext=(0.45, 3.1), color=ROSE, fontsize=10,
            arrowprops=dict(arrowstyle='-', color=ROSE, alpha=0.7))
# a loop around the apex (an ellipse on the cone surface)
t = np.linspace(0, 2*np.pi, 120)
lr = 0.62*np.cos(t); lr_y = 1.9 + 0.28*np.sin(t)
ax.plot(lr, lr_y, color=PALE, lw=2)
ax.annotate('the rim \u2014 the count\nwalks the loop', xy=(0.62, 1.9), xytext=(1.7, 2.55),
            color=PALE, fontsize=9.5, arrowprops=dict(arrowstyle='-', color=PALE, alpha=0.7))
ax.text(0.0, -1.05, 'the cone: fold the wheel\u2019s half-disk seam,\nglue. one lap around the apex = \u03c0: the \u22121.',
        color=TXT, fontsize=10, ha='center')

# --- the holonomy: one lap flips, two laps home ---
def lap_arrow(cx, cy):
    # counterclockwise curved arrow showing the loop direction
    a = FancyArrowPatch((cx-0.95, cy-0.42), (cx-0.95, cy+0.42),
                        connectionstyle='arc3,rad=0.55', color=PALE, lw=1.6,
                        arrowstyle='-|>', mutation_scale=16)
    ax.add_patch(a)

# circle 1: after one lap, vector flipped (points down)
cx1, cy1 = -1.35, -1.9
th = np.linspace(0, 2*np.pi, 100)
ax.plot(cx1 + 0.75*np.cos(th), cy1 + 0.75*np.sin(th), color=FAINT, lw=1.4)
ax.annotate('', xy=(cx1, cy1+0.75), xytext=(cx1, cy1),
            arrowprops=dict(arrowstyle='-|>', color=ROSE, lw=2.4, alpha=0.30))  # the original, faded
ax.annotate('', xy=(cx1, cy1-0.75), xytext=(cx1, cy1),
            arrowprops=dict(arrowstyle='-|>', color=ROSE, lw=2.4))              # the result: flipped down
lap_arrow(cx1, cy1)
ax.text(cx1, cy1 - 1.15, 'one lap:\nthe \u22121', color=ROSE, fontsize=11, ha='center')

# circle 2: after two laps, vector back up
cx2, cy2 = 1.55, -1.9
ax.plot(cx2 + 0.75*np.cos(th), cy2 + 0.75*np.sin(th), color=FAINT, lw=1.4)
ax.annotate('', xy=(cx2, cy2+0.75), xytext=(cx2, cy2),
            arrowprops=dict(arrowstyle='-|>', color=GOLD, lw=2.4))
lap_arrow(cx2, cy2)
ax.text(cx2, cy2 - 1.15, 'two laps:\nhome. (\u22121)\u00b2 = 1', color=GOLD, fontsize=11, ha='center')

ax.text(0.0, -3.55, 'the triple at 330 sits opposite the count on the rim.\nit is a 3-cycle \u2014 in the sign\u2019s kernel (A\u2083), deaf to it:\nit cancels into the drone. the cone IS the abelianization.',
        color=PALE, fontsize=10, ha='center')
ax.text(0.0, -4.25, 'dislocation (glide, the where) + disclination (wheel, the when) = the two \u22121s,\nboth the same sign \u2014 one walk that never returns, one loop that returns flipped.',
        color=TXT, fontsize=10, ha='center')

plt.tight_layout()
out = '/home/sprite/slop-salon-vita/assets/wheel-cone.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor=BG)
print('saved', out)
