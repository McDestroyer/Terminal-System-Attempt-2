import copy

import system.objects.helper_objects.coordinate_objects.axis as axis
from system.objects.helper_objects.coordinate_objects.point import Point


class Coordinate:
    """A coordinate object that contains two axes.

    Properties:
        screen_size (tuple[int, int]): The screen size.
        x_axis (axis.Axis): The x-axis.
        y_axis (axis.Axis): The y-axis.
        x_char (int): The character value of the x-axis.
        y_char (int): The character value of the y-axis.
        x_percent (float): The percentage value of the x-axis.
        y_percent (float): The percentage value of the y-axis.
    """

    def __init__(self, x_axis: axis.Axis = axis.Axis(), y_axis: axis.Axis = axis.Axis()) -> None:
        """Initialize the Coordinate object.

        Args:
            x_axis (axis.Axis, optional):
                The x-axis.
                Defaults to axis.Axis().
            y_axis (axis.Axis, optional):
                The y-axis.
                Defaults to axis.Axis().
        """
        self._x_axis, self._y_axis = x_axis, y_axis

        self._screen_size = Point(self._x_axis.screen_size, self._y_axis.screen_size)

    @property
    def screen_size(self) -> Point:
        """Return the screen size.

        Returns:
            Point:
                The screen size.
        """
        return self._screen_size

    @screen_size.setter
    def screen_size(self, new_screen_size: Point) -> None:
        """Set the screen size.

        Args:
            new_screen_size (Point):
                The new screen size.
        """
        self._screen_size = new_screen_size

        self._x_axis.screen_size = new_screen_size.x
        self._y_axis.screen_size = new_screen_size.y

    @property
    def x_axis(self) -> axis.Axis:
        """Return the x-axis.

        Returns:
            axis.Axis:
                The x-axis.
        """
        return self._x_axis

    @property
    def y_axis(self) -> axis.Axis:
        """Return the y-axis.

        Returns:
            axis.Axis:
                The y-axis.
        """
        return self._y_axis

    @property
    def x_char(self) -> int:
        """Return the character value of the x-axis.

        Returns:
            int:
                The character value of the x-axis.
        """
        return int(self._x_axis.char_value)

    @property
    def y_char(self) -> int:
        """Return the character value of the y-axis.

        Returns:
            int:
                The character value of the y-axis.
        """
        return int(self._y_axis.char_value)

    @property
    def x_percent(self) -> float:
        """Return the percentage value of the x-axis.

        Returns:
            float:
                The percentage value of the x-axis.
        """
        return self._x_axis.percent_value

    @property
    def y_percent(self) -> float:
        """Return the percentage value of the y-axis.

        Returns:
            float:
                The percentage value of the y-axis.
        """
        return self._y_axis.percent_value

    @x_axis.setter
    def x_axis(self, new_x_axis: axis.Axis) -> None:
        """Set the x-axis.

        Args:
            new_x_axis (axis.Axis):
                The new x-axis.
        """
        self._x_axis = new_x_axis

    @y_axis.setter
    def y_axis(self, new_y_axis: axis.Axis) -> None:
        """Set the y-axis.

        Args:
            new_y_axis (axis.Axis):
                The new y-axis.
        """
        self._y_axis = new_y_axis

    @x_char.setter
    def x_char(self, new_x_char: int) -> None:
        """Set the character value of the x-axis.

        Args:
            new_x_char (int):
                The new character value of the x-axis.
        """
        self._x_axis.char_value = new_x_char

    @y_char.setter
    def y_char(self, new_y_char: int) -> None:
        """Set the character value of the y-axis.

        Args:
            new_y_char (int):
                The new character value of the y-axis.
        """
        self._y_axis.char_value = new_y_char

    @x_percent.setter
    def x_percent(self, new_x_percent: float) -> None:
        """Set the percentage value of the x-axis.

        Args:
            new_x_percent (float):
                The new percentage value of the x-axis.
        """
        self._x_axis.percent_value = new_x_percent

    @y_percent.setter
    def y_percent(self, new_y_percent: float) -> None:
        """Set the percentage value of the y-axis.

        Args:
            new_y_percent (float):
                The new percentage value of the y-axis.
        """
        self._y_axis.percent_value = new_y_percent

    def __str__(self) -> str:
        """Return the string representation of the coordinate.

        Returns:
            str:
                The string representation of the coordinate.
        """
        return f"({self._x_axis}, {self._y_axis})"

    def __repr__(self) -> str:
        """Return the string representation of the coordinate.

        Returns:
            str:
                The string representation of the coordinate.
        """
        return f"Coordinate({self._x_axis}, {self._y_axis})"

    def __eq__(self, other: object) -> bool:
        """Return whether the coordinate is equal to another object.

        Args:
            other (object):
                The object to compare to.

        Returns:
            bool:
                True if the coordinate is equal to the other object, False otherwise.
        """
        if not isinstance(other, Coordinate):
            return False

        return self._x_axis == other.x_axis and self._y_axis == other.y_axis

    def __ne__(self, other: object) -> bool:
        """Return whether the coordinate is not equal to another object.

        Args:
            other (object):
                The object to compare to.

        Returns:
            bool:
                True if the coordinate is not equal to the other object, False otherwise.
        """
        return not self.__eq__(other)

    def __add__(self, other: object) -> 'Coordinate':
        """Add the coordinate to another object.

        Args:
            other (object):
                The object to add to the coordinate.

        Returns:
            Coordinate:
                The sum of the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for +: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis + other.x_axis, self._y_axis + other.y_axis)

    def __sub__(self, other: object) -> 'Coordinate':
        """Subtract the coordinate from another object.

        Args:
            other (object):
                The object to subtract from the coordinate.

        Returns:
            Coordinate:
                The difference between the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for -: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis - other.x_axis, self._y_axis - other.y_axis)

    def __mul__(self, other: object) -> 'Coordinate':
        """Multiply the coordinate by another object.

        Args:
            other (object):
                The object to multiply the coordinate by.

        Returns:
            Coordinate:
                The product of the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for *: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis * other.x_axis, self._y_axis * other.y_axis)

    def __truediv__(self, other: object) -> 'Coordinate':
        """Divide the coordinate by another object.

        Args:
            other (object):
                The object to divide the coordinate by.

        Returns:
            Coordinate:
                The quotient of the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for /: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis / other.x_axis, self._y_axis / other.y_axis)

    def __floordiv__(self, other: object) -> 'Coordinate':
        """Floor divide the coordinate by another object.

        Args:
            other (object):
                The object to floor divide the coordinate by.

        Returns:
            Coordinate:
                The floor quotient of the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for //: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis // other.x_axis, self._y_axis // other.y_axis)

    def __mod__(self, other: object) -> 'Coordinate':
        """Mod the coordinate by another object.

        Args:
            other (object):
                The object to mod the coordinate by.

        Returns:
            Coordinate:
                The modulus of the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for %: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis % other.x_axis, self._y_axis % other.y_axis)

    def __pow__(self, other: object) -> 'Coordinate':
        """Raise the coordinate to the power of another object.

        Args:
            other (object):
                The object to raise the coordinate to the power of.

        Returns:
            Coordinate:
                The power of the coordinate and the other object.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(f"unsupported operand type(s) for **: 'Coordinate' and '{type(other)}'")

        return Coordinate(self._x_axis ** other.x_axis, self._y_axis ** other.y_axis)

    def __getitem__(self, item: int) -> axis.Axis:
        """Get the axis at the index.

        Args:
            item (int):
                The index of the axis.

        Returns:
            axis.Axis:
                The axis at the index.
        """
        return [self._x_axis, self._y_axis][item]

    def __setitem__(self, key: int, value: axis.Axis) -> None:
        """Set the axis at the index.

        Args:
            key (int):
                The index of the axis.
            value (axis.Axis):
                The axis to set.
        """
        if key == 0:
            self._x_axis = value
        elif key == 1:
            self._y_axis = value
        else:
            raise IndexError(f"Index out of range: {key}")

    def __iter__(self):
        """Return the iterator of the coordinate.

        Returns:
            iter:
                The iterator of the coordinate.
        """
        return iter([self._x_axis, self._y_axis])

    def __len__(self) -> int:
        """Return the length of the coordinate.

        Returns:
            int:
                The length of the coordinate.
        """
        return 2

    def __contains__(self, item: axis.Axis) -> bool:
        """Return whether the coordinate contains the axis.

        Args:
            item (axis.Axis):
                The axis to check for.

        Returns:
            bool:
                True if the coordinate contains the axis, False otherwise.
        """
        return item in [self._x_axis, self._y_axis]

    def __hash__(self) -> int:
        """Return the hash of the coordinate.

        Returns:
            int:
                The hash of the coordinate.
        """
        return hash((self._x_axis, self._y_axis))

    def __copy__(self) -> 'Coordinate':
        """Return a shallow copy of the coordinate.

        Returns:
            Coordinate:
                A shallow copy of the coordinate.
        """
        return Coordinate(self._x_axis, self._y_axis)

    def __deepcopy__(self, memo_dict) -> 'Coordinate':
        """Return a deep copy of the coordinate.

        Args:
            memo_dict:
                The memo dictionary.

        Returns:
            Coordinate:
                A deep copy of the coordinate.
        """
        return Coordinate(copy.deepcopy(self._x_axis), copy.deepcopy(self._y_axis))

    def __bool__(self) -> bool:
        """Return whether the coordinate is true.

        Returns:
            bool:
                True if the coordinate is true, False otherwise.
        """
        return bool(self._x_axis) or bool(self._y_axis)

    def __neg__(self) -> 'Coordinate':
        """Return the negation of the coordinate.

        Returns:
            Coordinate:
                The negation of the coordinate.
        """
        return Coordinate(-self._x_axis, -self._y_axis)

    def __pos__(self) -> 'Coordinate':
        """Return the positive of the coordinate.

        Returns:
            Coordinate:
                The positive of the coordinate.
        """
        return Coordinate(+self._x_axis, +self._y_axis)

    def __abs__(self) -> 'Coordinate':
        """Return the absolute value of the coordinate.

        Returns:
            Coordinate:
                The absolute value of the coordinate.
        """
        return Coordinate(abs(self._x_axis), abs(self._y_axis))

    def __round__(self, n: int = 0) -> 'Coordinate':
        """Return the rounded value of the coordinate.

        Args:
            n (int, optional):
                The number of decimal places to round to.
                Defaults to 0.

        Returns:
            Coordinate:
                The rounded value of the coordinate.
        """
        return Coordinate(round(self._x_axis, n), round(self._y_axis, n))
