import itertools
from collections import defaultdict, deque
from datetime import datetime
from heapq import heappop, heappush

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    return lines


DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def find_start_end(G):
    start, end = None, None
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == "S":
                start = (i, j)
            elif G[i][j] == "E":
                end = (i, j)

    if not start or not end:
        raise ValueError("startend not found")
    return start, end


def find_candidates(G):
    cands = set()
    for r in range(1, len(G) - 1):
        for c in range(1, len(G[0]) - 1):
            if G[r][c] in ".S":
                for dr, dc in DIRS:
                    rr, cc = r + dr, c + dc

                    if G[rr][cc] == "#":
                        for ddr, ddc in DIRS:
                            rrr, ccc = rr + ddr, cc + ddc
                            if (
                                0 <= rrr < len(G)
                                and 0 <= ccc < len(G[0])
                                and G[rrr][ccc] != "#"
                                and (rrr, ccc) != (r, c)
                            ):
                                cands.add(((r, c), (rrr, ccc)))
    return cands


def find_paths_to_end(origin, end, start):
    q = deque([end])
    dists_to_end = {end: 0}

    curr_dist = 0
    while q:
        state = q.popleft()
        if state not in origin:
            assert state == start
            continue
        prev = origin[state]
        q.append(prev)
        dists_to_end[prev] = curr_dist + 1
        curr_dist += 1

    return dists_to_end


def dijkstra(
    start,
    end,
    G,
):
    distances = defaultdict(lambda: float("inf"))
    distances[start] = 0
    origin = {}
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, (r, c) = heappop(pq)
        state = r, c

        if state in visited:
            continue
        visited.add(state)

        for dr, dc in DIRS:
            rr, cc = r + dr, c + dc
            new_state = rr, cc

            if G[rr][cc] != "#" and distances[new_state] >= dist + 1:
                distances[new_state] = dist + 1
                origin[new_state] = state
                heappush(pq, (dist + 1, new_state))

    min_dist = distances[end]

    dists_from_end = find_paths_to_end(origin, end, start)
    if set(dists_from_end.keys()) ^ set(distances.keys()):
        raise ValueError(
            "Non unique path",
            set(dists_from_end.keys()) ^ set(distances.keys()),
        )

    return min_dist, distances, dists_from_end, origin


@timeit
def run(filename: str):
    G = [list(x) for x in parse(filename)]
    start, end = find_start_end(G)
    _, _, dists_from_end, _ = dijkstra(start, end, G)

    candidates = find_candidates(G)

    score = 0
    diffs = defaultdict(lambda: 0)
    diffs_points = defaultdict(set)
    for start, end in candidates:
        diff = dists_from_end[start] - dists_from_end[end]
        if diff > 2:
            score += 1
            diffs[diff - 2] += 1
            diffs_points[diff - 2].add((start, end))

    if "input" in filename:
        ab_100 = {k: v for k, v in diffs.items() if k >= 100}
        score = sum(ab_100.values())
    return score


def manh(p1, p2):
    a_x, a_y = p1
    (
        b_x,
        b_y,
    ) = p2
    dist = abs(a_x - b_x) + abs(a_y - b_y)
    return dist


@timeit
def runp2(filename: str):
    G = [list(x) for x in parse(filename)]
    start, end = find_start_end(G)
    _, dists_from_start, dists_from_end, _ = dijkstra(start, end, G)

    lim = 50 if "sample" in filename else 100

    diffs = defaultdict(lambda: 0)
    for start, end in itertools.combinations(dists_from_start.keys(), 2):
        diff = dists_from_end[start] - dists_from_end[end]
        s, e = (start, end) if diff > 0 else (end, start)

        dist = manh(s, e)
        if dist > 20 or dist < 2:
            continue
        diffs[diff - dist] += 1

    print(len(diffs))
    ab_100 = {k: v for k, v in diffs.items() if k >= lim}
    score = sum(ab_100.values())
    return score


if __name__ == "__main__":
    day = 20
    dt = datetime(2024, 12, day)
    exp = {"a": 44, "b": 285}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
