from datetime import datetime

from utils import run_and_submit

DIRS = [
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (1, 1),
]


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return lines


def search(r, c, dr, dc, G):
    word = []
    while 0 <= r < len(G) and 0 <= c < len(G[0]) and len(word) < 4:
        word.append(G[r][c])
        r += dr
        c += dc
    if "".join(word) == "XMAS":
        return True
    return False


def run(filename: str):
    G = parse(filename)

    score = 0
    for r in range(len(G)):
        for c in range(len(G[0])):
            for dr, dc in DIRS:
                score += int(search(r, c, dr, dc, G))

    return score


def search2(r, c, G):
    diag1 = [G[r - 1][c - 1], G[r][c], G[r + 1][c + 1]]
    diag2 = [G[r - 1][c + 1], G[r][c], G[r + 1][c - 1]]

    if "".join(diag1) in ["MAS", "SAM"] and "".join(diag2) in ["MAS", "SAM"]:
        return True

    return False


def runp2(filename: str):
    G = parse(filename)

    score = 0
    for r in range(1, len(G) - 1):
        for c in range(1, len(G[0]) - 1):
            score += int(search2(r, c, G))

    out = score
    return out


if __name__ == "__main__":
    day = 4
    dt = datetime(2024, 12, day)
    exp = {"a": 18, "b": 9}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
