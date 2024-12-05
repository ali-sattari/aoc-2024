from typing import List, Tuple

def solution1(lines: List[str]) -> int:
    sum = 0
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "X":
                sum += get_adjacent_words(lines, (j, i))

    return sum

def get_adjacent_words(map: List, curr: Tuple) -> int:
    res = 0
    w, h = len(map[0]), len(map)
    for path in get_moves():
        word = "X"
        for step in path:
            x, y = curr[0] + step[0], curr[1] + step[1]
            if is_in_bounds(x, y, w, h):
                word += map[y][x]

        if  len(word) > 1 and is_valid(word): res += 1

    return res

def get_moves() -> List:
    e = [(0,1),(0,2),(0,3)]
    w = [(0,-1),(0,-2),(0,-3)]
    s = [(1,0),(2,0),(3,0)]
    n = [(-1,0),(-2,0),(-3,0)]

    se = mix_dirs(s, e)
    sw = mix_dirs(s, w)
    ne = mix_dirs(n, e)
    nw = mix_dirs(n, w)

    return [n, ne, e, se, s, sw, w, nw]

def is_valid(s: str) -> bool:
    if s == "XMAS" or s == "SAMX":
        return True
    return False

def solution2(lines: List[str]) -> int:
    sum = 0
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "A":
                sum += check_adjacent_chars(lines, (j, i))

    return sum

def check_adjacent_chars(map: List, curr: Tuple) -> int:
    res = 0
    w, h = len(map[0]), len(map)
    chars = ""
    for point in get_points():
        x, y = curr[0] + point[0], curr[1] + point[1]
        if is_in_bounds(x, y, w, h):
            chars += map[y][x]
    if len(chars) > 1 and is_valid2(chars):
        res += 1

    return res

def get_points() -> List:
    return [(-1,-1), (-1,1), (1,-1), (1,1)]

def is_valid2(s: str) -> bool:
    v = ["MMSS", "MSMS", "SMSM","SSMM"]
    return s in v

def is_in_bounds(x, y: int, w, h: int) -> bool:
    if x >= 0 and x < w and y >= 0 and y < h:
       return True
    return False

def mix_dirs(a, b: List[Tuple]) -> List[Tuple]:
    return [(c[0]+d[0],c[1]+d[1]) for c, d in zip(a, b)]


def input_to_list(f: str) -> List:
    list = []
    with open(file=f, mode='r') as file:
        for line in file:
            r = line.strip()
            list.append(r)

    return list

if __name__ == "__main__":
    list = input_to_list("./input")
    # res1 = solution1(list)
    # print(res1)
    res2 = solution2(list)
    print(res2)
