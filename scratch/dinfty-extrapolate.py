"""Extrapolate d(infinity) from Alkauskas Table 1 eigenvalues (16 digits, n<=16).

d(n) = n*( |lambda_n| phi^{2n} - 1 - C/sqrt(n) ),   C = 5^{1/4} zeta(3/2)/(2 sqrt(pi)).
Table 1: (-1)^{n+1} lambda_n.
"""
from mpmath import mp, mpf, sqrt, pi, power, zeta
mp.dps = 60
phi = (1 + sqrt(5)) / 2
C = power(5, mpf(1)/4) * zeta(mpf(3)/2) / (2 * sqrt(pi))
print(f"C = {C}")

# Table 1: n -> (-1)^{n+1} lambda_n
tab1 = {
 1: mpf("1.0000000000000000"),
 2: mpf("0.3036630028987326"),
 3: mpf("0.1008845092931040"),
 4: mpf("0.03549615902165984"),
 5: mpf("0.01284379036244026"),
 6: mpf("0.004717777511571031"),
 7: mpf("0.001748675124305511"),
 8: mpf("0.0006520208583205029"),
 9: mpf("0.0002441314655245158"),
10: mpf("0.00009168908376859330"),
11: mpf("0.00003451654616385425"),
12: mpf("0.000013017697877023030"),
13: mpf("0.000004916782302464491"),
14: mpf("0.000001859307351509042"),
15: mpf("0.00000070381134308703980"),
16: mpf("0.00000026664134344795640"),
}

print("\nn   d(n) from Table-1 lambda_n   (paper Table 2)")
for n, l in tab1.items():
    d = n * (l * phi**(2*n) - 1 - C/sqrt(n))
    paper = {1:"0.51605",2:"0.60424",3:"0.52221",4:"0.46629",5:"0.43430",
             10:"0.38504",20:"0.36884"}.get(n, "")
    print(f"{n:2d}   {d:.10f}        {paper}")
