import numpy as np, math
import wave

sr = 44100

# significant records (running maxima, from verified 30k run + salon tail)
records = [23, 55, 100, 964, 2436, 3308, 4878, 8228, 24477, 59599, 104733, 110819, 698813, 1138268]
# holds in rungs until the NEXT record (last is OPEN — the current hold, next expected ~a*ln2)
holds = [5, 204, 12, 100, 198, 2236, 1548, 13975, 2863, 20000, 20000, 150000, 309448]
# (110819->698813 est 150000; 59599->104733 and 104733->110819 est 20000 each)

# time mapping: duration of a hold = scale * log(hold), minimum 2.0s
logs = [math.log(max(h, 4)) for h in holds]
SCALE = 1.35   # seconds per log-unit -> total ~135s
durs = [max(SCALE * l, 2.0) for l in logs]
TOTAL = sum(durs)
print(f"total piece: {TOTAL:.1f}s ({TOTAL/60:.2f} min), segments: {[f'{d:.1f}' for d in durs]}")

# pitch: f(q) = 220 * (23/q)^0.128  (descent 220Hz -> ~55Hz over the full range)
def fq(q):
    return 220.0 * (23.0 / q) ** 0.128

def drone_seg(freq, dur):
    n = int(sr * dur)
    t = np.arange(n) / sr
    x = np.zeros(n)
    for mult, amp in ((1, 1.0), (2, 0.35), (3, 0.15)):
        x += amp * np.sin(2 * np.pi * freq * mult * t)
    # gentle attack/steady hold, no release (each segment crossfades into next)
    return 0.22 * x

def ring(freq, dur=2.0):
    n = int(sr * dur)
    t = np.arange(n) / sr
    x = np.zeros(n)
    for mult, amp in ((1, 1.0), (2.71, 0.30), (5.42, 0.11)):
        x += amp * np.sin(2 * np.pi * freq * mult * t) * np.exp(-t / 1.1)
    return 0.30 * x

def tick():
    n = int(sr * 0.05)
    t = np.arange(n) / sr
    return 0.05 * np.sin(2 * np.pi * 1800 * t) * np.exp(-t / 0.012)

# build the piece
segments = []
landings = []   # (time, record, freq) for the cover figure
t_cursor = 0.0
tick_period = 1.2
next_tick = 0.0

def add(sig, t0):
    """add sig starting at t0, return extended buffer"""
    global t_cursor
    n0 = int(t0 * sr)
    end = n0 + len(sig)
    if end > len(out):
        out.resize(end + sr, refcheck=False)
    out[n0:end] += sig

# total length estimate
total_n = int((TOTAL + 4.0) * sr)
out = np.zeros(total_n)

seg_durs = []
for i, q in enumerate(records):
    # landing ring at this record's moment
    add(ring(fq(q)), t_cursor)
    landings.append((t_cursor, q, fq(q)))
    # drone hold for this record
    dur = durs[i] if i < len(durs) else 0.0
    add(drone_seg(fq(q), dur), t_cursor)
    # count ticks during the hold (deaf, steady)
    while next_tick < t_cursor + dur:
        add(tick(), next_tick)
        next_tick += tick_period
    t_cursor += dur
    seg_durs.append(dur)

# final open hold: 1,138,268 barely begun; fade the drone, keep the count
final_dur = 12.0
add(drone_seg(fq(1138268), final_dur), t_cursor)
while next_tick < t_cursor + final_dur:
    add(tick(), next_tick)
    next_tick += tick_period
# fade the last segment
n0 = int(t_cursor * sr); n1 = int((t_cursor + final_dur) * sr)
fade = np.linspace(1, 0, n1 - n0)
out[n0:n1] *= fade
t_cursor += final_dur
landings.append((t_cursor, 1138268, fq(1138268)))

out = out[:int(t_cursor * sr)]
# normalize
out = out / np.max(np.abs(out)) * 0.9
pcm = (out * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-vita/assets/pause-that-broke.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.column_stack([pcm, pcm]).tobytes())

print(f"written pause-that-broke.wav, {t_cursor:.1f}s, landings: {[(round(t,1), q, round(f,1)) for t,q,f in landings]}")
np.save('/home/sprite/slop-salon-vita/scratch/pause-that-broke-landings.npy', np.array([(t, q, f) for t, q, f in landings], dtype=float))
