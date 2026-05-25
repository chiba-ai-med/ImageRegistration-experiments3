source("src/Functions.R")

# Parameter
dataset <- commandArgs(trailingOnly=TRUE)[1]
outfile <- commandArgs(trailingOnly=TRUE)[2]

# Loading
markers <- get_markers(dataset)
n_target_markers <- length(markers$target)
cc_cols <- 2:(1 + n_target_markers)
methods <- c("qgw", "frlc", "lrgw",
             "ir_sum_rigid", "ir_sum_affine", "ir_sum_sitk_rigid",
             "ir_anat_rigid", "ir_anat_affine", "ir_anat_sitk_rigid",
             "guidedpls")
qgw_params <- c("1E+8", "1E+9", "1E+10", "1E+11", "1E+12", "1E+13", "1E+14")
frlc_params <- c("10", "20", "30", "50")
lrgw_params <- c("10", "20", "30", "50")
gdata <- data.frame(method=NULL, cc=NULL, param=NULL)
for(p in qgw_params){
    qgw <- unlist(read.table(paste0("output/", dataset, "/qgw/", p, "/cc.csv"), header=FALSE)[, cc_cols])
    tmp <- data.frame(method="qgw", cc=qgw, param=p)
    gdata <- rbind(gdata, tmp)
}
for(p in frlc_params){
    frlc <- unlist(read.table(paste0("output/", dataset, "/frlc/", p, "/cc.csv"), header=FALSE)[, cc_cols])
    tmp <- data.frame(method="frlc", cc=frlc, param=p)
    gdata <- rbind(gdata, tmp)
}
for(p in lrgw_params){
    lrgw <- unlist(read.table(paste0("output/", dataset, "/lrgw/", p, "/cc.csv"), header=FALSE)[, cc_cols])
    tmp <- data.frame(method="lrgw", cc=lrgw, param=p)
    gdata <- rbind(gdata, tmp)
}
ir_methods <- c("ir_sum_rigid", "ir_sum_affine", "ir_sum_sitk_rigid",
                "ir_anat_rigid", "ir_anat_affine", "ir_anat_sitk_rigid")
for(m in ir_methods){
    ir <- unlist(read.table(paste0("output/", dataset, "/", m, "/cc.csv"), header=FALSE)[, cc_cols])
    tmp <- data.frame(method=m, cc=ir, param=NA)
    gdata <- rbind(gdata, tmp)
}
guidedpls <- unlist(read.table(paste0("output/", dataset, "/guidedpls/cc.csv"), header=FALSE)[, cc_cols])
tmp <- data.frame(method="guidedpls", cc=guidedpls, param=NA)
gdata <- rbind(gdata, tmp)
gdata$method <- factor(gdata$method, levels=methods)

# ggplot
# Calculate mean and standard deviation for each method and sample
gdata_summary <- gdata %>%
    group_by(method) %>%
    summarise(mean_cc = mean(cc, na.rm = TRUE),
              sd_cc = sd(cc, na.rm = TRUE))

# ggplot with error bars
g <- ggplot(gdata_summary, aes(x=method, y=mean_cc, fill=method)) +
    geom_bar(stat="identity", position=position_dodge(width=0.9)) +
    geom_errorbar(aes(ymin=mean_cc-sd_cc, ymax=mean_cc+sd_cc),
                  position=position_dodge(width=0.9), width=0.25) +
    theme(axis.text.x=element_text(angle=45, hjust=1)) +
    labs(title="", x="Method", y="CC") +
    scale_fill_manual(values=c(
        "qgw"="#1B9E77", "frlc"="#D95F02", "lrgw"="#7570B3",
        "ir_sum_rigid"="#E7298A", "ir_sum_affine"="#66A61E", "ir_sum_sitk_rigid"="#E6AB02",
        "ir_anat_rigid"="#A6761D", "ir_anat_affine"="#666666", "ir_anat_sitk_rigid"="#1F78B4",
        "guidedpls"="#E41A1C"))

ggsave(outfile, g, width=8, height=6, dpi=300)
