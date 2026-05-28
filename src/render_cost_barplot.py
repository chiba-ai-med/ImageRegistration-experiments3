"""Render per-method computational-cost bar plots (one per dataset × metric).

Reads snakemake's benchmark files at `benchmarks/{dataset}_{method}_*.txt`
(tab-separated; columns `s` for wall-time seconds, `max_rss` for peak RSS MB)
and aggregates mean ± SD across all parameter values per method.

Layout mirrors Fig3B / Fig3C (one tissue per panel, no mixing):
- one bar per method (qgw, frlc, lrgw, ir_*, guidedpls) — 10 methods total
- short / wide layout (10 × 3.5 in), 14-16 pt fonts
- legend strip is the same as Fig3B/C — not regenerated here

Usage:
    python3 src/render_cost_barplot.py <dataset> <metric> <out>
    dataset ∈ {251208, kidney}; metric ∈ {time, memory}
Example:
    python3 src/render_cost_barplot.py 251208 time   plot/Figures/main/Fig3D_brain_cost_time.png
    python3 src/render_cost_barplot.py kidney memory plot/Figures/main/Fig3G_kidney_cost_memory.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from pathlib import Path


METHODS = [
    "ir_sum_rigid", "ir_sum_affine", "ir_sum_sitk_rigid",
    "ir_anat_rigid", "ir_anat_affine", "ir_anat_sitk_rigid",
    "qgw", "frlc", "lrgw",
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


def render(dataset, metric, out_path):
    data = _collect(dataset, metric)
    xpos = np.arange(len(METHODS))
    means, sds = [], []
    for m in METHODS:
        vals = data[m]
        vals = vals[~np.isnan(vals)]
        means.append(vals.mean() if vals.size else np.nan)
        sds.append(vals.std(ddof=1) if vals.size > 1 else 0.0)

    fig, ax = plt.subplots(figsize=(10, 3.5), dpi=150)
    ax.bar(xpos, means, yerr=sds,
           color=[COLORS[m] for m in METHODS],
           capsize=4, edgecolor="black", linewidth=0.5,
           error_kw=dict(elinewidth=1.5))
    # Strip x-axis tick labels; mapping comes from the shared legend strip
    ax.set_xticks(xpos)
    ax.set_xticklabels([])
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel(YLABEL[metric], fontsize=16)
    ax.tick_params(axis="y", labelsize=14)
    if metric == "time":
        ax.set_yscale("log")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    dataset, metric, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    render(dataset, metric, out_path)
