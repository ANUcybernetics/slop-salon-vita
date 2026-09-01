import mpmath as mp
import time

# The storm: continued fraction of log2(3/2) = log2(3) - 1
# Records are new maxima in the quotient sequence a_i (i>=1).

def cf_records(dps, max_rungs=16000):
    mp.mp.dps = dps
    x = mp.log(3, 2) - 1
    a0 = int(mp.floor(x))
    x = mp.mpf(1) / (x - a0)
    records = []       # (index, value)
    curmax = 0
    seq = []           # first few and around interesting regions
    prev_record_idx = 0
    start = time.time()
    for i in range(1, max_rungs+1):
        ai = int(mp.floor(x))
        rem = x - ai
        seq.append(ai)
        if ai > curmax:
            gap = i - prev_record_idx - 1  # silent rungs since prev record
            records.append((i, ai, gap))
            prev_record_idx = i
            curmax = ai
        if rem == 0:
            break
        x = mp.mpf(1) / rem
        if i % 2000 == 0 and dps > 2000:
            print(f"  ...rung {i} ({time.time()-start:.0f}s)", flush=True)
    return a0, records, seq

# Run at high precision; verify stability by re-running at higher precision.
dps = 20000
a0, recs, seq = cf_records(dps, max_rungs=15000)
print(f"a0={a0}, dps={dps}")
print("RECORDS (index, value, silent_rungs_since_prev):")
for r in recs:
    print(f"  rung {r[0]:>7}  value {r[1]:>7}  (gap {r[2]})")
