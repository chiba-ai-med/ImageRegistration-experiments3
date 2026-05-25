# -*- coding: utf-8 -*-

# Package Loading
import sys
import numpy as np
import pandas as pd
import ot
from scipy.spatial import distance
from sklearn.cluster import KMeans
import pickle

# Arguments
args = sys.argv
infile1 = args[1]
infile2 = args[2]
infile3 = args[3]
outfile1 = args[4]
outfile2 = args[5]
epsilon = float(args[6])

# Loading Data
source_all_exp = pd.read_csv(infile1, header=0)
source_exp = np.loadtxt(infile2)
target_exp = np.loadtxt(infile3)

# Column Names
source_cols = source_all_exp.columns.to_numpy()

# Distance (Expression)
source_exp = source_exp.reshape(1, -1)
target_exp = target_exp.reshape(1, -1)
C_exp = distance.cdist(source_exp.T, target_exp.T)

# Merginal Distribution
h1 = np.ones(C_exp.shape[0]) / C_exp.shape[0]
h2 = np.ones(C_exp.shape[1]) / C_exp.shape[1]

# Sinkhorn
P = ot.sinkhorn(h1, h2, C_exp, epsilon)

if P.max() != 0:
    row_sums = P.sum(axis=1)
    P = P / row_sums[:, np.newaxis]

# Transportation
t_source_all_exp = np.matmul(P.T, source_all_exp)

# Save
with open(outfile1, 'wb') as f:
    pickle.dump(P, f)

out = pd.DataFrame(t_source_all_exp)
out.columns = source_cols
out.to_csv(outfile2, index=False)
