from typing import List, Optional, Tuple, Dict, TypeAlias
from pprint import pprint
from math import floor
from collections import defaultdict, namedtuple
from collections.abc import Callable, Iterable, Iterator
import math
import sys
from vector import Vector
from queue import Queue
from termcolor import colored

class Solution:
    def __init__(self, bytes: dict[Vector, int], room: Vector):
        self.bytes = bytes
        self.blocks = dict()
        self.room = room
        self.start = Vector(0, 0)
        self.end = room - Vector(1, 1)
        self.paths: List[list[Vector]] = []

    def calculate(self, falls:int) -> int:
        self.blocks = self.filter_bytes(falls)
        # self.render(list(self.blocks.keys()))

        # score = self.dijkstra()
        score = self.astar()

        print(f"Part 1, one of the shortest paths among {len(self.paths)}:")
        self.render(self.paths[0])
        # for i, p in enumerate(self.paths):
        #     print(f"Path {i}")
        #     self.render(p)

        return score

    def dijkstra(self) -> int:
        costs: dict[Vector, float] = {self.start: 0}
        paths: dict[Vector, list[list]] = {self.start: [[self.start]]}
        to_do: set[Vector] = {self.start}

        while len(to_do):
            current = min(to_do, key=lambda t: costs[t])
            if current == self.end:
                break

            to_do.remove(current)
            for nbr in self.get_buren(current):
                new_dist = costs[current] + 1
                if new_dist < costs.get(nbr, math.inf):
                    print(f"found a nbr {nbr} with cost {new_dist} for {current}")
                    costs[nbr] = new_dist
                    paths[nbr] = [path + [nbr] for path in paths[current]]
                    to_do.add(nbr)
                elif new_dist == costs.get(nbr, math.inf):
                    paths[nbr].extend([path + [nbr] for path in paths[current]])

        self.paths = paths[current]
        return int(costs[current])

    def astar(self) -> int:
        costs: dict[Vector, float] = {self.start: 0}
        paths: dict[Vector, list[list]] = {self.start: [[self.start]]}
        to_do: set[Vector] = {self.start}

        while to_do:
            current = min(to_do, key=lambda t: costs[t] + self.cost_heuristic(t))
            if current == self.end:
                break

            to_do.remove(current)
            for nbr in self.get_buren(current):
                new_dist = costs[current] + 1
                if new_dist < costs.get(nbr, math.inf):
                    # print(f"found a nbr {nbr} with cost {new_dist} for {current}")
                    costs[nbr] = new_dist
                    paths[nbr] = [path + [nbr] for path in paths[current]]
                    to_do.add(nbr)
                elif new_dist == costs.get(nbr, math.inf):
                    paths[nbr].extend([path + [nbr] for path in paths[current]])

        self.paths = paths[self.end]
        return int(costs[self.end])

    def cost_heuristic(self, node: Vector) -> float:
        # Manhattan Distance
        return abs(node.x - self.end.x) + abs(node.y - self.end.y)

    def filter_bytes(self, count: int) -> dict[Vector, int]:
        f = {}
        for k, v in self.bytes.items():
            if v >= count:
                break
            f[k] = v
        return f

    def get_buren(self, pos: Vector) -> List[Vector]:
        dirs = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)]
        bs = []
        for d in dirs:
            t = d + pos
            if t not in self.blocks and t.is_inbounds(self.room.x, self.room.y):
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

def process_input(f: str):
    stuff: dict[Vector, int] = dict()
    i = 0
    with open(file=f, mode='r') as file:
        for line in file:
            l = line.strip().split(',')
            stuff[
                Vector(
                    int(l[0]),
                    int(l[1])
                )
            ] = i
            i += 1
    return stuff

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer = 22
    # # test_answer2 = 64
    # inst = Solution(test_input, Vector(7, 7))
    # moves = inst.calculate(12)
    # print("Part1:", moves, moves == test_answer)
    # # print("Part2:", tiles, tiles == test_answer2)

    input = process_input("./input")
    room = Vector(71, 71)
    inst = Solution(input, room)
    moves = inst.calculate(1024)
    print("Part 1:", moves)
    # print("Part 2:", tiles)

    # p1: 232
    # p2:
