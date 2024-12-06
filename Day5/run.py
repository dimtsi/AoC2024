import re
from collections import defaultdict
from datetime import datetime
from functools import cmp_to_key, partial

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        rules, upd = f.read().strip().split("\n\n")

        rules = [
            list(map(int, re.findall(r"-?\d+", line)))
            for line in rules.split("\n")
        ]
        upd = [
            list(map(int, re.findall(r"-?\d+", line)))
            for line in upd.split("\n")
        ]
    return rules, upd


@timeit
def run(filename: str):
    rules, upd = parse(filename)

    G = defaultdict(set)

    for a, b in rules:
        G[b].add(a)

    score = 0

    for u in upd:
        for i in range(len(u)):
            el = u[i]
            rest = set(u[i + 1 :])
            if G[el] & rest:
                break
        else:
            score += u[(len(u) // 2)]

    return score


def cust_cmp(a, b, G):
    if a in G[b]:
        return -1
    elif b in G[a]:
        return 1
    else:
        return 0


@timeit
def runp2(filename: str):
    rules, upd = parse(filename)

    G = defaultdict(set)

    for a, b in rules:
        G[b].add(a)

    score = 0

    corrected = []
    for u in upd:
        sorted_u = list(sorted(u, key=cmp_to_key(partial(cust_cmp, G=G))))
        if sorted_u != u:
            corrected.append(sorted_u)

    for u in corrected:
        score += u[(len(u) // 2)]

    return score


if __name__ == "__main__":
    day = 5
    dt = datetime(2024, 12, day)
    exp = {"a": 143, "b": 123}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
