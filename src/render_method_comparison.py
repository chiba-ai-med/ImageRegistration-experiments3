"""Render all method-comparison slice panels in supplementary/representative_panels/.

Reads each method's warped.txt and plots the evaluation marker on target
coordinates. Used to regenerate every slice at a consistent point size
without going through the R pipeline.

Brain marker:  HexCer.42.1.O2  (warped.txt col label "HexCer 42:1;O2"; actual name varies)
Kidney marker: FA.22.6         (warped.txt col label "FA 22:6")
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path


METHODS_BRAIN = [
    ("01_ir_sum_rigid",       "ir_sum_rigid",      False),
    ("02_ir_sum_affine",      "ir_sum_affine",     False),
    ("03_ir_sum_sitk_rigid",  "ir_sum_sitk_rigid", False),
    ("04_ir_anat_rigid",      "ir_anat_rigid",     False),
    ("05_ir_anat_affine",     "ir_anat_affine",    False),
    ("06_ir_anat_sitk_rigid", "ir_anat_sitk_rigid",False),
    ("07_qGW",                "qgw/1E+10",         False),
    ("08_FRLC",               "frlc/10",           False),
    ("09_LR-GW",              "lrgw/20",           False),
    ("10_guidedPLS",          "guidedpls",         False),
]
# Kidney: LR-GW absent (degenerate); slot 09 intentionally skipped
METHODS_KIDNEY = [
    ("01_ir_sum_rigid",       "ir_sum_rigid",      False),
    ("02_ir_sum_affine",      "ir_sum_affine",     False),
    ("03_ir_sum_sitk_rigid",  "ir_sum_sitk_rigid", False),
    ("04_ir_anat_rigid",      "ir_anat_rigid",     False),
    ("05_ir_anat_affine",     "ir_anat_affine",    False),
    ("06_ir_anat_sitk_rigid", "ir_anat_sitk_rigid",False),
    ("07_qGW",                "qgw/1E+10",         False),
    ("08_FRLC",               "frlc/20",           False),
    ("10_guidedPLS",          "guidedpls",         False),
]


def _coords(x, y, dataset):
    """Apply per-dataset target coordinate transform."""
    if dataset == "251208":
        y_flipped = y.max() - y + 1
        return x, -y_flipped
    elif dataset == "kidney":
        return -y, -x
    raise ValueError(dataset)


def _resolve_column(df_cols, marker):
    """Match a column whose name corresponds to the evaluation marker."""
    if marker in df_cols:
        return marker
    # Some warped.txt use space/colon naming: "HexCer 42:1;O2" vs marker "HexCer.42.1.O2"
    target = marker.replace(".", " ", 1).replace(".", ":", 1).replace(".", ";", 1)
    if target in df_cols:
        return target
    # Fall back to substring match
    matches = [c for c in df_cols if marker.replace(".", "").replace(":", "").replace(";", "")
               in c.replace(" ", "").replace(":", "").replace(";", "")]
    if matches:
        return matches[0]
    raise KeyError(f"could not find column for {marker} in warped.txt columns")


def render(dataset, methods, marker, s):
    name = "brain" if dataset == "251208" else dataset
    out_dir = Path(f"plot/Figures/supplementary/representative_panels/{name}")
    out_dir.mkdir(parents=True, exist_ok=True)
    x = pd.read_csv(f"data/{dataset}/target/x.csv", header=None).iloc[:, 0].values
    y = pd.read_csv(f"data/{dataset}/target/y.csv", header=None).iloc[:, 0].values
    xc, yc = _coords(x, y, dataset)

    # source panel (00_source) — render from original source coords
    sx = pd.read_csv(f"data/{dataset}/source/x.csv", header=None).iloc[:, 0].values
    sy = pd.read_csv(f"data/{dataset}/source/y.csv", header=None).iloc[:, 0].values
    src_df = pd.read_csv(f"data/{dataset}/source/all_exp.csv")
    src_col = _resolve_column(src_df.columns, marker)
    sz = src_df[src_col].values
    if dataset == "251208":
        # brain source uses same transform as target
        sy_flipped = sy.max() - sy + 1
        sxc, syc = sx, -sy_flipped
    else:  # kidney source
        sxc, syc = sy, -sx
    out = out_dir / "method_comparison_alignment_00_source.png"
    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    ax.scatter(sxc, syc, c=sz, cmap="viridis", s=s,
               marker="o", linewidths=0, edgecolors="none")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_aspect("equal")
    fig.savefig(out, dpi=100, transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"  wrote {out}", flush=True)

    # per-method panels
    for label, subpath, _ in methods:
        warped_path = f"output/{dataset}/{subpath}/warped.txt"
        try:
            df = pd.read_csv(warped_path)
        except FileNotFoundError:
            print(f"  SKIP {label}: {warped_path} missing", flush=True)
            continue
        try:
            col = _resolve_column(df.columns, marker)
        except KeyError:
            print(f"  SKIP {label}: column for {marker} not found", flush=True)
            continue
        z = df[col].values
        out = out_dir / f"method_comparison_alignment_{label}.png"
        fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
        ax.scatter(xc, yc, c=z, cmap="viridis", s=s,
                   marker="o", linewidths=0, edgecolors="none")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
        ax.set_aspect("equal")
        fig.savefig(out, dpi=100, transparent=True, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        print(f"  wrote {out}", flush=True)


if __name__ == "__main__":
    s_brain = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    s_kidney = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    render("251208", METHODS_BRAIN, "HexCer.42.1.O2", s_brain)
    render("kidney", METHODS_KIDNEY, "FA.22.6",       s_kidney)
