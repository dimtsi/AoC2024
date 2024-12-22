import itertools
import re
from collections import defaultdict, deque
from datetime import datetime

from aoc_helpers import DIRS
from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    return lines


NK = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["", "0", "A"],
]

DK = [["", "^", "A"], ["<", "v", ">"]]


def find_all_shortest_paths(G, start, end):
    R = len(G)
    C = len(G[0])

    min_len = float("inf")

    q = deque([[start]])
    spaths = []
    visited = set()

    while q:
        path = q.popleft()
        elem = path[-1]
        r, c = elem

        if len(path) > min_len:
            continue

        visited.add((elem, len(path)))

        if elem == end:
            if len(path) < min_len:
                spaths = [path]
                min_len = len(path)
            elif len(path) == min_len:
                spaths.append(path)
            continue

        for dr, dc in DIRS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < R and 0 <= cc < C and G[rr][cc] != "":
                if ((rr, cc), len(path) + 1) not in visited:
                    q.append(path + [(rr, cc)])

    return spaths


def build_paths(G):
    M = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
    RM = {v: k for k, v in M.items()}

    dr_to_origins = defaultdict(dict)
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "":
                continue
            for ii in range(len(G)):
                for jj in range(len(G[0])):
                    if G[ii][jj] == "":
                        continue
                    if (i, j) == (ii, jj):
                        continue
                    transl_paths = []
                    start = i, j
                    end = ii, jj
                    shortest_paths = find_all_shortest_paths(G, start, end)

                    for path in shortest_paths:
                        transl = ""
                        for r in range(len(path) - 1):
                            dr = path[r + 1][0] - path[r][0]
                            dc = path[r + 1][1] - path[r][1]
                            transl += RM[(dr, dc)]
                        transl_paths.append(transl)
                    dr_to_origins[G[i][j]][G[ii][jj]] = transl_paths
    return dr_to_origins


def get_seq(seq, M):
    seq = ["A"] + list(seq)
    min_len = float("inf")
    final_paths = []
    q = deque([(0, [])])
    while q:
        idx, curr_path = q.popleft()
        if idx == len(seq) - 1:
            output_path = "A".join(curr_path) + "A"
            if len(output_path) <= min_len:
                final_paths.append(output_path)

            continue
        start, end = seq[idx], seq[idx + 1]

        if start == end:
            new_path = curr_path + [""]
            q.append((idx + 1, new_path))
        else:
            for neigh in M[start][end]:
                new_path = curr_path + [neigh]
                q.append((idx + 1, new_path))

    return final_paths


def run(filename: str):
    lines = parse(filename)

    numpad_paths = build_paths(NK)
    dirpad_paths = build_paths(DK)

    score = 0
    for line in lines:
        ll = list(line)
        first_seqs = get_seq(ll, numpad_paths)

        second_seqs = []
        for first_seq in first_seqs:
            second_seqs.extend(get_seq(first_seq, dirpad_paths))
        min_second_seqs = min(len(x) for x in second_seqs)
        second_seqs = [
            seq for seq in second_seqs if len(seq) == min_second_seqs
        ]

        third_seqs = []
        for seq in second_seqs:
            third_seqs.extend(get_seq(seq, dirpad_paths))
        min_third_seqs = min(len(x) for x in third_seqs)
        third_seqs = [seq for seq in third_seqs if len(seq) == min_third_seqs]
        min_len_third = min(len(x) for x in third_seqs)

        num = list(map(int, re.findall(r"\d+", line)))[0]
        score += min_len_third * num
    return score


def get_seq_at_t(seq, t, paths, cache):
    if (seq, t) in cache:
        return cache[(seq, t)]
    if t == 0:
        return len(seq)

    total = 0
    for a, b in itertools.pairwise("A" + seq):
        if a == b:
            total += get_seq_at_t("A", t - 1, paths, cache)
        else:
            min_path = float("inf")
            for path in paths[a][b]:
                min_path = min(
                    min_path, get_seq_at_t(path + "A", t - 1, paths, cache)
                )
            total += min_path

    cache[(seq, t)] = total
    return total


def runp2(filename: str):
    lines = parse(filename)

    numpad_paths = build_paths(NK)
    dirpad_paths = build_paths(DK)

    score = 0
    cache = {}
    for line in lines:
        ll = list(line)
        first_seqs = get_seq(ll, numpad_paths)
        min_len = min(
            get_seq_at_t(seq, 25, dirpad_paths, cache) for seq in first_seqs
        )
        num = list(map(int, re.findall(r"\d+", line)))[0]
        score += min_len * num

    return score


if __name__ == "__main__":
    day = 21
    dt = datetime(2024, 12, day)
    exp = {"a": 126384, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
