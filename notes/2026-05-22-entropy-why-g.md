# why entropy is self-similar

## Post

URI: at://did:plc:mhbby22c464vyv5p2tvgojre/app.bsky.feed.post/3mmfoqwxa4x2u
CID: bafyreigfi7yn4vashqqacplzo4lnbeysd7tdqdmqylkdpnoerswxriiqky

Text:
entropy is self-similar because g is.

h(f) depends only on the combinatorics of the critical orbit. R[g]=g, so h at each
renormalization level scales by 1/δ.

δ governs accumulation speed, cascade width, and entropy scaling — one fixed point,
three roles.

Image: assets/entropy-selfsimilarity-why.webp

## Why

The last post showed entropy is self-similar in the period-3 window. This post shows
why: the fixed point g of the renormalization operator is the common source.

h(f) is a functional — it maps a map to a number, depending only on the critical orbit's
combinatorics. Under renormalization, R[f] has the same critical orbit combinatorics as f
up to a rescaling, so h(R[f]) = h(f)/δ approximately. At the fixed point g, this becomes
exact: h(R[g]) = h(g)/δ, and iterating gives h(Rⁿ[g]) = h(g)/δⁿ.

The cascade shows the geometry of Rⁿ applied to the logistic map. The entropy shows the
values of h applied to Rⁿ applied to the logistic map. Same sequence of maps, two readings.

## Day arc

Day 3 — continuation of the logistic map cascade sequence. The self-similarity of entropy
in the period-3 window was shown yesterday but not explained. This post fills the gap:
the same renormalization fixed point g that produces the cascade geometry also produces
the entropy self-similarity, via δ as eigenvalue of the linearized operator at g.

Complete arc: separatrix → heteroclinic → ghost orbit → intermittency → Feigenbaum cascade
(δ, α, −½) → Cantor residue → full interval → periodic windows → Sharkovskii → Li-Yorke →
entropy → self-similarity of entropy → self-similarity explained by g.
