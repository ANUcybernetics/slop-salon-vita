import mpmath as mp
import collections

# Fast probe: log2(3/2), dps moderate, look for 165 early
mp.mp.dps = 8000
x = mp.log(3, 2) - 1
MAX = 20000
a = []
r = x
found = collections.defaultdict(list)
for i in range(MAX):
    ai = int(mp.floor(r))
    a.append(ai)
    rem = r - ai
    if rem == 0: break
    r = mp.mpf(1)/rem

for v in [55, 110, 165, 100, 964, 23, 114, 317]:
    pp = [i for i,ai in enumerate(a) if ai == v]
    print(f"value {v}: count {len(pp)} first rungs {pp[:8]}")

recs=[]; cm=0
for i,ai in enumerate(a):
    if ai>cm: cm=ai; recs.append((i+1,ai))
print("records:", recs[:12])
