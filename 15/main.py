from typing import List, Optional, Tuple, Dict
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict
import time
import math
from vector import Vector
from queue import Queue

class Thing:
    def __init__(self, pos: Vector, symbol: str, movable: bool):
        self.position = pos
        self.symbol = symbol
        self.movable = movable

    def __repr__(self):
        return self.symbol

    def is_movable(self) -> bool:
        return self.movable

    def try_moving(self, grid: dict, next: Optional[Vector] = None) -> bool:
        v = self.position + next
        nbr = grid.get(v)

        if nbr is not None and nbr.is_movable():
            # print(self, v, nbr, nbr.movable)
            if nbr.try_moving(grid, next):
                self.move(v, grid)
                return True

        elif nbr is None:
            self.move(v, grid)
            return True

        return False

    def move(self, v: Vector, grid:dict):
        del grid[self.position]
        grid[v] = self
        self.position = v

    def get_gps(self) -> int:
        return self.position.y * 100 + self.position.x

class Robot(Thing):
    def __init__(self, pos: Vector):
        super().__init__(pos, '@', True)
        self.start = pos
        self.moves: Queue[Vector] = Queue()

    def load_moves(self, moves:str):
        dir_map = {
            "^": Vector(0, -1),
            ">": Vector(1, 0),
            "v": Vector(0, 1),
            "<": Vector(-1, 0),
        }
        for m in moves:
            self.moves.put(dir_map[m])

    def try_moving(self, grid: dict, next: Optional[Vector] = None):
        next = self.moves.get()
        return super().try_moving(grid, next)

    def has_move(self) -> bool:
        return not self.moves.empty()

class Box(Thing):
    def __init__(self, pos: Vector):
        super().__init__(pos, 'O', True)

class Wall(Thing):
    def __init__(self, pos: Vector):
        super().__init__(pos, '#', False)

class Solution:
    def __init__(self, grid: dict, room: Vector):
        self.grid = grid
        self.room = room
        self.robot = [x for x in grid.values() if isinstance(x, Robot)][0]

    def calculate1(self) -> int:
        self.render()

        while self.robot.has_move():
            self.robot.try_moving(self.grid)

        self.render()
        return self.get_gps_sum()

    def get_gps_sum(self) -> int:
        total = 0
        for obj in self.grid.values():
            if isinstance(obj, Box):
                total += obj.get_gps()
        return total

    def render(self):
        grid = ""

        for y in range(self.room.y):
            for x in range(self.room.x):
                p = Vector(x, y)
                if p in self.grid:
                    grid += str(self.grid[p])
                else:
                    grid += '.'
            grid += "\n"

        print(grid)

def input_to_list(f: str):
    grid: dict[Vector, Robot|Box|Wall] = dict()
    moves = ""
    first = True
    row = 0
    width = 0
    height = 0
    with open(file=f, mode='r') as file:
        for line in file:
            if line.strip() == '':
                first = False
                continue

            l = line.strip()
            if first:
                if width == 0: width = len(l)
                for i, c in enumerate(l[:]):
                    v = Vector(i, row)
                    match c:
                        case '#':
                            obj = Wall(v)
                        case 'O':
                            obj = Box(v)
                        case '@':
                            obj = robot = Robot(v)
                        case _:
                            obj = None
                    if obj:
                        grid[v] = obj
                row += 1
            else:
                if height == 0: height = row
                moves += l

    robot.load_moves(moves)

    return grid, Vector(width, height)

if __name__ == "__main__":
    # test_grid, test_room = input_to_list("./test-input")
    # test_answer1 = 10092
    # # test_answer2 = 1206
    # inst = Solution(test_grid, test_room)
    # ans1 = inst.calculate1()
    # # ans2 = inst.calculate2()
    # print("Part1:", ans1, ans1 == test_answer1)
    # # print("Part2:", ans2)

    grid, room = input_to_list("./input")
    inst = Solution(grid, room)
    ans1 = inst.calculate1()
    print("Part 1:", ans1)

    # ans2 = inst.calculate2()
    # print("Part 2:", ans2)

    # p1: 1413675
    # p2:
