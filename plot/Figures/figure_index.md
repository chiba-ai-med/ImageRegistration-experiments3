# Figure Index — ImageRegistration-experiments3

Curated figure candidates for **Fig. 3 — Spatial omics / Image registration** in the guidedPLS manuscript. Two tissues (mouse brain `251208`, mouse kidney) are presented across nine panel groups (A–I); brain and kidney are kept in **separate** panels, never mixed in a single bar.

All filenames here are stable; refer to them from `paper_takeaway.md` and from the manuscript LaTeX source.

> **⚠️ Orientation caveat.** MSI source and ST target coordinate frames do not share a global orientation, and individual method outputs can additionally be flipped. Brain target panels in `main/` have already been vertically flipped to match the source orientation; kidney panels are untouched. Visually verify every panel against the source/target overview before submission.

## Fig. 3 — Main candidates (`plot/Figures/main/`)

| Panel | Tissue | Description | Files |
|---|---|---|---|
| **A** | both | Tissue slices (source / target / source-anatomy / target-anatomy) | `Fig3A_{brain,kidney}_{source,target,source_anatomy,target_anatomy}.png` (8) |
| **B** | brain | Per-method CC bar plot + horizontal legend | `Fig3B_brain_cc_summary{,_legend}.png` |
| **C** | kidney | Per-method CC bar plot + horizontal legend | `Fig3C_kidney_cc_summary{,_legend}.png` |
| **D** | brain | Per-method wall time (log y) | `Fig3D_brain_cost_time.png` |
| **E** | kidney | Per-method wall time (log y) | `Fig3E_kidney_cost_time.png` |
| **F** | brain | Per-method peak memory | `Fig3F_brain_cost_memory.png` |
| **G** | kidney | Per-method peak memory | `Fig3G_kidney_cost_memory.png` |
| **H** | brain | Warped `HexCer.42.1.O2` from every method in the bar plot (source + 10 methods) | `Fig3H_brain_alignment_{00_source,01_qGW,02_FRLC,03_LR-GW,04..09_ir_*,10_guidedPLS}.png` (11) |
| **I** | kidney | Warped `FA.22.6` from every method (source + 9 methods; LR-GW absent — degenerate, no usable warp) | `Fig3I_kidney_alignment_{00_source,01_qGW,02_FRLC,04..09_ir_*,10_guidedPLS}.png` (10) |

Slice point sizes: brain `s=17`, kidney `s=60` (tuned to per-tissue spot density). Re-render via `src/render_slices.py` and `src/render_method_comparison.py`.

### Headline numbers per panel

**Fig. 3B / 3C — CC** (mean ± SD across all (param, marker) pairs):

| Tissue | qGW | FRLC | LR-GW | ir_* (best) | guidedPLS |
|---|---|---|---|---|---|
| Brain | ≈ −0.02 | ≈ 0.01 | ≈ 0.00 | ≈ 0.13 | **≈ 0.34** (HexCer family 0.65–0.73) |
| Kidney | ≈ −0.03 | ≈ −0.03 | NA | ≈ 0.00 | **≈ 0.78** |

**Fig. 3D / 3E — wall time** (representative point per method):

| Tissue | qGW (ε=1E+12) | FRLC (10) | LR-GW (10) | ir_anat_rigid | ir_anat_sitk_rigid | guidedpls |
|---|---|---|---|---|---|---|
| Brain | 55 s | 46 s | 79 s | 30 s | 33 s | 196 s |
| Kidney | 166 s | 358 s | 21 s* | 658 s | 154 s | 152 s |

**Fig. 3F / 3G — peak RSS** (MB):

| Tissue | qGW (ε=1E+12) | FRLC (10) | LR-GW (10) | ir_anat_rigid | ir_anat_sitk_rigid | guidedpls |
|---|---|---|---|---|---|---|
| Brain | 2,443 | 2,022 | **27,017** | 1,101 | 1,061 | 4,332 |
| Kidney | 5,602 | 3,214 | 4,687* | 5,227 | 4,239 | 6,166 |

*Kidney LR-GW exited non-zero on every rank (degenerate output). Wall + RSS in 3E/3G reflect "time/memory spent before failure", not "time to a valid warp". Note this in the figure caption.

## Supplementary (`plot/Figures/supplementary/`)

Each subdirectory is split into `brain/` and `kidney/`.

### `representative_panels/` — leftover hand-picked panels

What's left after promoting the method-comparison slices to `main/Fig3H/I`:
- `brain/representative_warped_features_{HexCer.42.1.O2,SM.42.3.O2,target_Mog,target_Sox10}.png` (4) — guidedPLS-warped lipids alongside target white-matter genes
- `brain/pairplot_{anatomy,legend}.png` (2)
- `kidney/representative_warped_features_{FA.22.6,target_Slc27a2}.png` (2)
- `kidney/pairplot_{anatomy,legend}.png` (2)

### `parameter_sensitivity/` (brain: 15, kidney: 11)

Single marker (`HexCer.42.1.O2` for brain, `FA.22.6` for kidney) across all parameter values per OT method.

### `per_method_alignment/` (brain: 88, kidney: ~190)

Full marker set per method, one subdir per `{dataset}/{method}_{param}`.

### `qc_preprocessing/` (brain: 6, kidney: 6)

Source/target density and log-scale distributions.

### `cross_method_pairplots/` (brain: 1, kidney: 1)

`{brain,kidney}/pairplot_batch.png` — pairplot coloured by batch rather than anatomy; sanity check.

(Workflow rule-graph PNGs live at the repo top level `plot/*.png` and are embedded in `README.md`, not duplicated here.)

## Regeneration scripts

- `src/render_slices.py` — Fig3A tissue-slice panels (brain `s=17`, kidney `s=60`).
- `src/render_method_comparison.py` — Fig3H / Fig3I per-method warped slices, reading each method's `warped.txt` directly (bypasses the R pipeline). Same s-values as Fig3A.
- `src/render_cc_barplot.py` — Fig3B / 3C per-method CC bar plot + horizontal legend strip.
- `src/render_cost_barplot.py` — Fig3D / 3E (wall time, log y) and Fig3F / 3G (peak RSS). Runs once per (dataset, metric, out_path).
- `src/bench_ot.py` — Re-runs FRLC + LR-GW on `{251208, kidney} × ranks {10, 20, 30, 50}` and writes benchmark files in snakemake format (the original snakemake `benchmark:` directives were never captured for these rules).

## Provenance

Numerical values quoted above are read from `output/{251208,kidney}/{guidedpls,qgw,frlc,lrgw,ir_*}/cc.csv` (gitignored) and `benchmarks/{251208,kidney}_{method}_*.txt`. CC values are regenerable via `snakemake -s workflow/evaluation.smk`; benchmarks via `src/bench_ot.py`. Plot files originate from `plot/{251208,kidney}/{dataset,guidedpls,qgw,frlc,lrgw}/` and `output/{251208,kidney}/{method}/warped.txt` (gitignored); only the curated `plot/Figures/` subtree and top-level `plot/*.png` DAGs are version-controlled.

## Conventions

- All file names start with `Fig3` (this repo contributes a single Fig. 3 to the manuscript).
- Naming pattern: `Fig3{Panel}_{tissue}_{description}.png`, where `{Panel} ∈ {A..I}` and `{tissue} ∈ {brain, kidney}`. For the per-method alignment panels (H, I), the description includes a numerical prefix matching the bar-plot order: `00_source` → `01_qGW` → `02_FRLC` → `03_LR-GW` → `04..09_ir_*` → `10_guidedPLS`.
- All images are PNG. PDF versions are not generated automatically; render from source if needed.
- Hand-curated figures live in `main/`; everything else lives under `supplementary/`.
- **Always check orientation** before finalizing any panel.
