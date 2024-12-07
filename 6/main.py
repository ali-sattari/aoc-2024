from typing import List, Tuple
from pprint import pprint
from collections import defaultdict

class Solution1:
    def __init__(self, grid: List):
        self.grid = grid
        self.log = grid.copy()
        self.height = len(grid)
        self.width = len(grid[0])
        self.visited = set()
        self.blocks = set()
        self.guard = '^'
        self.object = '#'
        self.marker = 'X'
        self.blocker = 'O'
        self.path_marker = {
            "up": '\u2191',
            "right": '\u2192',
            "down": '\u2193',
            "left": '\u2190',
        }

    def calculate1(self) -> int:
        guard_pos = self.locate_guard()
        direction = "up"
        y, x = guard_pos

        while True:
            ny, nx = self.move_in_dir(direction, y, x)
            self.record_log(direction, y, x, dir_mark=False)

            if self.is_inside_grid(ny, nx):
                if self.is_object(ny, nx):
                    direction = self.turn(direction)
                    continue

                y, x = ny, nx
            else:
                break

        return self.count_positions()

    def calculate2(self) -> int:
        self.log = self.grid.copy()

        guard_pos = self.locate_guard()
        direction = "up"
        pos = guard_pos

        while True:
            new_pos = self.move_in_dir(direction, *pos)
            if self.is_inside_grid(*new_pos) == False:
                break

            if self.is_object(*new_pos):
                direction = self.turn(direction)
                continue

            if(new_pos not in self.blocks and new_pos != guard_pos and  new_pos not in self.visited):
                foundLoop = self.is_loop(pos, self.turn(direction), new_pos)
                if foundLoop:
                    self.blocks.add(new_pos)
            pos = new_pos
            self.visited.add(pos)

        return len(self.blocks)

    def is_loop(self, pos: tuple, direction: str, block: tuple) -> bool:
        trace = defaultdict(list)
        while True:
            new_pos = self.move_in_dir(direction, *pos)
            if self.is_inside_grid(*new_pos) is not True:
                return False
            if self.is_object(*new_pos) or new_pos == block:
                direction = self.turn(direction)
                continue
            if new_pos in trace and direction in trace[new_pos]:
                return True

            pos = new_pos
            trace[pos].append(direction)

    def is_blocked(self, y, x) -> bool:
        return (y,x) in self.blocks

    def is_marked(self, y, x) -> bool:
        log = self.log[y][x]
        return log != "."

    def add_blockers(self):
        for y, x in self.blocks:
            self.log[y][x] = self.blocker

    def record_log(self, direction, y, x, dir_mark=True):
        if dir_mark:
            self.log[y][x] = self.path_marker[direction]
        else:
            self.log[y][x] = self.marker

    def count_positions(self) -> int:
        c = 0
        for row in self.log:
            for char in row:
                if char == self.marker:
                    c += 1
        return c

    def is_inside_grid(self, y: int, x: int) -> bool:
        return (y >= 0 and y < self.height) and (x >= 0 and x < self.width)

    def is_object(self, y: int, x: int) -> bool:
        c = self.grid[y][x]
        return c == self.object

    def move_in_dir(self, direction: str, y:int, x:int) -> Tuple[int, int]:
        next = (0,0)

        if direction == "up":
            next = (y-1, x)
        elif direction == "down":
            next = (y+1, x)
        elif direction == "right":
            next = (y, x+1)
        else: #left
            next = (y, x-1)

        return next

    def turn(self, direction) -> str:
        directions = ["up", "right", "down", "left"]
        curr = directions.index(direction)
        new = directions[curr+1] if curr+1 < len(directions) else directions[0]

        return new

    def is_guard(self, y: int, x: int) -> bool:
        c = self.grid[y][x]
        return c == self.guard

    def locate_guard(self) -> Tuple[int, int]:
        pos = (0 , 0)
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if self.is_guard(y, x):
                    pos = (y, x)

        return pos

    def output_path(self) -> str:
        out = ""
        for row in self.log:
            out += ''.join(row) + "\n"
        return out

def input_to_list(f: str) -> List:
    lst = []
    with open(file=f, mode='r') as file:
        for line in file:
            lst.append(list(line.strip()))

    return lst

if __name__ == "__main__":
    #testing with sample inputs
    # test_input = input_to_list("./test-input")
    # test_answer = 6
    # inst = Solution1(test_input)
    # ans = inst.calculate2()
    # print(ans, ans == test_answer)
    # pprint(inst.blocks)

    res = Solution1(input_to_list("./input"))
    ans = res.calculate1()
    print("Part1:", ans)
    res2 = Solution1(input_to_list("./input"))
    ans2 = res2.calculate2()
    print("Part2:", ans2)
    # res.add_blockers()
    # pprint(res.output_path())
