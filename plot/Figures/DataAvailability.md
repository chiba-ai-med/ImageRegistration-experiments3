# Data Availability

Data used to generate **Fig. 3 (Brain)** and **Suppl. Fig. S (Kidney)** in this repository.

## Brain (mouse, dataset code `251208`)

Adjacent serial sections from the same mouse brain.

- **Source — Spatial lipidomics (MSI, Positive mode)**
  - Section: `SL section 12`
  - Raw input file: `data/251208/data/df_sl12.csv` (~150 MB, normalized/scaled)
  - Coverage: 47,734 spots × 173 lipid features
  - Origin: **TBD** — public dataset. Provide a GEO / MetaSpace / journal-supplementary accession (`GSE######` or DOI / project URL).
- **Target — Spatial transcriptomics (ST)**
  - Section: `ST section 32`
  - Raw input file: `data/251208/data/df_st32.csv` (~194 MB, normalized/scaled)
  - Coverage: 39,891 spots × 1,120 gene features
  - Origin: **TBD** — public dataset. Provide a GEO accession (`GSE######`) or equivalent.

Both files are gitignored in this repository. The preprocessing script `src/preprocess_csv.py` reads these CSVs and produces `data/251208/{source,target}/*.csv`. The representative single markers shown in Fig. 3a are **HexCer 42:1;O2** (source lipid) and **Mog** (target gene).

## Kidney (mouse)

Two paired modalities on the same kidney section (or adjacent sections).

- **Source — MALDI-MSI (Negative mode)**
  - Raw input file: `data/kidney/kidney_maldi.csv` (~62 MB)
  - Coverage: 12,275 spots × 422 lipid features
  - Origin: **TBD** — confirm whether public (provide accession) or **collaborator-provided** (state collaborator institution / lab and reference paper if any).
- **Target — Xenium (10× Genomics, spatial transcriptomics)**
  - Raw input file: `data/kidney/kidney_xenium.csv` (~1 GB)
  - Coverage: 177,369 spots × multiple gene panels
  - Origin: **TBD** — same as above. Note that 10× Genomics Xenium output may have a vendor demo / public dataset URL if applicable.

Both files are gitignored. Representative single markers in Suppl. Fig. S are **FA 22:6** (DHA, source lipid) and **Slc27a2** (target gene; proximal-tubule fatty-acid transporter).

## Annotation (anatomy guide variable)

guidedPLS and the `ir_anat_*` baselines use spot-level anatomical region annotations as the guide / reference image.

- **Brain**: CCF region labels (Allen Brain Atlas Common Coordinate Framework), column `ccf_region_name` in the source CSV. Region count: ~200 fine-grained categories.
- **Kidney**: region labels via the `region` column in the source CSV. Provide ontology / lab convention reference (**TBD**).

## Preprocessed outputs (this repo)

The Snakemake workflow rule `preprocess_csv` (in `workflow/preprocess.smk`) writes per-tissue `source/` and `target/` sub-directories containing:

- `all_exp.csv` — full normalized expression matrix
- `exp.csv` — single representative-marker expression vector (Fig. 3a / Suppl. Fig. Sa)
- `anatomy.csv` — one-hot anatomical annotation
- `x.csv`, `y.csv` — spot coordinates

These intermediate files are also gitignored; regenerate from the raw inputs with `snakemake -s workflow/preprocess.smk`.

## Code availability

This repository (`chiba-ai-med/ImageRegistration-experiments3`) contains all scripts, Snakemake workflows, and rendering code needed to reproduce Fig. 3 and Suppl. Fig. S from the raw CSVs above. See `README.md` for environment / Singularity container details and `figure_index.md` for the per-panel mapping.

## Sibling repositories

The guidedPLS manuscript is supported by four sibling repos; data availability for each is documented separately:

- `chiba-ai-med/guidedPLS-experiments-sim` — synthetic data (no accession needed)
- `chiba-ai-med/guidedPLS-experiments-bulk` — bulk multi-omics
- `chiba-ai-med/guidedPLS-experiments-sc` — single-cell multi-omics
- `chiba-ai-med/ImageRegistration-experiments3` (this repo) — Spatial omics / Image registration

## To fill in before submission

Items currently marked **TBD** above. Please replace with concrete accessions / collaborator names:

1. Brain SL (section 12) — GSE? MetaSpace project? DOI?
2. Brain ST (section 32) — GSE? Visium accession?
3. Kidney MALDI — public accession or collaborator (institution / PI / paper)?
4. Kidney Xenium — public accession or collaborator?
5. Kidney anatomy ontology — what reference?
