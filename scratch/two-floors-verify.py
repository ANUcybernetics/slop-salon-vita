#!/usr/bin/env python3
"""Verify the record near-fusions: do the tightest ring-to-seat approaches
correspond to slips (count != 1), or do they hold the count?
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 15
N_GAPS = 1200
print("computing zeros...")
gams = np.array([float(mp.zetazero(k).imag) for k in range(1, N_GAPS + 61)])
print("computing gram points...")
grams = np.array([float(mp.grampoint(n)) for n in range(N_GAPS + 2)])

# counts per gap
counts = []
lo = 0
for n in range(1, N_GAPS + 1):
    a, b = grams[n], grams[n + 1]
    while lo < len(gams) and gams[lo] <= a:
        lo += 1
    c = 0
    j = lo
    while j < len(gams) and gams[j] < b:
        c += 1
        j += 1
    counts.append(c)
counts = np.array(counts)

# the exact nearest-zero-to-seat distance (absolute, not normalized)
def nearest_zero(seat):
    i = np.searchsorted(gams, seat)
    d = min(abs(gams[i] - seat), abs(gams[i - 1] - seat),
            abs(gams[i + 1] - seat) if i + 1 < len(gams) else 1e9)
    return d

sites = [1, 3, 6, 8, 12, 33, 62, 482, 899]
print("\nrecord near-fusions (absolute |zero - seat|, and /spacing):")
for n in sites:
    seat = grams[n]
    d = nearest_zero(seat)
    spacing = min(grams[n] - grams[n - 1], grams[n + 1] - grams[n])
    # adjacent gap counts
    c_left = counts[n - 2] if n >= 2 else None   # gap n-1
    c_right = counts[n - 1]                      # gap n
    slip = ""
    if c_left != 1 or c_right != 1:
        slip = f"  <-- SLIP: counts ({c_left},{c_right})"
    print(f"  n={n:5d}  |z-g| = {d:.6f}  /spacing = {d/spacing:.5f}"
          f"  gaps({c_left},{c_right}){slip}")

# also: is the tightest ring-to-seat (0.0006 at 899) near a slip in the walk?
print("\nwalk value around n=899 and 1110:")
cum = np.cumsum(counts - 1)
for n in [897, 898, 899, 900, 901, 1108, 1109, 1110, 1111, 1112]:
    if 1 <= n <= N_GAPS:
        print(f"  gap {n}: count {counts[n-1]}, walk {cum[n-1]}")

# and the record at 62: counts there
print("\nwalk around n=62:")
for n in [60, 61, 62, 63, 64]:
    print(f"  gap {n}: count {counts[n-1]}, walk {cum[n-1]}")

# the whole record list with slip flags
print("\nALL records (n, /spacing, counts):")
cur = 1e9
for n in range(1, N_GAPS + 1):
    d = nearest_zero(grams[n])
    sp = min(grams[n] - grams[n - 1], grams[n + 1] - grams[n])
    dn = d / sp
    if dn < cur:
        cur = dn
        c_left = counts[n - 2] if n >= 2 else None
        c_right = counts[n - 1]
        slip = "SLIP" if (c_left != 1 or c_right != 1) else "hold"
        print(f"  n={n:5d}  {dn:.5f}  counts({c_left},{c_right}) {slip}")
