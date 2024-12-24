from collections import defaultdict
from datetime import datetime
from functools import cached_property
from pprint import pprint

import pygraphviz as pgv
from z3.z3 import And, Bool, Or, Solver, Xor, is_true, sat

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        G = {}
        gates, instructions = f.read().strip().split("\n\n")
        for gate in gates.split("\n"):
            id_, num = gate.split(": ")
            G[id_] = int(num)

    return G, instructions


def run(filename: str):
    G, instructions = parse(filename)

    solver = Solver()
    vars = []
    OP = {"AND": And, "OR": Or, "XOR": Xor}
    pprint(G)
    for iin in instructions.split("\n"):
        n1, op, n2, target = iin.replace("-> ", "").split()

        if n1 in G:
            n1 = bool(G[n1])
        else:
            n1 = Bool(n1)
            vars.append(n1)

        if n2 in G:
            n2 = bool(G[n2])
        else:
            n2 = Bool(n2)
            vars.append(n2)

        if target in G:
            target = bool(G[target])
        else:
            target = Bool(target)
            vars.append(target)

        solver.add(OP[op](n1, n2) == target)

    if solver.check() == sat:
        model = solver.model()
        solution = {str(var): model[var] for var in vars}
        solution = {str(var): is_true(model[var]) for var in vars}

    zkeys = list(
        sorted(
            [
                (key, int(val))
                for key, val in solution.items()
                if key.startswith("z")
            ],
            reverse=True,
        )
    )
    return int("".join(str(x[1]) for x in zkeys), 2)


def get_maxs(I):
    maxx = 0
    maxy = 0
    maxz = 0
    for n1, op, n2, target in I:
        # n1, op, n2, target = iin

        for n in [n1, n2, target]:
            if n.startswith("x"):
                maxx = max(maxx, int(n[1:]))

            if n.startswith("y"):
                maxy = max(maxy, int(n[1:]))

            if n.startswith("z"):
                maxz = max(maxz, int(n[1:]))
    return maxx, maxy, maxz


class Gate:
    def __init__(self, a, op, b, target):
        self.a = a
        self.b = b
        self.op = op
        self.target = target

    @cached_property
    def key(self):
        return get_key(self.a, self.op, self.b)

    @cached_property
    def inputs(self):
        return {self.a, self.b}

    def __repr__(self):
        return f"{self.a} {self.op} {self.b} -> {self.target}"


def get_key(a, op, b):
    l = list(sorted([a, b]))
    return (l[0], op, l[1])


def print_grid_graph(gates, png_filename):
    G = pgv.AGraph(strict=True, directed=True, ranksep=0.5)
    for gate in gates.values():
        a, op, b = gate.a, gate.op, gate.b
        gate_s = "-".join(gate.key)
        G.add_edge(a, gate_s)
        G.add_edge(b, gate_s)
        G.add_edge(gate_s, gate.target)

    G.layout()
    G.layout(prog="neato")
    G.draw(png_filename)
    return G


# =========================== FORMULA =========================== #
# x XOR y -> K
# x AND y -> L
# carry XOR K -> z
# carry AND K -> M
# M OR L -> next_carry


def check_for_problems_for_given_xi_yi_zi(id_, G, FWD_GATES):
    x = f"x{id_}" if id_ > 9 else f"x0{id_}"
    y = f"y{id_}" if id_ > 9 else f"y0{id_}"
    z = f"z{id_}" if id_ > 9 else f"z0{id_}"

    # xandy = G[get_key(x, "AND", y)]
    xxory = G[get_key(x, "XOR", y)]
    K = xxory.target

    # This will always point to an AND and an XOR gate with the same sources (K, carry) (assuming everything is correct)
    carry_XOR_K = FWD_GATES[K][0]
    carry = (G[carry_XOR_K].inputs - {K}).pop()

    # We check if the output of the (carry XOR K) gate is the corresponding z.
    if (
        get_key(carry, "XOR", K) not in G
        or G[get_key(carry, "XOR", K)].target != z
    ):
        print(f"zproblem: {x, y, z}")


def check_for_logical_errors_and_draw(filename, output_png):
    _, instructions = parse(filename)

    G = {}
    FWD_GATES = defaultdict(list)
    instructions = [
        x.replace("-> ", "").split() for x in instructions.split("\n")
    ]
    maxx, maxy, maxz = get_maxs(instructions)

    for a, op, b, t in instructions:
        gate = Gate(a, op, b, t)
        G[gate.key] = gate
        FWD_GATES[a].append(gate.key)
        FWD_GATES[b].append(gate.key)

    # check for problems in every xi, yi, zi "neighbourhood" except for x0, y0, z0 (would cause index error).
    # It is correct upon visual inspection so we do not do any special handling
    for id_ in range(1, maxx + 1):
        check_for_problems_for_given_xi_yi_zi(id_, G, FWD_GATES)

    print_grid_graph(G, output_png)


def runp2(filename: str):
    check_for_logical_errors_and_draw(filename, "Day24/original_grid.png")
    # The above will print
    # zproblem: ('x15', 'y15', 'z15')
    # zproblem: ('x21', 'y21', 'z21')
    # zproblem: ('x30', 'y30', 'z30')
    # zproblem: ('x34', 'y34', 'z34')

    # At this point of the problem I checked manually into the drawed graph and
    # found in the problematic x,y points in the graph see which part of the FORMULA is invalid.
    # Since it is local, we determine the errors on the relevant gates.

    # After inspection on the 4 relevant components (15, 21, 30, 45) on the png graph we visually determine the 4 swaps.
    ##########################################
    #     "fph" <-> "z15" -  Addition 15     #
    #     "gds" <-> "z21" -  Addition 21     #
    #     "jrs" <-> "wrk" -  Addition 30     #
    #     "cqk" <-> "z34" -  Addition 34     #
    ##########################################

    print()
    # I created a separate file fixed_input.txt with the swapped gates and
    # reran to see if no problems appear to ensure
    print("Checking for problems given swapped input")
    check_for_logical_errors_and_draw(
        "Day24/fixed_input.txt", "Day24/modified_grid.png"
    )
    return ",".join(
        list(sorted(["fph", "z15", "gds", "z21", "jrs", "wrk", "cqk", "z34"]))
    )


if __name__ == "__main__":
    day = 24
    dt = datetime(2024, 12, day)
    exp = {"a": 2024, "b": None}

    run_and_submit(f"Day{day}/sample2.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
