# HTML
mkdir -p report
snakemake -s workflow/preprocess.smk --report report/preprocess.html
snakemake -s workflow/ot.smk --report report/ot.html
snakemake -s workflow/guidedpls.smk --report report/guidedpls.html
snakemake -s workflow/evaluation.smk --report report/evaluation.html
snakemake -s workflow/plot.smk --report report/plot.html
