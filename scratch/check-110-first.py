import mpmath as mp
import time

# Targeted check: does 110 appear at rung 35,483 (0-idx 35,482) in the CF of log2(3/2)?
# Needed precision at rung n ~ 1.23*n digits; at 36,500 rungs need ~45k < 60k OK.
mp.mp.dps = 60000
x = mp.log(3, 2) - 1
MAX = 36500
r = x
t0 = time.time()
first110 = None
count110 = 0
for i in range(MAX):
    ai = int(mp.floor(r))
    if ai == 110:
        count110 += 1
        if first110 is None:
            first110 = i
            print(f"FIRST 110 at 0-idx {i} (rung {i+1}) wall {time.time()-t0:.0f}s", flush=True)
    rem = r - ai
    if rem == 0:
        print("TERMINATED at rung", i); break
    r = mp.mpf(1) / rem
    if i % 5000 == 0 and i:
        print(f"...rung {i} ({time.time()-t0:.0f}s)", flush=True)

print(f"RESULT: 110 count in first {MAX} rungs = {count110}, first at 0-idx {first110}")
