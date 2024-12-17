import re
from copy import deepcopy
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    R = {}
    with open(filename, "r") as f:
        regs, instr = f.read().strip().split("\n\n")
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
        for reg, line in zip(["A", "B", "C"], regs.splitlines()):
            val = list(map(int, re.findall("-?\d+", line)))[0]
            R[reg] = val
        instr = list(map(int, re.findall("-?\d+", instr)))

    return R, instr


def combo(v, R):
    if v in [0, 1, 2, 3]:
        return v
    elif v == 4:
        return R["A"]
    elif v == 5:
        return R["B"]
    elif v == 6:
        return R["C"]
    elif v == 7:
        raise ValueError("Comboval 7 appeared")
    else:
        raise ValueError(f"Comboval {v} appeared")


def move(i, op, R):
    j, idx, out = False, None, []
    if i == 0:
        res = R["A"] // (2 ** combo(op, R))
        R["A"] = res

    elif i == 1:
        res = R["B"] ^ op
        R["B"] = res

    elif i == 2:
        res = combo(op, R) % 8
        R["B"] = res

    elif i == 3:
        if R["A"] != 0:
            j, idx = True, op

    elif i == 4:
        res = R["B"] ^ R["C"]
        R["B"] = res

    elif i == 5:
        res = combo(op, R) % 8
        out.append(res)

    elif i == 6:
        res = R["A"] // (2 ** combo(op, R))
        R["B"] = res

    elif i == 7:
        res = R["A"] // (2 ** combo(op, R))
        R["C"] = res

    else:
        raise ValueError(f"Wrong {i}")

    return j, idx, out


def run_program(a, R, I):
    idx = 0
    output = []
    R["A"] = a
    # run
    while True:
        if idx >= len(I):
            break
        i, op = I[idx], I[idx + 1]

        j, idx_new, out = move(i, op, R)

        if j:
            assert idx_new is not None
            idx = idx_new
        else:
            idx += 2
        if out:
            output.extend(out)
    return output


def run(filename: str):
    R, I = parse(filename)

    output = run_program(R["A"], R, I)

    res = ",".join((str(o) for o in output))
    return res


def runp2(filename: str):
    R, I = parse(filename)
    candidates = [0]
    for last_k in range(1, len(I) + 1):
        # last k digits must be the same moving backwards
        new_candidates = []
        for a_cand in candidates:
            RR = deepcopy(R)
            for offset in range(8):
                aa = (a_cand * 8) + offset
                output = run_program(aa, RR, I)

                if output == I[-last_k:]:
                    # print(f"found: {output}, {I}, {aa}, {last_k}")
                    new_candidates.append(aa)
        candidates = new_candidates

    return min(candidates)


if __name__ == "__main__":
    day = 17
    dt = datetime(2024, 12, day)
    exp = {"a": "4,6,3,5,6,3,5,2,1,0", "b": 117440}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample2.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
