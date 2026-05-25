import pandas as pd
from snakemake.utils import min_version

#################################
# Setting
#################################
min_version("8.10.0")

DATASETS = ['251208', 'kidney']

container: 'docker://koki/ir-experiments-r:20250826'

rule all:
	input:
		expand('output/{dataset}/guidedpls/warped.txt', dataset=DATASETS),
		expand('output/{dataset}/guidedpls/guidedpls.RData', dataset=DATASETS)

rule guidedpls:
	input:
		'data/{dataset}/source/all_exp.csv',
		'data/{dataset}/target/all_exp.csv',
		'data/{dataset}/source/anatomy.csv',
		'data/{dataset}/target/anatomy.csv'
	output:
		'output/{dataset}/guidedpls/warped.txt',
		'output/{dataset}/guidedpls/guidedpls.RData'
	resources:
		mem_mb=1000000
	benchmark:
		'benchmarks/{dataset}_guidedpls.txt'
	log:
		'logs/{dataset}_guidedpls.log'
	shell:
		'src/guidedpls.sh {input} {output} >& {log}'
