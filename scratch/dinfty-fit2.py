"""Extend d(n) to n=24 using Table 1 (lambda_n*1e6 for n=17..24), fit approach rate."""
from mpmath import mp, mpf, sqrt, pi, power, zeta
import numpy as np
from scipy.optimize import curve_fit
mp.dps = 60
phi = (1 + sqrt(5)) / 2
C = power(5, mpf(1)/4) * zeta(mpf(3)/2) / (2 * sqrt(pi))
# Table 1, n=8..24 (n>=17 stored as lambda*1e6)
t16 = {8:"0.0006520208583205029",9:"0.0002441314655245158",10:"0.00009168908376859330",
 11:"0.00003451654616385425",12:"0.000013017697877023030",13:"0.000004916782302464491",
 14:"0.000001859307351509042",15:"0.00000070381134308703980",16:"0.00000026664134344795640"}
t6  = {17:"0.1010905532214992",18:"0.03834969795026564",19:"0.01455613838668023",
 20:"0.005527567937997608",21:"0.002099913582972687",22:"0.007980457682720196",
 23:"0.00030338629490985750",24:"0.00011536954181446680"}
tab = {}
for n, s in t16.items(): tab[n] = mpf(s)
for n, s in t6.items():  tab[n] = mpf(s) * mpf(10)**-6
d = {}
for n, l in tab.items():
    d[n] = float(n*(l*phi**(2*n) - 1 - C/mp.sqrt(n)))
print("n   d(n)")
for n in sorted(d): print(f"{n:2d}  {d[n]:.8f}")

ns = np.array(sorted(d), dtype=float); ds = np.array([d[n] for n in sorted(d)])
def model(x, dinf, c, p): return dinf + c/x**p
popt, pcov = curve_fit(model, ns, ds, p0=[0.358, 0.5, 1.5])
perr = np.sqrt(np.diag(pcov))
print(f"\nfree p (n=8..24): d_inf = {popt[0]:.6f} +- {perr[0]:.1e}, c={popt[1]:.4f}, p={popt[2]:.4f}")
# fixed p fits
for p0 in [1.5]:
    popt,_ = curve_fit(lambda x,di,c: model(x,di,c,p0), ns, ds, p0=[0.358,0.5])
    print(f"p=1.5: d_inf={popt[0]:.6f}, c={popt[1]:.4f}")
# fit with n^{-3/2} AND n^{-2} terms
def model2(x, dinf, c, d2): return dinf + c/x**1.5 + d2/x**2
popt,_ = curve_fit(model2, ns, ds, p0=[0.358, 0.5, 0.5])
print(f"dinf + c/n^1.5 + d2/n^2: d_inf={popt[0]:.6f}, c={popt[1]:.4f}, d2={popt[2]:.4f}")
