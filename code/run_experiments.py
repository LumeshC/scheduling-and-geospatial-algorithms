"""
Timing experiments for greedy interval scheduling and closest-pair D&C.

Produces CSV results and matplotlib figures under report/figures/.
"""

from __future__ import annotations

import csv
import math
import platform
import random
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from dac_closest_pair import closest_pair, generate_random_points
from greedy_interval_scheduling import (
    generate_random_intervals,
    schedule_earliest_finish,
)

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "report" / "figures"
DATA_DIR = ROOT / "code" / "results"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "figure.dpi": 140,
    }
)


def time_call(fn, *args, repeats: int = 5) -> float:
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - t0)
    return statistics.mean(times)


def run_greedy(sizes, trials_per_size: int = 5, seed: int = 42):
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        trial_times = []
        for _ in range(trials_per_size):
            ivs = generate_random_intervals(n, rng)
            trial_times.append(time_call(schedule_earliest_finish, ivs, repeats=3))
        mean_t = statistics.mean(trial_times)
        nlogn = n * math.log2(n) if n > 1 else 1.0
        rows.append(
            {
                "n": n,
                "mean_seconds": mean_t,
                "n_log_n": nlogn,
                "t_over_nlogn": mean_t / nlogn,
            }
        )
        print(f"greedy n={n}: {mean_t:.6e} s")
    return rows


def run_closest(sizes, trials_per_size: int = 5, seed: int = 7):
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        trial_times = []
        for _ in range(trials_per_size):
            pts = generate_random_points(n, rng)
            trial_times.append(time_call(closest_pair, pts, repeats=3))
        mean_t = statistics.mean(trial_times)
        nlogn = n * math.log2(n) if n > 1 else 1.0
        rows.append(
            {
                "n": n,
                "mean_seconds": mean_t,
                "n_log_n": nlogn,
                "t_over_nlogn": mean_t / nlogn,
            }
        )
        print(f"closest n={n}: {mean_t:.6e} s")
    return rows


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["n", "mean_seconds", "n_log_n", "t_over_nlogn"]
        )
        writer.writeheader()
        writer.writerows(rows)


def plot_results(rows, title: str, out_prefix: str):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    ns = [r["n"] for r in rows]
    ts = [r["mean_seconds"] for r in rows]
    ratios = [r["t_over_nlogn"] for r in rows]

    ref = [r["n_log_n"] for r in rows]
    scale = ts[-1] / ref[-1]
    ref_scaled = [scale * v for v in ref]

    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    ax.plot(ns, ts, "o-", label="Measured wall time", color="#0B3D5C", linewidth=2)
    ax.plot(
        ns,
        ref_scaled,
        "s--",
        label=r"Reference $c\,n\log_2 n$",
        color="#C45C26",
        linewidth=1.6,
    )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel(r"Problem size $n$")
    ax.set_ylabel("Mean wall-clock time (s)")
    ax.set_title(title)
    ax.legend(frameon=False)
    ax.grid(True, which="both", linestyle=":", alpha=0.55)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{out_prefix}_runtime.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    ax.plot(ns, ratios, "o-", color="#0B3D5C", linewidth=2)
    ax.set_xscale("log", base=2)
    ax.set_xlabel(r"Problem size $n$")
    ax.set_ylabel(r"$T(n)/(n\log_2 n)$")
    ax.set_title(title + r": normalized cost")
    ax.grid(True, which="both", linestyle=":", alpha=0.55)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{out_prefix}_ratio.pdf")
    plt.close(fig)


def main():
    print(f"Platform: {platform.platform()}")
    greedy_sizes = [2**k for k in range(10, 17)]
    closest_sizes = [2**k for k in range(10, 16)]

    print("=== Greedy interval scheduling ===")
    greedy_rows = run_greedy(greedy_sizes)
    write_csv(DATA_DIR / "greedy_timing.csv", greedy_rows)
    plot_results(
        greedy_rows,
        "OR block scheduling (earliest-finish greedy)",
        "greedy",
    )

    print("=== Closest pair (divide and conquer) ===")
    closest_rows = run_closest(closest_sizes)
    write_csv(DATA_DIR / "closest_timing.csv", closest_rows)
    plot_results(
        closest_rows,
        "Asset proximity query (closest-pair D&C)",
        "closest",
    )

    print(f"Figures written to {FIG_DIR}")
    print(f"CSV written to {DATA_DIR}")


if __name__ == "__main__":
    main()
