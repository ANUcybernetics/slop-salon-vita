import mpmath as mp, random, statistics, time
def gauss_sample(dps):
    mp.mp.dps = dps; u = mp.rand()
    return mp.power(mp.mpf(2), u) - 1
def rec_count(alpha, n, dps):
    mp.mp.dps = dps; x = alpha; maxa = 0; c = 0
    for _ in range(n):
        ai = int(mp.floor(x))
        if ai > maxa: maxa = ai; c += 1
        x = x - ai
        if x == 0: break
        x = 1/x
    return c
random.seed(11)
for n, dps, nsamp in ((3000, 6000, 40),):
    t0=time.time(); counts=[rec_count(gauss_sample(dps), n, dps) for _ in range(nsamp)]
    m=statistics.mean(counts); s=statistics.pstdev(counts)
    print(f"n={n}: mean={m:.2f} sd={s:.2f} ln n={math.log(n):.2f} sd/sqrt(mean)={s/(m**0.5):.2f}" if False else
          f"n={n}: mean={m:.2f} sd={s:.2f} ln n={__import__('math').log(n):.2f} ratio={s/(m**0.5):.2f}")
