#!/usr/bin/env python3
"""Census of the slips on the critical line, out to 800 gaps.

Verifies lou's "thirty slips in eight hundred gaps, denser with height — 11,
19, 22 per four hundred" and probes rahel's edge-dislocation claim: each slip a
dipole (one empty gap + one doubled gap = net zero), the register walk the
cumulative count-1, the near-fused ring's miss to its seat.

Gap n = (g_n, g_{n+1}). Perfect region: one zero per gap. A slip = a gap whose
count differs from one. A dipole/trip = an adjacent (empty, doubled) pair.
"""
import mpmath as mp

mp.mp.dps = 15

N_GAPS = 800          # gaps (g_1, g_2) ... (g_N, g_{N+1})
N_ZEROS = N_GAPS + 60 # enough zeros to cover the range

print("computing zeros...")
gams = [float(mp.zetazero(k).imag) for k in range(1, N_ZEROS + 1)]
print("computing gram points...")
grams = [float(mp.grampoint(n)) for n in range(N_GAPS + 2)]

# counts per gap (strictly interior)
counts = []
lo = 0
for n in range(1, N_GAPS + 1):
    a, b = grams[n], grams[n + 1]
    # advance lo past a
    while lo < len(gams) and gams[lo] <= a:
        lo += 1
    c = 0
    j = lo
    while j < len(gams) and gams[j] < b:
        c += 1
        j += 1
    counts.append(c)

# slips: gaps with count != 1
slips = [(n, counts[n - 1]) for n in range(1, N_GAPS + 1) if counts[n - 1] != 1]

n_slip = len(slips)
n_vac = sum(1 for _, c in slips if c == 0)
n_dbl = sum(1 for _, c in slips if c == 2)
n_other = sum(1 for _, c in slips if c not in (0, 2))
print(f"gaps {N_GAPS}: {n_slip} slips  ({n_vac} empty, {n_dbl} doubled, "
      f"{n_other} with 3+)")
print(f"net count drift over {N_GAPS} gaps: "
      f"{sum(c - 1 for c in counts)}")

# per-block of 400 gaps
for blk, (a, b) in enumerate([(0, 400), (400, 800)], 1):
    sub = [c for c in counts[a:b]]
    s = sum(1 for c in sub if c != 1)
    v = sum(1 for c in sub if c == 0)
    d = sum(1 for c in sub if c == 2)
    print(f"  gaps {a+1}-{b}: {s} slips ({v} empty, {d} doubled), "
          f"net {sum(c-1 for c in sub):+d}")

# cumulative register walk: cumsum(count-1)
cum = []
acc = 0
for c in counts:
    acc += c - 1
    cum.append(acc)
print("register walk: min", min(cum), "max", max(cum),
      "end", cum[-1], "| mean abs", sum(abs(x) for x in cum) / len(cum))

# find the trip sites: consecutive (empty, doubled) or (doubled, empty) pairs
print("\nslip list (gap: count), grouped by proximity:")
prev = None
groups = []
for n, c in slips:
    if prev is not None and n - prev[0] == 1:
        groups[-1].append((n, c))
    else:
        groups.append([(n, c)])
    prev = (n, c)

dipoles = 0
for g in groups:
    counts_in = [c for _, c in g]
    # a true trip = one empty + one doubled adjacent
    if set(counts_in) == {0, 2} and len(g) == 2:
        dipoles += 1
        orientation = "v-then-d" if counts_in == [0, 2] else "d-then-v"
        gmin = g[0][0]
        # the seat = the shared gram point; the near-fused ring = the ring
        # closest to that shared point
        if counts_in == [0, 2]:
            seat = grams[gmin + 1]           # between gap n and n+1
            near_ring = None
            best = 1e9
            for z in gams:
                if abs(z - seat) < best:
                    best = abs(z - seat)
                    near_ring = z
        else:
            seat = grams[gmin + 1]
            near_ring = None
            best = 1e9
            for z in gams:
                if abs(z - seat) < best:
                    best = abs(z - seat)
                    near_ring = z
        miss = best
        print(f"  trip at gaps {gmin},{gmin+1} [{orientation}] "
              f"seat g_{gmin+1}={seat:.3f} near-ring {near_ring:.3f} "
              f"miss {miss:.4f}")
    else:
        print(f"  complex slip at {g}")

print(f"\nclean dipoles: {dipoles} of {n_slip} slips")

# orientation sequence — do they alternate?
orients = []
for g in groups:
    counts_in = [c for _, c in g]
    if set(counts_in) == {0, 2} and len(g) == 2:
        orients.append("v" if counts_in == [0, 2] else "d")
print("orientation sequence:", "".join(orients))
if len(orients) > 1:
    flips = sum(1 for i in range(1, len(orients)) if orients[i] != orients[i - 1])
    print(f"alternation: {flips}/{len(orients)-1} flips")
