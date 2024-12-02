import re
from collections import Counter
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    return lines


def run(filename: str):
    lines = parse(filename)
    l1 = [el[0] for el in lines]
    l2 = [el[1] for el in lines]

    l1.sort()
    l2.sort()

    dists = 0
    for a, b in zip(l1, l2):
        dists += abs(a - b)

    return dists


def runp2(filename: str):
    lines = parse(filename)
    l1 = [el[0] for el in lines]
    l2 = [el[1] for el in lines]

    c2 = Counter(l2)
    similarity = 0
    for a in l1:
        if a in c2:
            similarity += a * c2[a]

    out = similarity
    return out


if __name__ == "__main__":
    day = 1
    dt = datetime(2024, 12, day)
    exp = {"a": 11, "b": 31}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
