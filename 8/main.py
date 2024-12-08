from typing import List, Tuple
from collections import defaultdict
from pprint import pprint
import itertools

class Solution:
    def __init__(self, grid: List):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.antennas = defaultdict(list)
        self.antinodes = []
        self.antinodes2 = []

    def calculate1(self) -> int:
        self.find_antennas()
        self.find_antinodes()

        return len(set(self.antinodes))

    def calculate2(self) -> int:
        self.find_antinodes_in_line()

        return len(set(self.antinodes2))

    def find_antinodes(self):
        for freq, ants in self.antennas.items():
            pairs = list(itertools.combinations(ants, 2))
            for pair in pairs:
                ans = self.get_antinodes(pair[0], pair[1])
                for a in ans:
                    if self.is_inside_grid(*a): self.antinodes.append(a)

    def find_antinodes_in_line(self):
        for freq, ants in self.antennas.items():
            pairs = list(itertools.combinations(ants, 2))
            for pair in pairs:
                self.get_antinodes_in_line(pair[0], pair[1])

    def get_antinodes(self, a: Tuple, b: Tuple) -> List[Tuple]:
        dy, dx = b[0] - a[0], b[1] - a[1]
        antinodes = [
            (a[0] - dy, a[1] - dx),
            (b[0] + dy, b[1] + dx)
        ]
        return antinodes

    def get_antinodes_in_line(self, a: Tuple, b: Tuple):
        dy, dx = b[0] - a[0], b[1] - a[1]

        self.antinodes2.append(a)
        self.antinodes2.append(b)

        for i in itertools.count(start=1):
            t = (a[0] - i * dy, a[1] - i * dx)
            if self.is_inside_grid(*t):
                self.antinodes2.append(t)
            else:
                break

        for i in itertools.count(start=1):
            t = (b[0] + i * dy, b[1] + i * dx)
            if self.is_inside_grid(*t):
                self.antinodes2.append(t)
            else:
                break

    def find_antennas(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col != ".":
                    self.antennas[col].append((y, x))

    def is_inside_grid(self, y: int, x: int) -> bool:
        return (y >= 0 and y < self.height) and (x >= 0 and x < self.width)

    def render_antinodes(self, part=1):
        g = self.grid.copy()
        src = self.antinodes if part == 1 else self.antinodes2
        for a in src:
            p = g[a[0]][a[1]]
            if p == ".":
                g[a[0]][a[1]] = "#"

        for r in g:
            print(''.join(r))

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            stuff.append(list(line.strip()))

    return stuff


if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer1 = 14
    # test_answer2 = 34
    # inst = Solution(test_input)
    # ans1 = inst.calculate1()
    # ans2 = inst.calculate2()
    # print("Part1:", ans1, ans1 == test_answer1)
    # print("Part2:", ans2, ans2 == test_answer2)
    # inst.render_antinodes(part=2)

    input = input_to_list("./input")
    inst = Solution(input)
    ans1 = inst.calculate1()
    ans2 = inst.calculate2()
    print("Part 1:", ans1)
    print("Part 2:", ans2)

    # p1: 299
    # p2: 1032
