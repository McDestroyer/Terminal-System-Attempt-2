from enum import Enum


class UnitNames(Enum):
    CHAR = "CHAR"
    PERCENT = "PERCENT"


class Axis:
    """A class to represent an axis on the screen.

    Properties:
        value (int):
            The value of the axis.
        char_value (int):
            The value of the axis in terms of characters.
        percent_value (int):
            The value of the axis in terms of a percentage of the given screen size.
        screen_size (int):
            The size of the screen.
    """

    def __init__(self, value: int = 0, unit: UnitNames = UnitNames.CHAR, axis_size: int = 1) -> None:
        """Initialize the Axis object.

        Args:
            value (int, optional):
                The value of the axis.
                Defaults to 0.
            unit (UnitNames, optional):
                The unit of the axis.
                Defaults to UnitNames.CHAR.
            axis_size (int, optional):
                The size of the screen.
                Defaults to 1.
        """
        self._unit: UnitNames = unit
        self._axis_size: int = axis_size

        self._value: int = value
        self._char_value: int = self._get_char_value()
        self._percent_value: int = self._get_percent_value()

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        self._value = new_value
        self._char_value = self.char_value
        self._percent_value = self.percent_value

    @property
    def char_value(self) -> int:
        return self._char_value

    @char_value.setter
    def char_value(self, new_value: int) -> None:
        self._char_value = new_value

        self._value = self._get_value(UnitNames.CHAR)
        self._percent_value = self._get_percent_value()

    @property
    def percent_value(self) -> int:
        return self._percent_value

    @percent_value.setter
    def percent_value(self, new_value: int) -> None:
        self._percent_value = new_value

        self._value = self._get_value(UnitNames.PERCENT)
        self._char_value = self._get_char_value()

    @property
    def screen_size(self) -> int:
        return self._axis_size

    @screen_size.setter
    def screen_size(self, new_screen_size: int) -> None:
        self._axis_size = new_screen_size

        if self._unit == UnitNames.CHAR:
            self._percent_value = self._get_percent_value()
        else:
            self._char_value = self._get_char_value()
            self._value = self._get_value(self._unit)

    def _get_value(self, unit: UnitNames) -> int:
        """Return the value of the axis in the specified unit.
        
        Args:
            unit (UnitNames): The unit to return the value in.
            
        Returns:
            int: The value of the axis in the specified unit.
        """
        if self._unit == unit:
            return self._value
        elif unit == UnitNames.CHAR:
            return self._get_char_value()
        elif unit == UnitNames.PERCENT:
            return self._get_percent_value()
        else:
            raise ValueError(f"Invalid unit: {unit}")

    def _get_char_value(self) -> int:
        """Return the value of the axis in terms of characters.

        Returns:
            int: The value of the axis in terms of characters.
        """
        if self._unit == UnitNames.CHAR:
            return self._value
        elif self._unit == UnitNames.PERCENT:
            return self._value * self._axis_size
        else:
            raise ValueError(f"Invalid unit: {self._unit}")

    def _get_percent_value(self) -> int:
        """Return the value of the axis in terms of a percentage of the given screen size.

        Returns:
            int: The value of the axis in terms of percentage of the given screen size.
        """
        if self._unit == UnitNames.PERCENT:
            return self._value
        elif self._unit == UnitNames.CHAR:
            return self._value / self._axis_size if self._axis_size != 0 else 0
        else:
            raise ValueError(f"Invalid unit: {self._unit}")

    def __str__(self) -> str:
        return f"Axis({self._unit}, {self._axis_size})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: 'Axis') -> bool:
        return self._unit == other._unit and self._axis_size == other._axis_size and self._value == other._value

    def __ne__(self, other: 'Axis') -> bool:
        return not self == other

    def __lt__(self, other: 'Axis') -> bool:
        return self._char_value < other._char_value

    def __le__(self, other: 'Axis') -> bool:
        return self._char_value <= other._char_value

    def __gt__(self, other: 'Axis') -> bool:
        return self._char_value > other._char_value

    def __ge__(self, other: 'Axis') -> bool:
        return self._char_value >= other._char_value

    def __add__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(self._value + other._value, self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(self._value + other._char_value, self._unit, self._axis_size)
        else:
            return Axis(self._value + other._percent_value, self._unit, self._axis_size)

    def __sub__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(self._value - other._value, self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(self._value - other._char_value, self._unit, self._axis_size)
        else:
            return Axis(self._value - other._percent_value, self._unit, self._axis_size)

    def __mul__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(self._value * other._value, self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(self._value * other._char_value, self._unit, self._axis_size)
        else:
            return Axis(self._value * other._percent_value, self._unit, self._axis_size)

    def __truediv__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(int(self._value / other._value), self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(int(self._value / other._char_value), self._unit, self._axis_size)
        else:
            return Axis(int(self._value / other._percent_value), self._unit, self._axis_size)

    def __floordiv__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(self._value // other._value, self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(self._value // other._char_value, self._unit, self._axis_size)
        else:
            return Axis(self._value // other._percent_value, self._unit, self._axis_size)

    def __mod__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(self._value % other._value, self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(self._value % other._char_value, self._unit, self._axis_size)
        else:
            return Axis(self._value % other._percent_value, self._unit, self._axis_size)

    def __pow__(self, other: 'Axis') -> 'Axis':
        if self._unit == other._unit:
            return Axis(self._value ** other._value, self._unit, self._axis_size)
        elif self._unit == UnitNames.CHAR:
            return Axis(self._value ** other._char_value, self._unit, self._axis_size)
        else:
            return Axis(self._value ** other._percent_value, self._unit, self._axis_size)

    def __abs__(self) -> 'Axis':
        return Axis(abs(self._value), self._unit, self._axis_size)

    def __neg__(self) -> 'Axis':
        return Axis(-self._value, self._unit, self._axis_size)

    def __pos__(self) -> 'Axis':
        return Axis(+self._value, self._unit, self._axis_size)

    def __round__(self, n: int = 0) -> 'Axis':
        return Axis(round(self._value, n), self._unit, self._axis_size)

    def __floor__(self) -> 'Axis':
        return Axis(self._value // 1, self._unit, self._axis_size)

    def __ceil__(self) -> 'Axis':
        return Axis(self._value // 1 + 1, self._unit, self._axis_size)

    def __trunc__(self) -> 'Axis':
        return Axis(self._value // 1, self._unit, self._axis_size)

    def __int__(self) -> int:
        return int(self._value)
