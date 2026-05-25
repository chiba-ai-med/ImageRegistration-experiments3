source("src/Functions.R")

# Parameter
infile1 <- commandArgs(trailingOnly=TRUE)[1]
infile2 <- commandArgs(trailingOnly=TRUE)[2]
infile3 <- commandArgs(trailingOnly=TRUE)[3]
infile4 <- commandArgs(trailingOnly=TRUE)[4]
outfile1 <- commandArgs(trailingOnly=TRUE)[5]
outfile2 <- commandArgs(trailingOnly=TRUE)[6]
# infile1 = 'data/source/all_exp.csv'
# infile2 = 'data/target/all_exp.csv'
# infile3 = 'data/source/anatomy.csv'
# infile4 = 'data/target/anatomy.csv'

# Loading
source_all_exp <- as.matrix(read.csv(infile1, header=TRUE))
target_all_exp <- as.matrix(read.csv(infile2, header=TRUE))
source_anatomy <- as.matrix(read.csv(infile3, header=TRUE))
target_anatomy <- as.matrix(read.csv(infile4, header=TRUE))

# Guided-PLS
out <- guidedPLS(
	X1=source_all_exp,
	X2=target_all_exp,
	Y1=source_anatomy,
	Y2=target_anatomy,
	cortest=TRUE,
	verbose=TRUE)

out2 <- kNNWarping(out, source_all_exp, source_anatomy,
	r=18, k=11)

# Save
write.table(out2$warped_exp, outfile1,
    col.names=TRUE, row.names=FALSE, sep=",")
save(out, out2, file=outfile2)