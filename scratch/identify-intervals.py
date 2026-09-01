"""Identify which just intervals have crowns (42,55,111,270,1251) giving
counts (84,110,222,540,2502) in lou's five-interval claim."""
import mpmath as mp
from collections import Counter

intervals = {
    "3/2 fifth": mp.mpf(3)/2,
    "4/3 fourth": mp.mpf(4)/3,
    "5/4 M3": mp.mpf(5)/4,
    "6/5 m3": mp.mpf(6)/5,
    "5/3 M6": mp.mpf(5)/3,
    "8/5 m6": mp.mpf(8)/5,
    "7/4 h7": mp.mpf(7)/4,
    "7/5 h3": mp.mpf(7)/5,
    "9/8 tone": mp.mpf(9)/8,
    "16/15 semitone": mp.mpf(16)/15,
    "45/32 tritone": mp.mpf(45)/32,
    "25/16 aug4": mp.mpf(25)/16,
    "64/45 dtrit": mp.mpf(64)/45,
    "15/8 M7": mp.mpf(15)/8,
    "8/7 h2": mp.mpf(8)/7,
    "11/8 h4": mp.mpf(11)/8,
    "10/9 m2": mp.mpf(10)/9,
    "12/11 h": mp.mpf(12)/11,
}

mp.mp.dps = 4000  # moderate; enough for ~3000 reliable rungs
N = 3000

def cf_of(alpha, max_rungs):
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
    return a0, qs

for name, alpha in intervals.items():
    a0, qs = cf_of(alpha, N)
    cnt = Counter(qs)
    # top 8 quotients by frequency
    top = cnt.most_common(8)
    topstr = ", ".join(f"{q}:{c}" for q, c in top)
    # largest quotients
    big = sorted(set(qs), reverse=True)[:6]
    print(f"{name:16s} a0={a0}  top={topstr}")
    print(f"{'':16s}   biggest={big}")
