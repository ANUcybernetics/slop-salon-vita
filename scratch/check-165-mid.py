import mpmath as mp
import collections, time

mp.mp.dps = 30000
x = mp.log(3, 2) - 1
MAX = 40000
a = [0]*MAX
r = x
recs = []; curmax = 0
t0 = time.time()
for i in range(MAX):
    ai = int(mp.floor(r))
    a[i] = ai
    if ai > curmax:
        curmax = ai; recs.append((i, ai))
    rem = r - ai
    if rem == 0: print("TERMINATED", i); break
    r = mp.mpf(1)/rem
    if i % 20000 == 0 and i: print(f"...rung {i} ({time.time()-t0:.0f}s)", flush=True)

pos = collections.defaultdict(list)
for i, ai in enumerate(a):
    pos[ai].append(i)

for v in [55, 110, 165, 100, 964, 23]:
    pp = pos.get(v, [])
    print(f"value {v}: count {len(pp)} rungs(0-idx) {pp[:10]}")

print("records(0-idx):", recs[:15])
for i in pos.get(165, [])[:5]:
    print(f"165 at 0-idx {i} (rung {i+1}): neighbors {[(j,a[j]) for j in range(max(0,i-2), min(MAX,i+3))]}")
