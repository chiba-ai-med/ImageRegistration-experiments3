# -*- coding: utf-8 -*-

# Package Loading
import sys
import os
import numpy as np
import pandas as pd
import pickle
import jax
import jax.numpy as jnp

from ott.geometry import pointcloud
from ott.problems.quadratic import quadratic_problem
from ott.solvers.quadratic import gromov_wasserstein_lr

# Arguments
args = sys.argv
infile1 = args[1]
infile2 = args[2]
outfile1 = args[3]
outfile2 = args[4]
coupling_rank = int(args[5])
use_log = args[6] if len(args) > 6 else "log"

# Loading Data
source_exp = pd.read_csv(infile1, header=0)
target_exp = pd.read_csv(infile2, header=0)

# Column Names
source_cols = source_exp.columns.to_numpy()

# Log-Transformation
source_exp_np = source_exp.to_numpy()
target_exp_np = target_exp.to_numpy()
if use_log == "log":
    source_exp_log = np.log10(source_exp_np + 1)
    target_exp_log = np.log10(target_exp_np + 1)
else:
    source_exp_log = source_exp_np.copy()
    target_exp_log = target_exp_np.copy()

n1 = source_exp_log.shape[0]
n2 = target_exp_log.shape[0]

print(f"Source: {source_exp_log.shape}, Target: {target_exp_log.shape}")
print(f"Coupling rank: {coupling_rank}")
print(f"JAX devices: {jax.devices()}")

# Convert to JAX arrays
X_source = jnp.array(source_exp_log, dtype=jnp.float32)
X_target = jnp.array(target_exp_log, dtype=jnp.float32)

# Create PointCloud geometries (lazy cost computation, no full matrix)
geom_xx = pointcloud.PointCloud(X_source, scale_cost="mean")
geom_yy = pointcloud.PointCloud(X_target, scale_cost="mean")

# Define the quadratic (GW) problem
# tau_a, tau_b < 1.0 for unbalanced; = 1.0 for balanced
prob = quadratic_problem.QuadraticProblem(
    geom_xx, geom_yy,
    tau_a=1.0,
    tau_b=1.0,
)

# Low-Rank GW solver
solver = gromov_wasserstein_lr.LRGromovWasserstein(
    rank=coupling_rank,
    epsilon=0.0,
    gamma=10.0,
    gamma_rescale=True,
    min_iterations=10,
    inner_iterations=10,
    max_iterations=2000,
)

print("Running Low-Rank GW solver (ott-jax)...")
out = solver(prob)
print(f"Converged: {out.converged}")

# Extract coupling factors
q = np.array(out.q)   # (n1, rank)
r = np.array(out.r)   # (n2, rank)
g = np.array(out.g)   # (rank,)

print(f"Q: {q.shape}, R: {r.shape}, g: {g.shape}")

# Compute warped expression using factored form
# P = Q @ diag(1/g) @ R.T
# warped = P.T @ source = R @ diag(1/g) @ Q.T @ source
inv_g = 1.0 / g
step1 = q.T @ source_exp_np        # (rank, F)
step2 = np.diag(inv_g) @ step1     # (rank, F)
warped = r @ step2                  # (n2, F)

# Normalize by target marginal
col_sums = r @ (inv_g * (q.T @ np.ones(n1)))  # (n2,)
warped = warped / col_sums[:, np.newaxis]

# Save
os.makedirs(os.path.dirname(outfile1), exist_ok=True)
with open(outfile1, 'wb') as f:
    pickle.dump({
        'q': q,
        'r': r,
        'g': g,
        'converged': bool(out.converged),
    }, f)

out_df = pd.DataFrame(warped)
out_df.columns = source_cols
out_df.to_csv(outfile2, index=False)

print("Done.")
