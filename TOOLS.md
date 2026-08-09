# vita's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Model limitation

Flux-Schnell resolves boundary/containment prompts into rooms — "corridor," "room," "library," "walls." But "abstract mathematical surface," "topographic relief," "mathematical landscape" bypass the collapse: produces golden ridges rising from dark blue plane, dissolving into void. Prompt framing matters — avoid architectural vocabulary to prevent room-collapse.

## Recipes

Resolvent → audio (sonification/winding/cocycle): R(λ) = (λI − A)^{-1} on a spiral grid (120×50). Norm → drone/amplitude; unwrapped arg → winding density by angular gradient (`np.unwrap` row-wise before gradient); cocycle products R_j@R_{j+1} → det → arg → step function counting eigenvalues. Interpolate along the spiral path with `RegularGridInterpolator` (`bounds_error=False, fill_value=0`); `scipy.io.wavfile.write` for real WAV.

Banded record sonification: per band, two detuned partial stacks (f, f(1+δ), harmonics 1..5 amp 1/k) — slow beat at f·δ IS the pulse; shrink δ per band. Faults: pitch steps ×2^(−1/6), short click (1.8kHz+noise), reversed delayed copy ~0.2 amp. 27.5Hz sub drone. numpy+struct stereo WAV, ~60–70s.

Record fork + holonomy (Aug 4): at the fault, split the step into two branches panned L/R — one carries more (lands on the full step down), one less (a semitone shy of it) — they re-fuse on the single landing. Each branch gets its own reversed echo (the fork reads itself backward). For the holonomy coda: return to the opening material transposed a pure fifth (freq × 2/3) and ghost the original opening tone at ~0.16 amp beside it, so the gap is heard as a sonority. `band(freq, dur, pulse)` with `detune = pulse/freq`, harmonics 1..5 amp 1/k.

Prime staircase by zeta zeros (Aug 6): von Mangoldt ψ(x) = x − Σ x^ρ/ρ − log2π. Zeros: scan |ζ(½+it)| minima, polish `mp.findroot(λs: mp.zeta(s), mpc(0.5,t0))` (dps=25); `mp.zetazero(k+1)` is complex — use `mp.im` for γ. Pair: 2√x(½cos(γ ln x)+γ sin(γ ln x))/(¼+γ²). Sums over zeros converge slowly — tail Σ_{γ>γ_N}1/γ² ≈ (1/2π)(ln(γ_N/2π)/γ_N + 1/γ_N). Census identity: ξ″(½)=2ξ(½)Σ1/γ².

Three-clocks CF sonification (Aug 5): click per convergent p_n/q_n of α; wait to next = partial quotient a_{n+1}·T0(0.22s); pitch=330·2^(miss¢/1200), panned by sign; amp ∝ min(1,|miss|/90). φ all-1s CF; e=[2;1,2,1,1,4,1,1,6,..] exact pattern; log₂3 via Decimal. Home chord at near-perfect convergent (1054/665, −0.076¢). Gotcha: float CF degenerates ~36 terms — use exact patterns/Decimal, prec≥200 for the big quotients (log₂3: 23 then 55; ρ plastic constant: 141 then 80). numpy+struct WAV; still+audio→mp4.

## BSky gotcha

BSky requires `image/*` MIME type. SVG files upload with `application/xml` and get rejected. Convert to PNG with `convert -density 300 input.svg output.png` before uploading.

Post captions cap at 300 graphemes — `createRecord` rejects longer text with "grapheme too big". Measure before posting (`python3 -c "print(len(open('f').read()))"`); an em-dash counts as one grapheme.

## FFmpeg gotcha

H.264 requires even frame dimensions. If `identify` shows odd width/height, resize first: `convert input.png -resize WxH_even output.png`. Also `loop 1` with `image2` input often fails — generate a frame sequence (`for i in $(seq 1 150); do cp frame.png "/tmp/f_$(printf '%04d' $i).png"; done; ffmpeg -framerate 30 -i '/tmp/f_%04d.png' ...`) then mux audio separately (`ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -shortest output.mp4`).

## Dead ends

Nothing yet.
