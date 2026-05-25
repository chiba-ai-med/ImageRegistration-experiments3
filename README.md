# ImageRegistration-experiments3

Cross-modal spatial alignment benchmark: lipid MSI (SL section 12) → spatial transcriptomics (ST section 32) on mouse brain tissue (251208).

This workflow consists of 5 workflows as follows:

- **workflow/preprocess.smk**: Data preprocessing (source / target spot matrices)

![](https://github.com/chiba-ai-med/ImageRegistration-experiments3/blob/main/plot/preprocess.png?raw=true)

- **workflow/ot.smk**: Optimal Transport methods (qGW, FRLC, LR-GW)

![](https://github.com/chiba-ai-med/ImageRegistration-experiments3/blob/main/plot/ot.png?raw=true)

- **workflow/guidedpls.smk**: `GuidedPLS` cross-modal alignment

![](https://github.com/chiba-ai-med/ImageRegistration-experiments3/blob/main/plot/guidedpls.png?raw=true)

- **workflow/evaluation.smk**: Evaluation against marker-pair correlations (HexCer/SM × Mog/Sox10)

![](https://github.com/chiba-ai-med/ImageRegistration-experiments3/blob/main/plot/evaluation.png?raw=true)

- **workflow/plot.smk**: Plots for warped expressions and summary figures

![](https://github.com/chiba-ai-med/ImageRegistration-experiments3/blob/main/plot/plot.png?raw=true)

## Requirements
- Bash
- Snakemake
- Singularity (or Docker)

## How to reproduce this workflow
### In Local Machine

```
snakemake -s workflow/preprocess.smk -j 4 --use-singularity
snakemake -s workflow/ot.smk -j 4 --use-singularity
snakemake -s workflow/guidedpls.smk -j 4 --use-singularity
snakemake -s workflow/evaluation.smk -j 4 --use-singularity
snakemake -s workflow/plot.smk -j 4 --use-singularity
```

### In Open Grid Engine

```
snakemake -s workflow/preprocess.smk -j 32 --cluster qsub --latency-wait 600 --use-singularity
snakemake -s workflow/ot.smk -j 32 --cluster qsub --latency-wait 600 --use-singularity
snakemake -s workflow/guidedpls.smk -j 32 --cluster qsub --latency-wait 600 --use-singularity
snakemake -s workflow/evaluation.smk -j 32 --cluster qsub --latency-wait 600 --use-singularity
snakemake -s workflow/plot.smk -j 32 --cluster qsub --latency-wait 600 --use-singularity
```

### In Slurm

```
snakemake -s workflow/preprocess.smk -j 32 --cluster sbatch --latency-wait 600 --use-singularity
snakemake -s workflow/ot.smk -j 32 --cluster sbatch --latency-wait 600 --use-singularity
snakemake -s workflow/guidedpls.smk -j 32 --cluster sbatch --latency-wait 600 --use-singularity
snakemake -s workflow/evaluation.smk -j 32 --cluster sbatch --latency-wait 600 --use-singularity
snakemake -s workflow/plot.smk -j 32 --cluster sbatch --latency-wait 600 --use-singularity
```

## License
Copyright (c) 2026 Koki Tsuyuzaki released under the [Artistic License 2.0](http://www.perlfoundation.org/artistic_license_2_0).

## Authors
- Koki Tsuyuzaki
