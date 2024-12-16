import sys
sys.path.append('..')

from typing import List, Optional, Tuple, Dict
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict
import time
import math
from vector import Vector

class Robot:
    def __init__(self, start: Vector, velocity: Vector, room: Vector):
        self.start = start
        self.position = start
        self.velocity = velocity
        self.room = room

    def move(self, seconds=1):
        p = self.position
        for s in range(seconds):
            p = (p + self.velocity) % self.room

        self.position = p

class Solution:
    def __init__(self, robots: List[Robot], room: Vector):
        self.robots = robots
        self.room = room

    def calculate1(self, seconds=1) -> int:
        # print("how it started:")
        # initial = [r.start for r in self.robots]
        # self.render(initial)

        pos = []
        for r in self.robots:
            r.move(seconds)
            pos.append(r.position)
        # print("how it ended:")
        # self.render(pos)
        # print("divided in quads:")
        # self.render(pos, quads=True)

        return self.risk_factor(pos)

    def calculate2(self) -> int:
        min_score = math.inf
        min_time = 0
        xmas = []
        ll = len(self.robots)
        for t in range(1, 10000):
            pos = []
            for r in self.robots:
                r.move(1)
                pos.append(r.position)

            lu = len(set(pos))
            print(f"time {t}, list of {ll} but only {lu} unique positions", end='\r')
            if lu == ll:
                min_time = t
                xmas = pos

        print(f"how it ended in {min_time} time:")
        self.render(xmas)

        return min_time


    def risk_factor(self, pos) -> int:
        qs = [0]*4
        midx = self.room.x // 2
        midy = self.room.y // 2
        for p in pos:
            match p:
                case p if p.x < midx and p.y < midy:
                    qs[0] += 1
                case p if p.x > midx and p.y < midy:
                    qs[1] += 1
                case p if p.x < midx and p.y > midy:
                    qs[2] += 1
                case p if p.x > midx and p.y > midy:
                    qs[3] += 1
        # print(qs)
        return math.prod(qs)

    def render(self, pos: List, quads=False):
        grid = ""
        if quads:
            midx = self.room.x // 2
            midy = self.room.y // 2

        for y in range(self.room.y):
            for x in range(self.room.x):
                if quads and (x == midx or y == midy):
                   grid += ' '
                   continue

                p = Vector(x=x, y=y)
                if p in pos:
                    grid += str(pos.count(p))
                else:
                    grid += '.'
            grid += "\n"

        print(grid)



def input_to_list(f: str, room:Vector) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            t = line.strip().split(' ')
            s = [int(n) for n in t[0].strip().split('=')[1].split(',')]
            v = [int(n) for n in t[1].strip().split('=')[1].split(',')]
            r = Robot(start=Vector(*s), velocity=Vector(*v), room=room)
            stuff.append(r)

    return stuff

if __name__ == "__main__":
    # test_room = Vector(11, 7)
    # test_input = input_to_list("./test-input", test_room)
    # test_answer1 = 12
    # # test_answer2 = 1206
    # inst = Solution(test_input, test_room)
    # ans1 = inst.calculate1(100)
    # # ans2 = inst.calculate2()
    # print("Part1:", ans1, ans1 == test_answer1)
    # # print("Part2:", ans2)

    room = Vector(101, 103)
    input = input_to_list("./input", room)
    inst = Solution(input, room)
    # ans1 = inst.calculate1(100)
    # print("Part 1:", ans1)

    ans2 = inst.calculate2()
    print("Part 2:", ans2)

    # p1: 217328832
    # p2: 7412
