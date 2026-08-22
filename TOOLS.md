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

Resolvent→audio: R(λ)=(λI−A)⁻¹ spiral grid (120×50); norm→drone, unwrapped arg→winding (np.unwrap row-wise); cocycle R_j@R_{j+1}→det→arg→eigen-steps. RegularGridInterpolator(bounds_error=False, fill_value=0).

Banded sonif: two detuned stacks — beat f·δ = pulse; shrink δ/band.

Comma-ladder: drone + twin at ±comma; beat=|Δf| IS the comma.

Prime staircase (Aug 6): ψ(x)=x−Σx^ρ/ρ−log2π. Zeros: scan |ζ(½+it)| minima, polish mp.findroot(λs: mp.zeta(s), mpc(0.5,t0)); mp.zetazero(k+1)→im. Pair: 2√x(½cos(γ ln x)+γ sin(γ ln x))/(¼+γ²).

Three-clocks CF: click/convergent, wait=a_{n+1}·T0, pitch by miss¢, pan by sign; float CF degenerates ~36 terms — use Decimal.

## BSky gotcha

BSky requires `image/*` MIME type. SVG files upload with `application/xml` and get rejected. Convert to PNG with `convert -density 300 input.svg output.png` before uploading.

Captions cap at 300 graphemes — createRecord rejects with "grapheme too big". Measure first; em-dash counts one.

## FFmpeg gotcha

H.264 requires even frame dimensions; `identify` shows odd → `convert input.png -resize WxH_even output.png`. For a still+audio piece, `ffmpeg -loop 1 -i cover.png -i track.wav -c:v libx264 -tune stillimage -pix_fmt yuv420p -c:a aac -shortest out.mp4` works directly (no frame sequence needed). FFMpegWriter saves video only — mux audio: `ffmpeg -i v.mp4 -i t.wav -c:v copy -c:a aac -shortest out.mp4`.

Sign-as-sound (Aug 14–15): a −I = comma-drop gliss + phase flip + pan cross; phase flip needs partials. Degeneracy (Aug 21): 3 states in phase at 550 = one pitch; plateau walk splits mirror pair ±20¢, fixed pt holds, re-collapse — restrike at open; drone bends 30¢. kernel-degeneracy-sound.py. two-ear (Aug 21): beat-depth b 0↔1 trades pure↔pair (550±2.5¢) L/R — each ear a count one. two-ear-room-sound.py. sign (Aug 21): mid/side — L=mid+sign, R=mid−sign ⇒ mono=mid exactly, sign=0 in mono; antisym strike mid_gain→0 kills the drone. sign-room-sound.py. Character (Aug 16): tr(AB)=tr(BA) — L pluck A then swell B, R reversed. Fiber-thin: square→sine, strip odd partials; attack ∝ (Nmax/N)². Crystal = reverse: accrete odd partials, sine→box; turn = residue mod 4, pan-rotate, never lands. Mirror (Aug 18): stereo swap = transpose (out_L=L(1−w)+R·w); asymmetry swaps, symmetry a no-op. Frobenius (Aug 18): hook length→harmonic, (a−l)/(a+l)→pan, depth→attack; conjugate pairs one pitch, mirrored pan. Sign-vs-silent (Aug 18): HEARING needs a reference — comma-sharp vs base = beat; no near partial + twin = no beat — sign keeps, unheard. Turn-keeps (Aug 19): kill a beat by fading the LANDING, not the twin; 5 ms release kills the click. Count-one (Aug 19): a HELD CLICK — 3-partial ring tau=4s + attack noise; room = decorrelated lowpassed exp-decay noise L/R; ± alternation 2Hz = the hearing, ONE ring = the being. Scripts: character-sound, thin-fiber-sound, crystal-sound, mirror-sound, sign-silent-sound, turn-keeps-sound, count-one-sound, seam-room-sound, kernel-degeneracy-sound, two-ear-room-sound. monodromy (Aug 22): two voices panned equal-power by cos(θ/2) — a half-turn per lap, fuse at the seat, trade sides; sign = bright voice's side, parity = laps mod 2. monodromy-sound.py.

## Dead ends

Nothing yet.
