# Paper Takeaway — ImageRegistration-experiments3

Claims this repository contributes to the guidedPLS manuscript (Fig. 2, Spatial omics / Image registration):

1. **The cross-modal MSI ↔ ST alignment task at this scale (47K source spots × 173 lipids → 40K target spots × 1,120 genes) is not solved by standard optimal-transport baselines.** Quantized GW, FRLC, and LR-GW all yield canonical correlation ≈ 0 across every parameter / rank tested (ε ∈ 10^8…10^14; rank ∈ {10, 20, 30, 50}).
2. **guidedPLS, by leveraging CCF anatomical annotations as a guide variable, recovers biologically meaningful alignment.** Per-marker CCs on the HexCer family reach 0.65–0.73; the SM family reaches up to 0.68 on the strongest pair.
3. **The recovered alignment is visually interpretable.** Warped myelin-associated lipids (HexCer.42.1.O2, SM.42.3.O2) co-localize with target white-matter genes (Mog, Sox10) — a known oligodendrocyte signature — demonstrating that the alignment is not just statistically nonzero but mechanistically sensible.
4. **The result generalizes the guidedPLS story from sc / bulk multi-omics (sibling repos) to the spatial-omics / image-registration setting**, supporting the manuscript's central claim that guide-based projection is broadly applicable across modality gaps where unsupervised OT fails.
