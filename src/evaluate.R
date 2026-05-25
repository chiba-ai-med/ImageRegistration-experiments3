source("src/Functions.R")

# Parameter
dataset <- commandArgs(trailingOnly=TRUE)[1]
infile1 <- commandArgs(trailingOnly=TRUE)[2]
infile2 <- commandArgs(trailingOnly=TRUE)[3]
outfile <- commandArgs(trailingOnly=TRUE)[4]

# Loading
warped_exp <- read.csv(infile1, header=TRUE)
target_all_exp <- read.csv(infile2, header=TRUE)

# Correlation
markers <- get_markers(dataset)
out <- cor_combination(warped_exp, target_all_exp,
    markers$source, markers$target)

# Save
write.table(out, outfile, col.names=FALSE)
