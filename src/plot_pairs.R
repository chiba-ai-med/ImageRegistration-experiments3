source("src/Functions.R")

# Parameter
infile1 <- commandArgs(trailingOnly=TRUE)[1]
infile2 <- commandArgs(trailingOnly=TRUE)[2]
infile3 <- commandArgs(trailingOnly=TRUE)[3]
outfile1 <- commandArgs(trailingOnly=TRUE)[4]
outfile2 <- commandArgs(trailingOnly=TRUE)[5]
outfile3 <- commandArgs(trailingOnly=TRUE)[6]

# Loading
load(infile1)
source_anatomy <- read.csv(infile2, header=TRUE)
target_anatomy <- read.csv(infile3, header=TRUE)

# Matrix => Vector
source_anatomy <- apply(source_anatomy, 1, function(x){
	colnames(source_anatomy)[which(x == max(x))[1]]
})
target_anatomy <- apply(target_anatomy, 1, function(x){
	colnames(target_anatomy)[which(x == max(x))[1]]
})

# Plot
## Setting
scoreX1 <- apply(out$scoreX1, 2, scale)
scoreX2 <- apply(out$scoreX2, 2, scale)
ndim <- min(10, ncol(scoreX1), ncol(scoreX2))
score_labels <- paste("Score", 1:ndim)
mat_all <- rbind(
  scoreX1[, 1:ndim],
  scoreX2[, 1:ndim]
)

# Batch-wise
col_batch <- c(rep("red", length=length(source_anatomy)),
	rep("blue", length=length(target_anatomy)))
png(outfile1, width=2000, height=2000)
pairs(
  mat_all,
  labels     = score_labels,
  cex.labels = 3,
  pch        = 16,
  cex        = 2,
  col        = col_batch
)
dev.off()

# Anatomy-wise
col_anatomy <- factor(c(source_anatomy, target_anatomy))
levs <- levels(col_anatomy)
n    <- length(levs)
pal_base <- brewer.pal(8, "Set1")                      # Dark2 の 8 色
pal      <- colorRampPalette(pal_base)(n)               # n 色に展開
palette(pal)
png(outfile2, width=2000, height=2000)
pairs(
  mat_all,
  labels     = score_labels,
  cex.labels = 3,
  pch        = 16,
  cex        = 2,
  col        = as.numeric(col_anatomy)                  # 因子→数値で palette インデックス指定
)
dev.off()

png(outfile3, width=400, height=400)
par(mar = c(0,0,0,0))
plot.new()
legend(
  "center",
  legend = levs,
  pch    = 16,
  col    = pal,
  pt.cex = 2,
  bty    = "n",
  title  = "Anatomy"
)
dev.off()
