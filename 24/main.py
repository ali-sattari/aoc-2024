from collections import defaultdict
from typing import List, Optional, Tuple, Dict, Literal
from pprint import pprint
import functools

class Solution:
    def __init__(self, initial: dict[str,int], gates: dict[str,tuple]):
        self.initial = initial
        self.gates = gates
        self.outputs = sorted([g for g in gates if g.startswith('z')], reverse=True)
        self.memory: dict[str, int] = dict()

    def calculate(self) -> int:
        out = ''
        for o in self.outputs:
            out += str(self.run_wire(o))
        return int(out, 2)

    def run_wire(self, wire:str) -> int:
        if wire in self.memory:
            return self.memory[wire]

        if wire in self.initial:
            return self.initial[wire]

        a, op, b = self.gates[wire]
        val_a = self.run_wire(a)
        val_b = self.run_wire(b)
        # print(f"wire {wire} gate {(a, op, b)}: {val_a}, {val_b}")

        res: int
        match op:
            case 'AND':
                res = int(bool(val_a) and bool(val_b))
            case 'OR':
                res = int(bool(val_a) or bool(val_b))
            case 'XOR':
                res = int(bool(val_a) ^ bool(val_b))
            case _:
                print(f"what the {wire} and {op}?!")

        self.memory[wire] = res
        return res

def process_input(f: str):
    values: dict[str, int] = dict()
    gates: dict[str, tuple] = dict()
    with open(file=f, mode='r') as file:
        vals_text, gates_text = file.read().split('\n\n')

        for line in vals_text.split('\n'):
            k, v = line.strip().split(':')
            values[k] = int(v.strip())

        for line in gates_text.strip().split('\n'):
            v, k = line.strip().split('->')
            gates[k.strip()] = tuple(v.strip().split(' '))

    return values, gates

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer1 = 2024
    # # test_answer2 = 'co,de,ka,ta'
    # inst = Solution(*test_input)
    # answ1 = inst.calculate()
    # print("Part1:", answ1 ,answ1 == test_answer1)
    # # answ2 = inst.calculate2()
    # # print("Part2:", answ2, answ2 == test_answer2)

    input = process_input("./input")
    inst = Solution(*input)
    answ1 = inst.calculate()
    print("Part 1:", answ1)
    # answ2 = inst.calculate2()
    # print("Part 2:", answ2)
