import mpmath as mp
mp.mp.dps = 4000
alpha = mp.log(mp.mpf(3)/2)/mp.log(2)

N = 600
x = alpha
a = []
for i in range(N):
    ai = int(mp.floor(x)); a.append(ai)
    x = x - ai
    if x == 0: break
    x = 1/x
n = len(a)

# convergents
p = [0]*(n+2); q = [0]*(n+2)
p[0], q[0] = 0, 1
p[1], q[1] = 1, 0
for k in range(n):
    p[k+2] = a[k]*p[k+1] + p[k]
    q[k+2] = a[k]*q[k+1] + q[k]

# Salon width W = q_k * ||q_k alpha|| = q_k^2 |alpha - p/q|  (records descend ~1/a_{k+1})
best = mp.mpf(1)
descent = []  # (k, q, a_{k+1}, W_salon)
for k in range(1, n):
    pk, qk = p[k+2], q[k+2]
    err = abs(alpha - mp.mpf(pk)/qk)
    W = qk*qk*err   # = qk * ||qk alpha||
    if W < best:
        best = W
        nxt = a[k+1] if k+1 < n else None
        descent.append((k, qk, nxt, W))

print("DESCENT of the salon width W=q||qα||  (records):")
print(f"{'k':>4} {'q':>12} {'a_{k+1}':>8} {'W':>12} {'1/a_{k+1}':>10}")
for k, qk, nxt, W in descent:
    inv = (mp.mpf(1)/nxt) if nxt else None
    invs = mp.nstr(inv,6) if inv else "-"
    print(f"{k:>4} {str(qk):>12} {str(nxt):>8} {mp.nstr(W,6):>12} {invs:>10}")

# The record QUOTIENTS (new maxima) and where they occur
print("\nRECORD QUOTIENTS (new maxima in a_k):")
maxa = 0
for i in range(n):
    if a[i] > maxa:
        maxa = a[i]
        print(f"  a[{i}] = {a[i]}")
