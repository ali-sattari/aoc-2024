from typing import List, Tuple
from pprint import pprint

class Solution:
    def __init__(self, equations: List):
        self.eqs = equations
        self.total = 0
        self.total2 = 0

    def calculate1(self) -> int:
        for eq in self.eqs:
            test = eq[0]
            nums = eq[1:]

            if self.find_operations(test, nums):
                self.total += test

        return self.total

    def calculate2(self) -> int:
        for eq in self.eqs:
            test = eq[0]
            nums = eq[1:]

            if self.find_operations2(test, nums[0], nums[1:]):
                self.total2 += test

        return self.total2

    def find_operations(self, target: int, nums: List[int]) -> bool:
        if len(nums) == 1:
            return True if nums[0] == target else False

        num1, rest_nums = nums[-1], nums[:-1]
        # check multiplication
        if target % num1 == 0:
            t = target // num1
            res = self.find_operations(t, rest_nums)
            if res == True:
                # print("\t", target, "can multiply", num1, t, rest_nums)
                return True

        # check addition
        t = target - num1
        res = self.find_operations(t, rest_nums)
        if res == True:
            # print("\t", target, "can add", num1, t, rest_nums)
            return True

    def find_operations2(self, target: int, current: int, nums: List[int]) -> bool:
        if current > target:
            return False
        if len(nums) == 0:
            return current == target

        num1, rest_nums = nums[0], nums[1:]

        addition = current + num1
        multiply = current * num1
        concat = int(f"{current}{num1}")

        res = (
            self.find_operations2(target, addition, rest_nums)
            or self.find_operations2(target, multiply, rest_nums)
            or self.find_operations2(target, concat, rest_nums)
        )
        return res

    def is_solvable(self, target, nums, operators):
        accumulated = [nums[0]]

        # don't include last number
        for num in nums[1:-1]:
            accumulated = [
                result
                for partial_result in accumulated
                for op in operators
                if (result := op(partial_result, num)) <= target
            ]

        # another explicit round for the last number so we can stop early
        for partial_result in accumulated:
            for op in operators:
                if op(partial_result, nums[-1]) == target:
                    return True

        return False

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            test, nums = line.split(":")
            stuff.append([int(test)] + [int(n) for n in nums.strip().split(" ")])

    return stuff


if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer1 = 3749
    # test_answer2 = 11387
    # inst = Solution(test_input)
    # ans1 = inst.calculate1()
    # ans2 = inst.calculate2()
    # print("Part1:", ans1, ans1 == test_answer1)
    # print("Part2:", ans2, ans2 == test_answer2)

    input = input_to_list("./input")
    inst = Solution(input)
    ans1 = inst.calculate1()
    ans2 = inst.calculate2()
    print("Part 1:", ans1)
    print("Part 2:", ans2)

    # p1: 5837374519342
    # p2: 492383931650959
