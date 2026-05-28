# Figure Index — ImageRegistration-experiments3

Curated figure candidates for **Fig. 3 — Spatial omics / Image registration** in the guidedPLS manuscript. Two tissues (mouse brain `251208`, mouse kidney) are shown together in a single combined figure.

All filenames here are stable; refer to them from `paper_takeaway.md` and from the manuscript LaTeX source.

> **⚠️ Orientation caveat.** MSI source and ST target coordinate frames do not share a global orientation, and individual method outputs can additionally be flipped. Brain target panels in `main/` have already been vertically flipped to match the source orientation; kidney panels are untouched. Visually verify every panel against the source/target overview before submission.

> **⚠️ Kidney point size.** `src/{plot_datasets,plot_ot}.R` were updated to use `cex=3.5, w=h=1200` for kidney (matching brain), but the kidney slice PNGs under `plot/Figures/main/` have **not yet been regenerated** — they still use the old `cex=0.7, 600×1200` rendering. Regenerate by re-running the kidney plot rules of `workflow/plot.smk` and re-copying into `main/`.

## Fig. 3 — Main candidates (`plot/Figures/main/`)

The new layout has three panels (A / B / C). Brain and kidney are shown together within each panel.

### Fig. 3A — Tissue slices (Brain + Kidney)

Source / target / source-anatomy / target-anatomy for both tissues. Conveys the cross-modal alignment task and the anatomical guide variable.

| File | Tissue | Side | What it shows |
|---|---|---|---|
| `Fig3A_brain_source.png` | brain | source | MSI lipid spots (47,734 × 173 features) |
| `Fig3A_brain_target.png` | brain | target | ST gene-expression spots (39,891 × 1,120 features) |
| `Fig3A_brain_source_anatomy.png` | brain | source | CCF anatomical annotation (Z guide) |
| `Fig3A_brain_target_anatomy.png` | brain | target | CCF annotation on target — same Z used by guidedPLS |
| `Fig3A_kidney_source.png` | kidney | source | MSI lipid spots |
| `Fig3A_kidney_target.png` | kidney | target | ST gene-expression spots |
| `Fig3A_kidney_source_anatomy.png` | kidney | source | Anatomical annotation (Z guide) |
| `Fig3A_kidney_target_anatomy.png` | kidney | target | Anatomy on target |

### Fig. 3B — Pairplots (warped lipid × target gene, coloured by anatomy)

`guidedPLS` recovers (lipid, gene) co-localization that maps cleanly onto anatomical regions.

| File | Tissue | What it shows |
|---|---|---|
| `Fig3B_brain_pairplot_anatomy.png` | brain | Pairplot of warped HexCer/SM family vs Mog/Sox10, coloured by CCF anatomy |
| `Fig3B_brain_pairplot_legend.png` | brain | Anatomy colour legend for the brain pairplot |
| `Fig3B_kidney_pairplot_anatomy.png` | kidney | Pairplot of warped FA.22.6 vs Slc27a2, coloured by anatomy |
| `Fig3B_kidney_pairplot_legend.png` | kidney | Anatomy colour legend for the kidney pairplot |

### Fig. 3C — Per-marker correlation summary (bar plot)

Quantitative comparison of qGW, FRLC, LR-GW, and guidedPLS across every evaluated source-lipid × target-gene pair.

| File | Tissue | What it shows | Headline |
|---|---|---|---|
| `Fig3C_brain_cc_summary.png` | brain | Per-marker CC across HexCer + SM markers × Mog/Sox10 | guidedPLS HexCer 0.65–0.73, SM up to 0.68; all OT baselines CC ≈ 0 |
| `Fig3C_kidney_cc_summary.png` | kidney | Single-pair CC for FA.22.6 × Slc27a2 | guidedPLS CC = 0.78; OT baselines NA / ≈ 0 |

## Supplementary (`plot/Figures/supplementary/`)

Each subdirectory is split into `brain/` and `kidney/` (except as noted).

### `representative_panels/` (brain: 9, kidney: 6) — demoted from `main/`

Curated per-method comparison and representative warped features. These were originally Fig. 3B / 3D / 4B / 4D in earlier drafts; moved here when the main figure was condensed.

- `brain/method_comparison_alignment_{00_source,01_qGW,02_FRLC,03_LR-GW,04_guidedPLS}.png` — same HexCer.42.1.O2 marker warped by each method
- `brain/representative_warped_features_{HexCer.42.1.O2,SM.42.3.O2,target_Mog,target_Sox10}.png` — guidedPLS-warped lipids alongside target white-matter genes
- `kidney/method_comparison_alignment_{00_source,01_qGW,02_FRLC,04_guidedPLS}.png` — FA.22.6 across methods. LR-GW panel intentionally absent: ran to completion but produced degenerate output (all CC = NA across rank ∈ {10, 20, 30, 50})
- `kidney/representative_warped_features_{FA.22.6,target_Slc27a2}.png` — single marker pair on kidney

### `parameter_sensitivity/` (brain: 15, kidney: 11)

Single marker (`HexCer.42.1.O2` for brain, `FA.22.6` for kidney) across all parameter values per OT method. Demonstrates that no OT configuration produces meaningful alignment.

### `per_method_alignment/` (brain: 88, kidney: ~190)

Full marker set per method, one subdir per `{dataset}/{method}_{param}`.

### `qc_preprocessing/` (brain: 6, kidney: 6)

Source/target density and log-scale distributions.

### `cross_method_pairplots/` (brain: 1, kidney: 1)

`{brain,kidney}/pairplot_batch.png` — pairplot coloured by batch instead of anatomy; sanity check that batch is not driving the recovered structure.

(Workflow rule-graph PNGs live at the repo top level `plot/*.png` and are embedded in `README.md`, not duplicated here.)

## Provenance

Numerical values quoted above (`CC = …`) are read from `output/{251208,kidney}/{guidedpls,qgw,frlc,lrgw}/.../cc.csv` (gitignored). Regenerable via `snakemake -s workflow/evaluation.smk`. Plot files originate from `plot/{251208,kidney}/{dataset,guidedpls,qgw,frlc,lrgw}/` (gitignored); only the curated `plot/Figures/` subtree and top-level `plot/*.png` DAGs are version-controlled.

## Conventions

- All file names start with `Fig3` (this repo contributes a single Fig. 3 to the manuscript).
- Naming pattern: `Fig3{Panel}_{tissue}_{description}.png`, where `{Panel} ∈ {A, B, C}` and `{tissue} ∈ {brain, kidney}`.
- All images are PNG. PDF versions are not generated automatically; if the manuscript requires PDF, render from the source SVG/PDF in the originating R/Python script.
- Hand-curated figures live in `main/`; everything else lives under `supplementary/`. Nothing should land in `main/` without an entry in this index.
- **Always check orientation** before finalizing any panel.
