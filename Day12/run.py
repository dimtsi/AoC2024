from datetime import datetime
from functools import partial

from utils import run_and_submit

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return lines


def explore(start, G):
    q = [start]

    v = set()
    per = set()
    area = 0
    while q:
        r, c = q.pop()
        if (r, c) in v:
            continue

        v.add((r, c))
        area += 1

        for dr, dc in DIRS:
            rr, cc = r + dr, c + dc

            if (
                0 <= rr < len(G)
                and 0 <= cc < len(G[0])
                and G[rr][cc] == G[r][c]
            ):
                q.append((rr, cc))
            else:
                per.add((rr, cc, dr, dc))

    sides = set()
    for r, c, dr, dc in per:
        if (dr, dc) in [(0, 1), (0, -1)]:
            ddr, ddc = (1, 0)
        elif (dr, dc) in [(1, 0), (-1, 0)]:
            ddr, ddc = (0, 1)
        else:
            raise ValueError("error")
        if (r + ddr, c + ddc, dr, dc) in per:
            continue
        else:
            sides.add((r, c, dr, dc))
    return v, area, len(per), len(sides)


def run(filename: str, p2=False):
    G = parse(filename)

    regions = []
    V = set()

    score = 0
    for i in range(len(G)):
        for j in range(len(G[0])):
            if (i, j) not in V:
                reg, ar, per, sides = explore((i, j), G)
                regions.append(reg)
                V |= reg

                if not p2:
                    score += ar * per
                else:
                    score += ar * sides

    return score


if __name__ == "__main__":
    day = 12
    dt = datetime(2024, 12, day)
    exp = {
        "a": 140,
        "a2": 772,
        "a3": 1930,
        "b": 80,
        "b4": 368,
        "b2": 1206,
        "b5": 236,
    }

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/sample2.txt", "a", run, expected=exp["a2"])
    run_and_submit(f"Day{day}/sample3.txt", "a", run, expected=exp["a3"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=False, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/sample5.txt", "b", partial(run, p2=True), expected=exp["b5"]
    )
    run_and_submit(
        f"Day{day}/sample4.txt", "b", partial(run, p2=True), expected=exp["b4"]
    )
    run_and_submit(
        f"Day{day}/sample3.txt", "b", partial(run, p2=True), expected=exp["b2"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
