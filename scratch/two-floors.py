#!/usr/bin/env python3
"""The two floors, measured.

The register's convergence (Aug 27-28): the fifths' near-misses are the
convergents of log2(3/2) — a deterministic sequence ~1/q^2, over/under, the
seat not in the lattice. The gap near-misses are a running minimum of the
critical-line lattice — a stochastic record ~1/N, scattered sites, no seat to
refuse. Both never land; the count reads both as one short. This script puts
numbers on both.

Floor 1 — the fifths: convergents p/q of x = log2(3/2).
Floor 2 — the gaps: over 1200 Gram gaps, d_n = distance of the nearest zero to
the seat g_n (in units of the local spacing); the running minimum and its
record sites.
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 40

# ---------------------------------------------------------------- the fifths
x = mp.log(1.5) / mp.log(2)

def convergents(x, n):
    """Return list of (p, q, error) convergent triples."""
    a0 = mp.floor(x)
    # standard CF of the fractional part
    cf = []
    r = x - a0
    # build continued fraction digits
    digits = [int(a0)]
    for _ in range(n):
        if r == 0:
            break
        ai = mp.floor(1 / r)
        digits.append(int(ai))
        r = 1 / r - ai
    # convergents from digits
    p0, q0 = digits[0], 1
    out = []
    if n >= 1:
        out.append((p0, q0, x - mp.mpf(p0) / q0))
    if len(digits) >= 2:
        p1, q1 = digits[0] * digits[1] + 1, digits[1]
        out.append((p1, q1, x - mp.mpf(p1) / q1))
    for i in range(2, len(digits)):
        p, q = digits[i] * p1 + p0, digits[i] * q1 + q0
        p0, q0, p1, q1 = p1, q1, p, q
        out.append((p, q, x - mp.mpf(p) / q))
    return out

print("=== THE FIFTHS ===")
print(f"x = log2(3/2) = {mp.nstr(x, 20)}")
convs = convergents(x, 14)
for p, q, err in convs[1:10]:
    qe = float(q * q * abs(err))
    cents = float(1200 * err)
    side = "over" if err > 0 else "under"
    print(f"  {p:6d}/{q:6d}  err {float(err):+.3e} oct  ({cents:+9.4f} cents) "
          f"{side:5s}  q^2|err| = {qe:.4f}")

print()
print("=== THE GAPS ===")
mp.mp.dps = 15
N_GAPS = 1200
print("computing zeros...")
gams = np.array([float(mp.zetazero(k).imag) for k in range(1, N_GAPS + 61)])
print("computing gram points...")
grams = np.array([float(mp.grampoint(n)) for n in range(N_GAPS + 2)])

# d_n: distance of the nearest zero to the seat g_n, in units of local spacing
# (min of the two adjacent gap widths)
d = np.full(N_GAPS + 1, np.inf)
for n in range(1, N_GAPS + 1):
    seat = grams[n]
    lo = 0
    while lo < len(gams) and gams[lo] < seat - 1:
        lo += 1
    best = min(abs(gams[j] - seat) for j in range(lo, min(lo + 4, len(gams))))
    spacing = min(grams[n] - grams[n - 1], grams[n + 1] - grams[n])
    d[n] = best / spacing

# running minimum and its records
runmin = np.full(N_GAPS + 1, np.inf)
records = []  # (n, value)
cur = np.inf
for n in range(1, N_GAPS + 1):
    if d[n] < cur:
        cur = d[n]
        records.append((n, d[n]))
    runmin[n] = cur

print(f"record sites (gap index n, miss/spacing):")
for n, v in records:
    print(f"  n = {n:5d}   miss = {v:.4f}   (1/n ~ {1/n:.6f})")
print(f"final running minimum over {N_GAPS} gaps: {cur:.4f}")

# scaling check: fit log(record) vs log(N) over the record tail
xs = [np.log(n) for n, _ in records]
ys = [np.log(v) for n, v in records]
if len(records) >= 3:
    slope = np.polyfit(xs, ys, 1)[0]
    print(f"log-log slope of the running minimum: {slope:.2f} "
          f"(1/N would be -1.0)")
