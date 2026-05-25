# Script to create smaller subsampled datasets for testing

# Create output directories
dir.create("data/source_small", showWarnings = FALSE, recursive = TRUE)
dir.create("data/target_small", showWarnings = FALSE, recursive = TRUE)

# Load original data
source_all_exp <- read.csv("data/source/all_exp.csv", header=TRUE)
target_all_exp <- read.csv("data/target/all_exp.csv", header=TRUE)
source_anatomy <- read.csv("data/source/anatomy.csv", header=TRUE)
target_anatomy <- read.csv("data/target/anatomy.csv", header=TRUE)

# Show original dimensions
cat("Original data dimensions:\n")
cat("source_all_exp:", dim(source_all_exp), "\n")
cat("target_all_exp:", dim(target_all_exp), "\n")
cat("source_anatomy:", dim(source_anatomy), "\n")
cat("target_anatomy:", dim(target_anatomy), "\n\n")

# Subsample rows (keep 100 random rows)
set.seed(42)  # For reproducibility
n_samples <- min(100, nrow(source_all_exp))
sample_indices <- sample(1:nrow(source_all_exp), n_samples)

# Subsample columns (keep 50 random columns for expression data)
n_exp_cols <- min(50, ncol(source_all_exp))
exp_col_indices <- sample(1:ncol(source_all_exp), n_exp_cols)

n_target_cols <- min(50, ncol(target_all_exp))
target_col_indices <- sample(1:ncol(target_all_exp), n_target_cols)

# Create small datasets
source_all_exp_small <- source_all_exp[sample_indices, exp_col_indices]
target_all_exp_small <- target_all_exp[sample_indices, target_col_indices]
source_anatomy_small <- source_anatomy[sample_indices, ]  # Keep all anatomy columns
target_anatomy_small <- target_anatomy[sample_indices, ]  # Keep all anatomy columns

# Show new dimensions
cat("Subsampled data dimensions:\n")
cat("source_all_exp_small:", dim(source_all_exp_small), "\n")
cat("target_all_exp_small:", dim(target_all_exp_small), "\n")
cat("source_anatomy_small:", dim(source_anatomy_small), "\n")
cat("target_anatomy_small:", dim(target_anatomy_small), "\n\n")

# Save small datasets
write.csv(source_all_exp_small, "data/source_small/all_exp.csv", row.names=FALSE)
write.csv(target_all_exp_small, "data/target_small/all_exp.csv", row.names=FALSE)
write.csv(source_anatomy_small, "data/source_small/anatomy.csv", row.names=FALSE)
write.csv(target_anatomy_small, "data/target_small/anatomy.csv", row.names=FALSE)

cat("Small datasets saved to data/source_small/ and data/target_small/\n")