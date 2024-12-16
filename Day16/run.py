from collections import defaultdict, deque
from datetime import datetime
from functools import partial
from heapq import heappop, heappush

from utils import run_and_submit, timeit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return lines


DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def rot_clock(dr, dc):
    return {
        (1, 0): (0, -1),
        (0, 1): (1, 0),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1),
    }[(dr, dc)]


def rot_counter_clock(dr, dc):
    return {
        (-1, 0): (0, -1),
        (0, -1): (1, 0),
        (1, 0): (0, 1),
        (0, 1): (-1, 0),
    }[(dr, dc)]


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


def dijkstra(G, start, end):
    distances = defaultdict(lambda: float("inf"))
    origin = defaultdict(set)
    distances[(*start, 0, 1)] = 0
    pq = [(0, (*start, 0, 1))]
    visited = set()

    while pq:
        dist, (r, c, dr, dc) = heappop(pq)
        state = r, c, dr, dc
        if state in visited:
            continue
        visited.add(state)

        # Continue straight
        rr, cc = r + dr, c + dc
        new_state = rr, cc, dr, dc
        if G[rr][cc] != "#" and distances[new_state] >= dist + 1:
            distances[new_state] = dist + 1
            origin[new_state].add(state)
            heappush(pq, (dist + 1, new_state))

        # rot
        for ddr, ddc in [rot_clock(dr, dc), rot_counter_clock(dr, dc)]:
            rr, cc = r + ddr, c + ddc
            new_state = rr, cc, ddr, ddc
            if G[rr][cc] != "#" and distances[new_state] >= dist + 1000 + 1:
                distances[new_state] = dist + 1000 + 1
                origin[new_state].add(state)
                heappush(pq, (dist + 1000 + 1, new_state))

    min_dist = min(distances[(*end, dr, dc)] for (dr, dc) in DIRS)
    n_points = find_n_shortest_path_points(origin, distances, start, end)
    return min_dist, n_points


def find_n_shortest_path_points(origin, distances, start, end):
    min_dist = min(distances[(*end, dr, dc)] for (dr, dc) in DIRS)

    end_origins = [
        (*end, dr, dc)
        for (dr, dc) in DIRS
        if distances[(*end, dr, dc)] == min_dist
    ]

    out = set()
    q = deque(end_origins)

    while q:
        state = q.popleft()
        r, c, _, _ = state
        out.add((r, c))
        for prev_state in origin[state]:
            q.append(prev_state)

    return len(out)


@timeit
def run(filename: str, p2=False):
    G = parse(filename)
    start, end = find_start_end(G)

    min_dist, n_points = dijkstra(G, start, end)
    if not p2:
        return min_dist
    else:
        return n_points


if __name__ == "__main__":
    day = 16
    dt = datetime(2024, 12, day)
    exp = {"a": 7036, "a2": 11048, "b": 45, "b2": 64}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/sample2.txt", "a", run, expected=exp["a2"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(
        f"Day{day}/sample.txt", "b", partial(run, p2=True), expected=exp["b"]
    )
    run_and_submit(
        f"Day{day}/sample2.txt", "b", partial(run, p2=True), expected=exp["b2"]
    )
    run_and_submit(
        f"Day{day}/input.txt", "b", partial(run, p2=True), submit=True, dt=dt
    )
