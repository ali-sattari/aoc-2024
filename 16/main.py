from typing import List, Optional, Tuple, Dict, TypeAlias
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict, namedtuple
from collections.abc import Callable, Iterable, Iterator
import time
import math
import sys
from vector import Vector
from queue import Queue
from termcolor import colored

Node: TypeAlias = tuple[Vector, Vector] #position, direction

class Solution:
    def __init__(self, blocks: set[Vector], room, start, end: Vector):
        self.blocks = blocks
        self.room = room
        self.start = start
        self.end = end
        self.path: list[Vector] = []
        self.paths: List[list[Vector]] = []
        self.initial_dir = Vector(1, 0) #facing right

    def calculate(self) -> tuple[int, int]:
        # self.dfs(self.start, [])
        # min_score = math.inf
        # min_path = 0
        # for i, p in enumerate(self.paths):
        #     s = self.get_score(p)
        #     if s < min_score:
        #         min_score = s
        #         min_path = i
        #     # print(f"Path {i} with len {len(p)} and score {s}:")
        #     # self.render(p)
        # self.path = self.paths[min_path]
        # self.render(path)

        score = self.dijkstra()
        tiles = self.count_tiles()

        print(f"Part 1, one of the shortest paths among {len(self.paths)}:")
        self.render(self.paths[0])

        print(f"Part 2, tiels in all of the best paths:")
        self.render_tiles(self.paths)

        return score, tiles

    def get_score(self, path) -> int:
        score = 0
        dir = self.initial_dir
        for i in range(1, len(path)):
            score += 1
            d = path[i] - path[i-1]
            if dir != d:
                score += 1000
                dir = d
        return score

    def count_tiles(self) -> int:
        tiles = set()
        for p in self.paths:
            tiles |= set(p)
        return len(tiles)

    def dfs(self, pos: Vector, path: List[Vector]) -> List[Vector]:
        if pos == self.end:
            return path + [pos]

        nbrs = self.get_buren(pos)
        for n in nbrs:
            if n not in path:
                t = self.dfs(n, path + [pos])
                if t:
                    self.paths.append(t)

    def dijkstra(self) -> float:
        start: Node = (self.start, self.initial_dir)
        costs: dict[Node, float] = {start: 0}
        paths: dict[Node, list[list]] = {start: [[self.start]]}
        to_do: set[Node] = {start}

        while len(to_do):
            current = min(to_do, key=lambda t: costs[t])
            if current[0] == self.end:
                break

            to_do.remove(current)
            for nbr in self.get_buren(current[0]):
                dir = current[1]
                c = self.get_cost(current[0], nbr, dir)
                new_dist = costs[current] + c
                n: Node = (nbr, nbr-current[0])
                if new_dist < costs.get(n, math.inf):
                    costs[n] = new_dist
                    paths[n] = [path + [nbr] for path in paths[current]]
                    to_do.add(n)
                elif new_dist == costs.get(n, math.inf):
                    paths[n].extend([path + [nbr] for path in paths[current]])

        self.paths = paths[current]
        return costs[current]

    def get_cost(self, src, dst, dir: Vector) -> int:
        # 1000 for turning, 1 for moving
        if dst - src != dir:
            return 1001
        # 1 for moving
        return 1

    def get_buren(self, pos: Vector) -> List[Vector]:
        dirs = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)]
        bs = []
        for d in dirs:
            t = d + pos
            if t not in self.blocks:
                bs.append(t)
        return bs

    def render_tiles(self, paths):
        t = set()
        for p in self.paths:
            t |= set(p)
        self.render(t)

    def render(self, path):
        grid = ""

        y = 0
        grid += '+' + ''.join([colored(str(n%10), 'blue') for n in range(self.room.x)]) + "\n"
        while y < self.room.y:
            grid += colored(str(y%10), 'blue')
            x = 0
            while x < self.room.x:
                p = Vector(x, y)
                match p:
                    case p if p in self.blocks:
                        grid += '#'
                    case p if p == self.start:
                        grid += colored('S', 'yellow', attrs=['bold'])
                    case p if p == self.end:
                        grid += colored('E', 'green', attrs=['bold'])
                    case p if p in path:
                        # grid += self.path[p]
                        grid += colored('+', 'red')
                    case _:
                        grid += '.'
                x += 1
            grid += "\n"
            y += 1
        print(grid)

    def dir2vec(self, dir: str) -> Vector:
        map = {
            "^": Vector(0, -1),
            ">": Vector(1, 0),
            "v": Vector(0, 1),
            "<": Vector(-1, 0),
        }
        return map[dir]

    def vec2dir(self, v: Vector) -> str:
        pam = {
            Vector(0, -1): "^",
            Vector(1, 0): ">",
            Vector(0, 1): "v",
            Vector(-1, 0): "<",
        }
        return pam[v]

def input_to_list(f: str):
    grid: set[Vector] = set()
    start = end = None
    width = height = 0
    row = 0
    with open(file=f, mode='r') as file:
        for line in file:
            l = line.strip()
            if width == 0: width = len(l)
            i = 0
            while i<len(l):
                c = l[i]
                v = Vector(i, row)
                match c:
                    case '#':
                        grid.add(v)
                    case 'S':
                        start = v
                    case 'E':
                        end = v
                i += 1
            row += 1
    height = row
    return grid, Vector(width, height), start, end

if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer = 11048
    # test_answer2 = 64
    # inst = Solution(*test_input)
    # score, tiles = inst.calculate()
    # print("Part1:", score, score == test_answer)
    # print("Part2:", tiles, tiles == test_answer2)

    input = input_to_list("./input")
    inst = Solution(*input)
    score, tiles = inst.calculate()
    print("Part 1:", score)
    print("Part 2:", tiles)

    # p1: 109496
    # p2: 551
