"""
Divide-and-conquer closest pair of points in the plane.

Domain: finding the two nearest weather stations (or delivery hubs).
Abstraction: given P subset R^2, return a pair minimizing Euclidean distance.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, float]
PairResult = Tuple[float, Point, Point]


def dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def closest_pair(points: Sequence[Point]) -> PairResult:
    """Return (distance, p, q) for a closest pair among points.

    Requires len(points) >= 2.
    """
    if len(points) < 2:
        raise ValueError("need at least two points")
    px = sorted(points, key=lambda p: (p[0], p[1]))
    py = sorted(points, key=lambda p: (p[1], p[0]))
    return _closest_rec(px, py)


def _closest_rec(px: List[Point], py: List[Point]) -> PairResult:
    n = len(px)
    if n <= 3:
        return _brute(px)

    mid = n // 2
    mid_x = px[mid][0]
    left_x = px[:mid]
    right_x = px[mid:]

    left_set = set(left_x)
    left_y = [p for p in py if p in left_set]
    right_y = [p for p in py if p not in left_set]

    dl, pl1, pl2 = _closest_rec(left_x, left_y)
    dr, pr1, pr2 = _closest_rec(right_x, right_y)
    if dl <= dr:
        delta, best_a, best_b = dl, pl1, pl2
    else:
        delta, best_a, best_b = dr, pr1, pr2

    strip = [p for p in py if abs(p[0] - mid_x) < delta]
    for i, p in enumerate(strip):
        # At most a constant number of candidates can lie in the delta x 2*delta box.
        for j in range(i + 1, min(i + 8, len(strip))):
            q = strip[j]
            if q[1] - p[1] >= delta:
                break
            d = dist(p, q)
            if d < delta:
                delta, best_a, best_b = d, p, q
    return delta, best_a, best_b


def _brute(points: Sequence[Point]) -> PairResult:
    best: Optional[PairResult] = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if best is None or d < best[0]:
                best = (d, points[i], points[j])
    assert best is not None
    return best


def closest_pair_brute(points: Sequence[Point]) -> PairResult:
    """O(n^2) oracle."""
    return _brute(points)


def generate_random_points(n: int, rng) -> List[Point]:
    return [(float(rng.random()), float(rng.random())) for _ in range(n)]


if __name__ == "__main__":
    import random

    rng = random.Random(1)
    for n in range(2, 30):
        for trial in range(25):
            pts = generate_random_points(n, rng)
            d1, a1, b1 = closest_pair(pts)
            d2, a2, b2 = closest_pair_brute(pts)
            assert abs(d1 - d2) < 1e-9, (n, trial, d1, d2, pts)
    print("dac_closest_pair: all oracle checks passed")
