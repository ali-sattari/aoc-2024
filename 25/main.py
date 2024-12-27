from collections import defaultdict
from typing import List, Optional, Tuple, Dict, Literal
from pprint import pprint
import functools

class Solution:
    def __init__(self, locks: list[tuple], keys: list[tuple]):
        self.locks = locks
        self.keys = keys

    def calculate(self) -> int:
        matches = set()
        full = tuple([6]*5)
        for i, k in enumerate(self.keys):
            for j, l in enumerate(self.locks):
                combo = self.sum_heights(k, l)
                if self.is_match(combo, full):
                    # print(f"{k} + {l} -> {combo} < {full}")
                    matches.add((k, l))

        return len(matches)

    def sum_heights(self, a, b: tuple) -> tuple:
        return tuple([sum(x) for x in zip(a,b)])

    def is_match(self, combo, full: tuple) -> bool:
        for i, x in enumerate(combo):
            if x >= full[i]:
                return False
        return True

def process_input(f: str):
    locks: list[tuple] = []
    keys: list[tuple] = []
    with open(file=f, mode='r') as file:
        schemas = file.read().split('\n\n')
        for item in schemas:
            schm = item.strip()
            if schm[0] == '#': # lock
                locks.append(count_pins(schm))
            else: # key
                keys.append(count_pins(schm))
    return locks, keys

def count_pins(schm:str) -> tuple:
    pins = [-1]*5
    for line in schm.split('\n'):
        for i, col in enumerate(list(line)):
            if col == '#':
                pins[i] += 1
    return tuple(pins)

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer1 = 3
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
