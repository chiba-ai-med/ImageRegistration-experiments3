source("src/Functions.R")

# Parameter
infile1 <- commandArgs(trailingOnly=TRUE)[1]
infile2 <- commandArgs(trailingOnly=TRUE)[2]
infile3 <- commandArgs(trailingOnly=TRUE)[3]
infile4 <- commandArgs(trailingOnly=TRUE)[4]

# Default files if not provided
if(is.na(infile1)) infile1 = 'data/source/all_exp.csv'
if(is.na(infile2)) infile2 = 'data/target/all_exp.csv'
if(is.na(infile3)) infile3 = 'data/source/anatomy.csv'
if(is.na(infile4)) infile4 = 'data/target/anatomy.csv'

# Loading
source_all_exp <- as.matrix(read.csv(infile1, header=TRUE))
target_all_exp <- as.matrix(read.csv(infile2, header=TRUE))
source_anatomy <- as.matrix(read.csv(infile3, header=TRUE))
target_anatomy <- as.matrix(read.csv(infile4, header=TRUE))

# Check data dimensions
cat("Data dimensions:\n")
cat("source_all_exp:", dim(source_all_exp), "\n")
cat("target_all_exp:", dim(target_all_exp), "\n")
cat("source_anatomy:", dim(source_anatomy), "\n")
cat("target_anatomy:", dim(target_anatomy), "\n\n")

# Check for NA values
cat("NA values:\n")
cat("source_all_exp:", sum(is.na(source_all_exp)), "\n")
cat("target_all_exp:", sum(is.na(target_all_exp)), "\n")
cat("source_anatomy:", sum(is.na(source_anatomy)), "\n")
cat("target_anatomy:", sum(is.na(target_anatomy)), "\n\n")

# Check for infinite values
cat("Infinite values:\n")
cat("source_all_exp:", sum(is.infinite(source_all_exp)), "\n")
cat("target_all_exp:", sum(is.infinite(target_all_exp)), "\n")
cat("source_anatomy:", sum(is.infinite(source_anatomy)), "\n")
cat("target_anatomy:", sum(is.infinite(target_anatomy)), "\n\n")

# Check for negative values
cat("Negative values:\n")
cat("source_all_exp:", sum(source_all_exp < 0), "\n")
cat("target_all_exp:", sum(target_all_exp < 0), "\n")
cat("source_anatomy:", sum(source_anatomy < 0), "\n")
cat("target_anatomy:", sum(target_anatomy < 0), "\n\n")

# Check if all values are zero
cat("All zero columns:\n")
cat("source_all_exp:", sum(colSums(abs(source_all_exp)) == 0), "\n")
cat("target_all_exp:", sum(colSums(abs(target_all_exp)) == 0), "\n")
cat("source_anatomy:", sum(colSums(abs(source_anatomy)) == 0), "\n")
cat("target_anatomy:", sum(colSums(abs(target_anatomy)) == 0), "\n\n")

# Check data variance
cat("Variance check (columns with zero variance):\n")
cat("source_all_exp:", sum(apply(source_all_exp, 2, var) == 0), "\n")
cat("target_all_exp:", sum(apply(target_all_exp, 2, var) == 0), "\n")
cat("source_anatomy:", sum(apply(source_anatomy, 2, var) == 0), "\n")
cat("target_anatomy:", sum(apply(target_anatomy, 2, var) == 0), "\n\n")

# Check data range
cat("Data range:\n")
cat("source_all_exp: [", min(source_all_exp), ",", max(source_all_exp), "]\n")
cat("target_all_exp: [", min(target_all_exp), ",", max(target_all_exp), "]\n")
cat("source_anatomy: [", min(source_anatomy), ",", max(source_anatomy), "]\n")
cat("target_anatomy: [", min(target_anatomy), ",", max(target_anatomy), "]\n\n")

# Try guidedPLS with different lambda values
lambdas <- c(10^5, 10, 1, 0.1, 0.01, 0.001)
for(lambda_val in lambdas){
    cat("Testing lambda =", lambda_val, "\n")
    tryCatch({
        out <- guidedPLS(
            X1=source_all_exp,
            X2=target_all_exp,
            Y1=source_anatomy,
            Y2=target_anatomy,
            sumcor=TRUE,
            lambda=lambda_val,
            cortest=FALSE,  # Disable cortest for debugging
            verbose=FALSE)
        cat("  Success!\n")
    }, error = function(e){
        cat("  Error:", e$message, "\n")
    })
}

# Try with data preprocessing
cat("\nTrying with standardized data:\n")
# Standardize the data (mean 0, variance 1)
source_all_exp_std <- scale(source_all_exp)
target_all_exp_std <- scale(target_all_exp)
source_anatomy_std <- scale(source_anatomy)
target_anatomy_std <- scale(target_anatomy)

# Remove columns with zero variance after scaling
source_all_exp_std <- source_all_exp_std[, apply(source_all_exp_std, 2, function(x) !any(is.na(x)))]
target_all_exp_std <- target_all_exp_std[, apply(target_all_exp_std, 2, function(x) !any(is.na(x)))]
source_anatomy_std <- source_anatomy_std[, apply(source_anatomy_std, 2, function(x) !any(is.na(x)))]
target_anatomy_std <- target_anatomy_std[, apply(target_anatomy_std, 2, function(x) !any(is.na(x)))]

for(lambda_val in lambdas){
    cat("Testing lambda =", lambda_val, "with standardized data\n")
    tryCatch({
        out <- guidedPLS(
            X1=source_all_exp_std,
            X2=target_all_exp_std,
            Y1=source_anatomy_std,
            Y2=target_anatomy_std,
            sumcor=TRUE,
            lambda=lambda_val,
            cortest=FALSE,
            verbose=FALSE)
        cat("  Success!\n")
    }, error = function(e){
        cat("  Error:", e$message, "\n")
    })
}