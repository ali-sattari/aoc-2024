from typing import List
from copy import deepcopy

def solution1(l: List) -> int: # part 1
    safes = 0
    for r in l:
        d = get_dir(r)
        s, i = is_safe(r, d)
        if s:
            safes += 1

    return safes

def solution2(l: List) -> int: #part 2
    safes = 0
    for r in l:
        d = get_dir(r)
        for i in range(len(r)):
            if can_be_safe(r, i, d):
                safes += 1
                break
            else:
                print(d, r[i], r)

    return safes

def get_dir(l: List) -> str:
    if l[0] < l[-1]:
        return 'incr'
    else:
        return 'decr'

def is_safe(l: List, dir: str) -> [bool, int]:
    for i in range(1,len(l)):
        d = l[i-1] - l[i]
        if not is_dir_correct(dir, d) or not is_diff_ok(d):
            return False, i
    return True, 0

def can_be_safe(l: List, i: int, dir: str) -> bool:
    d = l[:i] + l[i+1:]
    return is_safe(d, dir)[0]

def is_dir_correct(dir: str, diff: int):
    if dir == 'incr':
        return diff < 0
    else:
        return diff > 0

def is_diff_ok(diff: int):
    return abs(diff) >= 1 and abs(diff) <= 3

def input_to_list(f: str) -> List:
    list = []
    with open(file=f, mode='r') as file:
        for line in file:
            r = line.strip().split(" ")
            r = [int(x) for x in r]
            list.append(r)

    return list

if __name__ == "__main__":
    list = input_to_list("./input")
    res = solution2(list)
    print(res)
