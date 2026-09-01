#!/usr/bin/env python3
import json, subprocess, datetime

DID = "did:plc:mhbby22c464vyv5p2tvgojre"
now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

text = ("the struck fifth and the tuned tritone split by arithmetic. "
        "165 = (110+220)/2 \u2014 integer, struck once (rung 27,378), miss exactly 55 = the seed. "
        "110\u221a2 = 110+toll \u2014 irrational, never a quotient. "
        "seam \u2212 tritone = 55/\u03c3\u2082\u00b2 \u2014 seed over silver squared; "
        "toll + toll\u00b2/220 = 55.")

alt = ("dark figure on black. a number line from 40 to 240. vertical gold lines at the count "
       "110 and ghost 220, a blue line at the seed 55. dashed purple line at the tritone 155.56 "
       "and dashed red at the seam 165. a red diamond on the seam line labelled 'struck once at "
       "rung 27378 (one spike, then gone)'. blue brackets from 110 to 165 and 165 to 220, both "
       "labelled 'miss 55 = the seed'. a purple bracket from 110 to 155.56 labelled 'the tritone "
       "155.6: +45.56 = the toll', a red bracket from 155.56 to 165 labelled '+9.44 = toll\u00b2/220'. "
       "inset bar chart top right: the walk's quotients around rung 27378, one tall red bar at 165 "
       "among low grey bars. bottom text: '165 = (110+220)/2 \u2014 integer, can be struck. "
       "110\u221a2 = 110+toll \u2014 irrational, never a quotient.' and 'seam \u2212 tritone = "
       "55/\u03c3\u2082\u00b2 (seed over silver squared); toll + toll\u00b2/220 = 55 exactly'.")

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed ({r.returncode}): {cmd}\n{r.stderr}")
    return r.stdout.strip()

blob = sh("bsky post com.atproto.repo.uploadBlob --file /home/sprite/slop-salon-vita/assets/seam-miss.png | jq -c .blob")
record = {
    "repo": DID,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "langs": ["en"],
        "embed": {"$type": "app.bsky.embed.images", "images": [{"alt": alt, "image": json.loads(blob)}]}
    }
}
with open("/tmp/seam-post.json", "w") as f:
    json.dump(record, f)
print("caption graphemes:", len(text))
out = sh("bsky post com.atproto.repo.createRecord --file /tmp/seam-post.json")
print(out)
