Decision-Grade Scheduling & Geospatial Proximity

End-to-end algorithmic package for two enterprise decision primitives:

1. **Greedy / OR throughput:** maximize completed cases in a single procedure-room block (earliest-finish-time interval scheduling).
2. **Divide & conquer / asset proximity:** exact nearest pair in a sensing or logistics network (closest pair of points).

**Author:** Umesh Chandra Lavu · University of Florida (CISE)

**Submission artifact:** [`report/main.pdf`](report/main.pdf)

## Why this matters

| Decision | Business question | Guarantee |
|---|---|---|
| OR block scheduling | Which conflict-free cases maximize patients served? | Optimal cardinality, $O(n\log n)$ |
| Nearest-asset query | Which two sites are geographically closest? | Exact pair, $O(n\log n)$ |

Same abstractions transfer to classroom booking, EV-bay exclusivity, store cannibalization checks, and tower densification audits.

## Layout

```
report/          # ACM acmart paper (Overleaf-ready)
  main.tex
  main.pdf
  references.bib
  figures/       # experimental timing plots
  code/          # appendix source copies
code/
  greedy_interval_scheduling.py
  dac_closest_pair.py
  run_experiments.py
  results/       # CSV timing data
```

## Reproduce experiments

```bash
cd code
python3 greedy_interval_scheduling.py   # correctness checks
python3 dac_closest_pair.py             # correctness checks
python3 run_experiments.py              # timings + plots
```

Requires Python 3 and `matplotlib`.

## Compile the report

Upload `report/` to Overleaf (`acmart`), or locally:

```bash
cd report
pdflatex main && bibtex main && pdflatex main && pdflatex main
```
