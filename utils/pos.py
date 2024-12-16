class Pos:
    def __init__(self, y:int, x:int):
        self.y = y
        self.x = x

    def __repr__(self):
        return f"Pos({self.y}, {self.x})"

    def __add__(self, other):
        return Pos(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Pos(self.y - other.y, self.x - other.x)

    def __eq__(self, other):
        return isinstance(other, Pos) and (self.y, self.x) == (other.y, other.x)

    def __hash__(self):
        return hash((self.y, self.x))

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def is_inbounds(self, h: int, w: int):
        return 0 <= self.y < h and 0 <= self.x < w

    def get_buren(self):
        for delta in (Pos(0, 1), Pos(0, -1), Pos(1, 0), Pos(-1, 0)):
            yield self + delta
