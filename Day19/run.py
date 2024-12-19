from datetime import datetime
from functools import cache, partial

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        pats, ls = f.read().strip().split("\n\n")

    pats = frozenset(pats.split(", "))
    ls = ls.split("\n")

    return pats, ls


@cache
def match(s, P):
    if s == "":
        return True
    else:
        for p in P:
            if s.startswith(p):
                if match(s[len(p) :], P):
                    return True
        return False


@cache
def matchp2(s, P):
    if s == "":
        return 1
    else:
        combs = 0
        for p in P:
            if s.startswith(p):
                combs += matchp2(s[len(p) :], P)
        return combs


def run(filename: str, p2=False):
    pats, ls = parse(filename)

    f = match if not p2 else matchp2

    score = 0
    for l in ls:
        res = f(l, pats)
        score += res
    return score


if __name__ == "__main__":
    day = 19
    dt = datetime(2024, 12, day)
    exp = {"a": 6, "b": 16}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=False, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
