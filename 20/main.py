from typing import List, Optional, Tuple, Dict
from pprint import pprint
import math
from vector import Vector

class Solution:
    def __init__(self, blocks: set[Vector], room, start, end: Vector):
        self.all_blocks = blocks
        self.removed_blocks: set[Vector] = set()
        self.blocks = blocks
        self.room = room
        self.start = start
        self.end = end
        self.paths: List[list[Vector]] = []

    def calculate(self, min_saving=0) -> int:
        # self.render(self.blocks)
        base_score = self.astar()
        print(f"base score is {base_score}")

        rmv = self.removable_blocks(self.blocks, set())
        print(f"found {len(rmv)} removable blocks to cheat on")

        cheat_savings = []
        for r in rmv:
            self.blocks = self.all_blocks.copy()
            self.blocks.remove(r)
            s = self.astar()
            print(f"got a new score {s} with cheat block {r} at diff of {base_score -s}")
            cheat_savings.append(base_score - s)

        useful = [c for c in cheat_savings if c >= min_saving]

        return len(useful)

    def astar(self) -> int:
        costs: dict[Vector, float] = {self.start: 0}
        paths: dict[Vector, list[list]] = {self.start: [[self.start]]}
        to_do: set[Vector] = {self.start}

        while to_do:
            current = min(to_do, key=lambda t: costs[t] + self.cost_heuristic(t))
            if current == self.end:
                self.paths = paths[self.end]
                return int(costs[self.end])

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

        # If we exit the loop and haven't found the goal, it's unreachable
        self.paths = paths[current]
        return -1

    def cheat(self):

        pass

    def removable_blocks(self, blocks, used: set[Vector]) -> List[Vector]:
        dirs = Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)
        bs = []
        for blk in blocks:
            if blk in used:
                continue

            t, r, b, l = [blk + d for d in dirs]
            if (
                r.is_inbounds(self.room.x, self.room.y) and l.is_inbounds(self.room.x, self.room.y)
                and r not in blocks and l not in blocks
            ): #left and right of block is free
                bs.append(blk)

            if (
                t.is_inbounds(self.room.x, self.room.y) and b.is_inbounds(self.room.x, self.room.y)
                and t not in blocks and b not in blocks
            ): #top and bottom of block is free
                bs.append(blk)

        return bs

    def cost_heuristic(self, node: Vector) -> float:
        # Manhattan Distance
        return abs(node.x - self.end.x) + abs(node.y - self.end.y)

    def get_buren(self, pos: Vector) -> List[Vector]:
        dirs = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)]
        bs = []
        for d in dirs:
            t = d + pos
            if t not in self.blocks and t.is_inbounds(self.room.x, self.room.y):
                bs.append(t)
        return bs

def process_input(f: str):
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
    # test_input = process_input("./test-input")
    # test_answer = 22
    # # test_answer2 = Vector(6, 1)
    # inst = Solution(*test_input)
    # savings = inst.calculate(10)
    # print("Part1:", savings)
    # # print("Part2:", blocker, blocker == test_answer2)

    input = process_input("./input")
    room = Vector(71, 71)
    inst = Solution(*input)
    cheats = inst.calculate(100)
    print("Part 1:", cheats)
    # print("Part 2:", blocker)
