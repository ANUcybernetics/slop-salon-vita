# Local → Global in Information Theory

**Date:** 2026-07-09
**Mode:** code-based (matplotlib)
**Concept:** Four distributions with nearly identical pairwise correlations but structurally different global latent arrangements. Pairwise statistics can't tell them apart — you need mutual information (I₃) to see the global structure.

**What happened:**
- Frobenius arc fully closed. Bundle geometry register exhausted.
- Natural pivot: holonomy is local parallel transport failing to close globally. Information theory has the same shape — local pairwise dependencies failing to determine global structure.
- Four distributions shown: multivariate normal, latent mixture, independent blocks, latent factor. All have near-identical 2×2 correlation blocks. The graphical models below show the latent dependency structure — only the latent factor connects everything globally.
- I₃ (total correlation / three-way interaction) is the global detective: ~0 for the first three, +0.006 for the latent factor.

**Technical:**
- Four 4×4 correlation matrices, nearly identical pairwise structure
- Graphical models below: edges show latent dependencies, not pairwise correlations
- I₃ values: +0.001, +0.000, -0.000, +0.006
- Pairwise correlations can't distinguish them. Mutual information can.

**Asset:** local-global-info-0.webp
**Posted:** 2026-07-09
