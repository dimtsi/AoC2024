import re
from collections import deque
from datetime import datetime
from functools import cache
from itertools import pairwise

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [
            list(map(int, re.findall("-?\d+", line)))[0] for line in lines
        ]
    return lines


@cache
def next_(n):
    num = n * 64
    n ^= num
    n %= 16777216

    num = n // 32
    n ^= num
    n %= 16777216

    num = n * 2048
    n ^= num
    n %= 16777216

    return n


@timeit
def run(filename: str):
    lines = parse(filename)

    score = 0
    for n in lines:
        for _ in range(2000):
            n = next_(n)
        score += n

    return score


def get_sec_scores(n):
    mods = [x % 10 for x in n]
    diffs = [y - x for x, y in pairwise(mods)]

    seqs = {}

    w = deque([diffs[i] for i in range(3)])
    for i in range(4, len(diffs)):
        w.append(diffs[i - 1])
        key = tuple(w)
        if key not in seqs:
            seqs[key] = mods[i]
        w.popleft()
    return seqs


@timeit
def runp2(filename: str):
    lines = parse(filename)

    all_keys = set()
    seqs = []
    for n in lines:
        secrets = [n]

        for _ in range(2000):
            n = next_(n)
            secrets.append(n)
        res = get_sec_scores(secrets)
        seqs.append(res)
        all_keys |= set(res.keys())

    maxscore = 0
    for key in all_keys:
        score = sum(seq.get(key, 0) for seq in seqs)
        maxscore = max(maxscore, score)

    return maxscore


if __name__ == "__main__":
    day = 22
    dt = datetime(2024, 12, day)
    exp = {"a": 37327623, "b": 23}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample2.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
