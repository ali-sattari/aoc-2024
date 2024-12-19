import math

class Vector:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)

    def __eq__(self, other):
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __le__(self, other):
        return self.__eq__(other) or (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)

    def __ge__(self, other):
        return self.__eq__(other) or (self.x, self.y) > (other.x, other.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __mul__(self, n):
        if isinstance(n, int):
            return Vector(self.x*n, self.y*n)
        raise NotImplementedError('Can only multiply Vector by an integer')

    def distance_to(self, other):
        return abs(self - other)

    def is_inbounds(self, w: int, h: int):
        return 0 <= self.x < w and 0 <= self.y < h
