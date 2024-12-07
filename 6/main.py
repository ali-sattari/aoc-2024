from typing import List, Tuple
from pprint import pprint
from filecmp import dircmp

class Solution1:
    def __init__(self, grid: List):
        self.grid = grid
        self.log = grid.copy()
        self.height = len(grid)
        self.width = len(grid[0])
        self.blocks = dict()
        self.guard = '^'
        self.object = '#'
        self.marker = 'X'
        self.blocker = 'O'

    def calculate(self) -> int:
        guard_pos = self.locate_guard()
        direction = "up"
        y, x = guard_pos

        while True:
            ny, nx = self.move_in_dir(direction, y, x)
            self.record_log(direction, y, x)

            if self.is_inside_grid(ny, nx):
                if self.is_object(ny, nx):
                    direction = self.turn(direction)
                    continue

                y, x = ny, nx
            else:
                break

        return self.count_positions()

    def is_blocked(self, y, x) -> bool:
        return bool(self.blocks.get((y,x)))

    def is_marked(self, y, x) -> bool:
        log = self.log[y][x]
        return log != "."

    def record_log(self, direction, y, x):
        translate = {
            "up": '\u2191',
            "right": '\u2192',
            "down": '\u2193',
            "left": '\u2190',
        }
        # self.log[y][x] = self.marker
        self.log[y][x] = translate[direction]

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
    # pprint(test_input)
    # test_answer = 41
    # inst = Solution1(test_input)
    # ans = inst.calculate()
    # print(inst.height, inst.width)
    # print(ans, ans == test_answer)
    # pprint(inst.log)

    res = Solution1(input_to_list("./input"))
    ans = res.calculate()
    print("Part1:", ans)
    pprint(res.output_path())
