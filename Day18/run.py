import re
from collections import defaultdict
from datetime import datetime
from heapq import heappop, heappush

from aoc_helpers import DIRS
from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]

    return lines


DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def dijkstra(R, C, B, start, end):
    distances = defaultdict(lambda: float("inf"))
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, (r, c) = heappop(pq)
        state = r, c

        if state in visited:
            continue
        visited.add(state)

        for dr, dc in DIRS:
            rr, cc = r + dr, c + dc
            new_state = (rr, cc)
            if (
                new_state not in B
                and 0 <= rr < R
                and 0 <= cc < C
                and distances[new_state] > dist + 1
            ):
                distances[new_state] = dist + 1
                heappush(pq, (dist + 1, new_state))

    min_dist = distances[end]
    return min_dist


def run(filename: str):
    lines = parse(filename)

    lim = 12 if "sample" in filename else 1024
    R, C = (7, 7) if "sample" in filename else (71, 71)

    B = {(r, c) for (r, c) in lines[:lim]}

    out = dijkstra(R, C, B, (0, 0), (R - 1, C - 1))

    return out


@timeit
def runp2(filename: str):
    lines = parse(filename)

    lim = (
        12 if "sample" in filename else 1024
    )  # p1 solution for faster iteration
    R, C = (7, 7) if "sample" in filename else (71, 71)

    out = None
    for i in range(lim, len(lines), 1):
        BL = lines[:i]
        B = {(r, c) for (r, c) in BL}
        out = dijkstra(R, C, B, (0, 0), (R - 1, C - 1))
        if out == float("inf"):
            break

    res = ",".join((str(x) for x in BL[-1]))
    return res


if __name__ == "__main__":
    day = 18
    dt = datetime(2024, 12, day)
    exp = {"a": 22, "b": "6,1"}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
