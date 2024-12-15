import re
from collections import deque
from datetime import datetime
from pprint import pprint
from typing import Set

from utils import run_and_submit

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    # print(lines)
    return lines


def pos_at_t(t, pc, pr, vc, vr, R, C):
    out = (pr + vr * t) % R, (pc + vc * t) % C
    return out


def run(filename: str):
    rbts = parse(filename)
    if "sample" in filename:
        R, C = 7, 11
    else:
        R, C = 103, 101

    final_poss = [pos_at_t(100, *rbt, R, C) for rbt in rbts]

    x1, x2, x3, x4 = 0, 0, 0, 0

    for r, c in final_poss:
        if r == R // 2 or c == C // 2:
            continue
        if 0 <= r < R // 2:
            if 0 <= c < C // 2:
                x1 += 1
            else:
                x2 += 1
        else:
            if 0 <= c < C // 2:
                x3 += 1
            else:
                x4 += 1

    score = x1 * x2 * x3 * x4
    return score


def ppg(G):
    for row in G:
        pprint("".join(row))
    print("\n\n")


def bfs(G: Set):
    V = set()

    max_adj = 0
    for i, j in G:
        if (i, j) not in V:
            q = deque([(i, j)])

            v = set()
            while q:
                r, c = q.popleft()
                v.add((r, c))

                for dr, dc in DIRS:
                    rr, cc = r + dr, c + dc

                    if (rr, cc) in G and (rr, cc) not in v:
                        q.append((rr, cc))
            V |= v

            max_adj = max(max_adj, len(v))
    return max_adj


def runp2(filename: str):
    rbts = parse(filename)
    if "sample" in filename:
        R, C = 7, 11
    else:
        R, C = 103, 101

    max_adj_all, min_t = 0, float("inf")
    for t in range(20000):
        final_poss = {pos_at_t(t, *rbt, R, C) for rbt in rbts}  # type: ignore

        max_adj = bfs(final_poss)
        if max_adj > max_adj_all and max_adj > 50:
            G = [["." for _ in range(C)] for _ in range(R)]
            for r, c in final_poss:
                G[r][c] = "*"
            print(t)
            ppg(G)
            max_adj_all = max_adj
            min_t = min(min_t, t)
            break

    return min_t


if __name__ == "__main__":
    day = 14
    dt = datetime(2024, 12, day)
    exp = {"a": 12, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
