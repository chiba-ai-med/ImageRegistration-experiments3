source("src/Functions.R")

# Parameter
infile1 <- commandArgs(trailingOnly=TRUE)[1]
infile2 <- commandArgs(trailingOnly=TRUE)[2]
infile3 <- commandArgs(trailingOnly=TRUE)[3]
outfile <- commandArgs(trailingOnly=TRUE)[4]

# Loading
t_source_exp <- read.csv(infile1, header=TRUE)
target_x_coordinate <- unlist(read.csv(infile2, header=FALSE))
target_y_coordinate <- unlist(read.csv(infile3, header=FALSE))

# Detect dataset from path
is_kidney <- grepl("kidney", outfile)

# Flip y-axis for 251208 (match plot_datasets.R)
if (!is_kidney) {
    target_y_coordinate <- max(target_y_coordinate) - target_y_coordinate + 1
}

# Plot
outdir <- gsub("FINISH", "", outfile)

if (is_kidney) {
    plot_w <- 1200; plot_h <- 1200; plot_cex <- 3.5
    plot_fn <- function(x, y, z, cex=1) {
        plot(-y, -x, col=.mycolor(z), pch=16, cex=cex,
            xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
    }
} else {
    plot_w <- 1200; plot_h <- 1200; plot_cex <- 3.5
    plot_fn <- function(x, y, z, cex=1) {
        .plot_tissue_section(x, y, z, cex=cex)
    }
}

for(i in seq_len(ncol(t_source_exp))){
    filename = paste0(outdir, colnames(t_source_exp)[i], ".png")
    png(filename, width=plot_w, height=plot_h, bg="transparent")
    plot_fn(target_x_coordinate, target_y_coordinate,
        t_source_exp[,i], cex=plot_cex)
    dev.off()
}

file.create(outfile)
