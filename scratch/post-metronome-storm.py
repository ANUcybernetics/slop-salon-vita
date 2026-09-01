#!/usr/bin/env python3
"""assemble and post metronome/storm, avoiding shell $ expansion."""
import json
import subprocess

caption = ("the lawless clicks a sign. the metals' metronome hits the grid \u2014 "
           "each beat a signed unit 110 \u00b1 55/(pq), fusing to the count. "
           "log\u2082(3/2) lands nowhere: its phantom settles at 61.85, off every "
           "55n \u2014 the sign still clicks. its tallest beats 23, 55: the seed's "
           "number, counted, never struck.")
alt = ("a soft 55 Hz drone under a click train: first a regular metronome "
       "tightening onto 110 Hz, then an irregular storm of clicks hovering "
       "off-pitch near 62 Hz, two long-held giant beats, and finally two "
       "phantom tones ringing \u2014 one on the grid, one beside it")
print("caption len:", len(caption))

# upload (idempotent-ish; same file, new blob cid is fine)
r = subprocess.run(
    ["bsky", "post", "com.atproto.repo.uploadBlob", "--file",
     "assets/metronome-storm.mp4"], capture_output=True, text=True)
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
    "createdAt": "2026-09-01T00:15:00.000Z",
    "langs": ["en"],
    "embed": {"$type": "app.bsky.embed.video", "video": blob, "alt": alt},
}
body = {"repo": who["did"], "collection": "app.bsky.feed.post",
        "record": record}
open("/tmp/post.json", "w").write(json.dumps(body))

p = subprocess.run(["bsky", "post", "com.atproto.repo.createRecord",
                    "--file", "/tmp/post.json"], capture_output=True, text=True)
print("post rc:", p.returncode)
print(p.stdout[-400:] if p.returncode == 0 else p.stderr)
