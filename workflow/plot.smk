import pandas as pd
from snakemake.utils import min_version

#################################
# Setting
#################################
min_version("8.10.0")

DATASETS = ['251208', 'kidney']
QGW_PARAMETERS = ['1E+8','1E+9','1E+10','1E+11','1E+12','1E+13','1E+14']
FRLC_PARAMETERS = ['10','20','30','50']
LRGW_PARAMETERS = ['10','20','30','50']
IR_METHODS = ['ir_sum_rigid', 'ir_sum_affine', 'ir_sum_sitk_rigid',
              'ir_anat_rigid', 'ir_anat_affine', 'ir_anat_sitk_rigid']

rule all:
    input:
        # Datasets
        expand('plot/{dataset}/dataset/FINISH', dataset=DATASETS),
        # OT
        expand('plot/{dataset}/qgw/{qgwp}/FINISH',
            dataset=DATASETS, qgwp=QGW_PARAMETERS),
        expand('plot/{dataset}/frlc/{frlcp}/FINISH',
            dataset=DATASETS, frlcp=FRLC_PARAMETERS),
        expand('plot/{dataset}/lrgw/{lrgwp}/FINISH',
            dataset=DATASETS, lrgwp=LRGW_PARAMETERS),
        # IR
        expand('plot/{dataset}/{ir_method}/FINISH',
            dataset=DATASETS, ir_method=IR_METHODS),
        # Guided PLS
        expand('plot/{dataset}/guidedpls/FINISH', dataset=DATASETS),
        expand('plot/{dataset}/guidedpls/pairplot_batch.png', dataset=DATASETS),
        expand('plot/{dataset}/guidedpls/pairplot_anatomy.png', dataset=DATASETS),
        expand('plot/{dataset}/guidedpls/pairplot_anatomy_legend.png', dataset=DATASETS),
        # Evaluation Mesures
        expand('plot/{dataset}/cc.png', dataset=DATASETS)

# Datasets
rule plot_datasets:
    input:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv',
        'data/{dataset}/source/exp.csv',
        'data/{dataset}/target/exp.csv',
        'data/{dataset}/source/anatomy.csv',
        'data/{dataset}/target/anatomy.csv',
        'data/{dataset}/source/x.csv',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/source/y.csv',
        'data/{dataset}/target/y.csv'
    output:
        'plot/{dataset}/dataset/FINISH'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_datasets.txt'
    log:
        'logs/{dataset}_plot_datasets.log'
    shell:
        'src/plot_datasets.sh {wildcards.dataset} {input} {output} >& {log}'

# OT
rule plot_qgw:
    input:
        'output/{dataset}/qgw/{qgwp}/warped.txt',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/target/y.csv'
    output:
        'plot/{dataset}/qgw/{qgwp}/FINISH'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_qgw_{qgwp}.txt'
    log:
        'logs/{dataset}_plot_qgw_{qgwp}.log'
    shell:
        'src/plot_ot.sh {input} {output} >& {log}'

# FRLC
rule plot_frlc:
    input:
        'output/{dataset}/frlc/{frlcp}/warped.txt',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/target/y.csv'
    output:
        'plot/{dataset}/frlc/{frlcp}/FINISH'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_frlc_{frlcp}.txt'
    log:
        'logs/{dataset}_plot_frlc_{frlcp}.log'
    shell:
        'src/plot_ot.sh {input} {output} >& {log}'

# Low-Rank GW (ott-jax)
rule plot_lrgw:
    input:
        'output/{dataset}/lrgw/{lrgwp}/warped.txt',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/target/y.csv'
    output:
        'plot/{dataset}/lrgw/{lrgwp}/FINISH'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_lrgw_{lrgwp}.txt'
    log:
        'logs/{dataset}_plot_lrgw_{lrgwp}.log'
    shell:
        'src/plot_ot.sh {input} {output} >& {log}'

# Image Registration
rule plot_ir:
    input:
        'output/{dataset}/{ir_method}/warped.txt',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/target/y.csv'
    output:
        'plot/{dataset}/{ir_method}/FINISH'
    wildcard_constraints:
        ir_method="ir_(sum|anat)_(rigid|affine|sitk_rigid)"
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_{ir_method}.txt'
    log:
        'logs/{dataset}_plot_{ir_method}.log'
    shell:
        'src/plot_ot.sh {input} {output} >& {log}'

# Guided PLS
rule plot_guidedpls:
    input:
        'output/{dataset}/guidedpls/warped.txt',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/target/y.csv'
    output:
        'plot/{dataset}/guidedpls/FINISH'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_guidedpls.txt'
    log:
        'logs/{dataset}_plot_guidedpls.log'
    shell:
        'src/plot_ot.sh {input} {output} >& {log}'

rule plot_pairs_guidedpls:
    input:
        'output/{dataset}/guidedpls/guidedpls.RData',
        'data/{dataset}/source/anatomy.csv',
        'data/{dataset}/target/anatomy.csv'
    output:
        'plot/{dataset}/guidedpls/pairplot_batch.png',
        'plot/{dataset}/guidedpls/pairplot_anatomy.png',
        'plot/{dataset}/guidedpls/pairplot_anatomy_legend.png'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_pairs_guidedpls.txt'
    log:
        'logs/{dataset}_plot_pairs_guidedpls.log'
    shell:
        'src/plot_pairs.sh {input} {output} >& {log}'

# CC
rule plot_cc:
    output:
        'plot/{dataset}/cc.png'
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_plot_cc.txt'
    log:
        'logs/{dataset}_plot_cc.log'
    shell:
        'src/plot_cc.sh {wildcards.dataset} {output} >& {log}'
