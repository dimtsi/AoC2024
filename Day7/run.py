import re
from collections import deque
from datetime import datetime
from functools import partial

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(map(int, re.findall(r"\d+", line))) for line in lines]
    return lines


def calculate(res, nums, p2=False):
    s = nums[0]

    q = deque([(s, nums[1:])])

    while q:
        total, n = q.pop()

        if not n:
            if total == res:
                return True
            else:
                continue

        if total + n[0] <= res:
            q.append((total + n[0], n[1:]))
        if total * n[0] <= res:
            q.append((total * n[0], n[1:]))
        if p2:
            concat = int(str(total) + str(n[0]))
            if concat <= res:
                q.append((concat, n[1:]))
    return False


@timeit
def run(filename: str, p2=False):
    lines = parse(filename)

    out = 0
    for res, *nums in lines:
        if calculate(res, nums, p2):
            out += res

    return out


if __name__ == "__main__":
    day = 7
    dt = datetime(2024, 12, day)
    exp = {"a": 3749, "b": 11387}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
