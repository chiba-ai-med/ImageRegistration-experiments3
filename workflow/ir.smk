import pandas as pd
from snakemake.utils import min_version

#################################
# Setting
#################################
min_version("8.10.0")

DATASETS = ['251208', 'kidney']
IR_REFS = ['sum', 'anat']
IR_TRANSFORMS = ['rigid', 'affine', 'sitk_rigid']

rule all:
    input:
        expand('output/{dataset}/ir_{ref}_{tx}/warped.txt',
            dataset=DATASETS, ref=IR_REFS, tx=IR_TRANSFORMS),
        expand('output/{dataset}/ir_{ref}_{tx}/tx.pkl',
            dataset=DATASETS, ref=IR_REFS, tx=IR_TRANSFORMS)

#############################################
# Image Registration (sum_exp reference)
#############################################
rule ir_sum:
    input:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv',
        'data/{dataset}/source/x.csv',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/source/y.csv',
        'data/{dataset}/target/y.csv'
    output:
        'output/{dataset}/ir_sum_{tx}/warped.txt',
        'output/{dataset}/ir_sum_{tx}/tx.pkl'
    container:
        'docker://koki/ir-experiments:20241001'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_ir_sum_{tx}.txt'
    log:
        'logs/{dataset}_ir_sum_{tx}.log'
    shell:
        'src/ir.sh {input} {output} sum_exp {wildcards.tx} >& {log}'

#############################################
# Image Registration (anatomy reference)
#############################################
rule ir_anat:
    input:
        'data/{dataset}/source/all_exp.csv',
        'data/{dataset}/target/all_exp.csv',
        'data/{dataset}/source/x.csv',
        'data/{dataset}/target/x.csv',
        'data/{dataset}/source/y.csv',
        'data/{dataset}/target/y.csv',
        'data/{dataset}/source/anatomy.csv',
        'data/{dataset}/target/anatomy.csv'
    output:
        'output/{dataset}/ir_anat_{tx}/warped.txt',
        'output/{dataset}/ir_anat_{tx}/tx.pkl'
    container:
        'docker://koki/ir-experiments:20241001'
    resources:
        mem_mb=1000000
    benchmark:
        'benchmarks/{dataset}_ir_anat_{tx}.txt'
    log:
        'logs/{dataset}_ir_anat_{tx}.log'
    shell:
        'src/ir.sh {input[0]} {input[1]} {input[2]} {input[3]} {input[4]} {input[5]} {output} anatomy {wildcards.tx} {input[6]} {input[7]} >& {log}'
