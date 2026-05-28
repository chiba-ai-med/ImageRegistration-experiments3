"""Regenerate the per-method CC bar plot (Fig3B brain / Fig3C kidney).

Reads output/{dataset}/{method}/.../cc.csv for all methods listed in the
original src/plot_cc.R; aggregates mean ± SD across all (parameter, marker)
combinations per method; emits a wide / short bar plot with a separate
legend file. PNGs land at the destination paths passed on the command line.

Usage:
    python3 src/render_cc_barplot.py <dataset> <out_bar> <out_legend>

Example:
    python3 src/render_cc_barplot.py 251208 plot/Figures/main/Fig3B_brain_cc_summary.png plot/Figures/main/Fig3B_brain_cc_summary_legend.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import sys
from pathlib import Path


METHODS = [
    "qgw", "frlc", "lrgw",
    "ir_sum_rigid", "ir_sum_affine", "ir_sum_sitk_rigid",
    "ir_anat_rigid", "ir_anat_affine", "ir_anat_sitk_rigid",
    "guidedpls",
]
COLORS = {
    "qgw": "#1B9E77", "frlc": "#D95F02", "lrgw": "#7570B3",
    "ir_sum_rigid": "#E7298A", "ir_sum_affine": "#66A61E",
    "ir_sum_sitk_rigid": "#E6AB02",
    "ir_anat_rigid": "#A6761D", "ir_anat_affine": "#666666",
    "ir_anat_sitk_rigid": "#1F78B4",
    "guidedpls": "#E41A1C",
}
QGW_PARAMS = ["1E+8", "1E+9", "1E+10", "1E+11", "1E+12", "1E+13", "1E+14"]
FRLC_PARAMS = ["10", "20", "30", "50"]
LRGW_PARAMS = ["10", "20", "30", "50"]


def _read_cc(path):
    df = pd.read_csv(path, header=None, sep=r"\s+", engine="python")
    return df.iloc[:, 1:].values.flatten()


def _collect(dataset):
    out = {}
    for p in QGW_PARAMS:
        out.setdefault("qgw", []).extend(
            _read_cc(f"output/{dataset}/qgw/{p}/cc.csv"))
    for p in FRLC_PARAMS:
        out.setdefault("frlc", []).extend(
            _read_cc(f"output/{dataset}/frlc/{p}/cc.csv"))
    for p in LRGW_PARAMS:
        out.setdefault("lrgw", []).extend(
            _read_cc(f"output/{dataset}/lrgw/{p}/cc.csv"))
    for m in METHODS:
        if m in ("qgw", "frlc", "lrgw"):
            continue
        out[m] = list(_read_cc(f"output/{dataset}/{m}/cc.csv"))
    return out


def render(dataset, out_bar, out_legend):
    data = _collect(dataset)
    means = []
    sds = []
    for m in METHODS:
        vals = np.asarray(data[m], dtype=float)
        vals = vals[~np.isnan(vals)]
        means.append(vals.mean() if vals.size else 0.0)
        sds.append(vals.std(ddof=1) if vals.size > 1 else 0.0)

    fig, ax = plt.subplots(figsize=(10, 3.5), dpi=150)
    xpos = np.arange(len(METHODS))
    ax.bar(xpos, means, yerr=sds,
           color=[COLORS[m] for m in METHODS],
           capsize=4, edgecolor="black", linewidth=0.5,
           error_kw=dict(elinewidth=1.5))
    ax.set_xticks(xpos)
    ax.set_xticklabels(METHODS, rotation=45, ha="right", fontsize=14)
    ax.set_ylabel("CC", fontsize=16)
    ax.tick_params(axis="y", labelsize=14)
    ax.axhline(0, color="black", linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_bar, dpi=150, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_bar}")

    fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=150)
    handles = [mpatches.Patch(color=COLORS[m], label=m) for m in METHODS]
    ax.legend(handles=handles, loc="center", frameon=False, fontsize=14,
              title="Method", title_fontsize=16)
    ax.axis("off")
    fig.savefig(out_legend, dpi=150, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_legend}")


if __name__ == "__main__":
    dataset, out_bar, out_legend = sys.argv[1], sys.argv[2], sys.argv[3]
    Path(out_bar).parent.mkdir(parents=True, exist_ok=True)
    render(dataset, out_bar, out_legend)
