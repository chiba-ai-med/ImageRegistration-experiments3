# Paper Takeaway — ImageRegistration-experiments3

Claims this repository contributes to the guidedPLS manuscript via **Fig. 3 — Spatial omics / Image registration** (single combined figure covering both brain and kidney):

1. **The cross-modal MSI ↔ ST alignment task is not solved by standard optimal-transport baselines on either tissue.** On brain (47K source × 173 lipids → 40K target × 1,120 genes) and kidney (marker pair `FA.22.6 × Slc27a2`), qGW (ε ∈ 10^8…10^14), FRLC (rank ∈ {10, 20, 30, 50}), and LR-GW (rank ∈ {10, 20, 30, 50}) all yield canonical correlation ≈ 0. LR-GW additionally produces degenerate (all-NA) output on kidney.
2. **guidedPLS recovers biologically meaningful alignment on both tissues** (Fig. 3C). Brain: per-marker CCs on HexCer reach 0.65–0.73, SM up to 0.68. Kidney: FA.22.6 (DHA) × Slc27a2 reaches CC = 0.78 — the highest single-pair CC across both datasets.
3. **The recovered alignment is anatomically structured** (Fig. 3B pairplots). Warped lipid–gene pairs separate cleanly along the CCF anatomical annotation used as the guide variable, indicating the alignment is not just statistically nonzero but mechanistically sensible (myelin lipids ↔ white-matter genes in brain; DHA ↔ proximal-tubule transporter in kidney).
4. **The two-tissue replication generalizes the guidedPLS story from sc / bulk multi-omics (sibling repos) to the spatial-omics setting**, supporting the manuscript's central claim that guide-based projection is broadly applicable across modality gaps where unsupervised OT fails.
