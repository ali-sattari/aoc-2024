from typing_extensions import Counter, List

def distance(col1, col2):
    dist = 0
    for r in zip(col1, col2):
        dist += abs(r[0] - r[1])

    return dist

def similarity(col1, col2):
    col2_counter = Counter(col2)
    total = 0
    for e in col1:
        total += e*col2_counter[e]

    return total

def input_to_lists(f: str) -> List:
    col1 = []
    col2 = []
    with open(file=f, mode='r') as file:
        for line in file:
            s = line.strip().split("   ")
            col1.append(int(s[0]))
            col2.append(int(s[1]))

    col1.sort()
    col2.sort()

    return [col1, col2]

if __name__ == "__main__":
    f = "./input"
    col1, col2 = input_to_lists(f)
    dist = distance(col1, col2)
    sim = similarity(col1, col2)
    print("Distance:", dist)
    print("Similarity:", sim)
