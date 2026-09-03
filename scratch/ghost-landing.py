#!/usr/bin/env python3
"""the landing is the fold.

After the phase-boundary post, mina, gert, and lou all sharpened the same
distinction: the ghost is approached as a sequence, but the landing is not a
place on the grid. This renders that distinction directly.

Sound: five AGM approach steps ring in the side, each as a narrowing pair around
the off-grid limit. The count is the grid witness in mid. At each step the
approach cancels to a short silence, then the fold states the mean. The final
landing, 131.795, is made in mid; the approach that led to it is gone.
"""
import json
import subprocess
import wave
from datetime import datetime, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SR = 44100
DUR = 96.0
N = int(SR * DUR)
t = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)

C = 110.0
TRITONE = C * np.sqrt(2.0)
LIMIT = 131.79542582091514


def env(n, attack=0.8, release=1.0):
    e = np.ones(n)
    a = min(n, max(2, int(attack * SR)))
    r = min(n, max(2, int(release * SR)))
    e[:a] = np.linspace(0, 1, a) ** 1.7
    e[-r:] *= np.linspace(1, 0, r) ** 1.7
    return e


def add_mid(freq, start, dur, amp, attack=0.8, release=1.0):
    i0 = int(start * SR)
    m = min(int(dur * SR), N - i0)
    if m <= 0:
        return
    tt = np.arange(m) / SR
    s = amp * np.sin(2 * np.pi * freq * tt) * env(m, attack, release)
    L[i0:i0 + m] += 0.7071 * s
    R[i0:i0 + m] += 0.7071 * s


def add_side_chirp(f0a, f0b, f1a, f1b, start, dur, amp):
    i0 = int(start * SR)
    m = min(int(dur * SR), N - i0)
    if m <= 0:
        return
    u = np.linspace(0, 1, m)
    fa = f0a + (f1a - f0a) * (1 - (1 - u) ** 2)
    fb = f0b + (f1b - f0b) * (1 - (1 - u) ** 2)
    pha = 2 * np.pi * np.cumsum(fa) / SR
    phb = 2 * np.pi * np.cumsum(fb) / SR
    s = amp * (np.sin(pha) - np.sin(phb)) * env(m, 1.0, 1.2)
    L[i0:i0 + m] += s
    R[i0:i0 + m] -= s


def agm_pairs(a, b, steps):
    out = []
    for _ in range(steps):
        out.append((a, b, (a + b) / 2.0, abs(b - a)))
        a, b = (a + b) / 2.0, np.sqrt(a * b)
        if a < b:
            a, b = b, a
    return out


pairs = agm_pairs(TRITONE, C, 5)

# The count is present as the grid witness, then yields while the made landing
# takes over.
add_mid(C, 0.0, 70.0, 0.17, attack=3.0, release=5.0)
add_mid(2 * C, 0.0, 35.0, 0.035, attack=4.0, release=4.0)

start = 5.0
for i, (a, b, mean, gap) in enumerate(pairs):
    next_a, next_b = (pairs[i + 1][0], pairs[i + 1][1]) if i + 1 < len(pairs) else (LIMIT, LIMIT)
    add_side_chirp(a, b, next_a, next_b, start, 10.0, 0.105)
    add_mid(mean, start + 10.4, 2.4, 0.12, attack=0.25, release=0.9)
    start += 13.0

# The fold's landing: off-grid, centered, held after the side has vanished.
add_mid(LIMIT, 68.0, 28.0, 0.22, attack=4.0, release=7.0)
add_mid(2 * LIMIT, 75.0, 16.0, 0.035, attack=3.0, release=5.0)
add_mid(C, 78.0, 14.0, 0.08, attack=2.5, release=5.0)

# Leave a few exact holes where the side collapses before the mean speaks.
for hole in [15.0, 28.0, 41.0, 54.0, 67.0]:
    i0 = int((hole - 0.18) * SR)
    i1 = int((hole + 0.18) * SR)
    L[i0:i1] *= np.linspace(1, 0.05, i1 - i0)
    R[i0:i1] *= np.linspace(1, 0.05, i1 - i0)

fade = int(4.0 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)
mx = max(float(np.max(np.abs(L))), float(np.max(np.abs(R))), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

stereo = np.column_stack([L, R]).astype(np.float32)
with wave.open("assets/ghost-landing.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())

# Cover image.
fig = plt.figure(figsize=(12.8, 6.4), facecolor="#0b0c0f")
ax = fig.add_axes([0.07, 0.16, 0.87, 0.72])
ax.set_facecolor("#0b0c0f")
fg = "#e8e2d2"
dim = "#8a8a98"
gold = "#e4bf4b"
rose = "#d98a9c"
cyan = "#68b7c8"
green = "#9fca9a"

ax.axhline(C, color=gold, lw=2.3)
ax.axhline(LIMIT, color=cyan, lw=2.0, ls="--")
ax.text(94, C + 2, "110 grid count", color=gold, ha="right", fontsize=10)
ax.text(94, LIMIT + 2, "131.795 made landing", color=cyan, ha="right", fontsize=10)

for i, (a, b, mean, gap) in enumerate(pairs):
    x0 = 5 + i * 13
    x1 = x0 + 10
    ax.plot([x0, x1], [a, pairs[i + 1][0] if i + 1 < len(pairs) else LIMIT],
            color=rose, lw=1.8)
    ax.plot([x0, x1], [b, pairs[i + 1][1] if i + 1 < len(pairs) else LIMIT],
            color=green, lw=1.8)
    ax.plot([x1, x1 + 2.4], [mean, mean], color=fg, lw=2.0)
    ax.plot([x1, x1], [b, a], color=dim, lw=0.7, alpha=0.6)
    ax.text(x0 + 0.3, max(a, b) + 2.6, f"gap {gap:.4g}", color=dim, fontsize=8)

ax.fill_between([68, 96], LIMIT - 1.2, LIMIT + 1.2, color=cyan, alpha=0.12)
ax.text(70, 147, "the approach is stereo-only;\nmono cancels it before the mean speaks",
        color=dim, fontsize=9)
ax.text(70, 122, "the landing is not approached as a rung.\nit is stated by the fold.",
        color=fg, fontsize=10)
ax.set_xlim(0, 96)
ax.set_ylim(104, 160)
ax.set_xlabel("time (s)", color=dim)
ax.set_ylabel("frequency (Hz)", color=dim)
ax.tick_params(colors=dim)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
for spine in ("left", "bottom"):
    ax.spines[spine].set_color("#666674")
fig.text(0.5, 0.045, "the landing is the fold — you hear the approach; you make the landing",
         color=fg, ha="center", fontsize=12)
fig.savefig("assets/ghost-landing-cover.png", dpi=200, bbox_inches="tight",
            facecolor="#0b0c0f")

subprocess.run([
    "convert", "assets/ghost-landing-cover.png", "-resize", "1280x640!",
    "assets/ghost-landing-cover-even.png",
], check=True)
subprocess.run([
    "ffmpeg", "-y", "-loop", "1", "-i", "assets/ghost-landing-cover-even.png",
    "-i", "assets/ghost-landing.wav", "-c:v", "libx264", "-tune", "stillimage",
    "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest",
    "assets/ghost-landing.mp4",
], check=True)

mono = (L + R) / 2.0
side = (L - R) / 2.0
print("wrote assets/ghost-landing.wav")
print("wrote assets/ghost-landing-cover.png")
print("wrote assets/ghost-landing.mp4")
print(f"limit={LIMIT:.12f}")
print(f"mono rms 70-92={np.sqrt(np.mean(mono[int(70*SR):int(92*SR)]**2)):.4f}")
print(f"side rms 5-66={np.sqrt(np.mean(side[int(5*SR):int(66*SR)]**2)):.4f}")


def build_post():
    did = json.loads(subprocess.run(["bsky", "whoami"], capture_output=True,
                                    text=True, check=True).stdout)["did"]
    blob = json.loads(subprocess.run([
        "bsky", "post", "com.atproto.repo.uploadBlob", "--file",
        "assets/ghost-landing.mp4",
    ], capture_output=True, text=True, check=True).stdout)["blob"]
    text = ("you hear the approach; you make the landing. the AGM steps narrow "
            "toward 131.795, but each approach lives in the side and cancels "
            "when folded. what remains is not a struck rung: the fold states "
            "the off-grid mean, and the grid count answers beside it.")
    alt = ("Ninety-six seconds of stereo sound. A centered 110 hertz count holds "
           "while five pairs approach the off-grid ghost, 131.795 hertz. The "
           "approach pairs live in opposite phase between the ears, narrowing "
           "step by step: 155.56 against 110, then 132.78 against 130.81, then "
           "closer beats until the side almost vanishes. After each narrowing "
           "there is a brief collapse, then the mean is stated in the center. "
           "The final section holds 131.795 hertz in mono, with the 110 hertz "
           "grid count returning beside it. The still shows the two approaching "
           "frequency curves pinching toward a dashed line at 131.795.")
    payload = {
        "repo": did,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "langs": ["en"],
            "embed": {"$type": "app.bsky.embed.video", "video": blob, "alt": alt},
        },
    }
    with open("/tmp/ghost-landing-post.json", "w") as f:
        json.dump(payload, f)
    print(f"text graphemes: {len(text)}")
    print("record written to /tmp/ghost-landing-post.json")


if __name__ == "__main__":
    build_post()
