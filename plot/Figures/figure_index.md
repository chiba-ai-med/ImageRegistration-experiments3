# Figure Index — ImageRegistration-experiments3

Curated figure candidates for the **Spatial omics / Image registration** section of the guidedPLS manuscript. The 10-method comparison doesn't fit on a single tissue-combined panel, so the figure is split:

- **Fig. 3 — Brain** (mouse brain `251208`, lipid MSI → spatial transcriptomics)
- **Fig. 4 — Kidney** (mouse kidney, lipid MSI → spatial transcriptomics)

Each figure has five panels (A–E) with the same structure. All filenames here are stable; refer to them from `paper_takeaway.md` and from the manuscript LaTeX source.

> **⚠️ Orientation caveat.** MSI source and ST target coordinate frames do not share a global orientation, and individual method outputs can additionally be flipped. Brain target panels in `main/` have already been vertically flipped to match the source orientation; kidney panels are untouched. Visually verify every panel against the source/target overview before submission.

## Per-figure panel structure

| Panel | Content |
|---|---|
| **A** | Tissue slices — source / target / source-anatomy / target-anatomy (4 files) |
| **B** | Per-method CC bar plot + horizontal legend (`*_legend.png`) |
| **C** | Per-method wall time bar plot (log y) |
| **D** | Per-method peak memory bar plot |
| **E** | Warped slice for the evaluation marker across every method that appears in the bar plot |

## Fig. 3 — Brain (`plot/Figures/main/Fig3*`)

Evaluation marker: `HexCer.42.1.O2` (myelin-associated, warped lipid that should co-localize with white-matter genes Mog / Sox10).

| File | Panel | Notes |
|---|---|---|
| `Fig3A_brain_{source,target,source_anatomy,target_anatomy}.png` | 3A | 4 slices; MSI 47,734 spots × 173 lipids → ST 39,891 spots × 1,120 genes |
| `Fig3B_brain_cc_summary{,_legend}.png` | 3B | Mean ± SD CC across all (param, marker) pairs |
| `Fig3C_brain_cost_time.png` | 3C | Wall time per method (log y) |
| `Fig3D_brain_cost_memory.png` | 3D | Peak RSS per method |
| `Fig3E_brain_alignment_{00_source,01_qGW,02_FRLC,03_LR-GW,04..09_ir_*,10_guidedPLS}.png` | 3E | 11 panels: source reference + 10 methods |

## Fig. 4 — Kidney (`plot/Figures/main/Fig4*`)

Evaluation marker: `FA.22.6` (DHA; proximal-tubule transporter Slc27a2 is the matched target gene).

| File | Panel | Notes |
|---|---|---|
| `Fig4A_kidney_{source,target,source_anatomy,target_anatomy}.png` | 4A | 4 slices; ST target has 177,369 spots (≈ 4× brain target) |
| `Fig4B_kidney_cc_summary{,_legend}.png` | 4B | Single marker pair; per-method bars |
| `Fig4C_kidney_cost_time.png` | 4C | Wall time per method |
| `Fig4D_kidney_cost_memory.png` | 4D | Peak RSS per method |
| `Fig4E_kidney_alignment_{00_source,01_qGW,02_FRLC,04..09_ir_*,10_guidedPLS}.png` | 4E | **10 panels** — LR-GW absent (degenerate; no usable warp on kidney) |

Slice point sizes: brain `s=17`, kidney `s=60` (tuned to per-tissue spot density). Re-render via `src/render_slices.py` and `src/render_method_comparison.py`.

### Headline numbers

**Fig. 3B / 4B — CC** (mean ± SD across all (param, marker) pairs):

| Tissue | qGW | FRLC | LR-GW | ir_* (best) | guidedPLS |
|---|---|---|---|---|---|
| Brain | ≈ −0.02 | ≈ 0.01 | ≈ 0.00 | ≈ 0.13 | **≈ 0.34** (HexCer family 0.65–0.73) |
| Kidney | ≈ −0.03 | ≈ −0.03 | NA | ≈ 0.00 | **≈ 0.78** |

**Fig. 3C / 4C — wall time** (representative point per method):

| Tissue | qGW (ε=1E+12) | FRLC (10) | LR-GW (10) | ir_anat_rigid | ir_anat_sitk_rigid | guidedpls |
|---|---|---|---|---|---|---|
| Brain | 55 s | 46 s | 79 s | 30 s | 33 s | 196 s |
| Kidney | 166 s | 358 s | 21 s* | 658 s | 154 s | 152 s |

**Fig. 3D / 4D — peak RSS** (MB):

| Tissue | qGW (ε=1E+12) | FRLC (10) | LR-GW (10) | ir_anat_rigid | ir_anat_sitk_rigid | guidedpls |
|---|---|---|---|---|---|---|
| Brain | 2,443 | 2,022 | **27,017** | 1,101 | 1,061 | 4,332 |
| Kidney | 5,602 | 3,214 | 4,687* | 5,227 | 4,239 | 6,166 |

*Kidney LR-GW exited non-zero on every rank (degenerate output). Wall + RSS reflect "time/memory spent before failure", not "time to a valid warp". Note this in the figure caption.

## Supplementary (`plot/Figures/supplementary/`)

Each subdirectory is split into `brain/` and `kidney/`.

### `representative_panels/`

Hand-picked panels that didn't make the main figure split:
- `brain/representative_warped_features_{HexCer.42.1.O2,SM.42.3.O2,target_Mog,target_Sox10}.png` (4) — guidedPLS-warped lipids alongside target white-matter genes
- `brain/pairplot_{anatomy,legend}.png` (2)
- `kidney/representative_warped_features_{FA.22.6,target_Slc27a2}.png` (2)
- `kidney/pairplot_{anatomy,legend}.png` (2)

### `parameter_sensitivity/` (brain: 15, kidney: 11)

Single marker across all parameter values per OT method.

### `per_method_alignment/` (brain: 88, kidney: ~190)

Full marker set per method, one subdir per `{dataset}/{method}_{param}`.

### `qc_preprocessing/` (brain: 6, kidney: 6)

Source/target density and log-scale distributions.

### `cross_method_pairplots/` (brain: 1, kidney: 1)

`{brain,kidney}/pairplot_batch.png` — sanity check that batch is not driving the recovered structure.

(Workflow rule-graph PNGs live at the repo top level `plot/*.png` and are embedded in `README.md`, not duplicated here.)

## Regeneration scripts

- `src/render_slices.py <dataset> [s]` — Fig3A / Fig4A tissue-slice panels.
- `src/render_method_comparison.py <s_brain> <s_kidney>` — Fig3E / Fig4E per-method warped slices.
- `src/render_cc_barplot.py <dataset> <out_bar> <out_legend>` — Fig3B / Fig4B per-method CC bar plot + horizontal legend.
- `src/render_cost_barplot.py <dataset> <metric> <out>` — Fig3C/Fig3D / Fig4C/Fig4D (`metric ∈ {time, memory}`).
- `src/bench_ot.py` — Re-runs FRLC + LR-GW on `{251208, kidney} × ranks {10, 20, 30, 50}` and writes benchmark files in snakemake format.

## Provenance

Numerical values quoted above are read from `output/{251208,kidney}/{method}/cc.csv` and `benchmarks/{251208,kidney}_{method}_*.txt`. Both directories are gitignored; only the curated `plot/Figures/` subtree and top-level `plot/*.png` DAGs are version-controlled. CC values are regenerable via `snakemake -s workflow/evaluation.smk`; benchmarks via `src/bench_ot.py`.

## Conventions

- Naming: `Fig{N}{Panel}_{tissue}_{description}.png`, where `N ∈ {3, 4}` (3 = brain, 4 = kidney) and `{Panel} ∈ {A..E}`. For alignment panels (E), the description starts with a numerical prefix matching bar-plot order: `00_source` → `01_qGW` → `02_FRLC` → `03_LR-GW` → `04..09_ir_*` → `10_guidedPLS`.
- All images are PNG. Hand-curated figures live in `main/`; everything else lives under `supplementary/`.
- **Always check orientation** before finalizing any panel.
