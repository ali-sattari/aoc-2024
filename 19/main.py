from typing import List, Optional, Tuple, Dict
from pprint import pprint
from collections import defaultdict
from termcolor import colored
import re

class Solution:
    def __init__(self, patterns: list[str], designs: List[str]):
        self.patterns = patterns
        self.designs = designs

    def calculate(self) -> Tuple[int, int]:
        total = 0
        uniques = 0
        for d in self.designs:
            r = self.how_many_designs(d)
            # print(f"result {colored(r, 'blue')} \t for {colored(d, 'yellow')} ")
            if r > 0: uniques += 1
            total += r

        return uniques, total

    def can_design(self, design: str, patterns=None, memo=None) -> int:
        if design == '':
            return 1

        if patterns is None:
            patterns = self.patterns

        if memo is None:
            memo = {}

        if design in memo:
            return memo[design]

        for p in patterns:
            if design.startswith(p):
                if self.can_design(design[len(p):], patterns, memo):
                    memo[design] = 1
                    return 1

        memo[design] = 0
        return 0

    def how_many_designs(self, design: str, patterns=None, memo=None) -> int:
        if design == '':
            return 1

        if patterns is None:
            patterns = self.patterns

        if memo is None:
            memo = {}

        if design in memo:
            return memo[design]

        count = 0
        for p in patterns:
            if design.startswith(p):
                count += self.how_many_designs(design[len(p):], patterns, memo)

        memo[design] = count
        return count

def process_input(f: str):
    patterns = []
    designs = []
    with open(file=f, mode='r') as file:
        content = file.read().split("\n\n")

    patterns = sorted([t.strip() for t in content[0].split(',')], reverse=True, key=len)
    designs = [d.strip() for d in content[1].split('\n') if d != '']

    return patterns, designs

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer = 6
    # test_answer2 = 16
    # inst = Solution(*test_input)
    # uniques, total = inst.calculate()
    # print("Part1:", uniques, uniques == test_answer)
    # print("Part2:", total, total == test_answer2)

    input = process_input("./input")
    inst = Solution(*input)
    uniques, total = inst.calculate()
    print("Part 1:", uniques)
    print("Part 2:", total)

    # p1: 206
    # p2: 622121814629343
