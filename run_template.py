from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    print(lines)
    return lines


def run(filename: str):
    lines = parse(filename)
    return out


if __name__ == "__main__":
    day = 
    dt = datetime(2024, 12, day)
    exp = {"a": None, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", run, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", run, submit=True, dt=dt)
