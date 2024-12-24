from typing import List, Optional, Tuple, Dict, Literal
from pprint import pprint
from collections import Counter
import math
from vector import Vector
from termcolor import colored

class Solution:
    def __init__(self, codes: List):
        self.codes = codes
        self.pads = ['num_pad', 'dir_pad']
        self.num_pad: dict[str, Vector] = {
            '7': Vector(0,0), '8': Vector(1,0), '9': Vector(2,0),
            '4': Vector(0,1), '5': Vector(1,1), '6': Vector(2,1),
            '1': Vector(0,2), '2': Vector(1,2), '3': Vector(2,2),
                              '0': Vector(1,3), 'A': Vector(2,3),
        }
        self.num_pad_grid = set(self.num_pad.values())
        self.dir_pad: dict[str, Vector] = {
                              '^': Vector(1,0), 'A': Vector(2,0),
            '<': Vector(0,1), 'v': Vector(1,1), '>': Vector(2,1),
        }
        self.dir_pad_grid = set(self.dir_pad.values())
        self.path = []
        self.initial_key = 'A'
        self.press = 'A'

    def calculate(self) -> int:
        complexity = 0

        for code in self.codes:
            res = self.get_num_pad_sequence(code)
            res = self.get_dir_pad_sequence(res)
            res = self.get_dir_pad_sequence(res)
            comp = int(code.strip('A')) * len(res)
            print(f"dial {code} with {len(res)} steps with comp {comp}: {res}")
            complexity += int(code.strip('A')) * len(res)

        return complexity

    def get_num_pad_sequence(self, code:str) -> str:
        path = ''
        for i, c in enumerate(code):
            start = self.initial_key if i == 0 else code[i-1]
            res = self.astar(self.num_pad[start], self.num_pad[c], 'num_pad')
            res = sorted(res) + [self.press]
            path += ''.join(res)

        return path

    def get_dir_pad_sequence(self, code:str) -> str:
        path = ''
        for i, c in enumerate(''.join(code)):
            start = self.initial_key if i == 0 else code[i-1]
            res = self.astar(self.dir_pad[start], self.dir_pad[c], 'dir_pad')
            res = sorted(res) + [self.press]
            path += ''.join(res)

        return path

    def astar(self, start, end: Vector, pad: Literal['num_pad', 'dir_pad']) -> List[str]:
        costs: dict[Vector, float] = {start: 0}
        paths: dict[Vector, list[list]] = {start: [[start]]}
        dirs: dict[Vector, list[str]] = {start: []}
        to_do: set[Vector] = {start}

        while to_do:
            current = min(to_do, key=lambda t: costs[t] + self.cost_heuristic(t, end))
            if current == end:
                return dirs[end]

            to_do.remove(current)
            for nbr in self.get_buren(current, pad):
                new_dist = costs[current] + 1
                if new_dist < costs.get(nbr, math.inf):
                    costs[nbr] = new_dist
                    paths[nbr] = [path + [nbr] for path in paths[current]]

                    direction = self.vec2dir(nbr - current)
                    dirs[nbr] = dirs[current] + [direction]

                    to_do.add(nbr)

        return []  # Return an empty list if no path is found

    def cost_heuristic(self, node, end: Vector) -> float:
        # Manhattan Distance
        return abs(node.x - end.x) + abs(node.y - end.y)

    def get_buren(self, pos: Vector, pad: Literal['num_pad', 'dir_pad']) -> List[Vector]:
        grid = set(getattr(self, pad).values())

        dirs = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)]
        bs = []
        for d in dirs:
            t = d + pos
            if t in grid:
                bs.append(t)
        return bs

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
    input = []
    with open(file=f, mode='r') as file:
        for line in file:
            input.append(line.strip())
    return input

if __name__ == "__main__":
    test_input = process_input("./test-input")
    test_answer1 = 126384
    # test_answer2 = Vector(6, 1)
    inst = Solution(test_input)
    answ1 = inst.calculate()
    print("Part1:", answ1 ,answ1 == test_answer1)
    # print("Part2:", blocker, blocker == test_answer2)

    # input = process_input("./input")
    # room = Vector(71, 71)
    # inst = Solution(*input)
    # cheats = inst.calculate(100)
    # print("Part 1:", cheats)
    # # print("Part 2:", blocker)

    # p1:
    # p2:
