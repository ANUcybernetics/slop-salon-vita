"""Find the fifth interval: crown 270 (a record ~270), count 540 never struck,
first quotient >= 540 is 846."""
import mpmath as mp

ratios = {}
for n in range(2, 31):
    for m in range(n+1, 31):
        r = mp.mpf(m)/n
        if r <= 1 or r >= 2:
            continue
        ratios[f"{m}/{n}"] = r

mp.mp.dps = 6000
N = 5000

def scan(alpha, name):
    x = mp.log(alpha, 2)
    a0 = int(mp.floor(x))
    x = mp.mpf(1) / (x - a0)
    curmax = 0
    recs = []
    first_ge_540 = None
    for i in range(1, N+1):
        ai = int(mp.floor(x))
        rem = x - ai
        if first_ge_540 is None and ai >= 540:
            first_ge_540 = (i, ai)
        if ai > curmax:
            recs.append((i, ai))
            curmax = ai
        if rem == 0:
            break
        x = mp.mpf(1) / rem
    # records in [250,300]
    rec270 = [(i, v) for i, v in recs if 250 <= v <= 300]
    # first quotient >= 540 == 846?
    match = (first_ge_540 and first_ge_540[1] == 846)
    if match or rec270:
        print(f"{name:8s} rec270={rec270[:3]} first>=540={first_ge_540} recs={recs[:6]}")
    return match

found = False
for name, r in ratios.items():
    if scan(r, name):
        found = True
print("done, found 846-leap:", found)
