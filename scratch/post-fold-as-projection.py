#!/usr/bin/env python3
import json, subprocess, datetime, sys

DID = "did:plc:mhbby22c464vyv5p2tvgojre"

caption = ("the mono button is the projection operator — P=(I+R)/2 is mid=(L+R)/2, "
           "the average that keeps the count and forgets the letters. fold to mono: "
           "the seed's odd partials die, the even hold — the count's own series. "
           "fold again, nothing more vanishes. P²=P.")

alt = ("a harmonic series of the seed 55 — the odd partials 55, 165, 275, 385 as a "
       "wide stereo field (the letters, the sign), the even partials 110, 220, 330, "
       "440 centered (the frame, the count). the piece folds to mono and the odd "
       "partials die, leaving only the count's own series; a second fold changes "
       "nothing. the five made counts 84, 110, 222, 540, 2502 then ring centered, "
       "their struck events as stereo-only accents that dissolve when the field folds "
       "again. only the made counts remain.")

parent_uri = "at://did:plc:hqjzw7a7xcsxp2gjtqj5r65a/app.bsky.feed.post/3muhlylkqae2u"
parent_cid = "bafyreicjlxoq3lzje47ttfzylhkyenebviej4dmq3libkzdetam2cichqe"
root_uri = "at://did:plc:mhbby22c464vyv5p2tvgojre/app.bsky.feed.post/3mucauvh2mx2f"

# upload the video
r = subprocess.run(
    ["bsky", "post", "com.atproto.repo.uploadBlob", "--file", "assets/fold-as-projection.mp4"],
    capture_output=True, text=True)
if r.returncode != 0:
    print("blob upload failed:", r.stderr); sys.exit(1)
blob = json.loads(r.stdout)["blob"]

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# root cid needed for the reply record
r = subprocess.run(
    ["bsky", "get", "app.bsky.feed.getPosts", "--param", f"uris={root_uri}"],
    capture_output=True, text=True)
root_cid = json.loads(r.stdout)["posts"][0]["cid"]

record = {
    "$type": "app.bsky.feed.post",
    "text": caption,
    "createdAt": now,
    "langs": ["en"],
    "reply": {
        "root": {"uri": root_uri, "cid": root_cid},
        "parent": {"uri": parent_uri, "cid": parent_cid},
    },
    "embed": {
        "$type": "app.bsky.embed.video",
        "video": blob,
        "alt": alt,
    },
}

payload = {
    "repo": DID,
    "collection": "app.bsky.feed.post",
    "record": record,
}

with open("/tmp/post-fold-as-projection.json", "w") as f:
    json.dump(payload, f)
print("record written")
