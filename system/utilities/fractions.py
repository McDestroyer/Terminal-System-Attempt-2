import copy

from system.utilities.personal_functions import rounder


class Fraction:

    def __init__(self, numerator: int | 'Fraction' = 1, denominator: int | 'Fraction' = 1) -> None:
        """Create a fraction.

        Args:
            numerator (int | Fraction, optional):
                The numerator of the fraction.
                Defaults to 1.
            denominator (int | Fraction, optional):
                The denominator of the fraction.
                Defaults to 1.
        """
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        if isinstance(numerator, Fraction):
            self._numerator: int | 'Fraction' = numerator._numerator
            self._denominator: int | 'Fraction' = numerator._denominator
        else:
            self._numerator: int | 'Fraction' = numerator
            self._denominator: int | 'Fraction' = denominator

        self._simplify()

    def from_int(self, value: int) -> None:
        """Convert an integer to a fraction.

        Args:
            value (int):
                The integer to convert.
        """
        self._numerator = value
        self._denominator = 1

    def invert(self) -> None:
        """Invert the fraction."""
        self._numerator, self._denominator = self._denominator, self._numerator

    def from_float(self, value: float) -> None:
        """Convert a float to a fraction.

        Args:
            value (float):
                The float to convert.
        """
        self._numerator, self._denominator = value.as_integer_ratio()
        self._simplify()

    def from_string(self, value: str) -> None:
        """Convert a string to a fraction. The string should be in the format 'numerator/denominator', and the
        numerator and denominator should be integers.

        Args:
            value (str):
                The string to convert.
        """
        self._numerator, self._denominator = map(int, value.split('/'))
        self._simplify()

    def _simplify(self) -> None:
        """Simplify the fraction."""
        if self._denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        gcd = self._gcd(self._numerator, self._denominator)
        self._numerator //= gcd
        self._denominator //= gcd

        if self._denominator < 0:
            self._numerator = -self._numerator
            self._denominator = -self._denominator

    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    @property
    def reciprocal(self) -> 'Fraction':
        return Fraction(self._denominator, self._numerator)

    @property
    def is_integer(self) -> bool:
        return self._denominator == 1

    @numerator.setter
    def numerator(self, value: int | 'Fraction') -> None:
        self._numerator = value
        self._simplify()

    @denominator.setter
    def denominator(self, value: int | 'Fraction') -> None:
        self._denominator = value
        self._simplify()

    @classmethod
    def _gcd(cls, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def __copy__(self) -> 'Fraction':
        return Fraction(copy.copy(self._numerator), copy.copy(self._denominator))

    def __deepcopy__(self, memodict=None) -> 'Fraction':
        if memodict is None:
            memo = {}
        else:
            memo = memodict
        return Fraction(copy.deepcopy(self._numerator, memo), copy.deepcopy(self._denominator, memo))

    def __add__(self, other: 'Fraction') -> 'Fraction':
        new_denominator = self._denominator * other._denominator
        new_numerator = self._numerator * other._denominator + other._numerator * self._denominator

        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other: 'Fraction') -> 'Fraction':
        new_denominator = self._denominator * other._denominator
        new_numerator = self._numerator * other._denominator - other._numerator * self._denominator

        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other: 'Fraction') -> 'Fraction':
        new_numerator = self._numerator * other._numerator
        new_denominator = self._denominator * other._denominator

        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other: 'Fraction') -> 'Fraction':
        new_numerator = self._numerator * other._denominator
        new_denominator = self._denominator * other._numerator

        return Fraction(new_numerator, new_denominator)

    def __str__(self) -> str:
        return f'{self._numerator}/{self._denominator}'

    def __repr__(self) -> str:
        return f'Fraction({self._numerator}, {self._denominator})'

    def __eq__(self, other: 'Fraction') -> bool:
        return self._numerator == other._numerator and self._denominator == other._denominator

    def __ne__(self, other: 'Fraction') -> bool:
        return not self == other

    def __lt__(self, other: 'Fraction') -> bool:
        return self._numerator * other._denominator < other._numerator * self._denominator

    def __le__(self, other: 'Fraction') -> bool:
        return self._numerator * other._denominator <= other._numerator * self._denominator

    def __gt__(self, other: 'Fraction') -> bool:
        return self._numerator * other._denominator > other._numerator * self._denominator

    def __ge__(self, other: 'Fraction') -> bool:
        return self._numerator * other._denominator >= other._numerator * self._denominator

    def __float__(self) -> float:
        return float(self._numerator) / float(self._denominator)

    def __int__(self) -> int:
        return int(rounder(self._numerator / self._denominator))

    def __abs__(self) -> 'Fraction':
        return Fraction(abs(self._numerator), abs(self._denominator))

    def __neg__(self) -> 'Fraction':
        return Fraction(-self._numerator, self._denominator)

    def __pos__(self) -> 'Fraction':
        return Fraction(self._numerator, self._denominator)

    def __invert__(self) -> 'Fraction':
        return Fraction(self._denominator, self._numerator)

    def __round__(self, n: int = 0) -> 'Fraction':
        return Fraction(int(rounder(self._numerator / self._denominator, n)))

    def __ceil__(self) -> 'Fraction':
        return Fraction(self._numerator // self._denominator + 1)

    def __floor__(self) -> 'Fraction':
        return Fraction(self._numerator // self._denominator)

    def __trunc__(self) -> 'Fraction':
        return Fraction(self._numerator // self._denominator)

    def __pow__(self, power: int) -> 'Fraction':
        if power < 0:
            return Fraction(self._denominator ** -power, self._numerator ** -power)

        return Fraction(self._numerator ** power, self._denominator ** power)

    def __radd__(self, other: int) -> 'Fraction':
        return Fraction(self._numerator + other * self._denominator, self._denominator)

    def __rsub__(self, other: int) -> 'Fraction':
        return Fraction(self._numerator - other * self._denominator, self._denominator)

    def __rmul__(self, other: int) -> 'Fraction':
        return Fraction(self._numerator * other, self._denominator)

    def __rtruediv__(self, other: int) -> 'Fraction':
        return Fraction(self._denominator * other, self._numerator)

    def __rfloordiv__(self, other: int) -> 'Fraction':
        return Fraction(self._denominator // self._numerator * other)

    def __rmod__(self, other: int) -> 'Fraction':
        return Fraction(self._denominator % self._numerator * other)

    def __rdivmod__(self, other: int) -> tuple['Fraction', 'Fraction']:
        return (
            Fraction(self._denominator // self._numerator * other),
            Fraction(self._denominator % self._numerator * other)
        )

    def __rpow__(self, base: int) -> 'Fraction':

        return base ** (self._numerator / self._denominator)

    def __iadd__(self, other: 'Fraction') -> 'Fraction':
        self._numerator = self._numerator * other._denominator + other._numerator * self._denominator
        self._denominator = self._denominator * other._denominator
        return self

    def __isub__(self, other: 'Fraction') -> 'Fraction':
        self._numerator = self._numerator * other._denominator - other._numerator * self._denominator
        self._denominator = self._denominator * other._denominator
        return self

    def __imul__(self, other: 'Fraction') -> 'Fraction':
        self._numerator = self._numerator * other._numerator
        self._denominator = self._denominator * other._denominator
        return self

    def __itruediv__(self, other: 'Fraction') -> 'Fraction':
        self._numerator = self._numerator * other._denominator
        self._denominator = self._denominator * other._numerator
        return self

    def __ifloordiv__(self, other: 'Fraction') -> 'Fraction':
        self._numerator = self._numerator // other._numerator
        self._denominator = self._denominator // other._denominator
        return self

    def __imod__(self, other: 'Fraction') -> 'Fraction':
        self._numerator = self._numerator % other._numerator
        self._denominator = self._denominator % other._denominator
        return self

    def __ipow__(self, power: int) -> 'Fraction':
        if power < 0:
            self._numerator = self._denominator ** -power
            self._denominator = self._numerator ** -power
        else:
            self._numerator = self._numerator ** power
            self._denominator = self._denominator ** power
        return self

    def __bool__(self) -> bool:
        return bool(self._numerator)

    def __hash__(self) -> int:
        return hash((self._numerator, self._denominator))

    def __len__(self) -> int:
        return len(str(self))

    def __iter__(self):
        yield self._numerator
        yield self._denominator

    def __contains__(self, item: int) -> bool:
        return item in (self._numerator, self._denominator)

    def __getitem__(self, index: int) -> int:
        return (self._numerator, self._denominator)[index]

    def __setitem__(self, index: int, value: int) -> None:
        if index == 0:
            self._numerator = value
        elif index == 1:
            self._denominator = value
        else:
            raise IndexError("Index out of range.")

    def __delitem__(self, index: int) -> None:
        raise TypeError("Cannot delete items from a fraction.")

    def __reversed__(self):
        yield self._denominator
        yield self._numerator
