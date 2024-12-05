from typing import List, Tuple, Dict
from collections import defaultdict

class Solution1:
    def __init__(self, before: Dict, after: Dict, updates: List):
        self.before = before
        self.after = after
        self.updates = updates
        self.count = 0
        self.sum = 0

    def calculate(self) -> int:
        for u in self.updates:
            if self.is_valid(u):
                self.count += 1
                self.sum += self.get_middle(u)

        return self.sum

    def is_valid(self, update: List) -> bool:
        for i, n in enumerate(update):
            if bool(set(update[:i]) - self.before[n]) or bool(set(update[i+1:]) - self.after[n]):
                return False

        return True

    def get_middle(self, update) -> int:
        l = len(update)
        return update[l//2]

class Solution2:
    def __init__(self, before: Dict, after: Dict, updates: List):
        self.before = before
        self.after = after
        self.updates = updates
        self.count = 0
        self.sum = 0

    def calculate(self) -> int:
        for u in self.updates:
            iv = self.get_invalid(u)
            # print(u, iv)
            if len(iv) > 0:
                self.count += 1
                nu = self.sort_update(u)
                self.sum += self.get_middle(nu)

        return self.sum

    def sort_update(self, pages):
        for idx, page in enumerate(pages[:-1]):
            errors = self.after[page].intersection(pages[idx + 1 :])
            if errors:
                pages[idx:] = list(errors) + [n for n in pages[idx:] if n not in errors]
                return self.sort_update(pages)

        return pages


    def get_invalid(self, update: List) -> List:
        iv = []
        for i, n in enumerate(update):
            if bool(set(update[:i]) - self.before[n]) or bool(set(update[i+1:]) - self.after[n]):
                iv.append(i)

        return iv

    def get_middle(self, update) -> int:
        l = len(update)
        return update[l//2]


def make_rule_maps(rules: List) -> List[Dict]:
    map, pam = defaultdict(set), defaultdict(set)
    for k, v in rules:
        map[k].add(v)
        pam[v].add(k)

    return [pam, map]

def input_to_list(f: str) -> List:
    list = []
    with open(file=f, mode='r') as file:
        for line in file:
            r = line.strip().split('|')
            if len(r) == 1: r = r[0].split(',')
            r = [int(x) for x in r]
            list.append(r)

    return list

if __name__ == "__main__":
    #testing with sample inputs
    # test_rules = input_to_list("./sample-rules")
    # test_updates = input_to_list("./sample-updates")
    # test_results = [True, True, True, False, False, False]
    # sorted_updates = [
    #     [97,75,47,61,53],
    #     [61,29,13],
    #     [97,75,47,29,13]
    # ]
    # test_answer = 123

    # res = Solution2(*make_rule_maps(test_rules), test_updates)
    # ans = res.calculate()
    # print(ans == test_answer, ans)

    rules = input_to_list("./input-rules")
    updates = input_to_list("./input-updates")

    res1 = Solution1(*make_rule_maps(rules), updates)
    print("Part1:", res1.calculate())

    res2 = Solution2(*make_rule_maps(rules), updates)
    print("Part2:", res2.calculate())
