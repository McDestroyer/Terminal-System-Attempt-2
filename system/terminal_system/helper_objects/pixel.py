import copy


class Pixel:
    """A pixel object.

    Properties:
        char (str):
            The character of the pixel.
        colors (list[str]):
            The colors of the pixel.
        cancel_code (str):
            The cancel code for the colors.
        printable_str (str):
            The printable string of the pixel.

    Methods:
        set(other: Pixel) -> None:
            Set the pixel to be the same as another pixel.
    """
    def __init__(self, char: str = " ", colors: list[str] | None = None, cancel_code: str = "\033[0m") -> None:
        """Initialize the pixel.

        Args:
            char (str, optional):
                The character of the pixel.
                Defaults to " ".
            colors (list[str] | None, optional):
                The colors of the pixel.
                Defaults to [].
            cancel_code (str, optional):
                The cancel code for the colors.
                Defaults to "\033[0m".
        """
        self._char = char
        self._colors = colors if colors else []
        self._cancel_code = cancel_code

        self._color_str = "".join(colors) if colors else ""

        self._printable_str = f"{self._color_str}{self._char}"

    def __str__(self):
        return self.printable_str

    def __repr__(self):
        return self.printable_str

    @property
    def char(self) -> str:
        return self._char

    @property
    def colors(self) -> list[str]:
        return self._colors

    @property
    def cancel_code(self) -> str:
        return self._cancel_code

    @property
    def printable_str(self) -> str:
        return f"{self._color_str}{self._char}{self.cancel_code}"

    @char.setter
    def char(self, new_char: str) -> None:
        self._char = new_char
        self._printable_str = f"{self._color_str}{new_char}{self.cancel_code}"

    @colors.setter
    def colors(self, new_colors: list[str] | None) -> None:
        self._colors = new_colors if new_colors else []
        self._color_str = "".join(new_colors) if new_colors else ""
        self._printable_str = f"{self._color_str}{self._char}{self.cancel_code}"

    @cancel_code.setter
    def cancel_code(self, new_cancel_code: str) -> None:
        self._cancel_code = new_cancel_code
        self._printable_str = f"{self._color_str}{self._char}{self.cancel_code}"

    def set(self, other: 'Pixel') -> None:
        """Set the pixel to be the same as another pixel.

        Args:
            other (Pixel):
                The other pixel.
        """
        self._char = other.char
        self._colors = other.colors
        self._cancel_code = other.cancel_code

        self._color_str = "".join(other.colors) if other.colors else ""
        self._printable_str = f"{self._color_str}{other.char}{other.cancel_code}"

    def __eq__(self, other: 'Pixel') -> bool:
        return self.char == other.char and self.colors == other.colors and self.cancel_code == other.cancel_code

    def __ne__(self, other: 'Pixel') -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.char, tuple(self.colors), self.cancel_code))

    def __copy__(self) -> 'Pixel':
        return Pixel(self.char, copy.deepcopy(self.colors), self.cancel_code)

    def __deepcopy__(self, memo: dict) -> 'Pixel':
        return Pixel(self.char, copy.deepcopy(self.colors), self.cancel_code)

    def __len__(self) -> int:
        return len(self.char)

    def __getitem__(self, index: int) -> str:
        return self.char[index]

    def __setitem__(self, index: int, value: str) -> None:
        self.char = self.char[:index] + value + self.char[index + 1:]

    def __delitem__(self, index: int) -> None:
        self.char = self.char[:index] + self.char[index + 1:]

    def __iter__(self):
        return iter(self.char)

    def __contains__(self, item: str) -> bool:
        return item in self.char

    def __add__(self, other: 'Pixel') -> 'Pixel':
        return Pixel(self.char + other.char, self.colors + other.colors, self.cancel_code)

    def __iadd__(self, other: 'Pixel') -> 'Pixel':
        self.char += other.char
        self.colors += other.colors
        return self
