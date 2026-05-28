"""Render Fig3A tissue-slice panels (Python+matplotlib, no R).

Stand-alone, mirrors src/plot_datasets.R orientation handling per dataset:
- brain (251208): source uses (x, -y_flipped); target uses (x, -y_flipped)
- kidney:        source uses (y, -x);        target uses (-y, -x)
- viridis for expression, tab20 for anatomy
- 1200x1200 PNG, transparent bg, no axes

Use a larger `s` for kidney (12K spots, sparser) than for brain (47K spots).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sys


def _load(path):
    return pd.read_csv(path, header=None).iloc[:, 0].values


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


def _coords(x, y, dataset, side):
    """Return (xc, yc) for the scatter call, matching plot_datasets.R."""
    if dataset == "251208":
        # brain: plot_tissue_section uses plot(x, -y); R also flips y in src+tgt
        y_flipped = y.max() - y + 1
        return x, -y_flipped
    elif dataset == "kidney":
        if side == "source":
            return y, -x
        else:  # target
            return -y, -x
    raise ValueError(dataset)


def render_expr(dataset, side, exp_path, x_path, y_path, out_path,
                *, s, w=1200, h=1200, dpi=100):
    z = _load(exp_path)
    x, y = _load(x_path), _load(y_path)
    xc, yc = _coords(x, y, dataset, side)
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    ax.scatter(xc, yc, c=z, cmap="viridis", s=s, marker="o",
               linewidths=0, edgecolors="none")
    _blank_axes(ax)
    _save(fig, out_path, dpi)


def render_anatomy(dataset, side, anat_path, x_path, y_path, out_path,
                   *, s, w=1200, h=1200, dpi=100):
    df = pd.read_csv(anat_path)
    labels = df.idxmax(axis=1).values
    cats = sorted(set(labels))
    idx = [cats.index(l) for l in labels]
    cmap = matplotlib.colormaps["tab20"].resampled(len(cats))
    x, y = _load(x_path), _load(y_path)
    xc, yc = _coords(x, y, dataset, side)
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    ax.scatter(xc, yc, c=idx, cmap=cmap, s=s, marker="o",
               linewidths=0, edgecolors="none",
               vmin=-0.5, vmax=len(cats)-0.5)
    _blank_axes(ax)
    _save(fig, out_path, dpi)


def render_tissue(dataset, s):
    print(f"rendering {dataset} slices with s={s}", flush=True)
    name = "brain" if dataset == "251208" else dataset
    for side in ("source", "target"):
        render_expr(
            dataset, side,
            f"data/{dataset}/{side}/exp.csv",
            f"data/{dataset}/{side}/x.csv",
            f"data/{dataset}/{side}/y.csv",
            f"plot/Figures/main/Fig3A_{name}_{side}.png", s=s)
        render_anatomy(
            dataset, side,
            f"data/{dataset}/{side}/anatomy.csv",
            f"data/{dataset}/{side}/x.csv",
            f"data/{dataset}/{side}/y.csv",
            f"plot/Figures/main/Fig3A_{name}_{side}_anatomy.png", s=s)


if __name__ == "__main__":
    # Defaults tuned per density: kidney 12K spots (sparser) needs larger marker
    # area than brain 47K spots.
    if len(sys.argv) > 1:
        dataset = sys.argv[1]
        s = int(sys.argv[2]) if len(sys.argv) > 2 else (900 if dataset == "kidney" else 250)
        render_tissue(dataset, s)
    else:
        render_tissue("251208", 250)
        render_tissue("kidney", 900)
