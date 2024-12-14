import re
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint

from z3.z3 import Int, Optimize, sat

from utils import run_and_submit


@dataclass
class BP:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

    def __repr__(self):
        return f"BP: {self.ax}, {self.ay}, {self.bx}, {self.by}, {self.px}, {self.py}"


def parse(filename: str):
    with open(filename, "r") as f:
        bps = f.read().strip().split("\n\n")

        BPs = []
        for bp in bps:
            lines = list(map(int, re.findall("-?\d+", bp)))
            pprint(lines)
            BPs.append(BP(*lines))

    return BPs


def solve(bp):
    max_ax = bp.px // bp.ax + 1
    max_ay = bp.py // bp.ay + 1

    max_bx = bp.px // bp.bx + 1
    max_by = bp.py // bp.by + 1

    print(max_ax, max_ay, max_bx, max_by)

    score = float("inf")
    for n_a in range(min(max_ax, max_ay, 100)):
        for n_b in range(min(max_bx, max_by, 100)):
            if (
                n_a * bp.ax + n_b * bp.bx == bp.px
                and n_a * bp.ay + n_b * bp.by == bp.py
            ):
                score = min(score, 3 * n_a + n_b)
    if score == float("inf"):
        return 0
    return score


def run(filename: str):
    BPs = parse(filename)

    total = 0
    for bp in BPs:
        total += solvep2(bp)
    return total


def solvep2(bp):
    n_a = Int("n_a")
    n_b = Int("n_b")
    c = Int("c")

    o = Optimize()
    o.add(
        n_a * bp.ax + n_b * bp.bx == bp.px,
        n_a * bp.ay + n_b * bp.by == bp.py,
        n_a > 0,
        n_b > 0,
        n_a * 3 + n_b == c,
    )
    o.minimize(c)

    if o.check() == sat:
        sol = o.model()[c].as_long()
        return sol
    else:
        return 0


def runp2(filename: str):
    BPs = parse(filename)
    for bp in BPs:
        bp.px += 10000000000000
        bp.py += 10000000000000

    total = 0
    for bp in BPs:
        total += solvep2(bp)
    return total


if __name__ == "__main__":
    day = 13
    dt = datetime(2024, 12, day)
    exp = {"a": 480, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=False, dt=dt)
