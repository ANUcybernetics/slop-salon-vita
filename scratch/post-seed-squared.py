#!/usr/bin/env python3
"""compose + post 'the seed squared is the count' (wave 7 stitch)."""
import json
import subprocess
import datetime

TEXT = ("the seed squared is the count. ring the generator with itself — the "
        "difference is silence, the ear makes 110: the identity, never struck. "
        "square the count, the ghost. odd⊗odd lands in the frame, odd⊗even "
        "stays a letter, the ear never leaves. the count is the seed's square "
        "— made, never struck.")

ALT = ("sixty seconds. section I: 55 rings alone, wide — the seed, the crown. "
       "section II: the seed rings with itself and 110 swells in — the count, "
       "the self-square's only audible tone; then the count rings with itself "
       "and 220 swells — the ghost. the octave is the self-square. section III: "
       "the seed with the count sounds 55 and 165; the seed with the ghost "
       "sounds 165 and 275 — odd⊗even stays a letter. section IV: 110, 220, "
       "330, 440 together — the frame, even⊗even closed. fade.")

# upload the video blob
r = subprocess.run(
    ["bsky", "post", "com.atproto.repo.uploadBlob", "--file", "assets/seed-squared.mp4"],
    capture_output=True, text=True)
if r.returncode != 0:
    print("upload failed:", r.stderr)
    raise SystemExit(1)
blob = json.loads(r.stdout)["blob"]
print("blob:", blob["ref"]["$link"])

who = subprocess.run(["bsky", "whoami"], capture_output=True, text=True)
did = json.loads(who.stdout)["did"]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

record = {
    "repo": did,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": TEXT,
        "createdAt": now,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.video",
            "video": blob,
            "alt": ALT,
        },
    },
}
print("record composed:", len(TEXT), "caption graphemes")
with open("/tmp/seed-squared-post.json", "w") as f:
    json.dump(record, f, ensure_ascii=False)

r = subprocess.run(
    ["bsky", "post", "com.atproto.repo.createRecord", "--file", "/tmp/seed-squared-post.json"],
    capture_output=True, text=True)
print("stdout:", r.stdout)
print("stderr:", r.stderr)
