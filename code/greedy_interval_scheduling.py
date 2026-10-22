"""
Greedy interval scheduling by earliest finish time.

Domain: hospital operating-room / clinic appointment scheduling.
Abstraction: select a maximum-cardinality set of non-overlapping intervals.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

Interval = Tuple[float, float]  # (start, finish)


def schedule_earliest_finish(intervals: Sequence[Interval]) -> List[Interval]:
    """Return a maximum set of mutually non-overlapping intervals.

    Intervals are closed on the left and open on the right for adjacency:
    [s, f) and [f, f') do not overlap.
    """
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda iv: (iv[1], iv[0]))
    selected: List[Interval] = []
    last_finish = float("-inf")
    for start, finish in ordered:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    return selected


def schedule_brute_force(intervals: Sequence[Interval]) -> List[Interval]:
    """Exponential oracle: maximum compatible subset via subset enumeration."""
    n = len(intervals)
    best: List[Interval] = []
    for mask in range(1 << n):
        chosen = [intervals[i] for i in range(n) if mask & (1 << i)]
        if _compatible(chosen) and len(chosen) > len(best):
            best = chosen
    return best


def _compatible(intervals: Sequence[Interval]) -> bool:
    ordered = sorted(intervals, key=lambda iv: iv[0])
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:
            return False
    return True


def generate_random_intervals(n: int, rng) -> List[Interval]:
    """Generate n random half-open intervals on [0, 1]."""
    intervals: List[Interval] = []
    for _ in range(n):
        a = float(rng.random())
        b = float(rng.random())
        if a > b:
            a, b = b, a
        if a == b:
            b = min(1.0, a + 1e-6)
        intervals.append((a, b))
    return intervals


if __name__ == "__main__":
    import random

    rng = random.Random(0)
    for n in range(0, 12):
        for trial in range(40):
            ivs = generate_random_intervals(n, rng)
            g = schedule_earliest_finish(ivs)
            b = schedule_brute_force(ivs)
            assert len(g) == len(b), (n, trial, g, b, ivs)
            assert _compatible(g)
    print("greedy_interval_scheduling: all oracle checks passed")
