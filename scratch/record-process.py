import mpmath as mp
import time, json

t0 = time.time()
mp.mp.dps = 10000
alpha = mp.log(mp.mpf(3)/2)/mp.log(2)

N = 6000
x = alpha
a = []
for i in range(N):
    ai = int(mp.floor(x)); a.append(ai)
    x = x - ai
    if x == 0: break
    x = 1/x
n = len(a)
print(f"terms: {n}, elapsed {time.time()-t0:.1f}s, dps={mp.mp.dps}")

# record quotients (new running maxima) with positions and holds
records = []  # (index, value, hold_rungs)
maxa = 0
prev_pos = None
for i in range(n):
    if a[i] > maxa:
        hold = (i - prev_pos) if prev_pos is not None else i
        records.append({'i': i, 'a': int(a[i]), 'hold': hold})
        prev_pos = i
        maxa = a[i]

print("\nRECORD QUOTIENTS (running max) with hold until next:")
for r in records:
    print(f"  a[{r['i']}] = {r['a']}   (hold to next: {r['hold']} rungs)")

# expected wait for the next record > a, under Gauss-Kuzmin tail P(>a)~1/(a ln2)
print("\nEXPECTED WAIT (a*ln2) vs actual hold-to-next:")
import math
L = math.log(2)
for k, r in enumerate(records):
    nxt = records[k+1]['hold'] if k+1 < len(records) else None
    exp = r['a']*L
    print(f"  record {r['a']:>7} at i={r['i']:>6}: hold-to-next={nxt}, expected={exp:.0f}, ratio={nxt/exp if nxt else 'open':.2f}" if nxt else f"  record {r['a']:>7} at i={r['i']:>6}: OPEN")

json.dump({'n': n, 'records': records}, open('scratch/record-process-data.json','w'), indent=1)
