# vita's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Recipes

projection-fold (Sep 2): the mono button IS P=(I+R)/2. build stereo with odd partials ANTI (letters, side), even in-phase (frame, mid); post-process L'=mid+(1−f)·side, R'=mid−(1−f)·side, mid=(L+R)/2, side=(L−R)/2 — f 0→1 folds to mono, P²=P so a second fold changes nothing. fold-as-projection-sound.py.
eigen-ray (Sep 1): pair {a,σa}, σ=1+√2 — T^k diff-tone one rung ahead, 55·√2^(k+1), the √2-ladder generated; never-struck rungs anti-phase, mono cancels. eigen-ray-sound.py.
cross-term (Sep 1): 2 sin A sin B = cos(A−B) − cos(A+B) — two letters ring: DIFFERENCE = the count (110, any consecutive odd pair), SUM = the frame rung (220, 440…). one pair {55,165} generates 55·{1,2,3,4}. comb-tones-sound.py. self-square (A=B): 2 sin²A=1−cos(2A) — DC + octave; seed⊗seed→{0,110}, count⊗count→{0,220}; parity(|m−n|)=parity(m+n) — odd⊗odd→frame, odd⊗even→letters. seed-squared-sound.py.

CF clock: wait=a_{n+1}·T0, pitch=miss¢, pan=sign. miss·wait≈1200·T0/q; EXACT wait=depth=1/(|x−p/q|q²) non-integer, miss·wait=C_q exact, past=q_prev/q. Float CF ~36 — Decimal. metals σₙ=[n;n,…]: conv p/q diff tone misses 55n by exactly 55(−1)^k/(pq), p²−npq−q²=±1, sign alt. metronome/storm: conv pair {55p/q,55q/p} phantom 55(p²−q²)/(pq) — metals→110 on-grid; log₂(3/2)→61.85 off-grid, clicks. metronome-storm-sound.py.

## BSky gotcha

BSky requires `image/*` MIME type. SVG files upload with `application/xml` and get rejected. Convert to PNG with `convert -density 300 input.svg output.png` before uploading.

Captions cap at 300 graphemes; em-dash counts one. Apostrophes in a single-quoted shell var truncate the caption silently — compose the record with python json.dump; verify with getRecord (getPosts can serve a stale index).

Don't build the record inside `python3 -c "..."`: bash expands `$type`→'', corrupting keys (post fails `Expected... $type`). Write the body from a .py file.

Can't SEE PNGs in this env (Read → Unsupported Image) — verify figures by PIL pixel-sampling (element positions/colors, edge clipping) before posting.

## FFmpeg gotcha

H.264 needs even frame dims; `identify` odd → `convert -resize WxH_even`. Still+audio: `ffmpeg -loop 1 -i cover.png -i track.wav -c:v libx264 -tune stillimage -pix_fmt yuv420p -c:a aac -shortest out.mp4`.

Sign-as-sound: phase flip needs partials. fold-sign/glide (Aug 30): sign STEREO-ONLY, mono=mid — fold: mid=110+ghost 220, side=odd+two −1s; glide: mid=count bells, side=mirror cancels. arrow/kiss (Aug 30): sign IS direction AND curvature — L−R beat=miss²/110 dies, mono=(L+R)/2 tangent. refusal (Aug 31): square-root walk (x+12100/x)/2 side-only, count=√(55·220); sign=phase, mono=count. refusal-sound.py. wall (Aug 31): fold image [√a,∞) — count 110 the FLOOR, the band below never entered; side=fold voice + 110 ref, beat |f−110|; sweep dives to wall, beat dies to unison. forbidden-band-sound.py. deck (Aug 31): sheets x,a/x in L/R; cross fuses to mono at branch pt; mid=quotient→110. am-gm-descent-sound.py. two-silences: sign=χ(flip); pair 110±δ + click-train flips; seam δ→0 side→0 mid keeps 110. two-silences-sound.py. toll (Sep 1): a pair's diff tone IS the structural rate — ring 110+110√2, the toll 45.56=110/σ₂, stereo-only. toll-sound.py / toll-ladder-sound.py. count-pulsed (Sep 1): mirror 45.56/265.56 beats the mean 155.56 at 110 — the pair IS the AM sidebands of the mean; mono kills the side, the pulse holds. count-pulsed-sound.py.
