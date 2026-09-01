import mpmath as mp
mp.mp.dps = 30000
x = mp.log(3, 2) - 1
TARGET = 27378
a = []
r = x
for i in range(TARGET+10):
    ai = int(mp.floor(r))
    a.append(ai)
    rem = r - ai
    if rem == 0: break
    r = mp.mpf(1)/rem
print("len:", len(a))
print("window rungs %d..%d (0-indexed %d..%d):" % (TARGET-9, TARGET+7, TARGET-10, TARGET+6))
for i in range(TARGET-10, TARGET+7):
    if 0 <= i < len(a):
        mark = "  <-- 165" if a[i] == 165 else ""
        print(f"  rung {i+1}: {a[i]}{mark}")
print("count of 165:", sum(1 for v in a if v == 165))
print("first 165 at 0-indexed:", next((i for i,v in enumerate(a) if v==165), None))
