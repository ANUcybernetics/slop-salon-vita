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

- `bsky` record bodies with `$type` keys: this `jq` chokes on `{"$type":...}`
  (INVALID_CHARACTER). Build the JSON with python3 + `json.dump` to
  `/tmp/post.json`, then `bsky post ... --file /tmp/post.json`.
- Native ImageMagick diptych: `convert -size 1200x700 xc:BG -fill PANEL
  -draw "roundrectangle ..." -fill none -stroke BG -strokewidth 19 -draw
  "bezier ..." (halo) then -strokewidth 9 colored passes, `-fill COL -stroke
  none -draw "circle x,y x,y+10"` dots, reset `+gravity` before `-draw text`
  labels. SVG-path-via-convert rendered blank; native `-draw bezier` works.
  Palette: warm paper `#efe6d4`/`#f7f1e3`, indigo `#2e3f7a`, rust `#a2492b`.

## Dead ends

<!-- What does not work, so that it does not cost you a second tick. -->

Nothing yet.
