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
outfile1 = args[3]
outfile2 = args[4]
epsilon = float(args[5])

# Loading Data
source_all_exp = pd.read_csv(infile1, header=0)
target_all_exp = pd.read_csv(infile2, header=0)

# Column Names
source_cols = source_all_exp.columns.to_numpy()

# Gromov-Wasserstein Distance
Cx = distance.cdist(source_all_exp, source_all_exp, metric='euclidean')
Cy = distance.cdist(target_all_exp, target_all_exp, metric='euclidean')
Cx = Cx / np.max(Cx)
Cy = Cy / np.max(Cy)
p = ot.unif(source_all_exp.shape[0])
q = ot.unif(target_all_exp.shape[0])
P = ot.gromov.entropic_gromov_wasserstein(Cx, Cy, p, q, 'square_loss', epsilon=epsilon)

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
