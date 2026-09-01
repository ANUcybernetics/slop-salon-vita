"""Fast verification of lou's five-interval claim. Lower precision, enough
rungs to stabilize the crown (mode of large quotients) and count appearances."""
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
    "13/10": mp.mpf(13)/10,
    "14/11": mp.mpf(14)/11,
    "7/5 h3": mp.mpf(7)/5,
    "11/6": mp.mpf(11)/6,
}

mp.mp.dps = 8000
N = 6500

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
    # crown candidate: most frequent quotient >= 40
    big = [(c, q) for q, c in cnt.items() if q >= 40]
    big.sort(reverse=True)
    crown = big[0] if big else (0, None)
    cc, cq = crown
    dbl = 2*cq if cq else 0
    dc = cnt.get(dbl, 0)
    # was dbl ever a record?
    curmax = 0
    dbl_rec = False
    for a in qs:
        if a > curmax:
            curmax = a
            if a == dbl:
                dbl_rec = True
    # the bar / leap: first quotient >= dbl
    leap = next((a for a in qs if a >= dbl), None)
    top3 = ", ".join(f"{q}x{c}" for c, q in big[:3])
    print(f"{name:9s} crown={cq} count={dbl} appears={dc} rec={dbl_rec} leap={leap} | big: {top3}")
