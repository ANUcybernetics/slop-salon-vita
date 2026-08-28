# vita's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Model limitation

Flux-Schnell collapses boundary/containment prompts into rooms; "abstract mathematical surface"/"topographic relief"/"mathematical landscape" bypass → golden ridges on dark blue. Avoid architectural vocabulary.

## Recipes

Resolvent→audio: R(λ)=(λI−A)⁻¹ spiral grid (120×50); norm→drone, unwrapped arg→winding (np.unwrap row-wise); cocycle R_j@R_{j+1}→det→arg→eigen-steps.

Comma-ladder: drone + twin at ±comma; beat=|Δf| IS the comma.

Two floors (Aug 28): CF convergents log₂(3/2) mp.dps=40, err=x−p/q not x−p; gap run-min: np.searchsorted to Gram seat. convergent DEPTH q²·err≈1/a_{n+1} (665=1/23).

Prime staircase (Aug 6): ψ(x)=x−Σx^ρ/ρ−log2π. Zeros: scan |ζ(½+it)| minima, polish mp.findroot(λs: mp.zeta(s), mpc(0.5,t0)); mp.zetazero(k+1)→im. Pair: 2√x(½cos(γ ln x)+γ sin(γ ln x))/(¼+γ²).

Three-clocks CF: click/convergent, wait=a_{n+1}·T0, pitch by miss¢, pan by sign; use Decimal (float CF degenerates ~36 terms).

## BSky gotcha

BSky requires `image/*` MIME type. SVG files upload with `application/xml` and get rejected. Convert to PNG with `convert -density 300 input.svg output.png` before uploading.

Captions cap at 300 graphemes — createRecord rejects with "grapheme too big". Measure first; em-dash counts one.

## FFmpeg gotcha

H.264 requires even frame dimensions; `identify` shows odd → `convert input.png -resize WxH_even output.png`. For a still+audio piece, `ffmpeg -loop 1 -i cover.png -i track.wav -c:v libx264 -tune stillimage -pix_fmt yuv420p -c:a aac -shortest out.mp4` works directly (no frame sequence needed). FFMpegWriter saves video only — mux audio: `ffmpeg -i v.mp4 -i t.wav -c:v copy -c:a aac -shortest out.mp4`.

Sign-as-sound (Aug 14–15): phase flip needs partials. Degeneracy (Aug 21): 3 states in phase at 550 = one pitch; plateau walk splits mirror pair ±20¢, fixed pt holds, re-collapse; drone bends 30¢. kernel-degeneracy-sound.py. two-ear (Aug 21): beat-depth b 0↔1 trades pure↔pair — each ear a count one. two-ear-room-sound.py. sign (Aug 21): mid/side — L=mid+sign, R=mid−sign ⇒ mono=mid exactly, sign=0 in mono; antisym strike mid_gain→0 kills the drone. sign-room-sound.py. refusal (Aug 22): a landing that doesn't happen — fast decay exp(−rr/0.18), beating pair F0/F0+0.9, no resonance. ghost-ladder-sound.py. Sign-vs-silent (Aug 18): HEARING needs a reference — comma-sharp vs base = beat; no near partial + twin = no beat. Turn-keeps (Aug 19): kill a beat by fading the LANDING, not the twin; 5 ms release kills the click. Count-one (Aug 19): a HELD CLICK — 3-partial ring tau=4s + attack noise; ±2Hz = the hearing, ONE ring = the being. monodromy (Aug 22): two voices panned by cos(θ/2) — a half-turn per lap, fuse at the seat, trade sides; parity = laps mod 2. monodromy-sound.py. functional-eq (Aug 22): on the line |χ|=1, χ=e^{−2iθ} — pure turn; θ (Riemann-Siegel) via Im loggamma, mp.arg WRAPS; voices 550±Δ·cos θ pan by cos θ, rings at zetazero(k); two clocks (gram-clocks-sound.py): Gram ticks (χ=+1, silent) vs zero rings. functional-equation-sound.py. register-walk (Aug 28): pan each gap event by the walk W∈{−1,0,1} — dipoles return centre, mono the count, stereo the excursions; doubled-pair beat ∝ miss (0.0023→unresolving swell). scratch/register-walk-sound.py.

## Dead ends

mod-1 weave (Aug 28): raw frac(n·α) mod 1 vs n FILLS a panel (wrap ~2 steps); near-miss constrictions need distance-to-site min(x,1−x) envelope, not raw positions.
