"""Richardson-verify b(1) = 0: fit b(1;n) = b + c/sqrt(n) + d/n on large n."""
from mpmath import mp, mpf, jacobi, sqrt, pi, power
mp.dps = 60
phi = (1 + sqrt(5)) / 2
a1 = power(5, mpf(1)/4) / (2 * sqrt(pi))
ns = [200, 400, 800, 1600, 3200, 6400]
bs = []
for n in ns:
    P = jacobi(n - 1, 0, 1, mpf(3)/2)
    W1 = mpf(5)/4 * power(phi, -2*n) * P
    b = n * (W1 - a1 / sqrt(n))
    bs.append(b)
    print(f"n={n:5d}  b(1;n)={mp.nstr(b, 10)}")
# Richardson: assume b(1;n) = b0 + c/sqrt(n) + d/n. Use three consecutive to solve.
import numpy as np
def richardson(b, ns):
    # solve b0 + c/sqrt(n) + d/n for last three points
    n0,n1,n2 = ns[-3:]; b0,b1,b2 = b[-3:]
    s0,s1,s2 = [1/mp.sqrt(n) for n in (n0,n1,n2)]
    i0,i1,i2 = [1/mp.mpf(n) for n in (n0,n1,n2)]
    A = mp.matrix([[1, s0, i0],[1, s1, i1],[1, s2, i2]])
    rhs = mp.matrix([b0,b1,b2])
    sol = mp.lu_solve(A, rhs)
    return sol
sol = richardson(bs, ns)
print(f"\nRichardson (last 3): b(1) = {mp.nstr(sol[0], 12)}   c = {mp.nstr(sol[1], 6)}   d = {mp.nstr(sol[2], 6)}")
print("=> if b(1) ~ 0, the first tower rung carries no 1/n term.")
