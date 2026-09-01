import mpmath as mp
import collections

# CF of log2(3/2) — the exact walk
mp.mp.dps = 60000
x = mp.log(3, 2) - 1
MAX = 30000
a = [0]*MAX
r = x
recs = []; curmax = 0
for i in range(MAX):
    ai = int(mp.floor(r))
    a[i] = ai
    if ai > curmax:
        curmax = ai
        recs.append((i, ai))
    rem = r - ai
    if rem == 0:
        print("TERMINATED at rung", i); break
    r = mp.mpf(1)/rem

pos = collections.defaultdict(list)
for i, ai in enumerate(a):
    pos[ai].append(i)

for v in [55, 110, 165, 100, 964, 114, 317, 23]:
    pp = pos.get(v, [])
    print(f"value {v}: rungs {pp[:12]} (count {len(pp)})")

# where does 165 sit relative to records?
print("\nrecords:", recs)
# neighbors of any 165 hits
for i in pos.get(165, []):
    print(f"165 at rung {i}: neighbors {[(j,a[j]) for j in range(max(0,i-2), min(MAX,i+3))]}")
