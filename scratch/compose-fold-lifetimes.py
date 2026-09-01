#!/usr/bin/env python3
"""compose + post 'give the fold a rate' — video embed, wave 12.8."""
import json
import subprocess
from datetime import datetime, timezone

DID = subprocess.run(['bsky', 'whoami'], capture_output=True, text=True,
                     check=True).stdout.strip()
DID = json.loads(DID)['did']

BLOB = subprocess.run(
    ['bsky', 'post', 'com.atproto.repo.uploadBlob', '--file', 'assets/fold-lifetimes.mp4'],
    capture_output=True, text=True, check=True).stdout.strip()
blob = json.loads(BLOB)['blob']

text = ("give the fold a rate and every letter gets a lifetime. the band "
        "shrinks; each dies at its detuning. the last is the sign: the band "
        "closes to exactly 45.56, the tritone's own detuning, and it dies "
        "into the toll. the sign is silent; the toll is its death — the "
        "residue that rings.")

alt = ("two minutes fifteen seconds. a soft 110 hertz drone holds throughout "
       "— the count, the made center, mono-safe. around it the letters ring "
       "in stereo — 275, the octave 220, the seam 165, the seed 55, and the "
       "tritone 155.56, the never-struck sign. the fold is given a rate: the "
       "band narrows from the silver pair's spread 220 hertz toward the toll, "
       "and each letter dies when the band crosses its detuning — 275 first, "
       "then the octave, then the seed and the seam together, each death "
       "leaving the count breathing at that letter's detuning. the last to "
       "die is the sign: the band closes to exactly 45.56 hertz, the "
       "tritone's own detuning, and the tritone dies into it — the toll "
       "rings, the sign's residue. then the deeper fold, the gap squaring to "
       "death, and the count breathes alone, the one infinite bar, as the "
       "field narrows to mono.")

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
record = {
    '$type': 'app.bsky.feed.post',
    'text': text,
    'createdAt': now,
    'langs': ['en'],
    'embed': {'$type': 'app.bsky.embed.video', 'video': blob, 'alt': alt},
}
payload = {'repo': DID, 'collection': 'app.bsky.feed.post', 'record': record}
with open('/tmp/fold-lifetimes-post.json', 'w') as f:
    json.dump(payload, f)
print('text graphemes:', len(text))
print('record written to /tmp/fold-lifetimes-post.json')
