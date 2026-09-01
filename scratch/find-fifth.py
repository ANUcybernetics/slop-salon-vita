"""Find the fifth interval (crown 270 -> count 540). Scan many ratios for
quotients equal to 270 or 540."""
import mpmath as mp

ratios = {}
for n in range(2, 18):
    for m in range(n+1, 18):
        r = mp.mpf(m)/n
        if r == 1 or r >= 2:
            continue
        ratios[f"{m}/{n}"] = r

extra = {"7/6":mp.mpf(7)/6, "9/7":mp.mpf(9)/7, "11/10":mp.mpf(11)/10,
         "13/10":mp.mpf(13)/10, "15/14":mp.mpf(15)/14, "16/9":mp.mpf(16)/9,
         "27/16":mp.mpf(27)/16, "32/27":mp.mpf(32)/27, "81/64":mp.mpf(81)/64,
         "14/11":mp.mpf(14)/11, "11/6":mp.mpf(11)/6, "7/4":mp.mpf(7)/4,
         "8/7":mp.mpf(8)/7, "9/5":mp.mpf(9)/5, "10/7":mp.mpf(10)/7,
         "13/8":mp.mpf(13)/8, "15/8":mp.mpf(15)/8}
ratios.update(extra)

mp.mp.dps = 2500
N = 6000

def scan(alpha, name):
    x = mp.log(alpha, 2)
    a0 = int(mp.floor(x))
    x = mp.mpf(1) / (x - a0)
    seen270 = seen540 = None
    curmax = 0
    recs = []
    for i in range(1, N+1):
        ai = int(mp.floor(x))
        rem = x - ai
        if ai == 270 and seen270 is None:
            seen270 = i
        if ai == 540 and seen540 is None:
            seen540 = i
        if ai > curmax:
            recs.append((i, ai))
            curmax = ai
        if rem == 0:
            break
        x = mp.mpf(1) / rem
    giant = next(((i, v) for i, v in recs if v >= 30), None)
    if giant or seen270 or seen540:
        print(f"{name:8s} firstGiant={giant} q270@{seen270} q540@{seen540} recs={recs[:5]}")

for name, r in ratios.items():
    scan(r, name)
print("done")
