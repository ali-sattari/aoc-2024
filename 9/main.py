from typing import List, Tuple
from pprint import pprint
from math import floor
from itertools import repeat

# input is alternating file blocks and whitespace (one digit per each)
# expand input into array of files and following whitespace
# expand that into string representaiton by placing file ids repeated by number of blocks followed by . repeated for whitespace
# move blocks from enf to front inside whitespaces
# calculate checksum by multiplying position with id, and summing all of those

class Solution:
    def __init__(self, disk: List):
        self.disk = disk
        self.block_count = 0
        self.files = []
        self.disk_ids = []
        self.disk_tuples = []
        self.defragged = []
        self.defragged_files = []

    def calculate1(self) -> int:
        self.mapDisktoList()
        self.convertToIds()
        self.defragged = self.disk_ids.copy()
        self.defragDisk()
        # pprint(''.join(self.defragged))

        return self.checkSum(self.defragged)

    def calculate2(self) -> int:
        self.mapDisktoList()
        self.defragged_files = self.disk_ids.copy()
        self.defragDiskByFile()
        # pprint(''.join(self.defragged_files))

        return self.checkSum(self.defragged_files)

    def mapDisktoList(self):
        if len(self.files) > 0:
            return
        for i in range(0, len(self.disk), 2):
            blocks = self.disk[i]
            ws = self.disk[i+1] if i < len(self.disk)-1 else 0
            self.files.append((int(blocks), int(ws)))

    def convertToIds(self):
        for i, (b, s) in enumerate(self.files):
            for n in range(b):
                self.disk_ids.append(str(i))
            for m in range(s):
                self.disk_ids.append('.')

    def haveSpace(self) -> bool:
        t = ''.join(self.defragged).removesuffix('.')
        return t.count('.') > 0

    def defragDisk(self):
        l = 0
        r = len(self.defragged)-1
        while self.haveSpace() and l < r:
            if self.defragged[l] != '.':
                l += 1
                continue
            if self.defragged[r] == '.':
                r -= 1
                continue

            self.defragged[l] = self.defragged[r]
            self.defragged[r] = '.'
            l += 1
            r -= 1

    def defragDiskByFile(self):
        for i in range(len(self.files)-1, -1, -1):
            # print(i, self.defragged_files)
            idx = self.defragged_files.index(str(i))
            count = self.defragged_files.count(str(i))

            # find gap left of idx if exists
            gap = None
            for j in range(idx - count + 1):
                if self.defragged_files[j:j + count] == list(repeat('.', count)):
                    gap = j
                    break

            # if gap found, swap file into gap in memory
            if gap != None:
                self.defragged_files[idx:idx + count], self.defragged_files[j:j + count] = self.defragged_files[j:j + count], self.defragged_files[idx:idx + count]

    def checkSum(self, disk: list) -> int:
        sum = 0
        for i, id in enumerate(disk):
            if id == '.':
                continue
            sum += i * int(id)

        return sum

def input_to_list(f: str) -> List:
    stuff = []
    with open(file=f, mode='r') as file:
        for line in file:
            stuff.append(list(line.strip()))

    return stuff[0]


if __name__ == "__main__":
    # test_input = input_to_list("./test-input")
    # test_answer1 = 1928
    # test_answer2 = 2858
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

    # p1:6448989155953
    # p2:6476642796832
