from tarfile import itn
from typing import List, Optional, Tuple
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict
import time

class Plant:
    def __init__(self, name: str):
        self.name = name
        self.count = 0
        self.regions = []
        self.reg_count = 0
        self.points = []
        self.dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __repr__(self):
        return self.name

    def add_pos(self, pos:tuple):
        self.points.append(pos)

    def define_regions(self):
        for pos in self.points:
            r = self.get_region(pos)

            if r == -1:
                self.regions.append([pos])
                self.reg_count += 1
            else:
                self.regions[r].append(pos)

    def get_region(self, pos: tuple, visited=[]) -> int:
        reg = -1
        # for first pos per plant
        if len(self.regions) == 0:
            return reg

        to_check = []
        for d in self.dirs:
            c = add_tuples(pos, d)
            # if pos has any neighbor in points
            if c in self.points and c not in visited:
                # check existing regions
                for i, r in enumerate(self.regions):
                    if c in r:
                        reg = i
                    else:
                        to_check.append(c)

        if reg == -1:
            for c in to_check:
                # recurse on c to find region
                return self.get_region(c, visited + [c])

        return reg

    def price(self) -> int:
        p = 0
        for r in self.regions:
            p += self.perimeter(r) * self.area(r)
        return p

    def perimeter(self, region: list) -> int:
        walls = 0
        for p in region:
            for d in self.dirs:
                c = add_tuples(p, d)
                if c not in region:
                    walls += 1

        return walls

    def area(self, region: list) -> int:
        return len(region)

class Solution:
    def __init__(self, grid: List):
        self.plants = dict()
        self.grid = self.map_grid(grid)
        self.height = len(grid)
        self.width = len(grid[0])
        self.regions = defaultdict(list)

    def map_grid(self, grid: List):
        for y, row in enumerate(grid):
            for x, p in enumerate(row):
                if p not in self.plants:
                    self.plants[p] = Plant(p)
                self.plants[p].add_pos((y,x))

    def calculate1(self) -> int:
        total = 0
        for plant in self.plants.values():
            plant.define_regions()
            price = plant.price()
            total += price
            print(plant, price, plant.reg_count)
            # pprint(plant.regions)
            # print("-"*50)
        return total

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
    # test_input = input_to_list("./test-input")
    # test_answer1 = 1930 # 11 regions
    # inst = Solution(test_input)
    # ans1 = inst.calculate1()
    # # ans2 = inst.calculate2(7)
    # print("Part1:", ans1, ans1 == test_answer1)
    # # print("Part2:", ans2, ans2 == test_answer1)

    input = input_to_list("./input")
    inst = Solution(input)
    ans1 = inst.calculate1()
    # ans2 = inst.calculate2(75)
    print("Part 1:", ans1)
    # print("Part 2:", ans2)

    # p1: 1215102 too low
