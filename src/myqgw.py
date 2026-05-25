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
use_log = args[6] if len(args) > 6 else "log"

# Loading Data
source_exp = pd.read_csv(infile1, header=0)
target_exp = pd.read_csv(infile2, header=0)

# Column Names
source_cols = source_exp.columns.to_numpy()

# Log-Transformation
source_exp = source_exp.to_numpy()
target_exp = target_exp.to_numpy()
if use_log == "log":
    source_exp = np.log10(source_exp + 1)
    target_exp = np.log10(target_exp + 1)

# Merginal Distribution
n1 = source_exp.shape[0]
n2 = target_exp.shape[0]
h1 = np.ones(n1) / n1
h2 = np.ones(n2) / n2

# Clustering
n_clusters = 30
part1 = KMeans(n_clusters=n_clusters, random_state=0, n_init="auto").fit(source_exp).labels_
part2 = KMeans(n_clusters=n_clusters, random_state=0, n_init="auto").fit(target_exp).labels_

# Estimate full matrix feasibility (float64, two matrices)
mem_C1 = n1 * n1 * 8
mem_C2 = n2 * n2 * 8
total_mem = mem_C1 + mem_C2
use_full_matrix = total_mem < 60e9  # 60 GB threshold

if use_full_matrix:
    print(f"Using full distance matrix (estimated {total_mem/1e9:.1f} GB)")

    # Distance
    C1 = distance.cdist(source_exp, source_exp)
    C2 = distance.cdist(target_exp, target_exp)
    C1 = C1 / np.max(C1)
    C2 = C2 / np.max(C2)

    # Cluster representatives
    rep_indices1 = ot.gromov.get_graph_representants(C1, part1, rep_method='pagerank')
    rep_indices2 = ot.gromov.get_graph_representants(C2, part2, rep_method='pagerank')

    # Formatting (uses POT's own implementation)
    CR1, list_R1, list_h1 = ot.gromov.format_partitioned_graph(
        C1, h1, part1, rep_indices1, F=None, M=None, alpha=1.)
    CR2, list_R2, list_h2 = ot.gromov.format_partitioned_graph(
        C2, h2, part2, rep_indices2, F=None, M=None, alpha=1.)

else:
    print(f"Using memory-efficient mode (full matrix would be {total_mem/1e9:.1f} GB)")

    def get_representants_and_format(exp, h, part, n_clusters):
        cluster_indices = [np.where(part == k)[0] for k in range(n_clusters)]

        # Get representative per cluster (point closest to centroid)
        rep_indices = np.zeros(n_clusters, dtype=int)
        for k in range(n_clusters):
            idx = cluster_indices[k]
            centroid = exp[idx].mean(axis=0)
            dists = np.linalg.norm(exp[idx] - centroid, axis=1)
            rep_indices[k] = idx[np.argmin(dists)]

        # Estimate global max distance by sampling
        sample_size = min(5000, exp.shape[0])
        sample_idx = np.random.RandomState(0).choice(exp.shape[0], sample_size, replace=False)
        sample_dists = distance.cdist(exp[sample_idx], exp[sample_idx])
        global_max = sample_dists.max()

        # CR: distance between representatives
        rep_exp = exp[rep_indices]
        CR = distance.cdist(rep_exp, rep_exp)
        global_max = max(global_max, CR.max())

        # list_R: 1D distance from representative to each member in its cluster
        list_R = []
        list_h = []
        for k in range(n_clusters):
            idx = cluster_indices[k]
            Rk = distance.cdist(exp[rep_indices[k]:rep_indices[k]+1], exp[idx])[0]
            global_max = max(global_max, Rk.max())
            list_R.append(Rk)
            list_h.append(h[idx])

        # Normalize by global max (consistent with format_partitioned_graph)
        if global_max > 0:
            CR = CR / global_max
            list_R = [R / global_max for R in list_R]

        return CR, list_R, list_h

    CR1, list_R1, list_h1 = get_representants_and_format(source_exp, h1, part1, n_clusters)
    CR2, list_R2, list_h2 = get_representants_and_format(target_exp, h2, part2, n_clusters)

# Partitioned quantized gromov-wasserstein solver
T_global, Ts_local, _, log = ot.gromov.quantized_fused_gromov_wasserstein_partitioned(
    CR1, CR2, list_R1, list_R2, list_h1, list_h2, MR=None,
    alpha=1., build_OT=False, log=True, reg=epsilon, verbose=True)

# Transportation
t_source_exp = np.zeros((target_exp.shape[0], source_exp.shape[1]))

for i in range(n_clusters):
    list_Ti = []
    for j in range(n_clusters):
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
    t_source_exp += Ti.T @ source_exp[position, ]

# Save
with open(outfile1, 'wb') as f:
    pickle.dump(T_global, f)
    pickle.dump(Ts_local, f)
    pickle.dump(log, f)

out = pd.DataFrame(t_source_exp)
out.columns = source_cols
out.to_csv(outfile2, index=False)
