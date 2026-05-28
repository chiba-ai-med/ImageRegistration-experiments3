source("src/Functions.R")

# Parameter
dataset <- commandArgs(trailingOnly=TRUE)[1]
infile1 <- commandArgs(trailingOnly=TRUE)[2]
infile2 <- commandArgs(trailingOnly=TRUE)[3]
infile3 <- commandArgs(trailingOnly=TRUE)[4]
infile4 <- commandArgs(trailingOnly=TRUE)[5]
infile5 <- commandArgs(trailingOnly=TRUE)[6]
infile6 <- commandArgs(trailingOnly=TRUE)[7]
infile7 <- commandArgs(trailingOnly=TRUE)[8]
infile8 <- commandArgs(trailingOnly=TRUE)[9]
infile9 <- commandArgs(trailingOnly=TRUE)[10]
infile10 <- commandArgs(trailingOnly=TRUE)[11]
outfile <- commandArgs(trailingOnly=TRUE)[12]

# Loading
source_all_exp <- read.csv(infile1, header=TRUE)
target_all_exp <- read.csv(infile2, header=TRUE)
source_exp <- read.csv(infile3, header=FALSE)
target_exp <- read.csv(infile4, header=FALSE)
source_anatomy <- read.csv(infile5, header=TRUE)
target_anatomy <- read.csv(infile6, header=TRUE)
source_x_coordinate <- unlist(read.csv(infile7, header=FALSE))
target_x_coordinate <- unlist(read.csv(infile8, header=FALSE))
source_y_coordinate <- unlist(read.csv(infile9, header=FALSE))
target_y_coordinate <- unlist(read.csv(infile10, header=FALSE))

# Flip y-axis (only for 251208)
if (dataset == "251208") {
    source_y_coordinate <- max(source_y_coordinate) - source_y_coordinate + 1
}

# Pre-processing
source_exp <- unlist(source_exp)
target_exp <- unlist(target_exp)

source_anatomy <- apply(source_anatomy, 1, function(x){
	colnames(source_anatomy)[which(x == max(x))[1]]
})
target_anatomy <- apply(target_anatomy, 1, function(x){
	colnames(target_anatomy)[which(x == max(x))[1]]
})

# Setting
outdir <- gsub("FINISH", "", outfile)
outfile1 = paste0(outdir, "source.png")
outfile2 = paste0(outdir, "target.png")
outfile3 = paste0(outdir, "source_log.png")
outfile4 = paste0(outdir, "target_log.png")
outfile5 = paste0(outdir, "source_density.png")
outfile6 = paste0(outdir, "target_density.png")
outfile7 = paste0(outdir, "source_log_density.png")
outfile8 = paste0(outdir, "target_log_density.png")
outfile9 = paste0(outdir, "source_anatomy.png")
outfile10 = paste0(outdir, "target_anatomy.png")

# Plot helpers for rotated kidney slices
.plot_rotated <- function(x, y, z, cex=1) {
    plot(-y, -x, col=.mycolor(z), pch=16, cex=cex,
        xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
}
.plot_rotated2 <- function(x, y, z, cex=1, position="topright") {
    plot(-y, -x, col=.mycolor2(z), pch=16, cex=cex,
        xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
    legend(position, legend=sort(unique(z)),
        col=factor(sort(unique(z))), pch=16, cex=2)
}

if (dataset == "kidney") {
    src_w <- 1200; src_h <- 1200; src_cex <- 3.5
    tgt_w <- 1200; tgt_h <- 1200; tgt_cex <- 3.5
    src_plot_fn <- function(x, y, z, cex=1) {
        plot(y, -x, col=.mycolor(z), pch=16, cex=cex,
            xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
    }
    src_plot_fn2 <- function(x, y, z, cex=1, position="topright") {
        plot(y, -x, col=.mycolor2(z), pch=16, cex=cex,
            xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
        legend(position, legend=sort(unique(z)),
            col=factor(sort(unique(z))), pch=16, cex=2)
    }
    tgt_plot_fn <- .plot_rotated
    tgt_plot_fn2 <- .plot_rotated2
} else {
    src_w <- 1200; src_h <- 1200; src_cex <- 1
    tgt_w <- 1200; tgt_h <- 1200; tgt_cex <- 3.5
    src_plot_fn <- .plot_tissue_section
    src_plot_fn2 <- .plot_tissue_section2
    tgt_plot_fn <- .plot_tissue_section
    tgt_plot_fn2 <- .plot_tissue_section2
}

## Slice Plot (Expression)
png(outfile1, width=src_w, height=src_h, bg="transparent")
src_plot_fn(source_x_coordinate, source_y_coordinate,
    source_exp, cex=src_cex)
dev.off()

png(outfile2, width=tgt_w, height=tgt_h, bg="transparent")
tgt_plot_fn(target_x_coordinate, target_y_coordinate,
    target_exp, cex=tgt_cex)
dev.off()

png(outfile3, width=src_w, height=src_h, bg="transparent")
src_plot_fn(source_x_coordinate, source_y_coordinate,
    log10(source_exp + 1), cex=src_cex)
dev.off()

png(outfile4, width=tgt_w, height=tgt_h, bg="transparent")
tgt_plot_fn(target_x_coordinate, target_y_coordinate,
    log10(target_exp + 1), cex=tgt_cex)
dev.off()

## Density Plot (Expression)
source_exp <- data.frame(Expression = source_exp)
g1 <- ggplot(source_exp, aes(x = Expression)) +
	geom_density(fill="red", alpha = 0.5) +
	labs(x = "Expression", y = "Density")
ggsave(outfile5, plot=g1, width = 12, height = 6, bg = "transparent")

target_exp <- data.frame(Expression = target_exp)
g2 <- ggplot(target_exp, aes(x = Expression)) +
	geom_density(fill="blue", alpha = 0.5) +
	labs(x = "Expression", y = "Density")
ggsave(outfile6, plot=g2, width = 12, height = 6, bg = "transparent")

g3 <- ggplot(log10(source_exp + 1), aes(x = Expression)) +
	geom_density(fill="red", alpha = 0.5) +
	labs(x = "Log10(Expression + 1)", y = "Density")
ggsave(outfile7, plot=g3, width = 12, height = 6, bg = "transparent")

g4 <- ggplot(log10(target_exp + 1), aes(x = Expression)) +
	geom_density(fill="blue", alpha = 0.5) +
	labs(x = "Log10(Expression + 1)", y = "Density")
ggsave(outfile8, plot=g4, width = 12, height = 6, bg = "transparent")

## Slice Plot (Anatomy)
png(outfile9, width=src_w, height=src_h, bg="transparent")
src_plot_fn2(source_x_coordinate, source_y_coordinate,
	source_anatomy, cex=src_cex, position="topright")
dev.off()

png(outfile10, width=tgt_w, height=tgt_h, bg="transparent")
tgt_plot_fn2(target_x_coordinate, target_y_coordinate,
	target_anatomy, cex=tgt_cex, position="topright")
dev.off()

# Plot
for(i in seq_len(ncol(source_all_exp))){
    filename = paste0(outdir, colnames(source_all_exp)[i], ".png")
    png(filename, width=src_w, height=src_h, bg="transparent")
    src_plot_fn(source_x_coordinate, source_y_coordinate,
        source_all_exp[,i], cex=src_cex)
    dev.off()
}

# Marker (Target)
markers <- get_markers(dataset)
for(i in markers$target){
    filename = paste0(outdir, i, ".png")
    png(filename, width=tgt_w, height=tgt_h, bg="transparent")
    tgt_plot_fn(target_x_coordinate, target_y_coordinate,
        target_all_exp[,i], cex=tgt_cex)
    dev.off()
}

# Save
file.create(outfile)
