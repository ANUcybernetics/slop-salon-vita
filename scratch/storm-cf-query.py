import mpmath as mp
import time

mp.mp.dps = 40000
x = mp.log(3, 2) - 1
a0 = int(mp.floor(x)); x = mp.mpf(1)/(x - a0)

seq = []
records = []
curmax = 0
prev = 0
MAX = 30000
t0 = time.time()
for i in range(1, MAX+1):
    ai = int(mp.floor(x)); rem = x - ai
    seq.append(ai)
    if ai > curmax:
        records.append((i, ai, i-prev-1)); curmax = ai; prev = i
    if rem == 0: break
    x = mp.mpf(1)/rem
    if i % 5000 == 0: print(f"...rung {i} ({time.time()-t0:.0f}s)", flush=True)

print(f"a0={a0}, {MAX} rungs")
print("\nALL RECORDS:")
for r in records: print(f"  {r[0]:>7} @ rung  value {r[1]:>6}  (gap {r[2]})")

print("\nquotients rungs 1-30:", seq[:30])
print("rungs 14-30:", [(i+1, seq[i]) for i in range(13,30)])
print("\nmax quotient between rung 15 and 217 (the long gap):", max(seq[14:217]))
print("quotients 40-60:", [(i+1, seq[i]) for i in range(39,60)])
print("\nrungs 214-235:", [(i+1, seq[i]) for i in range(213,235)])
print("rungs 325-335:", [(i+1, seq[i]) for i in range(324,335)])

for target in (114, 317, 24477):
    hits = [i+1 for i,v in enumerate(seq) if v == target]
    print(f"\nquotient value {target} appears at rungs: {hits[:10]}{'...' if len(hits)>10 else ''} (total {len(hits)})")

# largest quotients overall
top = sorted(enumerate(seq), key=lambda t:t[1], reverse=True)[:15]
print("\nlargest 15 quotients in first %d rungs:" % MAX)
for i,v in top: print(f"  rung {i+1}: {v}")
