import mpmath as mp

mp.mp.dps = 60000
x = mp.log(3, 2) - 1  # log_2(3/2), CF = [0; ...]

MAX = 30000
a = [0]*MAX
r = x
recs = []
curmax = 0
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

print("RECORDS:", recs)

# search for specific values
import collections
pos = collections.defaultdict(list)
for i, ai in enumerate(a):
    pos[ai].append(i)

for v in [55, 110, 114, 317, 100, 964, 2436, 3308, 4878, 8228, 24477, 59599, 23]:
    pp = pos.get(v, [])
    print(f"value {v}: rungs {pp} (count {len(pp)})")

# quotients around the missing records
for center, span in [(528,3),(2764,3),(4312,3),(21150,3)]:
    print(f"rungs {center-1}-{center+1}:", [(i,a[i]) for i in range(center-1, center+2)])

# the pair gaps
print("pair gaps:", [230-218, 528-330, 2764-528+0 if False else 2764-330-198, 4312-2764, 21150-18287])
