#!/usr/bin/env python3
"""
Create smaller subsampled datasets for testing
"""
import pandas as pd
import numpy as np
import os

# Create output directories
os.makedirs("data/source_small", exist_ok=True)
os.makedirs("data/target_small", exist_ok=True)

# Load original data
print("Loading original data...")
source_all_exp = pd.read_csv("data/source/all_exp.csv")
target_all_exp = pd.read_csv("data/target/all_exp.csv")
source_anatomy = pd.read_csv("data/source/anatomy.csv")
target_anatomy = pd.read_csv("data/target/anatomy.csv")

# Show original dimensions
print("\nOriginal data dimensions:")
print(f"source_all_exp: {source_all_exp.shape}")
print(f"target_all_exp: {target_all_exp.shape}")
print(f"source_anatomy: {source_anatomy.shape}")
print(f"target_anatomy: {target_anatomy.shape}")

# Set random seed for reproducibility
np.random.seed(42)

# Subsample rows for source (keep 100 random rows)
n_source_samples = min(100, len(source_all_exp))
source_sample_indices = np.random.choice(len(source_all_exp), n_source_samples, replace=False)
source_sample_indices.sort()

# Subsample rows for target (keep 100 random rows)
n_target_samples = min(100, len(target_all_exp))
target_sample_indices = np.random.choice(len(target_all_exp), n_target_samples, replace=False)
target_sample_indices.sort()

# Subsample columns (keep 50 random columns for expression data)
n_exp_cols = min(50, len(source_all_exp.columns))
exp_col_indices = np.random.choice(len(source_all_exp.columns), n_exp_cols, replace=False)

n_target_cols = min(50, len(target_all_exp.columns))
target_col_indices = np.random.choice(len(target_all_exp.columns), n_target_cols, replace=False)

# Create small datasets
source_all_exp_small = source_all_exp.iloc[source_sample_indices, exp_col_indices]
target_all_exp_small = target_all_exp.iloc[target_sample_indices, target_col_indices]
source_anatomy_small = source_anatomy.iloc[source_sample_indices, :]
target_anatomy_small = target_anatomy.iloc[target_sample_indices, :]

# Show new dimensions
print("\nSubsampled data dimensions:")
print(f"source_all_exp_small: {source_all_exp_small.shape}")
print(f"target_all_exp_small: {target_all_exp_small.shape}")
print(f"source_anatomy_small: {source_anatomy_small.shape}")
print(f"target_anatomy_small: {target_anatomy_small.shape}")

# Save small datasets
source_all_exp_small.to_csv("data/source_small/all_exp.csv", index=False)
target_all_exp_small.to_csv("data/target_small/all_exp.csv", index=False)
source_anatomy_small.to_csv("data/source_small/anatomy.csv", index=False)
target_anatomy_small.to_csv("data/target_small/anatomy.csv", index=False)

print("\nSmall datasets saved to data/source_small/ and data/target_small/")