from typing import List, Optional, Tuple, Dict
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict
import time
import math
import numpy as np
from scipy.linalg import lu_factor, lu_solve

class Vector:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __le__(self, other):
        return self.__eq__(other) or (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)

    def __ge__(self, other):
        return self.__eq__(other) or (self.x, self.y) > (other.x, other.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __mul__(self, n):
        if isinstance(n, int):
            return Vector(self.x*n, self.y*n)
        raise NotImplementedError('Can only multiply Vector by an integer')

    def distance_to(self, other):
        return abs(self - other)

    def is_inbounds(self, w: int, h: int):
        return 0 <= self.x < w and 0 <= self.y < h

class Solution:
    def __init__(self, machines: List):
        self.machines = machines
        self.costs = {"A": 3, "B": 1}

    def calculate1(self) -> int:
        total = 0
        solvable = 0
        for i, m in enumerate(self.machines):
            c = self.get_cost(m)
            solvable += c > 0
            total += c

        print(f"Checked {len(self.machines)} machines, and {solvable} were solvable at cost of {total}")
        return total

    def calculate2(self) -> int:
            total = 0
            solvable = 0
            for i, m in enumerate(self.machines):
                c = self.get_cost(m, scaler=10000000000000)
                solvable += c > 0
                total += c

            print(f"Checked {len(self.machines)} machines, and {solvable} were solvable at cost of {total}")
            return total


    def get_cost(self, m: dict[str, Vector], scaler=0) -> int:
        C = np.array([
            [m["A"].x, m["B"].x],
            [m["A"].y, m["B"].y],
        ])
        P = m["P"]+Vector(scaler, scaler)
        D = np.array([P.x, P.y])

        lu, piv = lu_factor(C)
        A, B = lu_solve((lu, piv), D)
        if is_int(A) and is_int(B):
            return round(A)*self.costs["A"] + round(B)*self.costs["B"]

        return 0

def is_int(n: float) -> bool:
    return abs(n - round(n)) < 0.000001

def input_to_list(f: str) -> List:
    stuff = []
    l = 1
    m = {}
    with open(file=f, mode='r') as file:
        for line in file:
            t = line.strip()
            if t == '':
                continue

            if l == 1:
                conf = line.split("A:")[1].strip().split(",")
                m["A"] = conf_to_vector(conf)
                l += 1
                continue

            if l == 2:
                conf = line.split("B:")[1].strip().split(",")
                m["B"] = conf_to_vector(conf)
                l += 1
                continue

            if l == 3:
                conf = line.split(":")[1].strip().split(",")
                m["P"] = conf_to_vector(conf, separator="=")
                stuff.append(m)
                m = {}
                l = 1

    return stuff

def conf_to_vector(conf: list, separator="+") -> Vector:
    return Vector(int(conf[0].split(separator)[1]), int(conf[1].split(separator)[1]))

if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer1 = 480
    # # test_answer2 = 1206
    # inst = Solution(test_input)
    # ans1 = inst.calculate1()
    # ans2 = inst.calculate2()
    # print("Part1:", ans1, ans1 == test_answer1)
    # print("Part2:", ans2)

    input = input_to_list("./input")
    inst = Solution(input)
    ans1 = inst.calculate1()
    ans2 = inst.calculate2()
    print("Part 1:", ans1)
    print("Part 2:", ans2)

    # p1: 30973
