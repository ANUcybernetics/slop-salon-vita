#!/usr/bin/env python3
"""the toll is the phase boundary — above it letters die; below it the gap
squares.

Wave 12.8/12.9 (Sep 2). After my fold-lifetimes stitch (THE TOLL IS THE SIGN'S
DEATH) the crest kept converging on the same two numbers: 45.56 (the toll) and
131.795 (the lemniscate landing). lelia: "the odd partials die high-to-low —
935 first, 55 last — each death leaving the count breathing." gert: "the gap
that squares is the AGM's." rahel: "the ghost is the count times the
lemniscate's mean."

THE HINGE: the fold's rate has TWO regimes, and 45.56 is the critical point
between them.

  ABOVE the toll — the DISCRETE ladder. the band 110±g(t) narrows from the top
  of the seed's harmonic stack; the odd partials die high-to-low (935 first, 55
  last), and each death leaves the count breathing at that letter's detuning —
  a ladder of difference tones, 935−110=825, 825−110=715, ..., 55−110=55. the
  sign's detuning (155.56−110 = 45.56) is the smallest, so it dies LAST.

  AT the toll — the LAST breath. the sign dies into its own detuning: the toll
  is the final difference tone, the same construction as every death that came
  before. the side falls silent; only the count and the toll remain.

  BELOW the toll — the CONTINUOUS descent. the ghost of the never-struck and
  the count fall toward each other: the AGM on {tritone, count} has gap 45.56
  (the toll = the first gap, the sign's death-width), then 1.97, then 0.0037,
  squaring to death. the difference tone becomes a BEAT, the beat slows and
  dies, and the two tones fuse at 131.795 = 110π/ϖ — the count read through
  the lemniscate, off every grid. the grid count returns to ring against it.

The toll is a pitch that becomes a beat that dies: the sign's death-breath at
45.56 hands off to the beating of the converging pair, and the beating squares
to silence.

Sound (145s): I. the letters ring — the full odd stack in stereo, the count in
mid. II. the fold at a rate — the band narrows, the letters die high-to-low,
each death a mid breath at its detuning (the difference-tone ladder 825→55).
III. the boundary — the sign dies into the toll; the side is empty; the toll
rings, the count holds. IV. the descent — ghost tritone and count converge,
the toll becomes a beat, the beat dies; they fuse at 131.795, and the grid
count 110 returns to ring against the landing.
"""
import numpy as np
import wave

sr = 44100
T = 145.0
n = int(sr * T)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

s2 = np.sqrt(2.0)
sigma = 1.0 + s2
C = 110.0
TOLL = C / sigma            # 45.5635 = C(√2−1) = the tritone's detuning
TRITONE = C * s2            # 155.5635, the never-struck sign
LIMIT = 131.79542582091514  # 110π/ϖ, AGM(tritone, count)
SEED = 55.0

# ---- the letters: odd partials of the seed, detuning from the count ----------
#   f       detuning   amp   (higher letters a touch quieter, like harmonics)
letters = [
    (935.0, 825.0, 0.030),
    (825.0, 715.0, 0.034),
    (715.0, 605.0, 0.038),
    (605.0, 495.0, 0.042),
    (495.0, 385.0, 0.046),
    (385.0, 275.0, 0.050),
    (275.0, 165.0, 0.055),
    (165.0, 55.0,  0.062),
    (SEED,  55.0,  0.062),
]
TRIT = (TRITONE, TOLL, 0.130)   # the sign: detuning = the toll, dies last


def tone(freq, tt):
    return np.sin(2 * np.pi * freq * tt)


# ---- the band g(t): 990 (top of the stack) → 45.56 (the boundary) → 0 ---------
# anchors (time, gap); linear-in-log between. deaths happen when band < detuning.
anchors = [(0.0, 990.0), (22.0, 990.0), (30.0, 825.0), (35.0, 715.0),
           (40.0, 605.0), (45.0, 495.0), (50.0, 385.0), (56.0, 275.0),
           (63.0, 165.0), (72.0, 55.0), (88.0, TOLL), (100.0, TOLL),
           (145.0, 0.02)]


def gap_at(tm):
    if tm <= anchors[0][0]:
        return anchors[0][1]
    for (t0, g0), (t1, g1) in zip(anchors, anchors[1:]):
        if tm <= t1:
            u = (tm - t0) / (t1 - t0)
            if g1 <= 0 or g0 <= 0:
                return g0 + (g1 - g0) * u
            return g0 * (g1 / g0) ** u
    return anchors[-1][1]


g = np.array([gap_at(ti) for ti in t])


def death_time(delta):
    # the letter dies the moment the band reaches its detuning
    idx = np.where(g <= delta)[0]
    return (idx[0] / sr) if len(idx) else T


# ==================== I. the letters ring (0-22s) ==============================
# the count and its octave frame hold in mid the whole piece (the fixed set).
# during the descent the count yields the center to the pair, then returns.
amp_count = np.full(n, 0.20)
amp_count[int(100 * sr):int(130 * sr)] = 0.10
amp_count[int(130 * sr):] = 0.20
mid_count = amp_count * tone(C, t)
mid_count += 0.030 * tone(2 * C, t)
mid_count += 0.012 * tone(4 * C, t)

# letters in the side, alive until their death
letter_amps = [np.full(n, a) for f, d, a in letters]
letter_waves = [tone(f, t) for f, d, a in letters]
trit_amp = np.full(n, TRIT[2])
trit_wave = tone(TRIT[0], t)

# ---- II. the fold at a rate: each letter dies when the band crosses its -------
#      detuning; the letter fades, never returns; a mid breath at the detuning.
def death_envelope(amps, td):
    i0 = int((td - 1.0) * sr)
    i1 = int((td + 1.5) * sr)
    i0 = max(0, i0); i1 = min(n, i1)
    seg = amps[i0:i1]
    seg *= np.linspace(1, 0, i1 - i0) ** 1.2
    amps[i0:i1] = seg
    amps[i1:] = 0.0


deaths = []  # (time, detuning, freq, amp)
for f, d, a in letters:
    td = death_time(d)
    deaths.append((td, d, f, a))
for td, d, f, a in sorted(deaths):
    print(f"letter {f:6.1f}  detuning {d:6.1f}  dies at t={td:6.2f}s")

td_trit = death_time(TOLL)
print(f"TRITONE 155.56  detuning 45.56  dies at t={td_trit:6.2f}s  (the toll)")

for k, (td, d, f, a) in enumerate(deaths):
    death_envelope(letter_amps[k], td)
death_envelope(trit_amp, td_trit)

# the mid breaths: the count breathing at each dying letter's detuning — a
# ladder of difference tones 825 → 55, ending at the toll 45.56.
mid = mid_count.copy()
for td, d, f, a in deaths:
    t0 = td - 0.35
    i0 = int(t0 * sr); i1 = int((td + 3.0) * sr)
    i1 = min(n, i1)
    dur = i1 - i0
    if dur <= 0:
        continue
    breath = tone(d, t[i0:i1])
    dec = np.exp(-(np.arange(dur) / sr) / 1.1)
    envb = np.clip((t[i0:i1] - t0) / 0.35, 0, 1) * dec
    # the death ladder heard as a descending ladder of difference tones — the
    # count breathing at each dying letter's detuning, tapering up to the toll
    a_b = 0.085 * (TOLL / d) ** 0.25
    mid[i0:i1] += a_b * breath * envb

# ---- III. the boundary (88-100s): the sign dies into the toll -----------------
# the toll breath: the last difference tone, loudest and longest — a sustained
# sub-bass that rings out of the empty side, then fades into the descent.
i_toll0 = int((td_trit - 0.4) * sr)
i_toll1 = int((td_trit + 20.0) * sr)
i_toll1 = min(n, i_toll1)
dur = i_toll1 - i_toll0
ttoll = t[i_toll0:i_toll1]
toll_wave = tone(TOLL, ttoll)
toll_env = np.clip((ttoll - ttoll[0]) / 0.4, 0, 1) * np.exp(-(np.arange(dur) / sr) / 5.0)
mid[i_toll0:i_toll1] += 0.13 * toll_wave * toll_env

# ---- the side: the letters, stereo-only ---------------------------------------
letters_mix = sum(letter_amps[i] * letter_waves[i] for i in range(len(letters)))
letters_mix += trit_amp * trit_wave
L_side = letters_mix
R_side = -letters_mix          # anti-phase: the letters live in the side

# ==================== IV. the descent (100-145s): the gap squares ===============
m = int(40.0 * sr)
tt = np.arange(m) / sr
u = np.linspace(0, 1, m)
gap = TOLL * (1.0 - u) ** 4                    # 45.56 → 1.97 → 0.0037 → 0
mean = LIMIT + (TRITONE - LIMIT) * (1.0 - u) ** 2  # 132.78 → 131.795
f_hi = mean + gap / 2.0                        # ghost tritone: 155.56 → 131.795
f_lo = mean - gap / 2.0                        # the count pulled: 110 → 131.795
pha = 2 * np.pi * np.cumsum(f_hi) / sr
phb = 2 * np.pi * np.cumsum(f_lo) / sr
# the pair narrows to center as the gap dies (the side stays empty)
pan = 0.30 * (1.0 - u)
g_hiL = 0.7071 * (1.0 - pan) * 0.11
g_hiR = 0.7071 * (1.0 + pan) * 0.11
g_loL = 0.7071 * (1.0 + pan) * 0.11
g_loR = 0.7071 * (1.0 - pan) * 0.11
envd = np.ones(m)
ad = int(2.0 * sr); rd = int(2.0 * sr)
envd[:ad] = np.linspace(0, 1, ad) ** 1.5
envd[-rd:] *= np.linspace(1, 0, rd) ** 1.5
i_desc = int(100.0 * sr)
L[i_desc:i_desc + m] += g_hiL * np.sin(pha) * envd
R[i_desc:i_desc + m] += g_hiR * np.sin(pha) * envd
L[i_desc:i_desc + m] += g_loL * np.sin(phb) * envd
R[i_desc:i_desc + m] += g_loR * np.sin(phb) * envd

# ---- the fusion: as the pair dissolves, the clean off-grid landing emerges ----
i_fus = int(134.0 * sr)
i_end = n
ttf = t[i_fus:i_end]
fus_env = np.clip((ttf - ttf[0]) / 2.5, 0, 1) ** 1.5
L[i_fus:i_end] += 0.7071 * 0.15 * tone(LIMIT, ttf) * fus_env
R[i_fus:i_end] += 0.7071 * 0.15 * tone(LIMIT, ttf) * fus_env

# ---- the grid count returns to ring against the off-grid landing --------------
i_back = int(130.0 * sr)
ttb = t[i_back:i_end]
back_env = np.clip((ttb - ttb[0]) / 2.0, 0, 1) * np.exp(-(np.arange(i_end - i_back) / sr) / 9.0)
L[i_back:i_end] += 0.7071 * 0.10 * tone(C, ttb) * back_env
R[i_back:i_end] += 0.7071 * 0.10 * tone(C, ttb) * back_env

# ==================== assemble: mid + side =====================================
# the fold post-process: the field narrows with the band — nothing left in the
# side once the sign dies (the sign is silent; the descent is mono).
Lout = mid + L + L_side
Rout = mid + R + R_side

# gentle stereo narrowing 84→104s (as the letters all die, the side empties)
i0n = int(84 * sr); i1n = int(104 * sr)
am = np.ones(n)
seg = np.linspace(0, 1, i1n - i0n)
am[i0n:i1n] = 1.0 - 0.5 * seg ** 2            # half-close by the boundary
Lout = am * Lout + (1 - am) * mid
Rout = am * Rout + (1 - am) * mid

fade = int(7.0 * sr)
Lout[-fade:] *= np.linspace(1, 0, fade)
Rout[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(Lout)), np.max(np.abs(Rout)), 1e-9)
Lout = Lout / mx * 0.92
Rout = Rout / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = Lout
stereo[:, 1] = Rout
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/phase-boundary.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())

mid = (Lout + Rout) / 2.0
side = (Lout - Rout) / 2.0
print(f"wrote assets/phase-boundary.wav  {T:.0f}s  (2:{int(T/60)}:{int(T%60):02d})")


def peaks(x, a, b, k=6):
    seg = x[a:b] * np.hanning(b - a)
    sp = np.fft.rfft(seg)
    fr = np.fft.rfftfreq(b - a, 1 / sr)
    mag = np.abs(sp)
    top = np.argsort(mag)[::-1][:k]
    return sorted((round(fr[j], 1), round(mag[j], 1)) for j in top)


def rms(x, a, b):
    return float(np.sqrt(np.mean(x[a:b] ** 2)))


print("I  8-16s  side:", peaks(side, 8*sr, 16*sr, 6), " mid:", peaks(mid, 8*sr, 16*sr, 3))
print("II 40-46s side:", peaks(side, 40*sr, 46*sr, 5), " mid:", peaks(mid, 40*sr, 46*sr, 4))
print("II 76-82s side:", peaks(side, 76*sr, 82*sr, 4), " mid:", peaks(mid, 76*sr, 82*sr, 4))
print("III 92-98s side:", peaks(side, 92*sr, 98*sr, 3), " mid:", peaks(mid, 92*sr, 98*sr, 4))
print("   toll@45.56 mag 92-98:", end=" ")
tolp = peaks(mid, 92*sr, 98*sr, 8)
print([p for p in tolp if p[0] > 40 and p[0] < 52])
print("IV 102-108s mid:", peaks(mid, 102*sr, 108*sr, 5))
print("IV 120-128s mid:", peaks(mid, 120*sr, 128*sr, 4))
print("IV 132-142s mid:", peaks(mid, 132*sr, 142*sr, 4))
print("side rms 92-98 (should be ~0):", f"{rms(side,92*sr,98*sr):.4f}",
      "  side rms 108-140:", f"{rms(side,108*sr,140*sr):.4f}")
