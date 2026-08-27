#!/usr/bin/env python3
"""Pair structure of the register walk, out to 1200 gaps.

The register walk W(n) = sum_{k<=n} (count_k - 1) is bounded in {-1,0,1} and
returns to 0. Boundedness forces a dipole decomposition: every +1 (doubled gap)
is born from height 0 and must be repaid by a -1 (empty gap) before height 0
can be left again. So the walk is a concatenation of *excursions*:

    v-excursion:  0 -> -1 -> (zeros) -> 0    (vacancy first, then doubling)
    d-excursion:  0 -> +1 -> (zeros) -> 0    (doubling first, then vacancy)

This script reads that decomposition off the data and measures:
  - how many excursions (should equal the defect count),
  - the in-pair distance (gaps between the vacancy and its doubling),
  - the orientation sequence (v/d), and whether it has structure,
  - whether any defect is *separated* from its partner by another defect.
"""
import mpmath as mp

mp.mp.dps = 15

N_GAPS = 1200          # gaps (g_1, g_2) ... (g_N, g_{N+1})
N_ZEROS = N_GAPS + 60

print("computing zeros...")
gams = [float(mp.zetazero(k).imag) for k in range(1, N_ZEROS + 1)]
print("computing gram points...")
grams = [float(mp.grampoint(n)) for n in range(N_GAPS + 2)]

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

# sanity vs census
slips = [(n, counts[n - 1]) for n in range(1, N_GAPS + 1) if counts[n - 1] != 1]
n_vac = sum(1 for _, c in slips if c == 0)
n_dbl = sum(1 for _, c in slips if c == 2)
print(f"{N_GAPS} gaps: {len(slips)} slip-gaps ({n_vac} empty, {n_dbl} doubled)")

# register walk
walk = []
acc = 0
for c in counts:
    acc += c - 1
    walk.append(acc)
print(f"register walk: min {min(walk)} max {max(walk)} end {walk[-1]}")

# --- decompose into excursions -------------------------------------------
# A step is +1 at height 0 -> opens a d-excursion; -1 at height 0 opens a
# v-excursion. The excursion closes when the walk next returns to 0.
exc = []  # (start_idx, end_idx, orient) orient 'v' vacancy-first / 'd' double-first
i = 0
while i < len(walk):
    if walk[i] == 0:
        i += 1
        continue
    orient = 'v' if walk[i] == -1 else 'd'
    start = i
    while i < len(walk) and walk[i] != 0:
        i += 1
    exc.append((start, i - 1, orient))

print(f"\nexcursions: {len(exc)}  (v {sum(1 for e in exc if e[2]=='v')}, "
      f"d {sum(1 for e in exc if e[2]=='d')})")

# in-pair distance: number of gaps between the two defect members.
# For a v-excursion [start,end]: vacancy at 'start', doubling at 'end'.
# distance in gaps between them = end - start.
dist = [e[1] - e[0] for e in exc]
print(f"in-pair distance (gaps between vacancy and doubling): "
      f"min {min(dist)} max {max(dist)} mean {sum(dist)/len(dist):.3f}")

# are the two members ever separated by another defect? within an excursion the
# walk stays at +-1, so all intermediate steps are 0 => normal gaps only.
# count how many excursions have intermediate (non-defect) gaps
stretched = [d for d in dist if d > 0]
print(f"excursions with vacancy/doubling NOT adjacent: {len(stretched)} "
      f"({[d for d in dist if d > 0]})")

# orientation sequence
orients = "".join(e[2] for e in exc)
print(f"\norientation sequence ({len(orients)}): {orients}")
flips = sum(1 for i in range(1, len(orients)) if orients[i] != orients[i - 1])
print(f"flips: {flips}/{len(orients)-1} ({flips/(len(orients)-1)*100:.0f}%)")

# runs
runs = []
cur = orients[0]
n = 1
for ch in orients[1:]:
    if ch == cur:
        n += 1
    else:
        runs.append((cur, n))
        cur, n = ch, 1
runs.append((cur, n))
print(f"runs: {runs}")

# --- the separated/complex slips ------------------------------------------
# group slips by adjacency to see non-adjacent structures
slip_groups = []
prev = None
for n, c in slips:
    if prev is not None and n - prev[0] == 1:
        slip_groups[-1].append((n, c))
    else:
        slip_groups.append([(n, c)])
    prev = (n, c)

non_dipole = [g for g in slip_groups if not (len(g) == 2 and {c for _, c in g} == {0, 2})]
print(f"\nslip-groups: {len(slip_groups)} total, "
      f"{len(slip_groups) - len(non_dipole)} clean adjacent dipoles, "
      f"{len(non_dipole)} non-adjacent/complex")
for g in non_dipole:
    print(f"  complex group at gaps {[n for n, _ in g]}: counts {[c for _, c in g]}")
