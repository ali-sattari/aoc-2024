from collections import defaultdict
from typing import List, Optional, Tuple, Dict, Literal
from pprint import pprint
import functools

class Solution:
    def __init__(self, network: dict):
        self.network = network
        self.groups = set()

    def calculate(self) -> int:
        # pprint(self.network)
        self.form_groups()
        # print('\n'.join(sorted(self.groups)))

        return len(self.groups)

    def calculate2(self) -> str:
        # pprint(self.network)

        res = []
        self.find_many_mates([], set(self.network.keys()), set(), res)
        largest_group = sorted(res, reverse=True, key=len)[0]

        return ','.join(sorted(largest_group))

    def form_groups(self):
        for src, dsts in self.network.items():
            if src.startswith('t'):
                g = self.find_mates(src, dsts)
                self.groups.update(g)

    def find_many_mates(self, mates: list, candidates: set, visited: set, res=[]):
        if not candidates and not visited:
            return mates

        for c in list(candidates):
            t = self.find_many_mates(mates + [c], candidates & self.network[c], visited & self.network[c], res)
            if len(t) > 1:
                res.append(t)
            candidates.remove(c)
            visited.add(c)

        return []

    def find_mates(self, src: str, pairs: set) -> List[str]:
        pl = list(pairs)
        mates = []
        for i, n1 in enumerate(pl):
            for j in range (i+1, len(pl)):
                n2 = pl[j]
                if self.are_pairs(n1, n2):
                    mates.append(','.join(sorted([src, n1, n2])))
        return mates

    def are_pairs(self, n1, n2:str) -> bool:
        return n1 in self.network[n2]

def process_input(f: str):
    input: dict[str, set[str]] = defaultdict(set)
    with open(file=f, mode='r') as file:
        for line in file:
            k, v = line.strip().split('-')
            input[k].add(v)
            input[v].add(k)
    return input

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer1 = 7
    # test_answer2 = 'co,de,ka,ta'
    # inst = Solution(test_input)
    # # answ1 = inst.calculate()
    # # print("Part1:", answ1 ,answ1 == test_answer1)
    # answ2 = inst.calculate2()
    # print("Part2:", answ2, answ2 == test_answer2)

    input = process_input("./input")
    inst = Solution(input)
    answ1 = inst.calculate()
    print("Part 1:", answ1)
    answ2 = inst.calculate2()
    print("Part 2:", answ2)
