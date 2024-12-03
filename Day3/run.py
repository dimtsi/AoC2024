import re
from collections import deque
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return "".join(lines)


def run(filename: str):
    lines = parse(filename)

    matches = re.findall("mul\(\d+,\d+\)", lines)

    res = 0
    for match in matches:
        p1, p2 = list(map(int, re.findall("\d+", match)))
        res += p1 * p2

    return res


def runp2(filename: str):
    lines = parse(filename)

    matches = re.findall("(mul\(\d+,\d+\)|do\(\)|don't\(\))", lines)

    res = 0
    active = True

    q = deque(matches)

    while q:
        elem = q.popleft()
        if elem == "don't()":
            active = False
        elif elem == "do()":
            active = True
        else:
            if active:
                p1, p2 = list(map(int, re.findall("\d+", elem)))
                res += p1 * p2

    return res


if __name__ == "__main__":
    day = 3
    dt = datetime(2024, 12, day)
    exp = {"a": 161, "b": 48}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
