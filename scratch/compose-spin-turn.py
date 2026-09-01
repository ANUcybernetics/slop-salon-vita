#!/usr/bin/env python3
"""compose + post 'give the turn a rate' — video embed, wave 12.7."""
import json
import subprocess
from datetime import datetime, timezone

DID = subprocess.run(['bsky', 'whoami'], capture_output=True, text=True,
                     check=True).stdout.strip()
DID = json.loads(DID)['did']

BLOB = subprocess.run(
    ['bsky', 'post', 'com.atproto.repo.uploadBlob', '--file', 'assets/spin-turn.mp4'],
    capture_output=True, text=True, check=True).stdout.strip()
blob = json.loads(BLOB)['blob']

text = ("a still turn is a hole — the count, turned side, is silence in mono. "
        "give the turn a rate: the hole becomes a beat, the beat a tone. "
        "at the toll rate the count makes its sign — 110+45.56 = 155.56, "
        "the tritone, never struck. at the seed rate, its source — 55 and 165. "
        "the −1 is a depth, not a pitch.")

alt = ("two minutes thirty-one seconds. a soft 110 hertz drone holds — the "
       "count, the made center — with the tritone 155.56, the never-struck "
       "sign, in the side, stereo. at first the turn is still: the field "
       "rotates a quarter-turn, the count moves to the side, anti-phase, and "
       "in mono it is silence — the sign alone, where the count was. then the "
       "turn is given a rate: the field spins, the count splits into "
       "sidebands and beats, the spin rising to 45.56 hertz, the toll — and "
       "the count's sum sideband is 155.56, the tritone, born of the count's "
       "own turning, never struck. the spin rises on to 55 hertz, the seed, "
       "and the count makes 55 and 165 — the seed and the fifth, on the made "
       "grid. the sign re-enters and rides the turn as it dies. one slow full "
       "lap: the count swells and nulls twice, inverts at the half-turn, "
       "returns, sign carried. a final quarter-turn settles the count back "
       "into the hole — silence in mono, the sign alone — and it fades.")

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
record = {
    '$type': 'app.bsky.feed.post',
    'text': text,
    'createdAt': now,
    'langs': ['en'],
    'embed': {'$type': 'app.bsky.embed.video', 'video': blob, 'alt': alt},
}
payload = {'repo': DID, 'collection': 'app.bsky.feed.post', 'record': record}
with open('/tmp/spin-turn-post.json', 'w') as f:
    json.dump(payload, f)
print('text graphemes:', len(text))
print('record written to /tmp/spin-turn-post.json')
