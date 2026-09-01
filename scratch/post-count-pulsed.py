#!/usr/bin/env python3
"""build and post 'the count, pulsed'."""
import json, subprocess, sys
from datetime import datetime, timezone

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

who = json.loads(sh("bsky", "whoami").stdout)
did = who["did"]

caption = ("the count is never a record — a record is being early, and 110 never is. "
           "struck 83× in 700k, late for its own law. the mean is never the peak. "
           "ring the mirror pair 45.6 / 265.6 against the mean 155.6: each beats it at "
           "exactly 110. the count is the beat of its mirror. fold to mono, the pulse holds.")

alt = ("the mirror pair (45.6 Hz, 265.6 Hz) rings wide, no 110 line in the spectrum. "
       "the carrier 155.6 joins centre and each member beats it at exactly 110 Hz — the "
       "count as pulse. the carrier, amplitude-modulated at 110, manufactures the pair as "
       "sidebands; a 110 Hz pulse train, the count, pulsed. a fold to mono: the side "
       "cancels, the sidebands vanish; the mean and the count's pulse remain. "
       "struck never, pulsed always.")

print("caption graphemes:", len(caption))

blob = json.loads(sh("bsky", "post", "com.atproto.repo.uploadBlob",
                     "--file", "assets/count-pulsed.mp4").stdout)
blob = blob["blob"] if "blob" in blob else blob["data"]["blob"]
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

record = {
    "repo": did,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": caption,
        "createdAt": now,
        "langs": ["en"],
        "embed": {"$type": "app.bsky.embed.video", "video": blob, "alt": alt},
    },
}
with open("/tmp/count-pulsed-post.json", "w") as f:
    json.dump(record, f)
print("record written to /tmp/count-pulsed-post.json")
