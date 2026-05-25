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

This repo is one of 3 repos that will be merged into a single paper:

- `chiba-ai-med/ImageRegistration-experiments3` (this repo) — cross-modal spatial alignment benchmark (MSI ↔ ST)
- `chiba-ai-med/guidedPLS-experiments-sc` — GuidedPLS on single-cell data
- `chiba-ai-med/guidedPLS-experiments-bulk` — GuidedPLS on bulk data

Each repo summarizes its own results in isolation; results are merged in the final paper.

## Benchmark results summary

All OT-based methods (qGW, FRLC, LR-GW) produced canonical correlation ≈ 0 on this dataset and do not work in practice at this scale / modality gap. **Only GuidedPLS produced meaningful alignment.** Plots/outputs from failed OT methods are retained for the negative-result comparison in the paper.

Notes on the failed methods (for reference, not to revisit):
- **qGW**: quantized GW, runs at scale but CC ≈ 0
- **FRLC**: low-rank factor-relaxation GW (cloned source under `FRLC/`, gitignored). Needs gamma retry (90 → 10) for numerical stability; `objective_grad.py` was patched for a dead-code path
- **LR-GW**: ott-jax low-rank GW. JAX CUDA vs PyTorch cuDNN conflicts; CPU fallback only

## Directory notes

- `plot/kidney/` — exploratory run on a different (kidney) dataset, kept for reference only; not part of the 251208 brain pipeline
- `workflow/{evaluate,ir}.smk` — older/superseded workflows; not included in `dag.sh` / `report.sh`. The 5 active workflows are `preprocess`, `ot`, `guidedpls`, `evaluation`, `plot`
- `plot/Figures/` — paper-ready figures hand-picked from `plot/{251208,kidney}/`. `plot/*.png` at the top level are Snakemake DAG images (embedded in README)

## What's gitignored

`data/`, `output/`, `logs/`, `report/`, `.snakemake/`, `.cache/`, `FRLC/`, and everything under `plot/` except top-level DAG PNGs and `plot/Figures/`. See `.gitignore`.
