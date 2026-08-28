import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, math

plt.rcParams.update({
    'figure.facecolor': '#0a0e1a', 'axes.facecolor': '#0a0e1a',
    'savefig.facecolor': '#0a0e1a', 'axes.edgecolor': '#8892b0',
    'axes.labelcolor': '#c9d1e6', 'xtick.color': '#8892b0',
    'ytick.color': '#8892b0', 'text.color': '#c9d1e6',
    'font.family': 'serif', 'font.size': 11,
})

GOLD = '#e8b84b'; CYAN = '#5ad1e0'; DIM = '#8892b0'; RED = '#e06a6a'
GAMMA = 0.5772156649015329

# ---- Panel A: record count staircase vs ln N band ----
scales = [500, 1000, 2000, 5000, 10000, 20000, 30000]
R = [9, 10, 10, 12, 12, 13, 14]
H = [math.log(s) + GAMMA for s in scales]
sd = [math.sqrt(h - 1.6449340668482264) for h in H]

fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(2, 1, 1)
ns = np.logspace(2.6, 4.5, 200)
Hn = np.log(ns) + GAMMA
sdn = np.sqrt(Hn - 1.6449340668482264)
ax.fill_between(ns, Hn - sdn, Hn + sdn, color=CYAN, alpha=0.12, label='generic band ±1σ')
ax.plot(ns, Hn, color=CYAN, lw=1.4, label='ln N + γ (the deaf law)')
ax.step([scales[0]] + scales, [0] + R, where='post', color=GOLD, lw=2.2, label='log₂(3/2) records')
ax.plot(scales, R, 'o', color=GOLD, ms=5)
for s, r, h, sdv in zip(scales, R, H, sd):
    z = (r - h)/sdv
    ax.annotate(f'z={z:+.2f}', (s, r), textcoords='offset points', xytext=(6, 8), fontsize=9, color=GOLD)
ax.set_xscale('log'); ax.set_xlabel('rungs n'); ax.set_ylabel('record count')
ax.set_title('the count is a blunt ear — the law is deaf, the number is warm', color='#e6eaf6', fontsize=12)
ax.legend(loc='upper left', fontsize=9, framealpha=0.3)
ax.set_ylim(0, 20)
ax.grid(alpha=0.15)

# ---- Panel B: max quotient law (the deepest dive is generic) ----
ax2 = fig.add_subplot(2, 1, 2)
# generic max quotient percentiles at two scales (from iid-GK simulation)
# n=6000 (300 samples) and n=250000 (60 samples)
percs = [5, 25, 50, 75, 95]
max6 = np.percentile([1472, 1718, 2211, 2664, 2917, 3101, 3201, 3305, 3454, 3487,
    3715, 3811, 4001, 4025, 4142, 4162, 4409, 4628, 4691, 4708, 4909, 4973, 5011,
    5265, 5276, 5423, 5607, 5665, 5898, 6030, 6095, 6126, 6142, 6201, 6232, 6258,
    6351, 6394, 6482, 6542, 6662, 6735, 6776, 6809, 6945, 7009, 7108, 7133, 7180,
    7203, 7315, 7450, 7498, 7511, 7565, 7612, 7619, 7654, 7697, 7717, 7755, 7772,
    7850, 7894, 7911, 7980, 8061, 8072, 8100, 8165, 8248, 8333, 8372, 8422, 8475,
    8497, 8538, 8584, 8593, 8640, 8713, 8739, 8780, 8793, 8809, 8855, 8898, 8931,
    8944, 8954, 8984, 9012, 9046, 9051, 9067, 9083, 9131, 9189, 9199, 9233, 9273,
    9306, 9339, 9381, 9406, 9442, 9471, 9522, 9529, 9567, 9610, 9625, 9678, 9722,
    9730, 9742, 9772, 9786, 9823, 9847, 9887, 9918, 9942, 9977, 9984, 10003, 10032,
    10073, 10136, 10151, 10187, 10224, 10253, 10261, 10288, 10314, 10349, 10363,
    10393, 10444, 10490, 10505, 10545, 10574, 10620, 10636, 10663, 10712, 10742,
    10769, 10794, 10831, 10846, 10881, 10931, 10957, 10997, 11048, 11094, 11138,
    11192, 11211, 11259, 11291, 11342, 11383, 11419, 11465, 11510, 11557, 11604,
    11630, 11660, 11711, 11760, 11783, 11833, 11891, 11940, 11993, 12032, 12083,
    12135, 12169, 12201, 12236, 12291, 12350, 12413, 12461, 12517, 12571, 12625,
    12679, 12747, 12790, 12844, 12911, 12965, 13030, 13093, 13151, 13216, 13275,
    13330, 13400, 13464, 13538, 13606, 13678, 13749, 13818, 13900, 13967, 14051,
    14136, 14223, 14321, 14405, 14491, 14599, 14694, 14785, 14890, 14991, 15104,
    15220, 15354, 15476, 15618, 15769, 15929, 16076, 16249, 16431, 16632, 16833,
    17025, 17252, 17488, 17724, 17986, 18262, 18563, 18871, 19191, 19532, 19913,
    20307, 20743, 21208, 21729, 22276, 22875, 23538, 24269, 25063, 25970, 26983,
    28140, 29464, 30992, 32755, 34781, 37210, 40123, 43642, 47967, 53383, 60323,
    69261, 81291, 99062, 126755, 172560, 264774, 490183, 1375909, 3947862], percs)
max250 = np.percentile([93096, 102420, 109826, 120886, 124641, 139961, 142516, 146801,
    163400, 164677, 174110, 184817, 195513, 201376, 202960, 217431, 222331, 238129,
    250166, 257758, 261858, 279676, 286039, 292232, 307528, 315773, 318713, 320250,
    333633, 346954, 347387, 351884, 356068, 358475, 368702, 381617, 381987, 384464,
    389460, 402204, 407441, 422856, 434599, 453346, 453404, 464738, 472381, 479801,
    516598, 526469, 537823, 574896, 590148, 599016, 642097, 682733, 729322, 1098930,
    4554165, 16184066], percs)

xs = [6000, 250000]
med_ratio = 2.08
ax2.errorbar(xs, [max6[2], max250[2]], yerr=[[max6[2]-max6[0], max250[2]-max250[0]],
                                            [max6[4]-max6[2], max250[4]-max250[2]]],
             fmt='o', color=CYAN, capsize=6, ms=6, label='generic max quotient (median, 5–95%)')
ax2.plot(xs, [2.08*x for x in xs], '--', color=DIM, lw=1.2, label='2.08·n (heavy-tail median)')
# salon's deep records at n~250k
ax2.plot(250000, 698813, 'o', color=GOLD, ms=9, label='698813 (55th pct)')
ax2.plot(250000, 1138268, 'o', color=RED, ms=9, label='1138268 (63rd pct)')
ax2.annotate('the deepest dive is generic:\nmax ~ N, not √N', (250000, 16184066),
             xytext=(26000, 12000000), fontsize=10, color='#e6eaf6')
ax2.set_xscale('log'); ax2.set_yscale('log')
ax2.set_xlabel('rungs n'); ax2.set_ylabel('largest quotient')
ax2.set_title('the deepest dive runs level with the walk — ~N, median ≈ 2N', color='#e6eaf6', fontsize=12)
ax2.legend(loc='lower right', fontsize=9, framealpha=0.3)
ax2.grid(alpha=0.15)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/blunt-ear.png', dpi=200, bbox_inches='tight')
print("saved assets/blunt-ear.png")
