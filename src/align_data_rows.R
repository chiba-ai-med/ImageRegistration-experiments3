#!/usr/bin/env Rscript
# Script to align row counts between source and target data
# guidedPLS requires same number of samples in both domains

cat("========================================\n")
cat("Aligning source and target data rows\n")
cat("========================================\n\n")

# Create output directories
dir.create("data/aligned", showWarnings = FALSE, recursive = TRUE)

# Load original data
cat("Loading original data...\n")
source_all_exp <- read.csv("data/source/all_exp.csv", header=TRUE)
target_all_exp <- read.csv("data/target/all_exp.csv", header=TRUE)
source_anatomy <- read.csv("data/source/anatomy.csv", header=TRUE)
target_anatomy <- read.csv("data/target/anatomy.csv", header=TRUE)

# Show original dimensions
cat("\nOriginal dimensions:\n")
cat(sprintf("Source: %d samples × %d expression features\n", nrow(source_all_exp), ncol(source_all_exp)))
cat(sprintf("Target: %d samples × %d expression features\n", nrow(target_all_exp), ncol(target_all_exp)))

# Determine alignment strategy
n_source <- nrow(source_all_exp)
n_target <- nrow(target_all_exp)
n_aligned <- min(n_source, n_target)

cat(sprintf("\nAlignment strategy: Use %d samples (minimum of source and target)\n", n_aligned))

# Method 1: Random sampling to align sizes
set.seed(123)  # For reproducibility

if(n_source > n_aligned) {
    cat(sprintf("Subsampling source from %d to %d samples...\n", n_source, n_aligned))
    source_indices <- sample(1:n_source, n_aligned, replace=FALSE)
    source_indices <- sort(source_indices)
} else {
    source_indices <- 1:n_source
}

if(n_target > n_aligned) {
    cat(sprintf("Subsampling target from %d to %d samples...\n", n_target, n_aligned))
    target_indices <- sample(1:n_target, n_aligned, replace=FALSE)
    target_indices <- sort(target_indices)
} else {
    target_indices <- 1:n_target
}

# Create aligned datasets
source_all_exp_aligned <- source_all_exp[source_indices, ]
target_all_exp_aligned <- target_all_exp[target_indices, ]
source_anatomy_aligned <- source_anatomy[source_indices, ]
target_anatomy_aligned <- target_anatomy[target_indices, ]

# Verify alignment
cat("\nAligned dimensions:\n")
cat(sprintf("Source: %d samples × %d features\n", nrow(source_all_exp_aligned), ncol(source_all_exp_aligned)))
cat(sprintf("Target: %d samples × %d features\n", nrow(target_all_exp_aligned), ncol(target_all_exp_aligned)))
cat(sprintf("Source anatomy: %d samples × %d features\n", nrow(source_anatomy_aligned), ncol(source_anatomy_aligned)))
cat(sprintf("Target anatomy: %d samples × %d features\n", nrow(target_anatomy_aligned), ncol(target_anatomy_aligned)))

# Save aligned datasets
cat("\nSaving aligned datasets...\n")
write.csv(source_all_exp_aligned, "data/aligned/source_exp.csv", row.names=FALSE)
write.csv(target_all_exp_aligned, "data/aligned/target_exp.csv", row.names=FALSE)
write.csv(source_anatomy_aligned, "data/aligned/source_anatomy.csv", row.names=FALSE)
write.csv(target_anatomy_aligned, "data/aligned/target_anatomy.csv", row.names=FALSE)

cat("Aligned data saved to data/aligned/\n")

# Method 2: Create repeated/tiled version (alternative approach)
cat("\n========================================\n")
cat("Alternative: Creating repeated version\n")
cat("========================================\n")

# This approach repeats samples to match counts
max_samples <- max(n_source, n_target)

# Repeat source data if needed
if(n_source < max_samples) {
    repeat_times <- ceiling(max_samples / n_source)
    source_exp_repeated <- source_all_exp[rep(1:n_source, length.out=max_samples), ]
    source_anatomy_repeated <- source_anatomy[rep(1:n_source, length.out=max_samples), ]
} else {
    source_exp_repeated <- source_all_exp[1:max_samples, ]
    source_anatomy_repeated <- source_anatomy[1:max_samples, ]
}

# Repeat target data if needed
if(n_target < max_samples) {
    repeat_times <- ceiling(max_samples / n_target)
    target_exp_repeated <- target_all_exp[rep(1:n_target, length.out=max_samples), ]
    target_anatomy_repeated <- target_anatomy[rep(1:n_target, length.out=max_samples), ]
} else {
    target_exp_repeated <- target_all_exp[1:max_samples, ]
    target_anatomy_repeated <- target_anatomy[1:max_samples, ]
}

# Save repeated datasets
dir.create("data/repeated", showWarnings = FALSE, recursive = TRUE)
write.csv(source_exp_repeated, "data/repeated/source_exp.csv", row.names=FALSE)
write.csv(target_exp_repeated, "data/repeated/target_exp.csv", row.names=FALSE)
write.csv(source_anatomy_repeated, "data/repeated/source_anatomy.csv", row.names=FALSE)
write.csv(target_anatomy_repeated, "data/repeated/target_anatomy.csv", row.names=FALSE)

cat(sprintf("\nRepeated data (%d samples each) saved to data/repeated/\n", max_samples))

cat("\n========================================\n")
cat("Data alignment completed!\n")
cat("Use data/aligned/ for subsampled data\n")
cat("Use data/repeated/ for repeated data\n")
cat("========================================\n")