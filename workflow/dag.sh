# DAG graph
snakemake -s workflow/preprocess.smk --rulegraph | dot -Tpng > plot/preprocess.png
snakemake -s workflow/ot.smk --rulegraph | dot -Tpng > plot/ot.png
snakemake -s workflow/guidedpls.smk --rulegraph | dot -Tpng > plot/guidedpls.png
snakemake -s workflow/evaluation.smk --rulegraph | dot -Tpng > plot/evaluation.png
snakemake -s workflow/plot.smk --rulegraph | dot -Tpng > plot/plot.png
