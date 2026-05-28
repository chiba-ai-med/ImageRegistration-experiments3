"""Render the 4 kidney slice panels for Fig3A with bigger markers.

Stand-alone (no R / no snakemake), mirrors src/plot_datasets.R kidney branch:
- source uses ( y, -x), target uses (-y, -x)
- categorical anatomy from argmax of one-hot columns
- viridis for expression, tab20 for anatomy
- 1200x1200 PNG, transparent bg, no axes
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sys


def _load_xy(x_path, y_path):
    x = pd.read_csv(x_path, header=None).iloc[:, 0].values
    y = pd.read_csv(y_path, header=None).iloc[:, 0].values
    return x, y


def _save(fig, out_path, dpi):
    fig.savefig(out_path, dpi=dpi, transparent=True,
                bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"  wrote {out_path}", flush=True)


def _blank_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_aspect("equal")


def render_expr(exp_path, x_path, y_path, out_path, *,
                target=False, s=900, w=1200, h=1200, dpi=100):
    z = pd.read_csv(exp_path, header=None).iloc[:, 0].values
    x, y = _load_xy(x_path, y_path)
    xc, yc = (-y, -x) if target else (y, -x)
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    ax.scatter(xc, yc, c=z, cmap="viridis", s=s, marker="o",
               linewidths=0, edgecolors="none")
    _blank_axes(ax)
    _save(fig, out_path, dpi)


def render_anatomy(anat_path, x_path, y_path, out_path, *,
                   target=False, s=900, w=1200, h=1200, dpi=100):
    df = pd.read_csv(anat_path)
    labels = df.idxmax(axis=1).values
    cats = sorted(set(labels))
    idx = [cats.index(l) for l in labels]
    cmap = matplotlib.colormaps["tab20"].resampled(len(cats))
    x, y = _load_xy(x_path, y_path)
    xc, yc = (-y, -x) if target else (y, -x)
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    ax.scatter(xc, yc, c=idx, cmap=cmap, s=s, marker="o",
               linewidths=0, edgecolors="none",
               vmin=-0.5, vmax=len(cats)-0.5)
    _blank_axes(ax)
    _save(fig, out_path, dpi)


def main(s=900):
    print(f"rendering kidney slices with s={s}", flush=True)
    render_expr(
        "data/kidney/source/exp.csv",
        "data/kidney/source/x.csv",
        "data/kidney/source/y.csv",
        "plot/Figures/main/Fig3A_kidney_source.png", s=s)
    render_expr(
        "data/kidney/target/exp.csv",
        "data/kidney/target/x.csv",
        "data/kidney/target/y.csv",
        "plot/Figures/main/Fig3A_kidney_target.png", target=True, s=s)
    render_anatomy(
        "data/kidney/source/anatomy.csv",
        "data/kidney/source/x.csv",
        "data/kidney/source/y.csv",
        "plot/Figures/main/Fig3A_kidney_source_anatomy.png", s=s)
    render_anatomy(
        "data/kidney/target/anatomy.csv",
        "data/kidney/target/x.csv",
        "data/kidney/target/y.csv",
        "plot/Figures/main/Fig3A_kidney_target_anatomy.png", target=True, s=s)


if __name__ == "__main__":
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    main(s=s)
