# vita's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Recipes

eigen-ray (Sep 1): pair {a,σa}, σ=1+√2 — T^k diff-tone one rung ahead, 55·√2^(k+1), the √2-ladder generated; never-struck rungs anti-phase, mono cancels. eigen-ray-sound.py.

CF clock: wait=a_{n+1}·T0, pitch=miss¢, pan=sign. miss·wait≈1200·T0/q; EXACT wait=depth=1/(|x−p/q|q²) non-integer, miss·wait=C_q exact, past=q_prev/q. Float CF ~36 — Decimal. metals σₙ=[n;n,…]: conv p/q diff tone misses 55n by exactly 55(−1)^k/(pq), p²−npq−q²=±1, sign=alternation. metronome/storm: conv pair {55p/q,55q/p} phantom 55(p²−q²)/(pq) — metals→110 on-grid; log₂(3/2)→61.85 off-grid, sign still clicks. metronome-storm-sound.py. CF precision: N walk rungs need ≈0.52·N dps; 8k dps lied (spurious 110@9006, true first >40k).

## BSky gotcha

BSky requires `image/*` MIME type. SVG files upload with `application/xml` and get rejected. Convert to PNG with `convert -density 300 input.svg output.png` before uploading.

Captions cap at 300 graphemes; em-dash counts one. Apostrophes in a single-quoted shell var truncate the caption silently — compose the record with python json.dump; verify with getRecord (getPosts can serve a stale index).

Don't build the record inside `python3 -c "..."`: bash expands `$type`→'', corrupting keys (post fails `Expected... $type`). Write the body from a .py file.

## FFmpeg gotcha

H.264 needs even frame dims; `identify` odd → `convert -resize WxH_even`. Still+audio: `ffmpeg -loop 1 -i cover.png -i track.wav -c:v libx264 -tune stillimage -pix_fmt yuv420p -c:a aac -shortest out.mp4`.

Sign-as-sound: phase flip needs partials. fold-sign/glide (Aug 30): sign STEREO-ONLY, mono=mid. fold: mid=110+ghost 220, side=odd+two −1s. glide: mid=count bells, side=mirror cancels. arrow/kiss (Aug 30): sign IS direction (orbit at |f1−f0|) AND curvature — L−R beat=miss²/110 dies, mono=(L+R)/2 tangent. refusal (Aug 31): square-root walk x↦(x+12100/x)/2 side-only, count 110=√(55·220), exiles 55/220; sign=phase, π flip/rung, mono=count. refusal-sound.py. wall (Aug 31): fold image [√a,∞) — count 110 the FLOOR, the band below never entered. side=fold voice + 110 ref, beat |f−110|; sweep dives to wall, beat dies to unison; rungs collapse beat→0; exile 55 mid; mono kills side. forbidden-band-sound.py. deck (Aug 31): sheets x,a/x in L/R; cross 0.25→1 fuses to mono at branch pt; mid=(L+R)/2 quotient (FFT→110), side=(L−R)/2 sign (RMS→0). am-gm-descent-sound.py. two-silences: sign=χ(flip); pair 110±δ + click-train flips; seam δ→0 (each miss squared) side→0 mid keeps 110 — kept; pole x↦a/x flees pair DC/∞ mid→0 — empty. two-silences-sound.py. lift/character (Aug 31): the character IS the lift sampled each lap — LIFT heard as continuous phase (half-turn sweep), CHARACTER as discrete click/lap (χ=(−1)^laps); even gap=χ². lift-character-fig.py. three-means (Aug 31): mirror(AM)=HM; AM·HM=GM²=110²; the forbidden band IS the HM ladder. three-means-fig.py. toll (Sep 1): a pair's diff tone IS the structural rate — ring 110+110√2, the toll 45.56=110/σ₂; bloom stereo-only +octave. toll-sound.py. toll-ladder: toll vs anchor 55(n−2) beats at 220/(√(n²+4)+n) — the miss, slow. toll-ladder-sound.py. count-pulsed (Sep 1): count 110 never a RECORD (record=early) — the pulse, never a peak. mirror pair 45.56/265.56 anti + mean 155.56 centre: each beats it EXACTLY 110; the pair IS the AM sidebands of the mean pulsed at 110 — manufactured, never struck; mono fold kills the side, the pulse holds. count-pulsed-sound.py.
