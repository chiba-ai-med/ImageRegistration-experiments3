# Figure Index — ImageRegistration-experiments3

Curated figure candidates for **Fig. 2 (Spatial omics / Image registration)** in the guidedPLS manuscript. Source dataset: mouse brain `251208`, lipid MSI (SL section 12) → spatial transcriptomics (ST section 32).

All filenames here are stable; refer to them from `paper_takeaway.md` and from the manuscript LaTeX source.

## Main figure candidates (`plot/Figures/main/`)

### Fig. 2A — Task overview

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig2A_task_overview_source.png` | 2A-i | 251208 MSI | — | Source lipid spots (47,734 spots × 173 lipids), pre-warp coordinates | Top-left panel |
| `Fig2A_task_overview_target.png` | 2A-ii | 251208 ST | — | Target gene-expression spots (39,891 spots × 1,120 genes) | Top-right panel |
| `Fig2A_task_overview_source_anatomy.png` | 2A-iii | 251208 MSI | — | Source spots colored by CCF anatomical annotation (Z guide) | Bottom-left panel |
| `Fig2A_task_overview_target_anatomy.png` | 2A-iv | 251208 ST | — | Target spots colored by CCF annotation; same Z used by guidedPLS | Bottom-right panel; conveys the cross-modal alignment task |

### Fig. 2B — Method comparison (representative alignment)

All four method panels show the same lipid (`HexCer.42.1.O2`, a myelin-associated marker) warped onto the target coordinates. The `00_source` panel shows the raw source distribution before warping.

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig2B_method_comparison_alignment_00_source.png` | 2B-i | 251208 | source | Raw HexCer.42.1.O2 on source coordinates | Reference |
| `Fig2B_method_comparison_alignment_01_qGW.png` | 2B-ii | 251208 | qGW (ε=1E+10) | Quantized GW warp (CC ≈ −0.02) | Representative param (all qGW params CC ≈ 0) |
| `Fig2B_method_comparison_alignment_02_FRLC.png` | 2B-iii | 251208 | FRLC (rank=10) | Factor-relaxation low-rank GW (CC ≈ 0.06, best of rank ∈ {10,20,30,50}) | |
| `Fig2B_method_comparison_alignment_03_LR-GW.png` | 2B-iv | 251208 | LR-GW (rank=20) | ott-jax low-rank GW (CC ≈ 0.00) | |
| `Fig2B_method_comparison_alignment_04_guidedPLS.png` | 2B-v | 251208 | guidedPLS | Anatomy-guided PLS warp (CC = 0.648) | Visually recovers myelin pattern |

### Fig. 2C — Marker-pair correlation (quantitative)

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig2C_marker_pair_correlation_summary.png` | 2C-i | 251208 | all | Per-marker CC bar/scatter summary across qGW, FRLC, LR-GW, guidedPLS | Main quantitative comparison |
| `Fig2C_marker_pair_correlation_pairplot_anatomy.png` | 2C-ii | 251208 | guidedPLS | Pairplot of (warped lipid, target gene) coloured by CCF anatomy | Shows HexCer/SM × Mog/Sox10 structure recovered |
| `Fig2C_marker_pair_correlation_pairplot_legend.png` | 2C-legend | 251208 | guidedPLS | Anatomy colour legend for 2C-ii | Use alongside 2C-ii |

### Fig. 2D — Representative warped features

guidedPLS-warped lipid markers side-by-side with their target gene counterparts. Co-localization with white-matter markers (Mog, Sox10) is the central claim.

| File | Candidate panel | Dataset | Method | What it shows | Notes |
|---|---|---|---|---|---|
| `Fig2D_representative_warped_features_HexCer.42.1.O2.png` | 2D-i | 251208 | guidedPLS | Warped HexCer.42.1.O2 (CC = 0.648) | Lipid panel |
| `Fig2D_representative_warped_features_SM.42.3.O2.png` | 2D-ii | 251208 | guidedPLS | Warped SM.42.3.O2 (CC = 0.683, best SM) | Lipid panel |
| `Fig2D_representative_warped_features_target_Mog.png` | 2D-iii | 251208 | — | Target gene Mog (myelin oligodendrocyte glycoprotein) | For visual co-localization with 2D-i, 2D-ii |
| `Fig2D_representative_warped_features_target_Sox10.png` | 2D-iv | 251208 | — | Target gene Sox10 (oligodendrocyte TF) | Same as above |

## Supplementary (`plot/Figures/supplementary/`)

### `parameter_sensitivity/` (15 files)

`HexCer.42.1.O2` across all parameter values per OT method. Demonstrates that no qGW (ε ∈ 10^8…10^14), FRLC (rank ∈ {10,20,30,50}), or LR-GW (rank ∈ {10,20,30,50}) configuration produces meaningful alignment.

- `qGW_{1E+8,…,1E+14}_HexCer.42.1.O2.png` (7 files)
- `FRLC_rank{10,20,30,50}_HexCer.42.1.O2.png` (4 files)
- `LR-GW_rank{10,20,30,50}_HexCer.42.1.O2.png` (4 files)

### `per_method_alignment/` (88 files, ~12 MB)

Full HexCer + SM marker set per method (one subdir per method). Allows direct visual inspection of any marker not chosen for the main figure.

- `qgw_1E+10/`, `frlc_10/`, `lrgw_20/`, `guidedpls/`

### `qc_preprocessing/` (6 files)

Source/target density and log-scale distributions used for preprocessing QC.

- `{source,target}_density.png`, `{source,target}_log.png`, `{source,target}_log_density.png`

### `cross_method_pairplots/` (1 file)

- `pairplot_batch.png` — pairplot coloured by batch instead of anatomy; sanity check that batch is not driving the recovered structure.

### `workflow_dag/` (5 files)

Snakemake rule-graphs for each sub-workflow. Useful for the methods section.

- `preprocess.png`, `ot.png`, `guidedpls.png`, `evaluation.png`, `plot.png`

## Provenance

Numerical values quoted above (`CC = …`) are read from `output/251208/{guidedpls,qgw,frlc,lrgw}/.../cc.csv` (gitignored). Regenerable via `snakemake -s workflow/evaluation.smk`. Plot files originate from `plot/251208/{dataset,guidedpls,qgw,frlc,lrgw}/` (gitignored); only the curated `plot/Figures/` subtree and top-level `plot/*.png` DAGs are version-controlled.

## Conventions

- File names follow `Fig2{Panel}_{description}[_{discriminator}].png`. The `{Panel}` letter matches the manuscript figure layout. Discriminators are numerically prefixed (e.g. `_01_qGW`, `_02_FRLC`) where panel order matters.
- All images are PNG. PDF versions are not generated automatically; if the manuscript requires PDF, render from the source SVG/PDF in the originating R/Python script.
- Hand-curated figures live in `main/`; automatically generated intermediates live in `supplementary/`. Nothing should land in `main/` without an entry in this index.
