"""Lean verification: count appearances of the count value in the four
identified intervals. Moderate precision, enough rungs."""
import mpmath as mp
from collections import Counter
import sys

mp.mp.dps = 16000
N = 13000

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

for name, alpha, countval in [
    ("5/4", mp.mpf(5)/4, 84),
    ("3/2", mp.mpf(3)/2, 110),
    ("9/8", mp.mpf(9)/8, 222),
    ("15/8", mp.mpf(15)/8, 2502),
]:
    qs = cf(alpha, N)
    cnt = Counter(qs)
    c = cnt.get(countval, 0)
    first = next((i+1 for i, a in enumerate(qs) if a == countval), None)
    curmax = 0
    rec = False
    for a in qs:
        if a > curmax:
            curmax = a
            if a == countval:
                rec = True
    print(f"{name:6s} count={countval} appears={c} first_rung={first} was_record={rec} max={curmax}", flush=True)
