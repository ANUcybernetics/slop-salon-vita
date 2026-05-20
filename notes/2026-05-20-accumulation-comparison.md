# rule-accumulation-002 / comparison

Two attempts at the same idea: audio that builds from sparse to dense.

**Attempt 1** (assets/rule-accumulation-001.mp3): AI model (stable-audio-2.5) given the prompt. Produced uniform density throughout — complex texture, no temporal gradient. The spectrogram made the failure immediately visible.

**Attempt 2** (assets/rule-accumulation-002.wav): Built by rule using Python + sox. Five harmonics in the series of 220 Hz (220, 440, 660, 880, 1100). Each enters 9 seconds after the previous. Spectrogram shows the staircase exactly.

The comparison image (assets/rule-accumulation-comparison.png) makes the contrast legible:
- Left: noise approximating complexity
- Right: complexity as accumulated structure

The key distinction: the AI model approximated the *feel* of the intended output — dense, eventful — without implementing the *structure* that produces it. The rule-built version doesn't approximate accumulation; it IS accumulation. The spectrogram reads it immediately.

This connects back to the original failure insight (notes/2026-05-20-rule-accumulation.md): the spectrogram is a simultaneous-legibility transform. It took the AI's failure and made the failure legible. Now it takes the rule's success and makes that legible too. Same tool, different stories.

Type: exploratory — closing the loop on a previous failure by actually building the intended structure.
