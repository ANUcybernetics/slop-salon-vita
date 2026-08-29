"""Compute b(1) = the 1/n coefficient of W_1(n) in the tower expansion.

W_1(n) = (5/4) phi^{-2n} P_{n-1}^{(0,1)}(3/2)  = a(1)/sqrt(n) + b(1)/n + ...
a(1) = 5^{1/4}/(2 sqrt(pi)).
d(infinity) = 0.358852 is the sum over ALL ell of b(ell) (if the 1/n
coefficient sums the same way the 1/sqrt(n) one does).
"""
from mpmath import mp, mpf, jacobi, sqrt, pi, power, log
mp.dps = 50

phi = (1 + sqrt(5)) / 2
a1 = power(5, mpf(1)/4) / (2 * sqrt(pi))
print(f"a(1) = {a1}")
print(f"d_inf (paper Table 2, n=150) = 0.358852")

for n in [50, 100, 200, 400, 800, 1600]:
    P = jacobi(n - 1, 0, 1, mpf(3)/2)
    W1 = mpf(5)/4 * power(phi, -2*n) * P
    b = n * (W1 - a1 / sqrt(n))
    print(f"n={n:5d}  W1(n)={W1:.12f}  b(1;n)={b:.8f}")
