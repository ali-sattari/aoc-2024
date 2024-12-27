from collections import defaultdict, deque
from typing import List, Optional, Tuple, Dict, Literal
from pprint import pprint
import functools

class Solution:
    def __init__(self, initial: list[int]):
        self.initial = initial
        self.memory: dict[int, int] = dict()
        self.prices: dict[tuple, list] = defaultdict(lambda: [0]*len(initial))

    def calculate(self, count=10) -> int:
        secrets = []
        for i, s in enumerate(self.initial):
            secrets.append(self.nth_secret(i, s, count))

        return sum(secrets)

    def calculate2(self, count=10) -> int:
        if len(self.prices) == 0:
            self.calculate(count)

        for k, v in self.prices.items():
            if sum(v) > 1600:
                print(k, sum(v), sum(i > 0 for i in v))

        sales = [sum(v) for k, v in self.prices.items()]
        return max(sales)

    def nth_secret(self, idx, num, n:int) -> int:
        price = num % 10
        window = deque(maxlen=4)
        # print(f"{num: >12}: {price}")
        for i in range(n):
            if i > 0:
                new_price = num % 10
                change =  new_price - price
                window.append(change)
                # print(f"{idx} {num: >12}: {new_price} ({change})")
                price = new_price
                self.prices[tuple(window)][idx] = price
            num = self.new_secret(num)
        return num

    def new_secret(self, num:int) -> int:
        if num in self.memory:
            return self.memory[num]

        denom = 16777216
        new = ((num * 64) ^ num) % denom
        new = new ^ (new // 32)
        new = ((new * 2048) ^ new) % denom

        self.memory[num] = new
        return new

def process_input(f: str):
    states: list[int] = []
    with open(file=f, mode='r') as file:
        for line in file:
            states.append(int(line.strip()))

    return states

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer1 = 37327623
    # test_answer2 = 23
    # inst = Solution(test_input)
    # answ1 = inst.calculate(2000)
    # print("Part1:", answ1 ,answ1 == test_answer1)
    # answ2 = inst.calculate2(2000)
    # print("Part2:", answ2, answ2 == test_answer2)

    input = process_input("./input")
    inst = Solution(input)
    answ1 = inst.calculate(2000)
    print("Part 1:", answ1)
    answ2 = inst.calculate2(2000)
    print("Part 2:", answ2)

    # p2: 1654 too low and 1725 too high
