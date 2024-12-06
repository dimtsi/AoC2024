from copy import deepcopy
from datetime import datetime
from pprint import pprint

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return lines


def rot(dr, dc):
    return {
        (1, 0): (0, -1),
        (0, 1): (1, 0),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1),
    }[(dr, dc)]


def inbound(r, c, G):
    return (0 <= r < len(G)) and (0 <= c < len(G[0]))


def find_start(G):
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "^":
                return (i, j)
    raise ValueError("start not Found")


def pg(G, r, c):
    GG = deepcopy(G)
    for i in range(len(GG)):
        row = list(GG[i])
        for j in range(len(GG[0])):
            if (i, j) == (r, c):
                row[j] = "X"
        pprint("".join(row))
    print("\n\n")


def get_path(G, start):
    r, c, dr, dc = *start, -1, 0
    moves = 0
    poss = set()

    while inbound(r, c, G):
        poss.add((r, c))
        while inbound(r + dr, c + dc, G) and G[r + dr][c + dc] == "#":
            dr, dc = rot(dr, dc)
        moves += 1
        r += dr
        c += dc

    return poss | set([start])


@timeit
def run(filename: str):
    G = parse(filename)
    start = find_start(G)

    path = get_path(G, start)

    return len(path)


def check_has_loop(G, start):
    r, c, dr, dc = *start, -1, 0
    moves = 0
    curr_path = set()
    while inbound(r, c, G):
        if (r, c, dr, dc) in curr_path:
            return True

        curr_path.add((r, c, dr, dc))

        while inbound(r + dr, c + dc, G) and G[r + dr][c + dc] == "#":
            dr, dc = rot(dr, dc)
        moves += 1
        r += dr
        c += dc

    return False


@timeit
def runp2(filename: str):
    G = parse(filename)
    start = find_start(G)
    O = get_path(G, start)

    res = 0
    G = [list(row) for row in G]
    for i, j in O:
        if not inbound(i, j, G) or (i, j) == start:
            continue
        G[i][j] = "#"
        res += check_has_loop(G, start)
        G[i][j] = "."

    return res


if __name__ == "__main__":
    day = 6
    dt = datetime(2024, 12, day)
    exp = {"a": None, "b": 6}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
