import itertools
from collections import defaultdict
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")[0]
        lines = [[int(x)] for x in lines.split()]
    return lines


def calc(n):
    if n == 0:
        return [1]
    elif len(str(n)) % 2 == 0:
        l = len(str(n))
        sn = str(n)
        return [int(sn[: (l // 2)]), int(sn[(l // 2) :])]
    else:
        return [n * 2024]


def run(filename: str):
    ll = parse(filename)

    new = ll
    for _ in range(25):
        new = list(itertools.chain(*new[:]))
        next_ = []
        for n in new:
            next_.append(calc(n))
        new = next_[:]

    out = list(itertools.chain(*new[:]))
    return len(out)


def calc2(n, start_cnt, C):
    if n == 0:
        out = 1
        C[out] += start_cnt
    elif len(str(n)) % 2 == 0:
        sl = len(str(n))
        sn = str(n)
        out = [int(sn[: (sl // 2)]), int(sn[(sl // 2) :])]
        for o in out:
            C[o] += start_cnt
    else:
        C[n * 2024] += start_cnt

    C[n] -= start_cnt
    if C[n] == 0:
        C.pop(n)
    return C


def runp2(filename: str):
    ll = parse(filename)
    cnts = defaultdict(lambda: 0, {l[0]: 1 for l in ll})

    for _ in range(75):
        vals_start_cnts = list(cnts.items())
        for val, start_cnt in vals_start_cnts:
            cnts = calc2(val, start_cnt, cnts)

    score = sum(cnts.values())

    return score


if __name__ == "__main__":
    day = 11
    dt = datetime(2024, 12, day)
    exp = {"a": 55312, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
