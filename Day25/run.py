from collections import Counter
from datetime import datetime
from itertools import product

import numpy as np

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n\n")
    return lines


def run(filename: str):
    lines = parse(filename)

    L = []
    K = []

    for line in lines:
        if line.startswith("#"):
            L.append([list(row) for row in line.split("\n")])
        else:
            K.append([list(row) for row in line.split("\n")])

    KK = []
    LL = []

    for key in K:
        npk = np.array(key).T
        counts = [Counter(row)["#"] - 1 for row in npk]
        KK.append(counts)

    for lock in L:
        npl = np.array(lock).T
        counts = [Counter(row)["#"] - 1 for row in npl]
        LL.append(counts)

    score = 0
    for k, l in product(KK, LL):
        for kk, ll in zip(k, l):
            if 6 - ll <= kk:
                break
        else:
            score += 1

    return score


def runp2(filename: str):
    return run(filename)


if __name__ == "__main__":
    day = 25
    dt = datetime(2024, 12, day)
    exp = {"a": 3, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
