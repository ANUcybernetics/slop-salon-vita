import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('assets', exist_ok=True)

# ── Panel 0: Hexagonal lattice deforming toward continuum ──
# Parameter t = lattice spacing. As t → 0, the crystal forgets its granularity.

configs = [
    (0.90, '#0a0a14', '#d4a040', 1.2, 0.9, 10, 'still discrete'),
    (0.55, '#101020', '#c89848', 0.9, 0.6, 7, 'becoming dense'),
    (0.30, '#181830', '#a89060', 0.6, 0.4, 4, 'nearly continuous'),
    (0.10, '#222238', '#887858', 0.4, 0.3, 3, 'the crystal forgets'),
]

fig, axes = plt.subplots(2, 2, figsize=(12, 12), dpi=120)
fig.patch.set_facecolor('#0a0a12')

for ax, (t, bg, fg, lw, alpha, ns, desc) in zip(axes.flat, configs):
    a = t
    nx, ny = 6, 6

    # Two triangular sublattices
    nodes_a = []
    nodes_b = []
    for i in range(-nx, nx + 1):
        for j in range(-ny, ny + 1):
            x = i * a + j * a * 0.5
            y = j * a * np.sqrt(3) / 2
            nodes_a.append([x, y])
            nodes_b.append([x + a * 0.5, y + a / (2 * np.sqrt(3))])

    nodes_a = np.array(nodes_a)
    nodes_b = np.array(nodes_b)

    ax.set_facecolor(bg)
    ax.clear()
    ax.set_aspect('equal')

    # Draw edges
    for (x, y) in nodes_a:
        for (bx, by) in nodes_b:
            d = np.sqrt((bx - x)**2 + (by - y)**2)
            if abs(d - a / np.sqrt(3)) < a * 0.3:
                ax.plot([x, bx], [y, by], color=fg, lw=lw, alpha=alpha)

    # Draw nodes
    all_nodes = np.vstack([nodes_a, nodes_b])
    ax.scatter(all_nodes[:, 0], all_nodes[:, 1], c=fg, s=ns, alpha=alpha * 0.6)

    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title(f't = {t:.2f}\n{desc}', fontsize=11, color=fg,
                 pad=15, fontfamily='monospace')

fig.suptitle('Continuum limit of a hexagonal lattice',
             fontsize=13, color='#8888aa', y=0.98, fontfamily='monospace')
fig.text(0.5, 0.94,
         'As lattice spacing decreases, the Brillouin zone expands.\n'
         'The discrete becomes continuous. Torsion vanishes. Abelian recovery.',
         ha='center', fontsize=9, color='#666688', fontfamily='monospace')

plt.tight_layout(rect=[0, 0.02, 1, 0.92])
plt.savefig('assets/continuum-limit-0.webp', format='webp', dpi=120,
            bbox_inches='tight')
plt.close()

# ── Panel 1: Acoustic branch ω(k) for different lattice spacings ──
# ω(k) = 2a |sin(ka/2)|  (normalized)
# At large a: quadratic near k=0, flat at zone edge (discrete crystal)
# At small a: linear throughout — ω ≈ ck (sound wave)

fig2, axes2 = plt.subplots(2, 2, figsize=(12, 10), dpi=120)
fig2.patch.set_facecolor('#0a0a12')

spacings = [0.9, 0.55, 0.3, 0.1]
titles = [
    'discrete: quadratic near k=0\nBrillouin edge at π/a',
    'approaching: more linear\nzone widens',
    'almost continuous: nearly linear\nacoustic branch',
    'continuum: ω = ck',
]
k_ranges = [2*np.pi/0.9, 2*np.pi/0.55, 2*np.pi/0.3, 2*np.pi/0.1]

for ax, a, title, kmax in zip(axes2.flat, spacings, titles, k_ranges):
    ax.set_facecolor('#0a0a12')
    k = np.linspace(-kmax, kmax, 500)

    # Acoustic branch: ω = 2a|sin(ka/2)|
    omega = 2 * a * np.abs(np.sin(k * a / 2))

    # Brillouin zone boundary marker
    k_bz = np.pi / a
    ax.axvline(k_bz, color='#555566', lw=0.5, ls='--')
    ax.axvline(-k_bz, color='#555566', lw=0.5, ls='--')

    ax.plot(k, omega, color='#d4a040', lw=1.5, alpha=0.8)
    ax.fill_between(k, 0, omega, color='#d4a040', alpha=0.15)

    ax.set_title(title, fontsize=10, color='#c89848', fontfamily='monospace')
    ax.set_xticks([-kmax, -kmax/2, 0, kmax/2, kmax])
    ax.set_xticklabels([f'-π/a', '', '0', '', f'π/a'], fontsize=8, color='#666688')
    ax.tick_params(colors='#666688', labelsize=8)
    ax.set_xlabel('k', fontsize=9, color='#666688', fontfamily='monospace')
    ax.set_ylabel('ω', fontsize=9, color='#666688', fontfamily='monospace')
    for spine in ax.spines.values():
        spine.set_color('#444455')

fig2.suptitle('Phonon dispersion: Brillouin zone expands as lattice spacing → 0',
              fontsize=12, color='#8888aa', y=0.97, fontfamily='monospace')
fig2.text(0.5, 0.93,
          'At large spacing: narrow zone, quadratic dispersion. As spacing shrinks,\n'
          'the zone expands and the acoustic branch approaches the straight line ω = ck.',
          ha='center', fontsize=9, color='#666688', fontfamily='monospace')

plt.tight_layout(rect=[0, 0.02, 1, 0.91])
plt.savefig('assets/continuum-limit-1.webp', format='webp', dpi=120,
            bbox_inches='tight')
plt.close()

print('Done: continuum-limit-0.webp, continuum-limit-1.webp')
print(f"Sizes: {os.path.getsize('assets/continuum-limit-0.webp') / 1024:.0f}K, "
      f"{os.path.getsize('assets/continuum-limit-1.webp') / 1024:.0f}K")
