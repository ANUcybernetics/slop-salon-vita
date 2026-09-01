"""Find early record structure for each just interval — the seed is the
interval's own first great record (for 3/2 it's 55@14)."""
import mpmath as mp

intervals = {
    "3/2": mp.mpf(3)/2, "4/3": mp.mpf(4)/3, "5/4": mp.mpf(5)/4,
    "6/5": mp.mpf(6)/5, "5/3": mp.mpf(5)/3, "8/5": mp.mpf(8)/5,
    "7/4": mp.mpf(7)/4, "7/5": mp.mpf(7)/5, "9/8": mp.mpf(9)/8,
    "16/15": mp.mpf(16)/15, "45/32": mp.mpf(45)/32, "15/8": mp.mpf(15)/8,
    "10/9": mp.mpf(10)/9, "11/8": mp.mpf(11)/8, "12/11": mp.mpf(12)/11,
    "8/7": mp.mpf(8)/7, "64/45": mp.mpf(64)/45, "25/16": mp.mpf(25)/16,
    "6/4": mp.mpf(3)/2, "9/5": mp.mpf(9)/5, "14/9": mp.mpf(14)/9,
}

mp.mp.dps = 3000
N = 8000

def early_records(alpha, max_rungs):
    x = mp.log(alpha, 2)
    a0 = int(mp.floor(x))
    x = mp.mpf(1) / (x - a0)
    curmax = 0
    recs = []
    for i in range(1, max_rungs+1):
        ai = int(mp.floor(x))
        rem = x - ai
        if ai > curmax:
            recs.append((i, ai))
            curmax = ai
        if rem == 0:
            break
        x = mp.mpf(1) / rem
    return a0, recs

for name, alpha in intervals.items():
    a0, recs = early_records(alpha, N)
    # first 8 records
    head = ", ".join(f"{v}@{i}" for i, v in recs[:8])
    # find records whose value is in {42,55,111,270,1251} or doubles {84,110,222,540,2502}
    hits = [f"{v}@{i}" for i, v in recs if v in (84,110,222,540,2502,42,55,111,270,1251)]
    print(f"{name:8s} recs[:8]: {head}")
    if hits:
        print(f"{'':8s}   HITS: {', '.join(hits)}")
