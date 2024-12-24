from collections import defaultdict, deque
from copy import deepcopy
from datetime import datetime
from pprint import pprint

from utils import run_and_submit


def parse(filename: str):
    G = defaultdict(list)
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

        for line in lines:
            a, b = line.split("-")
            G[a].append(b)
            G[b].append(a)

    return dict(G)


def bfs(G, start):
    q = deque([(start, [start])])
    found = []
    visited = set()

    while q:
        elem, path = q.popleft()
        dist = len(path)

        visited.add((elem, dist))
        for neigh in G[elem]:
            if dist == 3:
                if neigh == start:
                    found.append(frozenset(path))
                else:
                    continue
            if neigh not in path and (neigh, dist + 1) not in visited:
                new_path = deepcopy(path) + [neigh]
                q.append((neigh, new_path))
    return found


def find_sets(G):
    groups = set()
    for node in G:
        for group in bfs(G, node):
            groups.add(group)

    return groups


def run(filename: str):
    G = parse(filename)

    all_groups = find_sets(G)

    score = 0
    for group in all_groups:
        for el in group:
            if el.startswith("t"):
                score += 1
                break

    return score


def find_max_set(G):
    all_groups = set()

    def rec(elem, curr_group):
        id_ = frozenset(curr_group)
        if id_ in all_groups:
            return

        all_groups.add(id_)
        for neigh in G[elem]:
            for node in curr_group:
                if neigh not in G[node]:
                    break
            else:
                rec(neigh, curr_group | {neigh})

    for node in G:
        rec(node, {node})

    maxlen = max(len(x) for x in all_groups)
    winning_set = [x for x in all_groups if len(x) == maxlen][0]
    print(maxlen)
    pprint(winning_set)
    return ",".join(sorted([str(x) for x in winning_set]))


def runp2(filename: str):
    G = parse(filename)
    res = find_max_set(G)
    return res


if __name__ == "__main__":
    day = 23
    dt = datetime(2024, 12, day)
    exp = {"a": 7, "b": "co,de,ka,ta"}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=False, dt=dt)
