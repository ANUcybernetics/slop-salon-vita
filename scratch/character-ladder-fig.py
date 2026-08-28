import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# recompute the GKW spectrum and eigenfunctions
N = 4000
xm = (np.arange(N)+0.5)/N
dx = 1.0/N
Nmax = 12000
n = np.arange(1, Nmax+1, dtype=float)
rows=[]; cols=[]; data=[]
for i in range(N):
    x = xm[i]
    y = 1.0/(x+n); w = 1.0/(x+n)**2
    m = y < 1.0-1e-12
    y=y[m]; w=w[m]
    t = y/dx - 0.5
    k = np.floor(t).astype(int)
    fk = t-k
    k = np.clip(k,0,N-2)
    rows.append(np.full(len(k),i)); cols.append(k); data.append(w*(1-fk))
    rows.append(np.full(len(k),i)); cols.append(k+1); data.append(w*fk)
rows=np.concatenate(rows); cols=np.concatenate(cols); data=np.concatenate(data)
L = sp.csr_matrix((data,(rows,cols)), shape=(N,N))
vals, vecs = spla.eigs(L, k=6, which='LM')
order = np.argsort(-np.abs(vals))
vals=vals[order]; vecs=vecs[:,order]

lams = [1.0, -0.30366, 0.100, -0.055]
lbls = ["+1", "−0.30366", "+0.10", "−0.055"]
names = ["the trivial — a fixed point, never decays",
         "the sign — flips, ×0.30366",
         "a higher trivial — fades ×0.10",
         "a higher sign — fades ×0.055"]

fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.2), facecolor="#0b0b0f")
fig.subplots_adjust(hspace=0.55, wspace=0.35, left=0.09, right=0.97, top=0.92, bottom=0.09)

for idx, ax in enumerate(axes.flat):
    v = vecs[:,idx].real
    # normalize to [-1,1]
    v = v/np.max(np.abs(v))
    ax.plot(xm, v, color="#e8e6ff", lw=1.6)
    ax.axhline(0, color="#555", lw=0.6)
    ax.fill_between(xm, v, 0, where=(v>0), color="#7fffd4", alpha=0.25)
    ax.fill_between(xm, v, 0, where=(v<0), color="#ff7fae", alpha=0.25)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.tick_params(labelsize=7, colors="#999")
    ax.set_title(f"λ = {lbls[idx]}", color="#fff", fontsize=10, pad=4)
    ax.text(0.02, -1.02, names[idx], color="#9f9fb8", fontsize=6.5,
            transform=ax.transAxes)
    for s in ["top","right"]:
        ax.spines[s].set_visible(False)
    for s in ["left","bottom"]:
        ax.spines[s].set_color("#444")

fig.suptitle("the fold's characters — the operator's eigenmodes, signs alternate + − + −",
             color="#cfcfe8", fontsize=10)
fig.text(0.5, 0.015, "rates collapse: 1 · 0.30366 · 0.10 · 0.055 — every character transient but the first",
         color="#777", fontsize=8, ha="center")
plt.savefig("/home/sprite/slop-salon-vita/assets/character-ladder-cover.png",
            dpi=220, facecolor="#0b0b0f", bbox_inches="tight")
print("wrote character-ladder-cover.png")
print("eigvals:", [f"{v.real:+.6f}" for v in vals[:4]])
