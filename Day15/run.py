from collections import deque
from datetime import datetime
from pprint import pprint

from utils import run_and_submit


def ppg(G):
    for row in G:
        pprint("".join(row))
    print("\n\n")


def parse(filename: str):
    with open(filename, "r") as f:
        g, moves = f.read().strip().split("\n\n")

        g = [list(l) for l in g.split("\n")]

        moves = list(moves.replace("\n", ""))
    return g, moves


M = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def move(r, c, G, mv):
    if G[r][c] != "@":
        raise Exception(f"Wrong placement!!!!!!!!! {ppg(G)}")

    dr, dc = M[mv]

    rr, cc = r + dr, c + dc
    if G[rr][cc] == "#":
        return r, c

    elif G[rr][cc] == "O":
        n_o = 0
        rr_o, cc_o = rr, cc
        while G[rr_o][cc_o] == "O":
            n_o += 1
            rr_o += dr
            cc_o += dc
        if G[rr_o][cc_o] == ".":
            for i in range(1, n_o + 1):
                if dr:
                    G[rr + dr * i][cc] = "O"

                elif dc:
                    G[rr][cc + dc * i] = "O"
                else:
                    raise ValueError("Wrong")
            G[rr][cc] = "@"
            G[r][c] = "."
            return rr, cc
        else:
            assert G[rr_o][cc_o] == "#"
            return r, c
    elif G[rr][cc] == ".":
        G[rr][cc] = "@"
        G[r][c] = "."
        return rr, cc
    else:
        raise ValueError(f"Found wrong value, {ppg(G)}")


def find_start(G):
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "@":
                return (i, j)
    raise ValueError("Not found")


def score(G):
    s = 0
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "O":
                s += 100 * i + j
    return s


def run(filename: str):
    G, moves = parse(filename)
    r, c = find_start(G)

    q = deque(moves)

    while q:
        mv = q.popleft()
        r, c = move(r, c, G, mv)

    return score(G)


def resize(G):
    new_g = []

    for row in G:
        n_row = []
        for el in row:
            if el == "#":
                n_row.extend(["#", "#"])
            elif el == "O":
                n_row.extend(["[", "]"])
            elif el == "@":
                n_row.extend(["@", "."])
            elif el == ".":
                n_row.extend([".", "."])
        new_g.append(n_row)
    return new_g


def ppg2(B, H, start=None):
    max_r = max(H, key=lambda x: x[0])[0]
    max_c = max(H, key=lambda x: x[1])[1]

    G = [["." for i in range(max_c + 1)] for j in range(max_r + 1)]
    for i in range((max_r + 1)):
        for j in range(max_c + 1):
            if (i, j) in B:
                G[i][j] = "["
                G[i][j + 1] = "]"
            elif (i, j) in H:
                G[i][j] = "#"

            elif start and (i, j) == start:
                G[i][j] = "@"

    for row in G:
        print("".join(row))


def can_move_v(r, c, dr, visited, B, H):
    assert (r, c) in B, "Wrong invocation"

    visited.add((r, c))
    rr = r + dr

    if (rr, c) in H or (rr, c + 1) in H:
        return False

    if (rr, c) in B:
        return can_move_v(rr, c, dr, visited, B, H)
    elif (rr, c + 1) in B or (rr, c - 1) in B:
        to_check = []
        if (rr, c + 1) in B:
            to_check.append((rr, c + 1))

        if (rr, c - 1) in B:
            to_check.append((rr, c - 1))

        return all(can_move_v(p[0], p[1], dr, visited, B, H) for p in to_check)
    return True


def can_move_h(r, c, dc, visited, B, H):
    assert (r, c) in B, "Wrong invocation"
    visited.add((r, c))
    cc = c + 2 * dc

    if (dc == 1 and (r, cc) in H) or (dc == -1 and (r, c - 1) in H):
        return False

    if (r, cc) in B:
        return can_move_h(r, cc, dc, visited, B, H)
    return True


def movep2(r, c, B, H, mv):
    dr, dc = M[mv]

    rr, cc = r + dr, c + dc
    if (rr, cc) in H:
        return r, c

    elif (rr, cc) in B or (rr, cc - 1) in B:
        sc = cc if (rr, cc) in B else cc - 1
        sr = rr

        visited = set()
        if dc != 0:
            res_h = can_move_h(sr, sc, dc, visited, B, H)

            if res_h:
                for vr, vc in visited:
                    B.remove((vr, vc))
                for vr, vc in visited:
                    B.add((vr, vc + dc))
                return rr, cc
            else:
                return r, c
        else:
            res_v = can_move_v(sr, sc, dr, visited, B, H)

            if res_v:
                for vr, vc in visited:
                    B.remove((vr, vc))
                for vr, vc in visited:
                    B.add((vr + dr, vc))

                return rr, cc
            else:
                return r, c

    else:
        return rr, cc


def scorep2(B):
    score = 0
    for br, bc in B:
        score += 100 * br
        score += bc
    return score


def runp2(filename: str):
    G, moves = parse(filename)
    G = resize(G)
    r, c = find_start(G)

    B = set()
    H = set()

    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "[":
                B.add((i, j))
            elif G[i][j] == "#":
                H.add((i, j))

    q = deque(moves)

    while q:
        mv = q.popleft()
        r, c = movep2(r, c, B, H, mv)

    return scorep2(B)


if __name__ == "__main__":
    day = 15
    dt = datetime(2024, 12, day)
    exp = {"a": 2028, "a2": 10092, "b3": 105, "b2": 9021, "b": 105}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample2.txt", "b", runp2, expected=exp["b2"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
