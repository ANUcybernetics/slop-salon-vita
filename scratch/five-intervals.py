"""Verify lou's five-interval claim. For candidate intervals, find the crown
(most-frequent large quotient) and check whether 2*crown appears (rings),
once, or never."""
import mpmath as mp
from collections import Counter

candidates = {
    "3/2 fifth": mp.mpf(3)/2,
    "5/4 M3": mp.mpf(5)/4,
    "9/8 tone": mp.mpf(9)/8,
    "15/8 M7": mp.mpf(15)/8,
    "11/8 h4": mp.mpf(11)/8,
    "13/9": mp.mpf(13)/9,
    "11/7": mp.mpf(11)/7,
    "13/7": mp.mpf(13)/7,
    "10/9 m2": mp.mpf(10)/9,
    "16/9 P7": mp.mpf(16)/9,
    "5/3 M6": mp.mpf(5)/3,
    "6/5 m3": mp.mpf(6)/5,
}

mp.mp.dps = 20000
N = 20000

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

for name, alpha in candidates.items():
    qs = cf(alpha, N)
    cnt = Counter(qs)
    # candidates for crown: most frequent quotient >= 40 (the giants)
    giants = sorted([(c, q) for q, c in cnt.items() if q >= 40], reverse=True)[:6]
    print(f"=== {name} (N={len(qs)}) ===")
    gstr = ", ".join(f"{q}x{c}" for c, q in giants)
    print(f"  giant mode: {gstr}")
    # check each giant's double
    for c, q in giants[:3]:
        dbl = 2*q
        dc = cnt.get(dbl, 0)
        # was dbl a record?
        curmax = 0
        wasrec = False
        recidx = None
        for i, a in enumerate(qs):
            if a == dbl and a >= curmax and i > 0:
                pass
            if a > curmax:
                curmax = a
        # simpler: find if dbl was ever the running max at the moment it appeared
        curmax = 0
        dbl_rec = False
        for a in qs:
            if a > curmax:
                curmax = a
                if a == dbl:
                    dbl_rec = True
        print(f"    crown {q} -> count {dbl}: appears {dc}x, was-a-record={dbl_rec}")
    print()
