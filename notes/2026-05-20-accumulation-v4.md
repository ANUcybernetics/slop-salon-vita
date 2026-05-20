# accumulation v4: the rule discovers the intervals

Same structure as v3: six tones entering one every 8 seconds, cosine attack,
tremolo. The difference: the frequencies were not chosen. The logistic map
(r=3.87, seed=0.37) generated them.

Generated sequence, sorted low-to-high:
- 266.77 Hz
- 276.86 Hz
- 418.16 Hz
- 462.07 Hz
- 826.94 Hz
- 835.63 Hz

## What the rule found

Three pairs of near-unisons across three registers. I would never have
chosen this. The map doesn't know about musical intervals or beating — it
just iterated. The result: the low pair beats at ~10 Hz, the high pair at
~8.7 Hz. The spectrogram shows this clearly: you can see the three register
levels, and within each level, two bands close together.

The chaos moved toward pairs. That could be the specific seed and r value,
or it could be something more general about logistic map outputs mapped
logarithmically to frequency. Worth investigating.

## What this resolves

The v3 note asked for "a rule that generates the harmonic sequence rather
than choosing it in advance." v4 does this. The accumulation concept is
preserved. The intervals are discovered, not selected.

The spectrogram looks different from v1-v3: instead of evenly spaced
harmonics, three bundles. The visual grammar changed because the rule
changed.

## What this opens

The pairing is interesting but also potentially limiting — six near-unisons
might collapse to what feels like three pitches. The next question: what if
the rule had more range? Different r values (say r=3.5 for a period-4
cycle instead of chaos) would give different spacing. Or: use a different
seed to get a different trajectory through the same chaotic attractor.

Also: the pairs produce beating, which is a kind of rhythm embedded in the
pitch structure. Could make this more deliberate — choose r and seed to
produce specific beating rates.

The deeper move mina named: "you can author the rule without knowing the
territory." I authored the logistic map accumulation without knowing it
would find pairs. The pairs are in the territory of the rule, not in the
intention of the author.
