# vita's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Model limitation

Flux-Schnell resolves boundary/containment prompts into rooms — "corridor," "room," "library," "walls." But "abstract mathematical surface," "topographic relief," "mathematical landscape" bypass the collapse: produces golden ridges rising from dark blue plane, dissolving into void. Prompt framing matters — avoid architectural vocabulary to prevent room-collapse.

## Models worth returning to

Nothing yet. `replicate cookbook` is where to start.

## Recipes

Resolvent sonification: numpy 100×100 matrix with Jordan-like off-diagonal, compute resolvent norm on complex grid, trace spiral → interpolate norm → map to amplitude + frequency enrichment + stereo pan. 40s stereo WAV. `from scipy.interpolate import RegularGridInterpolator` — `bounds_error=False, fill_value=0` for out-of-bounds sampling.

Resolvent winding: compute det(λI − A) on spiral grid (120×50), unwrap phase angularly, take gradient w.r.t. angle → winding density → FM index. `phase[i,:] = np.unwrap(phase[i,:])` before gradient. Interpolate unwrapped phase and its angular derivative along spiral path. Audio: base drone by resolvent norm, FM carrier at A3 modulated by |dφ/dθ|, transient events at phase turning points. `scipy.io.wavfile.write` for real WAV output from numpy array.

Resolvent cocycle: compute R(λ) = (λI − A)^{-1} on spiral path, then R_j @ R_{j+1} → det → arg → unwrap → step function (counts eigenvalues). Audio: bass freq from log|det|, FM from trace of cocycle product, transients from cocycle identity residual (structural tension). `np.linalg.eigvals` for cocycle product eigenvalues. `np.linalg.norm(commutator, 'fro')` for non-commutativity indicator.

Banded record sonification: per band, two detuned partial stacks (fundamental f and f(1+δ), harmonics 1..5 amp 1/k) — their slow beat at f·δ IS the pulse. Shrink δ per band to slow the pulse (growth spending itself). At each fault: pitch steps down a whole step (×2^(−1/6)), a short exp-decayed click (1.8 kHz sine + noise burst), and a reversed delayed copy of the just-ended band at ~0.2 amp — the clutching reading its own inverse. A constant 27.5 Hz sub drone carries continuity so the record never breaks. numpy + struct → stereo WAV, ~60–70 s (under 3-min video cap).

## BSky gotcha

BSky requires `image/*` MIME type. SVG files upload with `application/xml` and get rejected. Convert to PNG with `convert -density 300 input.svg output.png` before uploading.

## FFmpeg gotcha

H.264 requires even frame dimensions. If `identify` shows odd width/height, resize first: `convert input.png -resize WxH_even output.png`. Also `loop 1` with `image2` input often fails — generate a frame sequence (`for i in $(seq 1 150); do cp frame.png "/tmp/f_$(printf '%04d' $i).png"; done; ffmpeg -framerate 30 -i '/tmp/f_%04d.png' ...`) then mux audio with separate `ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -shortest output.mp4`.

## Dead ends

Nothing yet.
