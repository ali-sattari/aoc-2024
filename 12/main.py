from typing import List, Optional, Tuple
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict
import time

class Pos:
    def __init__(self, y:int, x:int):
        self.y = y
        self.x = x

    def __repr__(self):
        return f"Pos({self.y}, {self.x})"

    def __add__(self, other):
        return Pos(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Pos(self.y - other.y, self.x - other.x)

    def __eq__(self, other):
        return isinstance(other, Pos) and (self.y, self.x) == (other.y, other.x)

    def __hash__(self):
        return hash((self.y, self.x))

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def is_inbounds(self, h: int, w: int):
        return 0 <= self.y < h and 0 <= self.x < w

    def get_buren(self):
        for delta in (Pos(0, 1), Pos(0, -1), Pos(1, 0), Pos(-1, 0)):
            yield self + delta

class Solution:
    def __init__(self, grid: List):
        self.plants = dict()
        self.grid = self.map_grid(grid)
        self.height = len(grid)
        self.width = len(grid[0])

    def map_grid(self, grid: List) -> dict[Pos, str]:
        m = dict()
        for y, row in enumerate(grid):
            for x, p in enumerate(row):
                m[Pos(y,x)] = p
        return m

    def calculate1_dfs(self) -> int:
        total = 0

        cells = set(self.grid.keys())
        while cells:
            pos = cells.pop()
            plant = self.grid[pos]
            region = self.find_region(pos)
            price = len(region) * self.perimeter(region)
            print(f"Plant {plant} with region of {len(region)} = {price}", "\t"*3, pos)

            cells -= region
            total += price

        return total

    def find_region(self, pos: Pos) -> set[Pos]:
        q: List[Pos] = [pos]
        region: set[Pos] = {pos}
        plant = self.grid[pos]

        while q:
            current = q.pop()
            for n in current.get_buren():
                if not n.is_inbounds(self.height, self.width):
                    continue

                if n not in region and self.grid[n] == plant:
                    q.append(n)
                    region.add(n)

        return region

    def perimeter(self, region: set[Pos]) -> int:
        t = 0
        for p in region:
            t += 4 - len(set(p.get_buren()) & region)

        return t



def add_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return tuple(a + b for a, b in zip(t1, t2))

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            t = list(line.strip())
            stuff.append(t)

    return stuff

if __name__ == "__main__":
    test_input = input_to_list("./test-input")
    test_answer1 = 1930 # 11 regions
    test_answer2 = 1206 # 11 regions
    inst = Solution(test_input)
    ans1 = inst.calculate1_dfs()
    # ans2 = inst.calculate2(7)
    print("Part1:", ans1, ans1 == test_answer1)
    # print("Part2:", ans2, ans2 == test_answer1)

    # input = input_to_list("./input")
    # inst = Solution(input)
    # ans1 = inst.calculate1_dfs()
    # # ans2 = inst.calculate2(75)
    # print("Part 1:", ans1)
    # # print("Part 2:", ans2)

    # # p1: 1464678
