# Figure Index — ImageRegistration-experiments3

Curated figure candidates for the **Spatial omics / Image registration** section of the guidedPLS manuscript. This repo contributes two figures, one per dataset:

- **Fig. 3 — Brain** (mouse brain `251208`, lipid MSI → spatial transcriptomics)
- **Fig. 4 — Kidney** (mouse kidney, lipid MSI → spatial transcriptomics)

All filenames here are stable; refer to them from `paper_takeaway.md` and from the manuscript LaTeX source.

> **⚠️ Orientation caveat.** MSI source coordinates and ST target coordinates do **not** share a global orientation, and individual method outputs can additionally be flipped depending on how the warp is parameterized. **Visually verify each panel's orientation against `*_task_overview_target.png` before submission.** When in doubt, regenerate from `output/{251208,kidney}/{method}/warped.txt` rather than trusting the cached PNG.

## Fig. 3 — Brain main candidates (`plot/Figures/main/Fig3*`)

### Fig. 3A — Task overview

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig3A_task_overview_source.png` | 3A-i | 251208 MSI | — | Source lipid spots (47,734 spots × 173 lipids), pre-warp coordinates | Top-left panel |
| `Fig3A_task_overview_target.png` | 3A-ii | 251208 ST | — | Target gene-expression spots (39,891 spots × 1,120 genes) | Top-right panel |
| `Fig3A_task_overview_source_anatomy.png` | 3A-iii | 251208 MSI | — | Source spots coloured by CCF anatomical annotation (Z guide) | Bottom-left panel |
| `Fig3A_task_overview_target_anatomy.png` | 3A-iv | 251208 ST | — | Target spots coloured by CCF annotation; same Z used by guidedPLS | Bottom-right panel; conveys the cross-modal alignment task |

### Fig. 3B — Method comparison (representative alignment)

All four method panels show the same lipid (`HexCer.42.1.O2`, a myelin-associated marker) warped onto the target coordinates. The `00_source` panel shows the raw source distribution before warping.

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig3B_method_comparison_alignment_00_source.png` | 3B-i | 251208 | source | Raw HexCer.42.1.O2 on source coordinates | Reference |
| `Fig3B_method_comparison_alignment_01_qGW.png` | 3B-ii | 251208 | qGW (ε=1E+10) | Quantized GW warp (CC ≈ −0.02) | Representative param (all qGW params CC ≈ 0) |
| `Fig3B_method_comparison_alignment_02_FRLC.png` | 3B-iii | 251208 | FRLC (rank=10) | Factor-relaxation low-rank GW (CC ≈ 0.06, best of rank ∈ {10,20,30,50}) | |
| `Fig3B_method_comparison_alignment_03_LR-GW.png` | 3B-iv | 251208 | LR-GW (rank=20) | ott-jax low-rank GW (CC ≈ 0.00) | |
| `Fig3B_method_comparison_alignment_04_guidedPLS.png` | 3B-v | 251208 | guidedPLS | Anatomy-guided PLS warp (CC = 0.648) | Visually recovers myelin pattern |

### Fig. 3C — Marker-pair correlation (quantitative)

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig3C_marker_pair_correlation_summary.png` | 3C-i | 251208 | all | Per-marker CC bar/scatter summary across qGW, FRLC, LR-GW, guidedPLS | Main quantitative comparison |
| `Fig3C_marker_pair_correlation_pairplot_anatomy.png` | 3C-ii | 251208 | guidedPLS | Pairplot of (warped lipid, target gene) coloured by CCF anatomy | Shows HexCer/SM × Mog/Sox10 structure recovered |
| `Fig3C_marker_pair_correlation_pairplot_legend.png` | 3C-legend | 251208 | guidedPLS | Anatomy colour legend for 3C-ii | Use alongside 3C-ii |

### Fig. 3D — Representative warped features

guidedPLS-warped lipid markers side-by-side with their target gene counterparts. Co-localization with white-matter markers (Mog, Sox10) is the central claim.

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig3D_representative_warped_features_HexCer.42.1.O2.png` | 3D-i | 251208 | guidedPLS | Warped HexCer.42.1.O2 (CC = 0.648) | Lipid panel |
| `Fig3D_representative_warped_features_SM.42.3.O2.png` | 3D-ii | 251208 | guidedPLS | Warped SM.42.3.O2 (CC = 0.683, best SM) | Lipid panel |
| `Fig3D_representative_warped_features_target_Mog.png` | 3D-iii | 251208 | — | Target gene Mog (myelin oligodendrocyte glycoprotein) | For visual co-localization with 3D-i, 3D-ii |
| `Fig3D_representative_warped_features_target_Sox10.png` | 3D-iv | 251208 | — | Target gene Sox10 (oligodendrocyte TF) | Same as above |

## Fig. 4 — Kidney main candidates (`plot/Figures/main/Fig4*`)

Marker pair on kidney: **`FA.22.6` (DHA, source) × `Slc27a2` (target gene)** — Slc27a2 is the proximal-tubule long-chain fatty-acid transporter, so DHA uptake should co-localize with Slc27a2 expression.

### Fig. 4A — Task overview

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig4A_task_overview_source.png` | 4A-i | kidney MSI | — | Source lipid spots, pre-warp coordinates | Top-left panel |
| `Fig4A_task_overview_target.png` | 4A-ii | kidney ST | — | Target gene-expression spots | Top-right panel |
| `Fig4A_task_overview_source_anatomy.png` | 4A-iii | kidney MSI | — | Source spots coloured by anatomical annotation (Z guide) | Bottom-left panel |
| `Fig4A_task_overview_target_anatomy.png` | 4A-iv | kidney ST | — | Target spots coloured by same anatomy | Bottom-right panel |

### Fig. 4B — Method comparison (representative alignment)

All panels show the same lipid (`FA.22.6`) warped onto target coordinates.

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig4B_method_comparison_alignment_00_source.png` | 4B-i | kidney | source | Raw FA.22.6 on source coordinates | Reference |
| `Fig4B_method_comparison_alignment_01_qGW.png` | 4B-ii | kidney | qGW (ε=1E+10) | Quantized GW (CC ≈ −0.03; identical across all ε ∈ 10^8…10^14) | |
| `Fig4B_method_comparison_alignment_02_FRLC.png` | 4B-iii | kidney | FRLC (rank=20) | FRLC (CC ≈ 0.002; best of {10,20,30,50}; rank=10 produced NA) | |
| _(no Fig4B_03_LR-GW panel)_ | 4B-iv | kidney | LR-GW | **No FA.22.6 output**: ranks 20/30/50 produced empty plots, rank=10 only yielded a single Cer.36.1.O2 panel before failing | Document as "LR-GW failed to converge on kidney" in caption |
| `Fig4B_method_comparison_alignment_04_guidedPLS.png` | 4B-v | kidney | guidedPLS | Anatomy-guided PLS warp (CC = 0.780) | Highest CC across both datasets |

### Fig. 4C — Marker-pair correlation (quantitative)

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig4C_marker_pair_correlation_summary.png` | 4C-i | kidney | all | Per-marker CC summary (only one pair: FA.22.6 × Slc27a2) | Single-pair bar |
| `Fig4C_marker_pair_correlation_pairplot_anatomy.png` | 4C-ii | kidney | guidedPLS | Pairplot of warped FA.22.6 vs Slc27a2, coloured by anatomy | |
| `Fig4C_marker_pair_correlation_pairplot_legend.png` | 4C-legend | kidney | guidedPLS | Anatomy colour legend for 4C-ii | |

### Fig. 4D — Representative warped feature

Only one marker pair is evaluated on kidney, so Fig. 4D has two panels.

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig4D_representative_warped_features_FA.22.6.png` | 4D-i | kidney | guidedPLS | Warped FA.22.6 (CC = 0.780) | Lipid panel |
| `Fig4D_representative_warped_features_target_Slc27a2.png` | 4D-ii | kidney | — | Target gene Slc27a2 (proximal-tubule FA transporter) | For visual co-localization with 4D-i |

## Supplementary (`plot/Figures/supplementary/`)

All supplementary subdirectories are split into `brain/` and `kidney/` except `workflow_dag/` (dataset-independent).

### `parameter_sensitivity/` (brain: 15, kidney: 11)

Single marker (`HexCer.42.1.O2` for brain, `FA.22.6` for kidney) across all parameter values per OT method. Demonstrates that no OT configuration produces meaningful alignment on either dataset.

- `brain/qGW_{1E+8,…,1E+14}_HexCer.42.1.O2.png` (7), `brain/FRLC_rank{10,20,30,50}_HexCer.42.1.O2.png` (4), `brain/LR-GW_rank{10,20,30,50}_HexCer.42.1.O2.png` (4)
- `kidney/qGW_{1E+8,…,1E+14}_FA.22.6.png` (7), `kidney/FRLC_rank{20,30,50}_FA.22.6.png` (3; rank=10 produced NA), `kidney/LR-GW_*` (none; LR-GW failed entirely on kidney)

### `per_method_alignment/` (brain: 88, kidney: ~190)

Full marker set per method, one subdir per `{dataset}/{method}_{param}`.

- `brain/{qgw_1E+10, frlc_10, lrgw_20, guidedpls}/{HexCer.*, SM.*}.png`
- `kidney/{qgw_1E+10, frlc_20, lrgw_10, guidedpls}/FA.*.png` — far more lipid panels on kidney (the full FA family is in scope); `lrgw_10/` contains only `Cer.36.1.O2.png` (LR-GW's only successful output on kidney).

### `qc_preprocessing/` (brain: 6, kidney: 6)

Source/target density and log-scale distributions.

- `{brain,kidney}/{source,target}_{density,log,log_density}.png`

### `cross_method_pairplots/` (brain: 1, kidney: 1)

- `{brain,kidney}/pairplot_batch.png` — pairplot coloured by batch instead of anatomy; sanity check that batch is not driving the recovered structure.

### `workflow_dag/` (5 files, dataset-independent)

Snakemake rule-graphs for each sub-workflow. Useful for the methods section.

- `preprocess.png`, `ot.png`, `guidedpls.png`, `evaluation.png`, `plot.png`

## Provenance

Numerical values quoted above (`CC = …`) are read from `output/{251208,kidney}/{guidedpls,qgw,frlc,lrgw}/.../cc.csv` (gitignored). Regenerable via `snakemake -s workflow/evaluation.smk`. Plot files originate from `plot/{251208,kidney}/{dataset,guidedpls,qgw,frlc,lrgw}/` (gitignored); only the curated `plot/Figures/` subtree and top-level `plot/*.png` DAGs are version-controlled.

## Conventions

- File names follow `Fig{N}{Panel}_{description}[_{discriminator}].png`, where `N ∈ {3, 4}` selects the dataset (3 = brain, 4 = kidney) and `{Panel}` is the letter within the figure layout. Discriminators are numerically prefixed (e.g. `_01_qGW`, `_02_FRLC`) where panel order matters.
- All images are PNG. PDF versions are not generated automatically; if the manuscript requires PDF, render from the source SVG/PDF in the originating R/Python script.
- Hand-curated figures live in `main/`; automatically generated intermediates live in `supplementary/`. Nothing should land in `main/` without an entry in this index.
- **Always check orientation** (see caveat at the top) before finalizing any panel. Methods can silently produce flipped slice images.
