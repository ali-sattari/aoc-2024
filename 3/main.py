import re
from typing import List

def solution1(lines: List) -> int:
    sum = 0
    muls = get_muls(lines)
    for m in muls:
        sum += do_mul(m)

    return sum

def solution2(lines: List) -> int:
    sum = 0
    insts = get_instructions(lines)
    enabled = True
    for ins in insts:
        if ins == "don't()":
            enabled = False
        elif ins == "do()":
            enabled = True
        elif ins[:3] == "mul" and enabled:
            sum += do_mul(ins)

    return sum

def get_muls(lines: List) -> List:
    regex = r"(mul\(\d{1,3}\,\d{1,3}\))"
    muls = []

    for l in lines:
        matches = re.finditer(regex, l, re.MULTILINE)
        for match in matches:
            muls.append(match.groups()[0])

    return muls

def get_instructions(lines: List) -> List:
    regex = r"(mul\(\d{1,3}\,\d{1,3}\)|don\'t\(\)|do\(\))"
    inst = []

    for l in lines:
        matches = re.finditer(regex, l, re.MULTILINE)
        for match in matches:
            inst.append(match.groups()[0])

    return inst

def do_mul(m: str) -> int:
    ds = m.strip("mul()").split(',')
    return int(ds[0]) * int(ds[1])

def input_to_list(f: str) -> List:
    list = []
    with open(file=f, mode='r') as file:
        for line in file:
            r = line.strip()
            list.append(r)

    return list

if __name__ == "__main__":
    list = input_to_list("./input")
    res1 = solution1(list)
    res2 = solution2(list)
    print(res1)
    print(res2)
