import pandas as pd
from snakemake.utils import min_version

#################################
# Setting
#################################
min_version("8.10.0")

DATASETS = ['251208', 'kidney']

container: 'docker://koki/ir-experiments:20241001'

rule all:
    input:
        expand('data/{dataset}/source/all_exp.csv', dataset=DATASETS),
        expand('data/{dataset}/target/all_exp.csv', dataset=DATASETS),
        expand('data/{dataset}/source/sum_exp.csv', dataset=DATASETS),
        expand('data/{dataset}/target/sum_exp.csv', dataset=DATASETS),
        expand('data/{dataset}/source/bin_sum_exp.csv', dataset=DATASETS),
        expand('data/{dataset}/target/bin_sum_exp.csv', dataset=DATASETS),
        expand('data/{dataset}/source/anatomy.csv', dataset=DATASETS),
        expand('data/{dataset}/target/anatomy.csv', dataset=DATASETS),
        expand('data/{dataset}/source/exp.csv', dataset=DATASETS),
        expand('data/{dataset}/target/exp.csv', dataset=DATASETS),
        expand('data/{dataset}/source/x.csv', dataset=DATASETS),
        expand('data/{dataset}/target/x.csv', dataset=DATASETS),
        expand('data/{dataset}/source/y.csv', dataset=DATASETS),
        expand('data/{dataset}/target/y.csv', dataset=DATASETS)

rule preprocess_csv:
    output:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv',
        'data/{dataset}/source/sum_exp.csv',
        'data/{dataset}/target/sum_exp.csv',
        'data/{dataset}/source/bin_sum_exp.csv',
        'data/{dataset}/target/bin_sum_exp.csv',
        'data/{dataset}/source/anatomy.csv',
        'data/{dataset}/target/anatomy.csv',
        'data/{dataset}/source/exp.csv',
        'data/{dataset}/target/exp.csv',
        'data/{dataset}/source/x.csv',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/source/y.csv',
        'data/{dataset}/target/y.csv'
    resources:
        mem_mb=10000000
    benchmark:
        'benchmarks/{dataset}_preprocess_csv.txt'
    log:
        'logs/{dataset}_preprocess_csv.log'
    shell:
        'src/preprocess_csv.sh {wildcards.dataset} {output} >& {log}'
