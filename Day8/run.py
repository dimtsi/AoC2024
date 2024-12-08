from datetime import datetime
from functools import partial
from typing import Dict

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(line) for line in lines]
    return lines


def build_g(matrix):
    G = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != ".":
                G[(i, j)] = matrix[i][j]
    return G


def inbound(r, c, matrix):
    R, C = len(matrix), len(matrix[0])

    return (0 <= r < R) and (0 <= c < C)


def find_same(x, G):
    return [k for k in G if G[k] == G[x] and k != x]


def get_antin_loc(pos1, pos2, matrix):
    r1, c1 = pos1
    r2, c2 = pos2

    a1 = r1 - (r2 - r1), c1 - (c2 - c1)
    a2 = r2 - (r1 - r2), c2 - (c1 - c2)

    return [(r, c) for r, c in [a1, a2] if inbound(r, c, matrix)]


def get_antin_loc_p2(pos1, pos2, matrix):
    r1, c1 = pos1
    r2, c2 = pos2

    a1 = []
    # r,c
    i = 0
    r, c = r1, c1
    while inbound(r, c, matrix):
        a1.append((r, c))
        i += 1
        r, c = r1 - i * (r2 - r1), c1 - i * (c2 - c1)

    a2 = []
    r, c = r2, c2
    while inbound(r, c, matrix):
        a2.append((r, c))
        i += 1
        r, c = r2 - i * (r1 - r2), c2 - i * (c1 - c2)

    return a1 + a2


@timeit
def run(filename: str, p2=False):
    matrix = parse(filename)

    G: Dict = build_g(matrix)

    antinode_func = get_antin_loc if not p2 else get_antin_loc_p2

    locs = set()
    for b in G:
        for neigh in find_same(b, G):
            locs |= set(antinode_func(b, neigh, matrix))

    out = len(locs)
    return out


if __name__ == "__main__":
    day = 8
    dt = datetime(2024, 12, day)
    exp = {"a": 14, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
