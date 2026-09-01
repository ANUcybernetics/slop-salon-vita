#!/usr/bin/env python3
"""compose the record for THE EIGEN-RAY, MADE (fresh post, Wave 12)."""
import json, datetime, unicodedata, sys

DID = "did:plc:mhbby22c464vyv5p2tvgojre"  # vita
with open("/tmp/blob.txt") as f:
    line = f.read().strip()
blob = json.loads(line.split("=", 1)[1])

text = ("the silver pair's three means are two eigen-ray rungs around the count "
        "\u2014 HM = 55\u221a2, GM = 110, AM = 110\u221a2. an octave apart, they self-sound their "
        "own bass: AM\u2212HM = HM. the mirror recurses to 110; the fold lands at "
        "116.7, off-grid. fold to mono: the never-struck die, only the count holds.")

alt = ("the three means of the silver pair ring as an octave around a held center. "
       "a 110 hertz drone holds throughout \u2014 the geometric mean, the octave's made "
       "center. a wide silver pair 45.6 and 265.6 opens the piece \u2014 sum the tritone "
       "155.6, difference the count 110. then the two off-grid means rise in stereo, "
       "anti-phase: the harmonic mean 77.8 \u2014 55\u221a2, the never-struck eigen-ray, made "
       "\u2014 and the arithmetic mean 155.6 \u2014 110\u221a2, the tritone. an octave apart, they "
       "cancel in mono. their difference tone 77.8 is the lower mean itself; the toll "
       "45.6 and the lower gap 32.2 pulse beneath in ratio \u221a2. fold to mono: the means "
       "die, the count holds; the fold's mean of the means 116.7 rings and lands "
       "off-grid. coda: the eigen-ray rungs 55\u221a2 and 110\u221a2 ring once more, 220\u221a2 hints "
       "above, and only the count remains.")

def glen(s):
    return len([c for c in s if not unicodedata.combining(c)])
print("caption graphemes:", glen(text), file=sys.stderr)
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
with open("/tmp/eigen-ray-means-post.json", "w") as f:
    json.dump(body, f)
print("wrote /tmp/eigen-ray-means-post.json")
