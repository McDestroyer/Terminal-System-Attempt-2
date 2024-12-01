import copy


class Point:

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    @property
    def amplitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def as_tuple(self):
        return self.x, self.y

    @property
    def as_list(self):
        return [self.x, self.y]

    @property
    def as_dict(self):
        return {"x": self.x, "y": self.y}

    @property
    def as_str(self):
        return f"({self.x}, {self.y})"

    @as_tuple.setter
    def as_tuple(self, new_tuple):
        self.x, self.y = new_tuple

    @as_list.setter
    def as_list(self, new_list):
        self.x, self.y = new_list

    @as_dict.setter
    def as_dict(self, new_dict):
        self.x = new_dict["x"]
        self.y = new_dict["y"]

    @as_str.setter
    def as_str(self, new_str):
        new_str = new_str.replace("(", "").replace(")", "")
        self.x, self.y = map(float, new_str.split(","))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False

        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for +: 'Point' and '{type(other)}'")

        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for -: 'Point' and '{type(other)}'")

        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for *: 'Point' and '{type(other)}'")

        return Point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for /: 'Point' and '{type(other)}'")

        return Point(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for //: 'Point' and '{type(other)}'")

        return Point(self.x // other.x, self.y // other.y)

    def __mod__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for %: 'Point' and '{type(other)}'")

        return Point(self.x % other.x, self.y % other.y)

    def __pow__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"unsupported operand type(s) for **: 'Point' and '{type(other)}'")

        return Point(self.x ** other.x, self.y ** other.y)

    def __getitem__(self, item):
        return [self.x, self.y][item]

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError(f"Index out of range: {key}")

    def __iter__(self):
        return iter([self.x, self.y])

    def __len__(self):
        return 2

    def __contains__(self, item):
        return item in [self.x, self.y]

    def __hash__(self):
        return hash((self.x, self.y))

    def __copy__(self):
        return Point(self.x, self.y)

    def __deepcopy__(self, memo_dict):
        return Point(copy.deepcopy(self.x), copy.deepcopy(self.y))

    def __bool__(self):
        return bool(self.x) or bool(self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __pos__(self):
        return Point(+self.x, +self.y)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __round__(self, n=0):
        return Point(round(self.x, n), round(self.y, n))

    def __floor__(self):
        return Point(self.x // 1, self.y // 1)

    def __ceil__(self):
        return Point(self.x // 1 + 1, self.y // 1 + 1)

    def __trunc__(self):
        return Point(self.x // 1, self.y // 1)

    def __lt__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"'<' not supported between instances of 'Point' and '{type(other)}'")

        return self.x < other.x and self.y < other.y

    def __le__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"'<=' not supported between instances of 'Point' and '{type(other)}'")

        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"'>' not supported between instances of 'Point' and '{type(other)}'")

        return self.x > other.x and self.y > other.y

    def __ge__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f"'>=' not supported between instances of 'Point' and '{type(other)}'")

        return self.x >= other.x and self.y >= other.y