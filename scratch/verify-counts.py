"""Verify the count status for the four identified intervals, and search
deeper for the fifth (a record 270 -> count 540 never struck)."""
import mpmath as mp
from collections import Counter

mp.mp.dps = 30000
N = 24000

def cf(alpha, max_rungs):
    x = mp.log(alpha, 2)
    a0 = int(mp.floor(x))
    x = mp.mpf(1) / (x - a0)
    qs = []
    for i in range(max_rungs):
        ai = int(mp.floor(x))
        rem = x - ai
        qs.append(ai)
        if rem == 0:
            break
        x = mp.mpf(1) / rem
    return qs

# --- Part 1: count appearances of the count value in the four confirmed ---
print("=== PART 1: count appearances ===")
for name, alpha, countval in [
    ("5/4", mp.mpf(5)/4, 84),
    ("3/2", mp.mpf(3)/2, 110),
    ("9/8", mp.mpf(9)/8, 222),
    ("15/8", mp.mpf(15)/8, 2502),
]:
    qs = cf(alpha, N)
    cnt = Counter(qs)
    c = cnt.get(countval, 0)
    # first occurrence rung
    first = next((i+1 for i, a in enumerate(qs) if a == countval), None)
    # was countval ever a record?
    curmax = 0
    rec = False
    for a in qs:
        if a > curmax:
            curmax = a
            if a == countval:
                rec = True
    print(f"{name:6s} count={countval} appears={c} first_rung={first} was_record={rec} (max={curmax})")

# --- Part 2: search for a record 270 in a wider set, deeper ---
print("=== PART 2: search record-270 ===")
ratios = {}
for n in range(2, 41):
    for m in range(n+1, 41):
        r = mp.mpf(m)/n
        if r <= 1 or r >= 2:
            continue
        ratios[f"{m}/{n}"] = r

for name, alpha in ratios.items():
    qs = cf(alpha, N)
    # is 270 a record? (first arrival at/above 270)
    curmax = 0
    rec270 = None
    recval = None
    for i, a in enumerate(qs):
        if a > curmax:
            curmax = a
            if curmax >= 270 and recval is None:
                recval = (i+1, a)  # first record >= 270
    if recval and recval[1] == 270:
        c540 = Counter(qs).get(540, 0)
        c270 = Counter(qs).get(270, 0)
        print(f"{name:8s} record-270 at rung {recval[0]}, 270 appears {c270}x, 540 appears {c540}x")
