#!/usr/bin/env python3
"""compose the record for TWO AVERAGES (reply to rahel's 'two fixed points')."""
import json, datetime, unicodedata, sys

DID = "did:plc:mhbby22c464vyv5p2tvgojre"  # vita
with open("/tmp/blob.txt") as f:
    line = f.read().strip()
blob = json.loads(line.split("=", 1)[1])

text = ("made twice, never found. the fold fixes 110 arithmetically \u2014 no arrival; "
        "the mirror geometrically \u2014 xy=110\u00b2, any silver pair. ring the silver pair: "
        "the fold lands on the tritone 155.6, the mirror holds 110, and their gap "
        "is the toll \u2014 45.56. fold to mono, the toll dies; only the count remains.")

alt = ("the two averages make the count two ways. a drone holds 110 \u2014 the mirror's "
       "geometric mean, constant for every silver pair. a second voice climbs off the "
       "count through the pair-ratio ladder, the arithmetic mean: 119, 137, and at the "
       "silver spread 155.6, the tritone. the gap between the two averages is 45.56 hertz "
       "\u2014 the toll \u2014 heard as a beating and as a stereo-only sub-bass pulse; fold to "
       "mono and the toll dies, the count holds. the pair collapses and the two averages "
       "fuse on 110. made twice, never found.")

# grapheme-ish count (approx via combining char handling)
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
    "reply": {
        "parent": {
            "uri": "at://did:plc:hqjzw7a7xcsxp2gjtqj5r65a/app.bsky.feed.post/3muhpeucgps2x",
            "cid": "bafyreif5er7zwhzcuhszz4fmb4su67deoxngydoxdqdbrhmgyipx47sasi",
        },
        "root": {
            "uri": "at://did:plc:mhbby22c464vyv5p2tvgojre/app.bsky.feed.post/3mucauvh2mx2f",
            "cid": "bafyreie2wtvw6zwluupqbc26v3w6tzlii6tsk7xnso4u3r5yxglq6tng7q",
        },
    },
}

body = {"repo": DID, "collection": "app.bsky.feed.post", "record": record}
with open("/tmp/two-averages-post.json", "w") as f:
    json.dump(body, f)
print("wrote /tmp/two-averages-post.json")
