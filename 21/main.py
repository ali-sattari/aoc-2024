from typing import List, Optional, Tuple, Dict, Literal
from pprint import pprint
import functools

class Solution:
    def __init__(self, codes: List):
        self.codes = codes
        self.path = []
        self.initial_key = 'A'
        self.press = 'A'
        self.num_moves = {
            '0,0': '', '0,1': '^<', '0,2': '^', '0,3': '^>', '0,4': '^^<', '0,5': '^^', '0,6': '^^>', '0,7': '^^^<', '0,8': '^^^', '0,9': '^^^>', '0,A': '>',
            '1,0': '>v', '1,1': '', '1,2': '>', '1,3': '>>', '1,4': '^', '1,5': '^>', '1,6': '^>>', '1,7': '^^', '1,8': '^^>', '1,9': '^^>>', '1,A': '>>v',
            '2,0': 'v', '2,1': '<', '2,2': '', '2,3': '>', '2,4': '<^', '2,5': '^', '2,6': '^>', '2,7': '<^^', '2,8': '^^', '2,9': '^^>', '2,A': 'v>',
            '3,0': '<v', '3,1': '<<', '3,2': '<', '3,3': '', '3,4': '<<^', '3,5': '<^', '3,6': '^', '3,7': '<<^^', '3,8': '<^^', '3,9': '^^', '3,A': 'v',
            '4,0': '>vv', '4,1': 'v', '4,2': 'v>', '4,3': 'v>>', '4,4': '', '4,5': '>', '4,6': '>>', '4,7': '^', '4,8': '^>', '4,A': '>>vv',
            '5,0': 'vv', '5,1': '<v', '5,2': 'v', '5,3': 'v>', '5,4': '<', '5,5': '', '5,6': '>', '5,7': '<^', '5,8': '^', '5,9': '^>', '5,A': 'vv>',
            '6,0': '<vv', '6,1': '<<v', '6,2': '<v', '6,3': 'v', '6,4': '<<', '6,5': '<', '6,6': '', '6,7': '<<^', '6,8': '<^', '6,9': '^', '6,A': 'vv',
            '7,0': '>vvv', '7,1': 'vv', '7,2': 'vv>', '7,3': 'vv>>', '7,4': 'v', '7,5': 'v>', '7,6': 'v>>', '7,7': '', '7,8': '>', '7,9': '>>', '7,A': '>>vvv',
            '8,0': 'vvv', '8,1': '<vv', '8,2': 'vv', '8,3': 'vv>', '8,4': '<v', '8,5': 'v', '8,6': 'v>', '8,7': '<', '8,8': '', '8,9': '>', '8,A': 'vvv>',
            '9,0': '<vvv', '9,1': '<<vv', '9,2': '<vv', '9,3': 'vv', '9,4': '<<v', '9,5': '<v', '9,6': 'v', '9,7': '<<', '9,8': '<', '9,9': '', '9,A': 'vvv',
            'A,0': '<', 'A,1': '^<<', 'A,2': '<^', 'A,3': '^', 'A,4': '^^<<', 'A,5': '<^^', 'A,6': '^^', 'A,7': '^^^<<', 'A,8': '<^^^', 'A,9': '^^^', 'A,A': '',
        }
        self.dir_moves = {
            '^,A': '>', '^,<': 'v<', '^,v': 'v', '^,>': 'v>', '^,^': '',
            '>,^': '<^', '>,A': '^', '>,<': '<<', '>,v': '<', '>,>': '',
            'v,^': '^', 'v,A': '^>', 'v,<': '<', 'v,>': '>', 'v,v': '',
            '<,^': '>^', '<,A': '>>^', '<,v': '>', '<,>': '>>', '<,<': '',
            'A,^': '<', 'A,<': 'v<<', 'A,v': '<v', 'A,>': 'v', 'A,A': '',
        }

    def calculate(self, robots=2) -> int:
        complexity = 0

        for code in self.codes:
            num_seq = self.get_sequence(code, 'num')
            print(f"code {code}")
            dir_seq = self.get_sequence(num_seq, 'dir', depth=robots)

            comp = int(code.strip('A')) * len(dir_seq)
            complexity += comp
            print(f"dial {code} with {len(dir_seq)} steps and complexity of {comp}")

        return complexity

    # @functools.cache
    def get_sequence(self, code:str, pad:Literal['num', 'dir'], depth=1, mem={}) -> str:
        if depth == 0:
            return code

        if code in mem:
                return mem[code]

        path = ''
        start = self.initial_key
        print(f"depth {depth}...", end='\r')
        for c in code:
            pos = f"{start},{c}"
            path += self.get_move(pos, pad)
            start = c

        mem[code] = path
        return self.get_sequence(path, pad, depth-1, mem)

    # @functools.cache
    def get_move(self, pos: str, pad:Literal['num', 'dir']) -> str:
        moves = getattr(self, f"{pad}_moves")
        return moves[pos] + self.press

def process_input(f: str):
    input = []
    with open(file=f, mode='r') as file:
        for line in file:
            input.append(line.strip())
    return input

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer1 = 126384
    # inst = Solution(test_input)
    # answ1 = inst.calculate()
    # print("Part1:", answ1 ,answ1 == test_answer1)
    # answ2 = inst.calculate(25)
    # print("Part2:", answ2)

    input = process_input("./input")
    inst = Solution(input)
    # answ1 = inst.calculate()
    # print("Part 1:", answ1)
    answ2 = inst.calculate(25)
    print("Part 2:", answ2)

    # p1: 184716
    # p2:
