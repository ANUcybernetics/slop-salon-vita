"""Deeper check: (a) count appearances of 84/222/2502 for 5/4, 9/8, 15/8;
(b) search for an interval with a record 270 (the fifth's crown)."""
import mpmath as mp
from collections import Counter
import sys

def flush(*a):
    print(*a, flush=True)

def cf(alpha, max_rungs):
    mp.mp.dps = max_rungs * 2 + 4000
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

flush("=== (a) count appearances (50k rungs) ===")
for name, alpha, countval in [
    ("5/4", mp.mpf(5)/4, 84),
    ("9/8", mp.mpf(9)/8, 222),
    ("15/8", mp.mpf(15)/8, 2502),
]:
    qs = cf(alpha, 50000)
    cnt = Counter(qs)
    c = cnt.get(countval, 0)
    rungs = [i+1 for i, a in enumerate(qs) if a == countval][:8]
    curmax = 0; rec = False
    for a in qs:
        if a > curmax:
            curmax = a
            if a == countval: rec = True
    flush(f"{name:6s} count={countval} appears={c} rungs={rungs} was_record={rec} max={curmax}")

flush("=== (b) search record-270 (30k rungs, ratios p/q<=40) ===")
ratios = {}
for n in range(2, 41):
    for m in range(n+1, 41):
        r = mp.mpf(m)/n
        if r <= 1 or r >= 2: continue
        ratios[f"{m}/{n}"] = r
for name, alpha in ratios.items():
    qs = cf(alpha, 30000)
    curmax = 0; rec270 = None
    for i, a in enumerate(qs):
        if a > curmax:
            curmax = a
            if curmax == 270:
                rec270 = i+1
                break
    if rec270:
        c270 = Counter(qs).get(270, 0)
        c540 = Counter(qs).get(540, 0)
        flush(f"{name:8s} record-270 at rung {rec270}, 270 appears {c270}x, 540 appears {c540}x")
flush("done")
