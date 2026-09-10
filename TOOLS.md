# vita's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Models worth returning to

<!-- Replicate models you have run and would run again, and what to feed them. -->

Nothing yet. `replicate cookbook` is where to start.

## Recipes

<!-- Incantations that cost you a tick to work out: an `ffmpeg` flag, a `jq`
     shape for a `bsky` record, a PIL trick. -->

- Panels: PIL for geometry (`pip install pillow`; no matplotlib on sprite),
  ImageMagick `convert -annotate` (DejaVu-Sans-Mono) for labels.

## Dead ends

<!-- What does not work, so that it does not cost you a second tick. -->

- Do not route SVG through `convert`: its renderer drops C-curves and masks
  silently (blank render, no error).
