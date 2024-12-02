import re
from datetime import datetime
from functools import partial

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    return lines


def validate(line):
    if line[1] - line[0] > 0:
        incr = 1
    elif line[1] - line[0] < 0:
        incr = -1
    else:
        return 0

    for i, el in enumerate(line[1:], 1):
        if el - line[i - 1] not in [incr, 2 * incr, 3 * incr]:
            return 0

    return 1


def validate2(line):
    res = validate(line)
    if res == 1:
        return 1
    for i in range(len(line)):
        new_l = line[:i] + line[i + 1 :]
        res = validate(new_l)
        if res:
            return 1

    return 0


@timeit
def run(filename: str, p2=False):
    lines = parse(filename)

    out = 0
    for line in lines:
        val = (validate2 if p2 else validate)(line)
        out += val

    return out


if __name__ == "__main__":
    day = 2
    dt = datetime(2024, 12, day)
    exp = {"a": 2, "b": 4}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
