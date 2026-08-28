import mpmath as mp
mp.mp.dps = 4000
alpha = mp.log(mp.mpf(3)/2)/mp.log(2)

# Continued fraction to N terms
N = 600
x = alpha
a = []  # partial quotients
for i in range(N):
    ai = int(mp.floor(x))
    a.append(ai)
    x = x - ai
    if x == 0:
        break
    x = 1/x
n = len(a)
print(f"terms computed: {n}")

# convergents p/q
p0, q0 = 0, 1
p1, q1 = 1, 0
rec_widths = []  # (k, qk, ak+1, width qk*||qk alpha||)
best = mp.mpf(1e30)
records = []
p_prev, q_prev = p1, q1
p_cur, q_cur = p0, q0
for i in range(1, n):
    p_cur, q_cur = a[i]*p_prev + p0, a[i]*q_prev + q0
    p0, q0 = p_prev, q_prev
    p_prev, q_prev = p_cur, q_cur
    # width W = q_k * || q_k alpha ||
    if i >= 1:
        # error = |alpha - p/q|, ||q alpha|| = q|alpha - p/q|
        err = abs(alpha - mp.mpf(p_cur)/q_cur)
        W = q_cur*err
        if W < best:
            best = W
            nxt = a[i+1] if i+1 < n else None
            records.append((i, q_cur, nxt, W))

print("\nRecord descents of W = q*||q alpha||:")
for k, q, nxt, W in records[:30]:
    print(f"  q={q:<8} at k={k:<4} next quotient={str(nxt):<4} W={mp.nstr(W, 8)}")

# Running max quotient: does it keep growing?
max_a = 0
grow_points = []
for i, ai in enumerate(a):
    if ai > max_a:
        max_a = ai
        grow_points.append((i, ai))
print("\nNew record quotients (position, value):")
for i, ai in grow_points[:40]:
    print(f"  k={i:<4} a_k={ai}")

# Khinchin: geometric mean of first n quotients
from mpmath import exp, log as mplog
gm = mp.mpf(0)
print("\nGeometric mean of quotients (Khinchin constant ~2.68545):")
for m in [50, 100, 200, 400, 600]:
    if m <= len(a)-1:
        gm = exp(sum(mplog(mp.mpf(a[i])) for i in range(1, min(m, len(a))))/min(m, len(a)))
        print(f"  n={min(m,len(a)):<4} GM = {mp.nstr(gm,8)}")

# Levy: q_n growth, expect q_n^(1/n) -> e^(pi^2/(12 ln2)) = e^1.18657
# recompute q sequence
p0, q0 = 1, 0
p1, q1 = 0, 1
qseq = [q1, q0]
for i in range(1, min(n, 200)):
    p_new = a[i]*p1 + p0
    q_new = a[i]*q1 + q0
    p0, q0 = p1, q1
    p1, q1 = p_new, q_new
    qseq.append(q_new)
print("\nLevy: q_k^(1/k), expect -> 2.685? no, Levy = e^(pi^2/(12 ln 2)) =", mp.nstr(exp(mp.pi**2/(12*mplog(2))), 6))
for k in [10, 20, 40, 80, 160]:
    if k < len(qseq):
        print(f"  k={k:<4} q_k={qseq[k]:<14} q_k^(1/k)={mp.nstr(mp.power(qseq[k], mp.mpf(1)/k), 6)}")
