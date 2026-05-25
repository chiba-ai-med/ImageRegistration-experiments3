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
infile4 = args[4]
infile5 = args[5]
infile6 = args[6]
outfile1 = args[7]
outfile2 = args[8]
epsilon = float(args[9])

# Loading Data
source_all_exp = pd.read_csv(infile1, header=0)
target_all_exp = pd.read_csv(infile2, header=0)
source_x_coordinate = np.loadtxt(infile3)
target_x_coordinate = np.loadtxt(infile4)
source_y_coordinate = np.loadtxt(infile5)
target_y_coordinate = np.loadtxt(infile6)

# Column Names
source_cols = source_all_exp.columns.to_numpy()

# Log-Transformation
source_all_exp = np.log10(source_all_exp.to_numpy() + 1)
target_all_exp = np.log10(target_all_exp.to_numpy() + 1)

# Distance (Expression)
C1_exp = distance.cdist(source_all_exp, source_all_exp)
C2_exp = distance.cdist(target_all_exp, target_all_exp)

# Distance (Coordinate)
source_coordinate = np.stack([source_x_coordinate, source_y_coordinate], axis=1)
target_coordinate = np.stack([target_x_coordinate, target_y_coordinate], axis=1)
C1_cord = distance.cdist(source_coordinate, source_coordinate)
C2_cord = distance.cdist(target_coordinate, target_coordinate)

# Distance (Merge)
w1, w2 = 0.9, 0.1
C1 = w1 * C1_exp / np.max(C1_exp) + w2 * C1_cord / np.max(C1_cord)
C2 = w1 * C2_exp / np.max(C2_exp) + w2 * C2_cord / np.max(C2_cord)

# Merginal Distribution
h1 = np.ones(C1.shape[0]) / C1.shape[0]
h2 = np.ones(C2.shape[0]) / C2.shape[0]

# Clustering（重いステップ1、C1/C2に対しては計算できなかった）
part1 = KMeans(n_clusters=30, random_state=0, n_init="auto").fit(source_all_exp).labels_
part2 = KMeans(n_clusters=30, random_state=0, n_init="auto").fit(target_all_exp).labels_

# Cluster Center
rep_indices1 = ot.gromov.get_graph_representants(C1, part1, rep_method='pagerank')
rep_indices2 = ot.gromov.get_graph_representants(C2, part2, rep_method='pagerank')

# Formatting
CR1, list_R1, list_h1 = ot.gromov.format_partitioned_graph(
    C1, h1, part1, rep_indices1, F=None, M=None, alpha=1.)
CR2, list_R2, list_h2 = ot.gromov.format_partitioned_graph(
    C2, h2, part2, rep_indices2, F=None, M=None, alpha=1.)

# Partitioned quantized gromov-wasserstein solver（重いステップ2, build_OT=Falseなら動く）
T_global, Ts_local, _, log = ot.gromov.quantized_fused_gromov_wasserstein_partitioned(
    CR1, CR2, list_R1, list_R2, list_h1, list_h2, MR=None,
    alpha=1., build_OT=False, log=True, reg=epsilon, verbose=True)

# Transportation
t_source_all_exp = np.zeros((target_all_exp.shape[0], source_all_exp.shape[1]))

for i in range(30):
    list_Ti = []
    for j in range(30):
        if T_global[i, j] == 0.:
            T_local = np.zeros((list_R1[i].shape[0], list_R2[j].shape[0]))
        else:
            T_local = T_global[i, j] * Ts_local[(i, j)]
        list_Ti.append(T_local)
    Ti = np.concatenate(list_Ti, axis=1)
    # Normalization
    if Ti.max() != 0:
        row_sums = Ti.sum(axis=1)
        Ti = Ti / row_sums[:, np.newaxis]
    # Update
    position = np.where(part1 == i)[0]
    t_source_all_exp += Ti.T @ source_all_exp[position, ]

# Save
with open(outfile1, 'wb') as f:
    pickle.dump(T_global, f)
    pickle.dump(Ts_local, f)
    pickle.dump(log, f)

out = pd.DataFrame(t_source_all_exp)
out.columns = source_cols
out.to_csv(outfile2, index=False)
