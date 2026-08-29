"""Fit d(n) -> d_inf + c/n^p from the precise d(n) values (n=8..16)."""
from mpmath import mp, mpf, sqrt, pi, power, zeta
import numpy as np
from scipy.optimize import curve_fit
mp.dps = 60
phi = (1 + sqrt(5)) / 2
C = power(5, mpf(1)/4) * zeta(mpf(3)/2) / (2 * sqrt(pi))
tab1 = {n: mpf(s) for n, s in {
 8: "0.0006520208583205029", 9: "0.0002441314655245158",
 10:"0.00009168908376859330",11:"0.00003451654616385425",
 12:"0.000013017697877023030",13:"0.000004916782302464491",
 14:"0.000001859307351509042",15:"0.00000070381134308703980",
 16:"0.00000026664134344795640"}.items()}
d = {n: float(n*(tab1[n]*phi**(2*n) - 1 - C/mp.sqrt(n))) for n in tab1}
ns = np.array(sorted(d), dtype=float); ds = np.array([d[n] for n in sorted(d)])

def model(x, dinf, c, p): return dinf + c/x**p
for p0 in [0.5, 1.0, 1.5, 2.0]:
    popt, _ = curve_fit(lambda x, di, c: model(x, di, c, p0), ns, ds, p0=[0.35, 0.5])
    print(f"fixed p={p0}: d_inf = {popt[0]:.6f}, c = {popt[1]:.4f}")
popt, pcov = curve_fit(model, ns, ds, p0=[0.358, 0.5, 1.0])
perr = np.sqrt(np.diag(pcov))
print(f"\nfree p: d_inf = {popt[0]:.6f} +- {perr[0]:.1e}, c = {popt[1]:.4f}, p = {popt[2]:.4f}")

# paper's own tail points
np_ = np.array([10,20,30,40,50,70,100,130,150], dtype=float)
dp = np.array([0.38504,0.36884,0.36460,0.36268,0.36159,0.36040,0.35952,0.359061,0.358852])
for p0 in [0.5,1.0,1.5,2.0]:
    popt,_ = curve_fit(lambda x, di, c: model(x, di, c, p0), np_, dp, p0=[0.358,0.3])
    print(f"paper tail fixed p={p0}: d_inf = {popt[0]:.6f}, c = {popt[1]:.4f}")
