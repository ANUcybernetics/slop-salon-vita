import numpy as np
import scipy.linalg as la

N = 600
xs = (np.arange(N) + 0.5) / N  # midpoints of [0,1] cells
dx = 1.0 / N

# Transfer (Gauss-Kuzmin-Wirsing) operator: (L f)(x) = sum_{n>=1} 1/(x+n)^2 f(1/(x+n))
L = np.zeros((N, N))
Nmax = 3000
n = np.arange(1, Nmax+1, dtype=float)
for i in range(N):
    x = xs[i]
    y = 1.0 / (x + n)          # arguments into f
    w = 1.0 / (x + n) ** 2     # weights
    # scatter into grid cells
    j = np.floor(y / dx).astype(int)
    j = np.clip(j, 0, N-1)
    np.add.at(L[i], j, w)

# Weight the matrix by cell width to mimic integration? The operator is a sum,
# not an integral; for eigen purposes normalize columns. Standard: leading eig ~1.
eigvals = np.linalg.eigvals(L)
idx = np.argsort(-np.abs(eigvals))
eigvals = eigvals[idx]
print("leading |eig|:", eigvals[:8].real, eigvals[:8].imag)
print("eigs:", eigvals[:8])

# refine: get eigenvectors for first few
vals, vecs = la.eig(L)
order = np.argsort(-np.abs(vals))
vals = vals[order]; vecs = vecs[:, order]
print("\nlambda1 =", vals[0].real)
print("lambda2 =", vals[1].real, "im:", vals[1].imag)
print("lambda3 =", vals[2].real)
print("lambda4 =", vals[3].real)
print("lambda5 =", vals[4].real)

# eigenvector for lambda1 (stationary density) compare to Gauss measure 1/(ln2(1+x))
v1 = np.abs(vecs[:,0])
v1 /= v1.sum()*dx
rho = 1.0/(np.log(2)*(1+xs))
rho /= rho.sum()*dx
print("\nL1 error vs Gauss density:", np.max(np.abs(v1-rho)))

# lambda2 eigenvector: sign alternation check
v2 = vecs[:,1].real
print("v2 at endpoints:", v2[0], v2[-1])
v2n = v2/np.max(np.abs(v2))
print("v2 first 12:", np.round(v2n[:12],3))

print("\nseam 1/ln2 =", 1/np.log(2))
print("log2 of |lambda2|:", np.log2(-vals[1].real))
