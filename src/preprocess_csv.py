# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np

# Dataset config
DATASET_CONFIG = {
    '251208': {
        'source_file': 'data/251208/data/df_sl12.csv',
        'target_file': 'data/251208/data/df_st32.csv',
        'region_col': 'ccf_region_name',
        'source_marker': 'HexCer 42:1;O2',
        'target_marker': 'Mog',
    },
    'kidney': {
        'source_file': 'data/kidney/kidney_maldi.csv',
        'target_file': 'data/kidney/kidney_xenium.csv',
        'region_col': 'region',
        'source_marker': 'FA 22:6',
        'target_marker': 'Slc27a2',
    },
}

# Arguments
args = sys.argv
dataset = args[1]
outfile1 = args[2]
outfile2 = args[3]
outfile3 = args[4]
outfile4 = args[5]
outfile5 = args[6]
outfile6 = args[7]
outfile7 = args[8]
outfile8 = args[9]
outfile9 = args[10]
outfile10 = args[11]
outfile11 = args[12]
outfile12 = args[13]
outfile13 = args[14]
outfile14 = args[15]

# Config
config = DATASET_CONFIG[dataset]

# Loading
source_all_exp = pd.read_csv(config['source_file'], header=0)
target_all_exp = pd.read_csv(config['target_file'], header=0)

# Drop rows with missing or empty region
region_col = config['region_col']
source_all_exp = source_all_exp.dropna(subset=[region_col])
source_all_exp = source_all_exp[source_all_exp[region_col].str.strip() != ""]
target_all_exp = target_all_exp.dropna(subset=[region_col])
target_all_exp = target_all_exp[target_all_exp[region_col].str.strip() != ""]

source_anatomy = source_all_exp[['X', 'Y', region_col]]
target_anatomy = target_all_exp[['X', 'Y', region_col]]
source_all_exp = source_all_exp.drop([region_col], axis=1)
target_all_exp = target_all_exp.drop([region_col], axis=1)

# Sort
source_all_exp = source_all_exp.sort_values(by=['X', 'Y'])
target_all_exp = target_all_exp.sort_values(by=['X', 'Y'])
source_anatomy = source_anatomy.sort_values(by=['X', 'Y'])
target_anatomy = target_anatomy.sort_values(by=['X', 'Y'])

# Coordinates
source_x_coordinate = np.array(source_all_exp['X'].values, dtype=np.int64)
source_y_coordinate = np.array(source_all_exp['Y'].values, dtype=np.int64)
target_x_coordinate = np.array(target_all_exp['X'].values, dtype=np.int64)
target_y_coordinate = np.array(target_all_exp['Y'].values, dtype=np.int64)

# Drop X, Y from expression data
source_all_exp = source_all_exp.iloc[:, 2:]
target_all_exp = target_all_exp.iloc[:, 2:]

# Extract anatomy labels
source_anatomy = source_anatomy.iloc[:, 2:]
target_anatomy = target_anatomy.iloc[:, 2:]

# One-hot Encoding (CCF regions used as-is)
s_source = source_anatomy.squeeze()
s_target = target_anatomy.squeeze()
all_labels = sorted(pd.Index(s_source.unique()).union(s_target.unique()))
ohe_source = (
    pd.get_dummies(s_source)
    .reindex(columns=all_labels, fill_value=0)
    .astype(int)
)
ohe_target = (
    pd.get_dummies(s_target)
    .reindex(columns=all_labels, fill_value=0)
    .astype(int)
)

# Representative expression (single marker for visualization)
source_exp = source_all_exp[config['source_marker']].values
target_exp = target_all_exp[config['target_marker']].values

# Summation
source_sum_exp = source_all_exp.to_numpy(dtype=np.float64).sum(axis=1)
target_sum_exp = target_all_exp.to_numpy(dtype=np.float64).sum(axis=1)

# Binarization
bin_source_sum_exp = np.where(source_sum_exp > 0, 1, 0)
bin_target_sum_exp = np.where(target_sum_exp > 0, 1, 0)

# Save (order matches Snakemake output in preprocess.smk)
source_all_exp.to_csv(outfile1, index=False)      # data/{dataset}/source/all_exp.csv
target_all_exp.to_csv(outfile2, index=False)      # data/{dataset}/target/all_exp.csv
np.savetxt(outfile3, source_sum_exp, fmt='%.10f') # data/{dataset}/source/sum_exp.csv
np.savetxt(outfile4, target_sum_exp, fmt='%.10f') # data/{dataset}/target/sum_exp.csv
np.savetxt(outfile5, bin_source_sum_exp, fmt='%d') # data/{dataset}/source/bin_sum_exp.csv
np.savetxt(outfile6, bin_target_sum_exp, fmt='%d') # data/{dataset}/target/bin_sum_exp.csv
ohe_source.to_csv(outfile7, index=False)          # data/{dataset}/source/anatomy.csv
ohe_target.to_csv(outfile8, index=False)          # data/{dataset}/target/anatomy.csv
np.savetxt(outfile9, source_exp, fmt='%.10f')     # data/{dataset}/source/exp.csv
np.savetxt(outfile10, target_exp, fmt='%.10f')    # data/{dataset}/target/exp.csv
np.savetxt(outfile11, source_x_coordinate, fmt='%d') # data/{dataset}/source/x.csv
np.savetxt(outfile12, target_x_coordinate, fmt='%d') # data/{dataset}/target/x.csv
np.savetxt(outfile13, source_y_coordinate, fmt='%d') # data/{dataset}/source/y.csv
np.savetxt(outfile14, target_y_coordinate, fmt='%d') # data/{dataset}/target/y.csv
