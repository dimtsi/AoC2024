import re
from datetime import datetime
from functools import partial

from utils import run_and_submit

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(map(int, re.findall("\d", line))) for line in lines]
    return lines


def dfs(start, G, cache):
    if start in cache:
        return cache[start]

    r, c = start
    elem = G[r][c]

    if elem == 9:
        cache[(r, c)] = {(r, c)}
        return {(r, c)}

    score = set()
    for dr, dc in DIRS:
        rr, cc = r + dr, c + dc

        if 0 <= rr < len(G) and 0 <= cc < len(G[0]) and G[rr][cc] - elem == 1:
            score |= dfs((rr, cc), G, cache)
    cache[start] = score
    return score


def dfs2(start, G, cache):
    if start in cache:
        return cache[start]

    r, c = start
    elem = G[r][c]

    if elem == 9:
        cache[(r, c)] = 1
        return 1

    score = 0
    for dr, dc in DIRS:
        rr, cc = r + dr, c + dc

        if 0 <= rr < len(G) and 0 <= cc < len(G[0]) and G[rr][cc] - elem == 1:
            score += dfs2((rr, cc), G, cache)
    cache[start] = score
    return score


def run(filename: str, p2=False):
    G = parse(filename)

    cache = {}
    score = 0
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == 0:
                if not p2:
                    score += len(dfs((i, j), G, cache))
                else:
                    score += dfs2((i, j), G, cache)
    return score


if __name__ == "__main__":
    day = 10
    dt = datetime(2024, 12, day)
    exp = {"a1": 3, "a2": 36, "b": 81}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a2"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
