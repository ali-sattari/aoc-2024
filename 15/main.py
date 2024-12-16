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
            # print(self, v, f"{nbr}", type(nbr), nbr.movable)
            if nbr.try_moving(grid, next):
                self.move(v, grid)
                return True

        elif nbr is None:
            self.move(v, grid)
            return True

        return False

    def move(self, v: Vector, grid:dict):
        # print(f"moving {self} from {self.position} to {v}")
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

class WideBox(Thing):
    def __init__(self, pos: Vector, half):
        super().__init__(pos, '[]', True)
        self.other_half = half

    def try_moving(self, grid: dict, next: Optional[Vector] = None) -> bool:
        if self.can_move(grid, next) and self.other_half.can_move(grid, next):
            self.move(self.position + next, grid)
            self.other_half.move(self.other_half.position + next, grid)
            return True

        return False

    def can_move(self, grid: dict, next: Vector) -> bool:
        v = self.position + next
        nbr = grid.get(v)

        if nbr is None:
            return True

        if nbr is not None and nbr.is_movable():
            return True

        return False

    def move(self, v: Vector, grid:dict):
        print(f"moving {self} from {self.position} to {v}")
        del grid[self.position]
        grid[v] = self
        self.position = v

class Wall(Thing):
    def __init__(self, pos: Vector):
        super().__init__(pos, '#', False)

class Solution:
    def __init__(self, grid: dict, room: Vector):
        self.grid = grid
        self.room = room
        self.robot = [x for x in grid.values() if isinstance(x, Robot)][0]

    def calculate(self) -> int:
        self.render()

        while self.robot.has_move():
            self.robot.try_moving(self.grid)
            self.render()

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

        y = 0
        while y < self.room.y:
            x = 0
            while x < self.room.x:
                p = Vector(x, y)
                if p in self.grid:
                    obj = self.grid[p]
                    grid += str(obj)
                    if type(obj) is WideBox:
                        x += 1
                else:
                    grid += '.'
                x += 1
            grid += "\n"
            y += 1
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

def input_to_list_wide(f: str):
    grid: dict[Vector, Robot|WideBox|Wall] = dict()
    moves = ""
    first = True
    row = 0
    width = 0
    height = 0
    ext = Vector(1, 0)
    with open(file=f, mode='r') as file:
        for line in file:
            if line.strip() == '':
                first = False
                continue

            l = line.strip()
            if first:
                if width == 0: width = len(l)*2
                i = 0
                while i<len(l):
                    c = l[i]
                    v1 = Vector(i*2, row)
                    v2 = Vector(i*2+1, row)
                    match c:
                        case '#':
                            grid[v1] = Wall(v1)
                            grid[v2] = Wall(v2)
                        case 'O':
                            lh = WideBox(v1, None)
                            rh = WideBox(v2, lh)
                            lh.other_half = rh
                            grid[v1] = lh
                            grid[v2] = rh
                        case '@':
                            obj = robot = Robot(v1)
                            grid[v1] = obj
                    i += 1

                row += 1
            else:
                if height == 0: height = row
                moves += l

    robot.load_moves(moves)

    return grid, Vector(width, height)

if __name__ == "__main__":
    # test_grid, test_room = input_to_list("./test-input")
    # test_answer = 10092
    # # test_answer2 = 1206
    # inst = Solution(test_grid, test_room)
    # ans1 = inst.calculate()
    # print("Part1:", ans1, ans1 == test_answer)

    test_wide_grid, test_wide_room = input_to_list_wide("./test-input")
    test_wide_answer = 9021
    inst2 = Solution(test_wide_grid, test_wide_room)
    ans2 = inst2.calculate()
    print("Part2:", ans2, ans2 == test_wide_answer)

    # grid, room = input_to_list("./input")
    # inst = Solution(grid, room)
    # ans1 = inst.calculate1()
    # print("Part 1:", ans1)

    # wide_grid, wide_room = input_to_list_wide("./input")
    # inst2 = Solution(wide_grid, wide_room)
    # ans2 = inst2.calculate()
    # print("Part 2:", ans2)


    # p1: 1413675
    # p2:
