# ImageRegistration-experiments3

Cross-modal spatial alignment benchmark: lipid MSI (SL section 12) → spatial transcriptomics (ST section 32) on mouse brain tissue using public data (251208).

## Architecture

```
data/251208/data/           Raw input (df_sl12.csv, df_st32.csv) - normalized/scaled
data/source/                Preprocessed source (47,734 spots × 173 lipid features, Positive mode)
data/target/                Preprocessed target (39,891 spots × 1,120 gene features)
src/                        All scripts (Python OT methods, R GuidedPLS/evaluation/plotting)
workflow/                   Snakemake workflow files (.smk)
output/{method}/            Computed results (warped expressions, transport plans, cc.csv)
plot/                       Generated plots
```

## Key differences from experiments2

- **Data source**: Public annotated SL data (Positive mode only, no SHexCer)
- **Scale**: Source 47K spots (vs 31K), Target 40K spots (vs 2K)
- **Features**: 173 lipids (vs 452), 1,120 genes (vs 19K)
- **Regions**: Fine-grained CCF regions (~200 categories vs 18 coarse)
- **Evaluation markers**: HexCer(10) + SM(10) × Mog + Sox10 = 40 pairs (vs 141)
- **OT scalability**: Full GW methods infeasible (O(n^2) memory); qGW recommended

## Commands

```bash
# Preprocessing
snakemake -s workflow/preprocess.smk --cores 4

# OT methods (qGW recommended for this data size)
snakemake -s workflow/ot.smk --cores 4

# GuidedPLS
snakemake -s workflow/guidedpls.smk --cores 4

# Evaluation
snakemake -s workflow/evaluation.smk --cores 4

# Plots
snakemake -s workflow/plot.smk --cores 4
```

## Containers

- `koki/ir-experiments:20241001` - preprocessing (Python)
- `koki/ot-experiments:20240719` - OT methods (Python + POT)
- `koki/ir-experiments-r:20250826` - GuidedPLS (R)
- `koki/ir-experiments-r:20250701` - Evaluation/plotting (R)

## Paper context

This repo is one of 4 repos that will be merged into a single paper:

- `chiba-ai-med/guidedPLS-experiments-sim` — GuidedPLS on synthetic data with known ground truth
- `chiba-ai-med/guidedPLS-experiments-bulk` — GuidedPLS on bulk data
- `chiba-ai-med/guidedPLS-experiments-sc` — GuidedPLS on single-cell data
- `chiba-ai-med/ImageRegistration-experiments3` (this repo) — cross-modal spatial alignment benchmark (MSI ↔ ST); contributes **Fig. 3 (Spatial omics / Image registration)** covering both brain and kidney in one combined figure

Each repo summarizes its own results in isolation; results are merged in the final paper. Figure assignments: sim → Fig. 2, this repo → Fig. 3, bulk / sc → Fig. 4+ (TBD).

## Benchmark results summary

All OT-based methods (qGW, FRLC, LR-GW) produced canonical correlation ≈ 0 on this dataset and do not work in practice at this scale / modality gap. **Only GuidedPLS produced meaningful alignment.** Plots/outputs from failed OT methods are retained for the negative-result comparison in the paper.

Notes on the failed methods (for reference, not to revisit):
- **qGW**: quantized GW, runs at scale but CC ≈ 0
- **FRLC**: low-rank factor-relaxation GW (cloned source under `FRLC/`, gitignored). Needs gamma retry (90 → 10) for numerical stability; `objective_grad.py` was patched for a dead-code path
- **LR-GW**: ott-jax low-rank GW. JAX CUDA vs PyTorch cuDNN conflicts; CPU fallback only

## Directory notes

- `plot/251208/` — brain pipeline outputs (Fig. 3 source). Marker pair: HexCer/SM × Mog/Sox10 (myelin).
- `plot/kidney/` — kidney pipeline outputs (Fig. 4 source). Marker pair: FA.22.6 × Slc27a2 (DHA / proximal-tubule transporter). Only a single source–target pair is evaluated.
- `workflow/{evaluate,ir}.smk` — older/superseded workflows; not included in `dag.sh` / `report.sh`. The 5 active workflows are `preprocess`, `ot`, `guidedpls`, `evaluation`, `plot`
- `plot/Figures/` — paper-ready figures hand-picked from `plot/{251208,kidney}/`. `main/` holds the new condensed Fig.3 layout: `Fig3A_{brain,kidney}_{source,target,...}.png` (slices), `Fig3B_{brain,kidney}_pairplot_*.png` (pairplots), `Fig3C_{brain,kidney}_cc_summary.png` (bar plots). Demoted per-method comparisons and representative warped features live under `supplementary/representative_panels/{brain,kidney}/`. Other supplementary topic dirs (`parameter_sensitivity`, `per_method_alignment`, `qc_preprocessing`, `cross_method_pairplots`) also split into `brain/` and `kidney/`. `plot/*.png` at the top level are Snakemake DAG images (embedded in README).

## Orientation caveat

MSI source and ST target coordinate frames do **not** share a global orientation, and individual OT methods can silently produce flipped slice outputs depending on warp parameterization. Always visually verify panel orientation against `Fig{3,4}A_task_overview_target.png` before finalizing any figure. When in doubt, regenerate from `output/{251208,kidney}/{method}/warped.txt` rather than trusting the cached PNG.

## What's gitignored

`data/`, `output/`, `logs/`, `report/`, `.snakemake/`, `.cache/`, `FRLC/`, and everything under `plot/` except top-level DAG PNGs and `plot/Figures/`. See `.gitignore`.
