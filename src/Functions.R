library("Mus.musculus")
library("tagcloud")
library("viridis")
library("ggplot2")
library("dplyr")
library("fields")
library("guidedPLS")
library("RANN")
library("RColorBrewer")

# Dataset-specific markers
get_markers <- function(dataset) {
    if (dataset == "251208") {
        list(
            source = c(
                "HexCer.36.1.O2.1", "HexCer.36.2.O2", "HexCer.38.2.O2",
                "HexCer.40.0.O2", "HexCer.40.1.O2", "HexCer.40.2.O2",
                "HexCer.41.1.O2", "HexCer.42.1.O2", "HexCer.42.2.O2",
                "HexCer.44.2.O2",
                "SM.31.1.O2", "SM.34.1.O2", "SM.35.1.O2",
                "SM.36.1.O2", "SM.36.2.O2", "SM.38.1.O2",
                "SM.41.2.O2", "SM.42.1.O2", "SM.42.2.O2", "SM.42.3.O2"),
            target = c("Mog", "Sox10"))
    } else if (dataset == "kidney") {
        list(
            source = c("FA.22.6"),
            target = c("Slc27a2"))
    } else {
        stop(paste("Unknown dataset:", dataset))
    }
}

cor_combination <- function(warped_exp, target_all_exp,
    source_markers, target_markers) {
	cor_mat <- matrix(NA,
		nrow = length(source_markers),
		ncol = length(target_markers),
		dimnames = list(source_markers, target_markers))
	for (s in source_markers) {
		for (t in target_markers) {
		cor_mat[s, t] <- cor(
			warped_exp[, s],
			target_all_exp[, t],
			method = "pearson")
		}
	}
	unlist(cor_mat)
}

# Warping based on kNN
kNNWarping <- function(out,
	source_all_exp, source_anatomy, r=5, k=5){
	scoreX1 <- apply(out$scoreX1, 2, scale)
	scoreX2 <- apply(out$scoreX2, 2, scale)
	r <- min(r, ncol(scoreX1), ncol(scoreX2))
	nn <- nn2(data  = scoreX1[, seq(r)],
	          query = scoreX2[, seq(r)], k = k)
	idx <- nn$nn.idx[,1:k]
	warped_exp <- t(apply(idx, 1, function(idxs) {
	  colMeans(source_all_exp[idxs, , drop = FALSE])
	}))
	warped_anatomy <- apply(idx, 1, function(idxs) {
	  tmp <- colMeans(source_anatomy[idxs, , drop = FALSE])
	  names(tmp)[which.max(tmp)]
	})
	list(warped_exp=warped_exp, warped_anatomy=warped_anatomy)	
}

# Jaccard index
jaccard <- function(a, b) {
    inter = sum(a*b)
    union = length(a) + length(b) - inter
    return (inter/union)
}

.mycolor <- function(z){
smoothPalette(z,
	palfunc=colorRampPalette(
		viridis(100), alpha=TRUE))
}

.mycolor2 <- function(z){
	factor(z, levels=sort(unique(z)))
}

# Flip y-axis
.plot_tissue_section <- function(x, y, z, cex=1){
	plot(x, -y, col=.mycolor(z), pch=16, cex=cex, xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
}

.plot_tissue_section2 <- function(x, y, z, cex=1, position="topright"){
	plot(x, -y, col=.mycolor2(z), pch=16, cex=cex, xaxt="n", yaxt="n", xlab="", ylab="", axes=FALSE)
	legend(position, legend=sort(unique(z)),
		col=factor(sort(unique(z))), pch=16, cex=2)
}
