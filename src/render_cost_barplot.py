"""Render Fig3D (time) and Fig3E (memory) — per-method computational cost.

Reads snakemake's benchmark files at `benchmarks/{dataset}_{method}_*.txt`
(format: tab-separated, first row column names, second row values; the
relevant columns are `s` for wall-time seconds and `max_rss` for peak RSS in
MB) and aggregates mean ± SD across all parameter values per method.

Layout matches Fig3B / Fig3C:
- one bar per method (qgw, frlc, lrgw, ir_*, guidedpls) — 10 methods total
- both tissues shown as grouped bars (brain vs kidney side by side)
- short / wide layout (10 × 3.5 in), 14-16 pt fonts
- separate horizontal legend (same as Fig3B legend; reuse)

Usage:
    python3 src/render_cost_barplot.py time   plot/Figures/main/Fig3D_cost_time.png
    python3 src/render_cost_barplot.py memory plot/Figures/main/Fig3E_cost_memory.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
PARAM_SETS = {
    "qgw":  ["1E+8", "1E+9", "1E+10", "1E+11", "1E+12", "1E+13", "1E+14"],
    "frlc": ["10", "20", "30", "50"],
    "lrgw": ["10", "20", "30", "50"],
}
DATASETS = ["251208", "kidney"]
TISSUE_LABEL = {"251208": "Brain", "kidney": "Kidney"}
COLUMN = {"time": "s", "memory": "max_rss"}
YLABEL = {"time": "Wall time (s)", "memory": "Peak RSS (MB)"}


def _read_value(path, col):
    if not Path(path).exists():
        return np.nan
    df = pd.read_csv(path, sep="\t")
    return float(df[col].iloc[0])


def _collect(dataset, metric):
    col = COLUMN[metric]
    out = {}
    for m in METHODS:
        if m in PARAM_SETS:
            vals = [_read_value(f"benchmarks/{dataset}_{m}_{p}.txt", col)
                    for p in PARAM_SETS[m]]
        else:
            vals = [_read_value(f"benchmarks/{dataset}_{m}.txt", col)]
        out[m] = np.asarray(vals, dtype=float)
    return out


def render(metric, out_path):
    data = {d: _collect(d, metric) for d in DATASETS}
    n_methods = len(METHODS)
    xpos = np.arange(n_methods)
    width = 0.4

    fig, ax = plt.subplots(figsize=(10, 3.5), dpi=150)
    for i, d in enumerate(DATASETS):
        means, sds = [], []
        for m in METHODS:
            vals = data[d][m]
            vals = vals[~np.isnan(vals)]
            means.append(vals.mean() if vals.size else np.nan)
            sds.append(vals.std(ddof=1) if vals.size > 1 else 0.0)
        offset = (i - 0.5) * width
        # hatch to distinguish tissues without relying on new colours
        hatch = "" if d == "251208" else "//"
        ax.bar(xpos + offset, means, width, yerr=sds,
               color=[COLORS[m] for m in METHODS],
               edgecolor="black", linewidth=0.5,
               hatch=hatch, capsize=3,
               error_kw=dict(elinewidth=1.2),
               label=TISSUE_LABEL[d])
    ax.set_xticks(xpos)
    ax.set_xticklabels(METHODS, rotation=45, ha="right", fontsize=14)
    ax.set_ylabel(YLABEL[metric], fontsize=16)
    ax.tick_params(axis="y", labelsize=14)
    if metric == "time":
        ax.set_yscale("log")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    # legend distinguishing tissues (hatch) — keep small, inside the plot
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor="lightgray", edgecolor="black",
                      hatch="", label="Brain"),
        plt.Rectangle((0, 0), 1, 1, facecolor="lightgray", edgecolor="black",
                      hatch="//", label="Kidney"),
    ]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    metric, out_path = sys.argv[1], sys.argv[2]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    render(metric, out_path)
