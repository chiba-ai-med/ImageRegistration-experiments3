# -*- coding: utf-8 -*-

# Package Loading
import sys
import os
import numpy as np
import pandas as pd
import torch
import pickle

# Add FRLC to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'FRLC', 'src'))
import FRLC
import util

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

device = 'cuda' if torch.cuda.is_available() else 'cpu'
dtype = torch.float64

print(f"Source: {source_exp_log.shape}, Target: {target_exp_log.shape}")
print(f"Device: {device}, Coupling rank: {coupling_rank}")

# Convert to torch tensors
X_source = torch.tensor(source_exp_log, dtype=dtype, device=device)
X_target = torch.tensor(target_exp_log, dtype=dtype, device=device)

# Low-rank distance factorization for intra-domain distances
lr_rank = 30   # rank for distance matrix factorization
lr_eps = 0.1   # approximation quality (smaller = better but slower)

print("Computing low-rank distance factorization for source...")
A1, A2 = util.low_rank_distance_factorization(
    X_source, X_source, r=lr_rank, eps=lr_eps, device=device, dtype=dtype)
# A ≈ A1 @ A2 where A1: (n1, lr_rank), A2: (lr_rank, n1)

print("Computing low-rank distance factorization for target...")
B1, B2 = util.low_rank_distance_factorization(
    X_target, X_target, r=lr_rank, eps=lr_eps, device=device, dtype=dtype)
# B ≈ B1 @ B2 where B1: (n2, lr_rank), B2: (lr_rank, n2)

# For pure GW (alpha=1.0), C is not used but API requires valid tensors
C1 = torch.zeros(n1, 1, dtype=dtype, device=device)
C2 = torch.zeros(1, n2, dtype=dtype, device=device)

# Run FRLC with GW (retry with lower gamma if NaN encountered)
for gamma_val in [90, 50, 30, 10, 5]:
    print(f"Running FRLC GW solver (gamma={gamma_val})...")
    Q, R, T, errs = FRLC.FRLC_LR_opt(
        C_factors=(C1, C2),
        A_factors=(A1, A2),
        B_factors=(B1, B2),
        r=coupling_rank,
        alpha=1.0,          # Pure GW (no Wasserstein term)
        device=device,
        dtype=dtype,
        printCost=False,
        min_iter=500,
        max_iter=1000,
        gamma=gamma_val,
        tau_in=50,
        convergence_criterion=True,
        tol=5e-6,
    )
    if not torch.isnan(T).any():
        print(f"Converged successfully with gamma={gamma_val}")
        break
    print(f"NaN detected with gamma={gamma_val}, retrying...")

# Compute warped expression using factored form
# P = Q @ Lambda @ R.T where Lambda = diag(1/gQ) @ T @ diag(1/gR)
one_N1 = torch.ones(n1, dtype=dtype, device=device)
one_N2 = torch.ones(n2, dtype=dtype, device=device)
gQ = Q.T @ one_N1
gR = R.T @ one_N2
Lambda = torch.diag(1.0 / gQ) @ T @ torch.diag(1.0 / gR)

# Use original (non-log) source expression for warping
source_orig_t = torch.tensor(source_exp_np, dtype=dtype, device=device)

# warped = P.T @ source = R @ Lambda.T @ Q.T @ source (factored, no full P)
step1 = Q.T @ source_orig_t       # (r, F)
step2 = Lambda.T @ step1          # (r, F)
warped = R @ step2                 # (n2, F)

# Normalize: divide by column sums of P (target marginal)
col_sums = R @ (Lambda.T @ gQ)    # (n2,)
warped = warped / col_sums.unsqueeze(1)

warped = warped.cpu().numpy()

# Save
os.makedirs(os.path.dirname(outfile1), exist_ok=True)
with open(outfile1, 'wb') as f:
    pickle.dump({
        'Q': Q.cpu().numpy(),
        'R': R.cpu().numpy(),
        'T': T.cpu().numpy(),
        'errs': errs
    }, f)

out = pd.DataFrame(warped)
out.columns = source_cols
out.to_csv(outfile2, index=False)

print("Done.")
