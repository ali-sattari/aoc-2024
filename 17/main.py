from typing import List, Optional, Tuple, Dict
from pprint import pprint

class Solution:
    def __init__(self, reg: dict[str, int], prog: List[int]):
        self.reg = reg
        self.prog = prog

    def calculate(self) -> str:
        pos = 0
        output = []
        reg_keys = list(self.reg.keys())

        while True:
            if pos > len(self.prog) - 1:
                break

            op = self.prog[pos]
            opnxt = self.prog[pos+1]
            assert 0 <= opnxt < 7
            combo = opnxt if opnxt < 4 else self.reg[reg_keys[opnxt-4]]

            if op == 0:  # adv
                self.reg['A'] = self.reg['A'] // 2 ** combo
            elif op == 1:  # bxl
                self.reg['B'] ^= opnxt
            elif op == 2:  # bst
                self.reg['B'] = combo % 8
            elif op == 3:  # jnz
                if self.reg['A'] != 0:
                    pos = opnxt
                    continue
            elif op == 4:  # bxl
                self.reg['B'] ^= self.reg['C']
            elif op == 5:
                output.append(str(combo % 8))
            elif op == 6:  # bdv
                self.reg['B'] = self.reg['A'] // 2 ** combo
            elif op == 7:  # cdv
                self.reg['C'] = self.reg['A'] // 2 ** combo

            pos += 2

        return ','.join(output)

def process_input(f: str):
    reg = dict()
    prog = []
    with open(file=f, mode='r') as file:
        content = file.read().split("\n\n")

    for r in content[0].split("\n"):
        n,v = r.split(':')
        n = n.split(' ')
        reg[n[1].strip()] = int(v.strip())

    p = content[1].split(':')[1].strip()
    prog = [int(x) for x in p.split(',')]

    return reg, prog

if __name__ == "__main__":
    # test_input = process_input("./test-input")
    # test_answer = '4,6,3,5,6,3,5,2,1,0'
    # # test_answer2 = 64
    # inst = Solution(*test_input)
    # out = inst.calculate()
    # print("Part1:", out, out == test_answer)
    # # print("Part2:", tiles, tiles == test_answer2)

    input = process_input("./input")
    inst = Solution(*input)
    out = inst.calculate()
    print("Part 1:", out)
    # print("Part 2:", tiles)

    # p1: 6,5,4,7,1,6,0,3,1
    # p2:
