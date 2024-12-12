from typing import List, Optional, Tuple
from pprint import pprint
from math import floor
from itertools import repeat
from collections import defaultdict
import time

# rules:
# If number 0, it is replaced by number 1
# If number that has an even number of digits, it is replaced by two halves of digits
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone

# optimization for part two:
# add a seen dict for calcs -> done
# add a count dict for count of each stone
#   after the first round go over the dict,
#   calculate new stones,
#   ++ new stone
#   -- the changed stone
#   get sum of dict values

class Solution:
    def __init__(self, arrangement: List):
        self.arrangement = arrangement
        self.seen = defaultdict(list)
        self.stones = defaultdict(int)
        self.blinks = 0

    def calculate1(self, blinks: int) -> int:
        for n in range(0, blinks):
            new_arr = []
            for stone in self.arrangement:
                if stone in self.seen:
                    t = self.seen[stone]
                else:
                    t = self.blink_on_stone(stone)
                    self.seen[stone] = t
                new_arr.extend(t)

            self.arrangement = new_arr.copy()
            print(n, len(new_arr))

        return len(self.arrangement)

    def calculate2(self, blinks: int) -> int:
        self.blinks = blinks

        count = 0
        for stone in self.arrangement:
            start_time = time.perf_counter()

            print("counting", stone, "...")
            c = self.blink(stone, 0)

            dur = time.perf_counter() - start_time
            print("="*30, f"{blinks} blinks at {stone} resulted in {c} stones", '(in {:5.4f}ms)'.format(dur*1000))
            count += c

        return count

    def blink(self, stone:int, depth:int, cache = None) -> int:
        if cache is None:
            cache = defaultdict(int)

        # print(" "*depth, depth, "\t"*2, stone, "\t"*2, cache.keys())

        if depth == self.blinks:
            return 1
        depth += 1

        cache_key = (stone, depth)
        if cache_key in cache:
            return cache[cache_key]

        new_stones = self.blink_on_stone(stone)
        count = 0
        for ns in new_stones:
            count += self.blink(ns, depth, cache)

        cache[cache_key] = count

        return count

    def count_stones(self) -> int:
        return sum(self.stones.values())

    def blink_on_stone(self, stone: int) -> List[int]:
        if stone == 0:
            return [1]

        if self.has_even_digits(stone):
            return self.split_stone(stone)

        return [stone * 2024]

    def has_even_digits(self, n: int) -> bool:
        return len(str(n)) % 2 == 0

    def split_stone(self, n: int) -> List[int]:
        s = str(n)
        mid = len(s) // 2
        return [int(s[:mid]), int(s[mid:])]

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            t = [int(x) for x in line.strip().split(' ')]
            stuff.append(t)

    return stuff[0]


if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer1 = 55312 # after 25 blinks
    # inst = Solution(test_input)
    # ans1 = inst.calculate1(25)
    # ans2 = inst.calculate2(7)
    # ans3 = inst.calculate3(25)
    # print("Part1:", ans1, ans1 == test_answer1)
    # print("Part2:", ans2, ans2 == test_answer1)
    # print("Part2:", ans3, ans3 == test_answer1)

    input = input_to_list("./input")
    inst = Solution(input)
    ans1 = inst.calculate2(25)
    ans2 = inst.calculate2(75)
    print("Part 1:", ans1)
    print("Part 2:", ans2)

    # p1: 182081
    # 0.08s user 0.03s system 64% cpu 0.174 total
    # p2: 216318908621637
    # 0.27s user 0.04s system 83% cpu 0.370 total
