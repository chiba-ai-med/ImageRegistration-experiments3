"""Render the 6 IR-method kidney slice panels for Fig.3 supplementary.

The R plotting pipeline never generated kidney IR slices (the FINISH sentinel
exists but the per-marker PNGs are missing). The warped expression matrix is
in output/kidney/{ir_*}/warped.txt, so we read FA 22:6 from there and plot
on target coordinates, matching the kidney orientation (-y, -x).

Output: supplementary/representative_panels/kidney/method_comparison_alignment_{04..09}_{ir_*}.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path


IR_METHODS = [
    "ir_sum_rigid", "ir_sum_affine", "ir_sum_sitk_rigid",
    "ir_anat_rigid", "ir_anat_affine", "ir_anat_sitk_rigid",
]
COLUMN = "FA 22:6"  # warped.txt column for kidney evaluation marker


def main(s=900):
    x = pd.read_csv("data/kidney/target/x.csv", header=None).iloc[:, 0].values
    y = pd.read_csv("data/kidney/target/y.csv", header=None).iloc[:, 0].values
    out_dir = Path("plot/Figures/supplementary/representative_panels/kidney")
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, m in enumerate(IR_METHODS):
        warped_path = f"output/kidney/{m}/warped.txt"
        df = pd.read_csv(warped_path)
        if COLUMN not in df.columns:
            print(f"  SKIP {m}: '{COLUMN}' column not found", flush=True)
            continue
        z = df[COLUMN].values
        num = f"{i + 4:02d}"
        out = out_dir / f"method_comparison_alignment_{num}_{m}.png"
        fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
        ax.scatter(-y, -x, c=z, cmap="viridis", s=s, marker="o",
                   linewidths=0, edgecolors="none")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_aspect("equal")
        fig.savefig(out, dpi=100, transparent=True,
                    bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        print(f"  wrote {out}", flush=True)


if __name__ == "__main__":
    main(s=int(sys.argv[1]) if len(sys.argv) > 1 else 900)
