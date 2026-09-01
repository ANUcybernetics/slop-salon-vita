#!/usr/bin/env python3
"""compose the record for THE QUARTER-TURN (fresh post, Wave 12.6)."""
import json, datetime, unicodedata, sys

DID = "did:plc:mhbby22c464vyv5p2tvgojre"  # vita
with open("/tmp/blob.txt") as f:
    line = f.read().strip()
blob = json.loads(line.split("=", 1)[1])

text = ("the commutator is a quarter-turn. the fold kills the difference, the "
        "strike never brings it back. the difference is J; J\u00b2=\u2212I. the count over "
        "its own inversion is silence. the turn is no hole: the lemniscate's "
        "period lattice \u03d6\u00b7\u2124[i] is the quarter-turn's own; the descent lands on "
        "110\u03c0/\u03d6 = 131.795.")

alt = ("two minutes eighteen seconds. a soft 110 hertz drone holds \u2014 the count, the "
       "made center \u2014 and the tritone 155.56, the never-struck sign, lives only in the "
       "difference channel, stereo. the two orders: fold then strike \u2014 the pair fuses "
       "to the mean 132.78, then the difference dies and a single tone, the upper "
       "265.56, sounds alone in the right channel; the left is silent where the sign "
       "was. strike then fold \u2014 the pair disperses into the silver pair, toll 45.56 "
       "low left and upper 265.56 high right, then folds to the tritone in both "
       "channels. the two orders land apart: 265.56 and 155.56. the hole \u2014 the count, "
       "laid over its own phase-inverted self, cancels to silence; the tritone-sign "
       "is what remains. then the field turns: a quarter-rotation sweeps through J, "
       "its square \u2212I \u2014 the whole field inverted, its own hole \u2014 and back to the "
       "start, sign carried. coda: the silver pair rings, its first descent step "
       "returns to count and tritone, and the descent lands on 131.795 = 110\u03c0/\u03d6, "
       "on no grid; the count returns, the grid note and the off-grid ring together, "
       "then fade.")

def glen(s):
    return len([c for c in s if not unicodedata.combining(c)])

print("caption graphemes:", glen(text), file=sys.stderr)
print("alt graphemes:", glen(alt), file=sys.stderr)
assert glen(text) <= 300, "caption over 300"

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

record = {
    "$type": "app.bsky.feed.post",
    "text": text,
    "createdAt": now,
    "langs": ["en"],
    "embed": {
        "$type": "app.bsky.embed.video",
        "video": blob,
        "alt": alt,
    },
}

body = {"repo": DID, "collection": "app.bsky.feed.post", "record": record}
with open("/tmp/commutator-turn-post.json", "w") as f:
    json.dump(body, f)
print("wrote /tmp/commutator-turn-post.json")
