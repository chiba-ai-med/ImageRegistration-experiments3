# Paper Takeaway — ImageRegistration-experiments3

Claims this repository contributes to the guidedPLS manuscript via **Fig. 3 — Spatial omics / Image registration** (single combined figure: slices in A, brain bar plot in B, kidney bar plot in C):

1. **The cross-modal MSI ↔ ST alignment task is not solved by standard optimal-transport baselines on either tissue.** On brain (47K source × 173 lipids → 40K target × 1,120 genes) and kidney (marker pair `FA.22.6 × Slc27a2`), qGW (ε ∈ 10^8…10^14), FRLC (rank ∈ {10, 20, 30, 50}), and LR-GW (rank ∈ {10, 20, 30, 50}) all yield mean CC ≈ 0. LR-GW additionally produces degenerate (all-NA) output on kidney.
2. **Classical image-registration baselines (ANTsPy rigid/affine, SITK rigid; sum-image or anatomy-driven) reach only modest CC ≈ 0.10–0.13 on brain and ≈ 0 on kidney**, confirming that simply aligning the two slices in image space is insufficient — the source and target have fundamentally different feature spaces.
3. **guidedPLS recovers biologically meaningful alignment on both tissues** (Fig. 3B brain, Fig. 3C kidney). Brain: mean CC ≈ 0.34, with per-marker CCs on HexCer reaching 0.65–0.73 and SM up to 0.68. Kidney: FA.22.6 × Slc27a2 reaches CC = 0.78 — the highest single-pair CC across both datasets.
4. **The two-tissue replication generalizes the guidedPLS story from sc / bulk multi-omics (sibling repos) to the spatial-omics setting**, supporting the manuscript's central claim that guide-based projection is broadly applicable across modality gaps where unsupervised OT and classical image registration both fail.
