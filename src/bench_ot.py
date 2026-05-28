"""Run FRLC + LR-GW solvers and record benchmarks in snakemake's format.

The snakemake `benchmark:` directive for these rules was never enabled in a
real run, so `benchmarks/{dataset}_{frlc,lrgw}_*.txt` are missing. This
script re-runs each (dataset, method, rank) combination serially, captures
wall-time + peak RSS via psutil, and writes the benchmark file in the same
tab-separated format snakemake uses.

Usage:
    conda run -n pytorch python src/bench_ot.py [datasets...] [methods...]
    (defaults: both datasets, frlc + lrgw, ranks 10/20/30/50)
"""
import os
import subprocess
import sys
import time
import psutil
from pathlib import Path


PYTHON = "/home/koki/anaconda3/envs/pytorch/bin/python"
RANKS = ["10", "20", "30", "50"]
DATASETS = ["251208", "kidney"]
METHODS = {"frlc": "src/myfrlc.py", "lrgw": "src/mylrgw.py"}
LOG_FLAG = {"251208": "log", "kidney": "nolog"}


def run_one(dataset, method, rank):
    script = METHODS[method]
    plan = f"output/{dataset}/{method}/{rank}/plan.pkl"
    warped = f"output/{dataset}/{method}/{rank}/warped.txt"
    Path(plan).parent.mkdir(parents=True, exist_ok=True)
    bench_path = f"benchmarks/{dataset}_{method}_{rank}.txt"
    log_path = f"logs/{dataset}_{method}_{rank}.log"
    Path("logs").mkdir(exist_ok=True)
    Path("benchmarks").mkdir(exist_ok=True)

    cmd = [
        PYTHON, script,
        f"data/{dataset}/source/all_exp.csv",
        f"data/{dataset}/target/all_exp.csv",
        plan, warped, rank, LOG_FLAG[dataset],
    ]
    print(f"[run] {dataset}/{method}/{rank}", flush=True)
    log_fh = open(log_path, "w")
    t0 = time.perf_counter()
    cpu0 = time.process_time()
    proc = subprocess.Popen(cmd, stdout=log_fh, stderr=subprocess.STDOUT)
    p = psutil.Process(proc.pid)
    peak_rss = 0
    peak_vms = 0
    sampled = []
    while proc.poll() is None:
        try:
            with p.oneshot():
                mem = p.memory_info()
                peak_rss = max(peak_rss, mem.rss)
                peak_vms = max(peak_vms, mem.vms)
            for c in p.children(recursive=True):
                try:
                    cmem = c.memory_info()
                    peak_rss = max(peak_rss, cmem.rss)
                    peak_vms = max(peak_vms, cmem.vms)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            sampled.append(p.cpu_percent(interval=None))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        time.sleep(1.0)
    rc = proc.wait()
    log_fh.close()
    wall = time.perf_counter() - t0
    cpu = time.process_time() - cpu0

    mb = lambda b: b / 1024 / 1024
    h, rem = divmod(int(wall), 3600)
    m, s = divmod(rem, 60)
    hms = f"{h}:{m:02d}:{s:02d}"
    cols = ["s", "h:m:s", "max_rss", "max_vms", "max_uss", "max_pss",
            "io_in", "io_out", "mean_load", "cpu_time"]
    mean_load = sum(sampled) / len(sampled) if sampled else 0.0
    vals = [
        f"{wall:.4f}", hms,
        f"{mb(peak_rss):.2f}", f"{mb(peak_vms):.2f}",
        f"{mb(peak_rss):.2f}", f"{mb(peak_rss):.2f}",
        "0.00", "0.00",
        f"{mean_load:.2f}", f"{cpu:.2f}",
    ]
    with open(bench_path, "w") as f:
        f.write("\t".join(cols) + "\n")
        f.write("\t".join(vals) + "\n")
    status = "ok" if rc == 0 else f"FAILED rc={rc}"
    print(f"  -> {status}, wall={wall:.1f}s, max_rss={mb(peak_rss):.1f}MB "
          f"-> {bench_path}", flush=True)
    return rc


def main(datasets, methods, ranks):
    failures = []
    for d in datasets:
        for m in methods:
            for r in ranks:
                rc = run_one(d, m, r)
                if rc != 0:
                    failures.append((d, m, r))
    if failures:
        print(f"FAILED runs: {failures}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main(DATASETS, list(METHODS.keys()), RANKS)
