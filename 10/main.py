from typing import List, Optional, Tuple
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict

# input is alternating file blocks and whitespace (one digit per each)
# expand input into array of files and following whitespace
# expand that into string representaiton by placing file ids repeated by number of blocks followed by . repeated for whitespace
# move blocks from enf to front inside whitespaces
# calculate checksum by multiplying position with id, and summing all of those

class Solution:
    def __init__(self, grid: List):
        self.grid = grid
        self.visited = set()
        self.height = len(grid)
        self.width = len(grid[0])
        self.trailHeads = defaultdict(list)
        self.score = 0

    def calculate1(self) -> int:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == 0:
                    head = (y, x)
                    t = self.walkTrail(head, [c])
                    self.score += int(t)
                    # print(head, self.trailHeads[head])

        return self.score

    def calculate2(self) -> int:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == 0:
                    head = (y, x)
                    t = self.walkTrail2(head, [c], {head})
                    self.trailHeads[head].extend(t)

        return self.getRating()

    def getRating(self) -> int:
        t = 0
        for h, s in self.trailHeads.items():
            t += len(s)
        return t

    def isInGrid(self, point: tuple) -> bool:
        return self.height > point[0] >= 0 and self.width > point[1] >= 0

    def getAdjacent(self, pos: tuple[int]) -> List:
        cells = []
        for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            c = self.addTuples(pos, d)
            if self.isInGrid(c):
                cells.append(c)
        return cells

    def addTuples(self, t1: tuple[int], t2: tuple[int]) -> tuple[int]:
        return tuple(a + b for a, b in zip(t1, t2))

    def getCell(self, coords: tuple[int]) -> int:
        y, x = list(coords)
        return self.grid[y][x]

    def walkTrail(self, start: tuple, path: list[int], visited=None) -> int:
        if visited is None:
            visited = set()

        visited.add(start)

        if self.getCell(start) == 9:
            return True

        trails = 0
        nbs = self.getAdjacent(start)
        l = path[-1]
        for n in nbs:
            c = self.getCell(n)
            if n not in visited and c - l == 1:
                # print('\tfor head', start, 'got', n, 'in nbs', nbs,  path)
                trails += self.walkTrail(n, path + [c], visited)

        return trails

    def walkTrail2(self, start: tuple, path: list[int], visited: set[tuple]) -> List:
        if self.getCell(start) == 9:
            return [visited]

        trails = []
        nbs = self.getAdjacent(start)
        l = path[-1]
        for n in nbs:
            c = self.getCell(n)
            if n not in visited and c - l == 1:
                # print('\tfor head', start, 'got', n, 'in nbs', nbs,  path)
                trails.extend(self.walkTrail2(n, path + [c], visited | {n}))

        return trails

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            t = [int(x) for x in line.strip()]
            stuff.append(t)

    return stuff


if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer1 = 36
    # test_answer2 = 81
    # inst = Solution(test_input)
    # ans1 = inst.calculate1()
    # ans2 = inst.calculate2()
    # print("Part1:", ans1, ans1 == test_answer1)
    # print("Part2:", ans2, ans2 == test_answer2)

    input = input_to_list("./input")
    inst = Solution(input)
    ans1 = inst.calculate1()
    ans2 = inst.calculate2()
    print("Part 1:", ans1)
    print("Part 2:", ans2)

    # p1: 461
    # p2: 875
