from typing import List, Tuple
from pprint import pprint

class Solution1:
    def __init__(self, equations: List):
        self.eqs = equations
        self.total = 0

    def calculate1(self) -> Tuple[int, int]:
        for eq in self.eqs:
            test = eq[0]
            nums = eq[1:]

            if self.find_operations(test, nums):
                self.total += test

        return self.total

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

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            test, nums = line.split(":")
            stuff.append([int(test)] + [int(n) for n in nums.strip().split(" ")])

    return stuff


if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer = 3749
    # inst = Solution1(test_input)
    # ans = inst.calculate1()
    # print(ans, ans == test_answer)

    input = input_to_list("./input")
    inst = Solution1(input)
    ans = inst.calculate1()
    print("Part 1:", ans)

    # 5751665302886 too low
    # 5837374516729 still too low
