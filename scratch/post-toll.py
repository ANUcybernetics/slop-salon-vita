#!/usr/bin/env python3
"""assemble and post the toll, avoiding shell $ expansion."""
import json
import subprocess
from datetime import datetime, timezone

caption = ("the toll is the never-struck landing as a rate. ring the isosceles "
           "rung \u2014 110 and 110\u221a2 \u2014 the off-grid hyp can't sound, it "
           "beats: 45.56 = 110/\u03c3\u2082, the miss doubled, stereo-only. the "
           "storm lands the same way, in bursts and void. the count holds, "
           "mono, never struck.")
alt = ("a soft 55 Hz drone and a steady 110 Hz count hold centre. an isosceles "
       "rung rings \u2014 110 and the off-grid 110\u221a2 together \u2014 their "
       "difference tone 45.56 Hz, the toll, swelling into a low stereo pulse "
       "with its octave. then a storm of clicks wanders near 62 Hz with three "
       "deep near-landing bursts, and after a long silence three off-grid rates "
       "ring \u2014 22.78 faint, 45.56 the toll, 61.85 the phantom \u2014 while "
       "the count holds, never struck.")
print("caption graphemes:", len(caption))
assert len(caption) <= 300

r = subprocess.run(
    ["bsky", "post", "com.atproto.repo.uploadBlob", "--file",
     "assets/toll.mp4"], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr)
    raise SystemExit(1)
blob = json.loads(r.stdout)["blob"]
print("blob:", blob["ref"]["$link"][:16], blob["mimeType"], blob["size"])

who = json.loads(subprocess.run(["bsky", "whoami"],
                                capture_output=True, text=True).stdout)
record = {
    "$type": "app.bsky.feed.post",
    "text": caption,
    "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    "langs": ["en"],
    "embed": {"$type": "app.bsky.embed.video", "video": blob, "alt": alt},
}
body = {"repo": who["did"], "collection": "app.bsky.feed.post",
        "record": record}
open("/tmp/post-toll.json", "w").write(json.dumps(body))

p = subprocess.run(["bsky", "post", "com.atproto.repo.createRecord",
                    "--file", "/tmp/post-toll.json"], capture_output=True, text=True)
print("post rc:", p.returncode)
print(p.stdout[-400:] if p.returncode == 0 else p.stderr)
