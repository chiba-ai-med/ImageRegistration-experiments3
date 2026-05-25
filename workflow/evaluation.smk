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
        # Optimal Transport
        expand("output/{dataset}/qgw/{qgwp}/cc.csv",
            dataset=DATASETS, qgwp=QGW_PARAMETERS),
        expand("output/{dataset}/frlc/{frlcp}/cc.csv",
            dataset=DATASETS, frlcp=FRLC_PARAMETERS),
        expand("output/{dataset}/lrgw/{lrgwp}/cc.csv",
            dataset=DATASETS, lrgwp=LRGW_PARAMETERS),
        # Image Registration
        expand("output/{dataset}/{ir_method}/cc.csv",
            dataset=DATASETS, ir_method=IR_METHODS),
        # Guided PLS
        expand("output/{dataset}/guidedpls/cc.csv",
            dataset=DATASETS)

rule evaluate_qgw:
    input:
        "output/{dataset}/qgw/{qgwp}/warped.txt",
        "data/{dataset}/target/all_exp.csv"
    output:
        "output/{dataset}/qgw/{qgwp}/cc.csv"
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_evaluate_qgw_{qgwp}.txt'
    log:
        'logs/{dataset}_evaluate_qgw_{qgwp}.log'
    shell:
        'src/evaluate.sh {wildcards.dataset} {input} {output} >& {log}'

rule evaluate_frlc:
    input:
        "output/{dataset}/frlc/{frlcp}/warped.txt",
        "data/{dataset}/target/all_exp.csv"
    output:
        "output/{dataset}/frlc/{frlcp}/cc.csv"
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_evaluate_frlc_{frlcp}.txt'
    log:
        'logs/{dataset}_evaluate_frlc_{frlcp}.log'
    shell:
        'src/evaluate.sh {wildcards.dataset} {input} {output} >& {log}'

rule evaluate_lrgw:
    input:
        "output/{dataset}/lrgw/{lrgwp}/warped.txt",
        "data/{dataset}/target/all_exp.csv"
    output:
        "output/{dataset}/lrgw/{lrgwp}/cc.csv"
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_evaluate_lrgw_{lrgwp}.txt'
    log:
        'logs/{dataset}_evaluate_lrgw_{lrgwp}.log'
    shell:
        'src/evaluate.sh {wildcards.dataset} {input} {output} >& {log}'

rule evaluate_ir:
    input:
        "output/{dataset}/{ir_method}/warped.txt",
        "data/{dataset}/target/all_exp.csv"
    output:
        "output/{dataset}/{ir_method}/cc.csv"
    wildcard_constraints:
        ir_method="ir_(sum|anat)_(rigid|affine|sitk_rigid)"
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_evaluate_{ir_method}.txt'
    log:
        'logs/{dataset}_evaluate_{ir_method}.log'
    shell:
        'src/evaluate.sh {wildcards.dataset} {input} {output} >& {log}'

rule evaluate_guidedpls:
    input:
        "output/{dataset}/guidedpls/warped.txt",
        "data/{dataset}/target/all_exp.csv"
    output:
        "output/{dataset}/guidedpls/cc.csv"
    container:
        'docker://koki/ir-experiments-r:20250701'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_evaluate_guidedpls.txt'
    log:
        'logs/{dataset}_evaluate_guidedpls.log'
    shell:
        'src/evaluate.sh {wildcards.dataset} {input} {output} >& {log}'
