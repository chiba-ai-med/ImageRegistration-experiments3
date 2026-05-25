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
LOG_FLAG = {'251208': 'log', 'kidney': 'nolog'}

rule all:
    input:
        # qGW (Log)
        expand('output/{dataset}/qgw/{qgwp}/plan.pkl',
            dataset=DATASETS, qgwp=QGW_PARAMETERS),
        expand('output/{dataset}/qgw/{qgwp}/warped.txt',
            dataset=DATASETS, qgwp=QGW_PARAMETERS),
        # FRLC
        expand('output/{dataset}/frlc/{frlcp}/plan.pkl',
            dataset=DATASETS, frlcp=FRLC_PARAMETERS),
        expand('output/{dataset}/frlc/{frlcp}/warped.txt',
            dataset=DATASETS, frlcp=FRLC_PARAMETERS),
        # Low-Rank GW (ott-jax)
        expand('output/{dataset}/lrgw/{lrgwp}/plan.pkl',
            dataset=DATASETS, lrgwp=LRGW_PARAMETERS),
        expand('output/{dataset}/lrgw/{lrgwp}/warped.txt',
            dataset=DATASETS, lrgwp=LRGW_PARAMETERS)

#############################################
# Quantized Gromov-Wasserstein
#############################################
rule qgw:
    input:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv'
    output:
        'output/{dataset}/qgw/{qgwp}/plan.pkl',
        'output/{dataset}/qgw/{qgwp}/warped.txt'
    container:
        'docker://koki/ot-experiments:20240719'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_qgw_{qgwp}.txt'
    log:
        'logs/{dataset}_qgw_{qgwp}.log'
    params:
        log_flag=lambda wc: LOG_FLAG[wc.dataset]
    shell:
        'src/qgw.sh {input} {output} {wildcards.qgwp} {params.log_flag} >& {log}'

#############################################
# FRLC (Factor Relaxation with Latent Coupling)
#############################################
rule frlc:
    input:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv'
    output:
        'output/{dataset}/frlc/{frlcp}/plan.pkl',
        'output/{dataset}/frlc/{frlcp}/warped.txt'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_frlc_{frlcp}.txt'
    log:
        'logs/{dataset}_frlc_{frlcp}.log'
    params:
        log_flag=lambda wc: LOG_FLAG[wc.dataset]
    shell:
        'src/frlc.sh {input} {output} {wildcards.frlcp} {params.log_flag} >& {log}'

#############################################
# Low-Rank GW (ott-jax)
#############################################
rule lrgw:
    input:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv'
    output:
        'output/{dataset}/lrgw/{lrgwp}/plan.pkl',
        'output/{dataset}/lrgw/{lrgwp}/warped.txt'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_lrgw_{lrgwp}.txt'
    log:
        'logs/{dataset}_lrgw_{lrgwp}.log'
    params:
        log_flag=lambda wc: LOG_FLAG[wc.dataset]
    shell:
        'src/lrgw.sh {input} {output} {wildcards.lrgwp} {params.log_flag} >& {log}'
