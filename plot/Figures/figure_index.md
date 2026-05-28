# Figure Index — ImageRegistration-experiments3

Curated figure candidates for the **Spatial omics / Image registration** section of the guidedPLS manuscript.

- **Fig. 3 — Brain** (mouse brain `251208`, lipid MSI **Positive mode** → spatial transcriptomics)
- **Suppl. Fig. S — Kidney** (mouse kidney, lipid MSI **Negative mode** → spatial transcriptomics)

Brain is the headline figure because it has: (a) interpretable anatomy (hippocampus, corpus callosum readable at a glance); (b) ~20 evaluated marker pairs vs kidney's 1, so CC bars carry SD; (c) a 3-level method-separation (OT ≈ 0, classical IR ≈ 0.13, guidedPLS ≈ 0.34) instead of a binary win; (d) a textbook biology link (HexCer/SM ↔ Mog/Sox10 myelin). Kidney moves to a supplementary "second-tissue replication" figure with the same 5-panel structure.

> **⚠️ Orientation caveat.** MSI source and ST target coordinate frames do not share a global orientation, and individual method outputs can additionally be flipped. Brain target panels have already been vertically flipped to match the source orientation; kidney panels are untouched. Visually verify every panel against the source/target overview before submission.

## Fig. 3 — Brain (`plot/Figures/main/Fig3*`)

Evaluation marker: `HexCer.42.1.O2` (myelin-associated). Five panels A–E.

| Panel | File | Notes |
|---|---|---|
| 3A | `Fig3A_brain_{source,target,source_anatomy,target_anatomy}.png` | 4 slices; MSI 47,734 × 173 lipids → ST 39,891 × 1,120 genes |
| 3B | `Fig3B_brain_cc_summary{,_legend}.png` | Mean ± SD CC across all (param, marker) pairs |
| 3C | `Fig3C_brain_cost_time.png` | Wall time per method (log y) |
| 3D | `Fig3D_brain_cost_memory.png` | Peak RSS per method |
| 3E | `Fig3E_brain_alignment_{00_source,01_qGW,02_FRLC,03_LR-GW,04..09_ir_*,10_guidedPLS}.png` | 11 panels: source reference + 10 methods |

Slice point size: `s=17` (tuned to brain's 47K-spot density). Re-render via `src/render_slices.py 251208 17` and `src/render_method_comparison.py 17 60`.

### Headline numbers (Brain)

| Metric | qGW | FRLC | LR-GW | ir_* (best) | guidedPLS |
|---|---|---|---|---|---|
| **CC** (mean) | ≈ −0.02 | ≈ 0.01 | ≈ 0.00 | ≈ 0.13 | **≈ 0.34** (HexCer 0.65–0.73) |
| **Wall time** (s) | 55 (ε=1E+12) | 46 (r=10) | 79 (r=10) | 30 (anat_rigid) | 196 |
| **Peak RSS** (MB) | 2,443 | 2,022 | **27,017** | 1,101 | 4,332 |

## Suppl. Fig. S — Kidney (`plot/Figures/supplementary/figS_kidney/FigS*`)

Second-tissue replication. Same 5-panel structure as Fig. 3 (A = slices, B = CC bar, C = time, D = memory, E = per-method warped). Evaluation marker: `FA.22.6` (DHA, paired with target `Slc27a2`).

| Panel | File | Notes |
|---|---|---|
| SA | `FigSA_kidney_{source,target,source_anatomy,target_anatomy}.png` | ST target = 177,369 spots (≈ 4× brain target) |
| SB | `FigSB_kidney_cc_summary{,_legend}.png` | Single marker pair — bars without SD |
| SC | `FigSC_kidney_cost_time.png` | Wall time |
| SD | `FigSD_kidney_cost_memory.png` | Peak RSS |
| SE | `FigSE_kidney_alignment_{00,01,02,04..10}_*.png` | **10 panels** — LR-GW absent (degenerate, no usable warp on kidney) |

Slice point size: `s=60`.

### Headline numbers (Kidney)

| Metric | qGW | FRLC | LR-GW | ir_* (best) | guidedPLS |
|---|---|---|---|---|---|
| **CC** | ≈ −0.03 | ≈ −0.03 | NA | ≈ 0.00 | **≈ 0.78** |
| **Wall time** (s) | 166 | 358 | 21* | 154 (anat_sitk_rigid) | 152 |
| **Peak RSS** (MB) | 5,602 | 3,214 | 4,687* | 4,239 | 6,166 |

*Kidney LR-GW exited non-zero on every rank. Wall + RSS reflect "time/memory spent before failure", not "time to a valid warp". Note in caption.

## Supplementary panels (`plot/Figures/supplementary/`)

Each subdirectory is split into `brain/` and `kidney/` unless noted.

### `figS_kidney/`

The kidney figure described above (formerly main Fig. 4).

### `representative_panels/`

Hand-picked panels that didn't make the main figure split:
- `brain/representative_warped_features_{HexCer.42.1.O2,SM.42.3.O2,target_Mog,target_Sox10}.png` (4)
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

- `src/render_slices.py <dataset> [s]` — Fig3A / FigSA tissue-slice panels.
- `src/render_method_comparison.py <s_brain> <s_kidney>` — Fig3E / FigSE per-method warped slices.
- `src/render_cc_barplot.py <dataset> <out_bar> <out_legend>` — Fig3B / FigSB per-method CC bar plot + horizontal legend.
- `src/render_cost_barplot.py <dataset> <metric> <out>` — Fig3C/Fig3D / FigSC/FigSD (`metric ∈ {time, memory}`).
- `src/bench_ot.py` — Re-runs FRLC + LR-GW on `{251208, kidney} × ranks {10, 20, 30, 50}` and writes benchmark files in snakemake format.

## Provenance

Numerical values quoted above are read from `output/{251208,kidney}/{method}/cc.csv` and `benchmarks/{251208,kidney}_{method}_*.txt`. Both directories are gitignored; only the curated `plot/Figures/` subtree and top-level `plot/*.png` DAGs are version-controlled. CC values are regenerable via `snakemake -s workflow/evaluation.smk`; benchmarks via `src/bench_ot.py`.

## Conventions

- Naming: `Fig3{Panel}_brain_{description}.png` for the main figure, `FigS{Panel}_kidney_{description}.png` for the supplementary tissue figure. For alignment panels (E), the description starts with a numerical prefix matching bar-plot order: `00_source` → `01_qGW` → `02_FRLC` → `03_LR-GW` → `04..09_ir_*` → `10_guidedPLS`.
- All images are PNG. Hand-curated figures live in `main/`; everything else lives under `supplementary/`.
- **Always check orientation** before finalizing any panel.
