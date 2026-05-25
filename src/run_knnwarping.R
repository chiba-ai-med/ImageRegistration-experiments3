#!/usr/bin/env Rscript
# Script to run kNNWarping separately after guidedPLS

source("src/Functions.R")

# Load guidedPLS results
cat("Loading guidedPLS results...\n")
load("output_test/results_fixed.RData")

# Load original data
source_all_exp <- as.matrix(read.csv("data/source_small/all_exp.csv", header=TRUE))
source_anatomy <- as.matrix(read.csv("data/source_small/anatomy.csv", header=TRUE))

cat("Data dimensions:\n")
cat("source_all_exp:", dim(source_all_exp), "\n")
cat("source_anatomy:", dim(source_anatomy), "\n")

# Debug the guidedPLS output structure
cat("\nChecking guidedPLS output structure:\n")
cat("Names in out:", names(out), "\n")

# Try different parameter values
r_values <- c(5, 10, 15)
k_values <- c(3, 5, 7)

for(r in r_values){
    for(k in k_values){
        cat(sprintf("\nTrying r=%d, k=%d...\n", r, k))
        tryCatch({
            out2 <- kNNWarping(out, source_all_exp, source_anatomy, r=r, k=k)
            cat("Success!\n")
            
            # Save results
            write.table(out2$warped_exp, "output_test/warped_exp_knn.csv",
                col.names=TRUE, row.names=FALSE, sep=",")
            save(out, out2, file="output_test/results_complete.RData")
            cat("Results saved successfully\n")
            break
        }, error = function(e){
            cat("Failed:", e$message, "\n")
        })
    }
}