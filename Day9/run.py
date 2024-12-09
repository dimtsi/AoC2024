from collections import deque
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")[0]
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
        lines = [int(x) for x in lines]
    return lines


def run(filename: str):
    l = parse(filename)

    x = deque([l[i] for i in range(0, len(l), 2)])
    y = deque([l[i] for i in range(1, len(l), 2)])

    q = []

    for i in range(max(len(x), len(y))):
        if 0 <= i < len(x):
            q.extend([i for _ in range(x[i])])

        if 0 <= i < len(y):
            q.extend(["." for _ in range(y[i])])

    l_idx, r_idx = 0, len(q) - 1
    while l_idx <= r_idx:
        while (0 <= l_idx < len(q)) and (q[l_idx] != "."):
            l_idx += 1
        while 0 <= r_idx < len(q) and q[r_idx] == ".":
            r_idx -= 1

        if 0 <= l_idx < len(q) and 0 <= r_idx < len(q):
            q[l_idx] = q[r_idx]
            r_idx -= 1

    q = q[: r_idx + 1]
    res = sum([i * v for (i, v) in enumerate(q)])
    return res


def runp2(filename: str):
    l = parse(filename)

    x_i = 0
    y_i = 0
    idx = 0

    x, y = [], []
    for i in range(len(l)):
        if i % 2 == 0:
            x.append([idx, x_i, l[i]])
            x_i += 1
        else:
            y.append([idx, ".", l[i]])
            y_i += 1

        idx += l[i]

    new = []
    for i, x_v in reversed(list(enumerate(x))):
        for j, y_v in enumerate(y):
            if x_v[0] >= y_v[0] and x_v[2] <= y_v[2] and y_v[2] != 0:
                new.append([y_v[0], x_v[1], x_v[2]])
                y.append([x_v[0], ".", x_v[2]])
                y[j][0] += x_v[2]
                y[j][2] -= x_v[2]
                x[i][2] = 0
                break

    x = [xx for xx in x if xx[2] != 0]
    y = [yy for yy in y if yy[2] != 0]
    new = [nn for nn in new if nn[2] != 0]

    total = 0
    m = list(sorted(x + new))

    for idx, val, off in m:
        for j in range(idx, idx + off):
            total += val * j

    res = total
    return res


if __name__ == "__main__":
    day = 9
    dt = datetime(2024, 12, day)
    exp = {"a": None, "b": 2858}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
