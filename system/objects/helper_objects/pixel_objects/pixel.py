import copy

from system.objects.helper_objects.pixel_objects.pixel_theme import ThemeDict, ThemeTypes
from system.utilities.color import Colors


class Pixel:
    """A pixel object.

    Properties:
        char (str):
            The character of the pixel.
        themes (ThemeDict):
            The colors of the pixel.
        printable_str (str):
            The printable string of the pixel.

    Methods:
        set(other: Pixel) -> None:
            Set the pixel to be the same as another pixel.
        change_theme(theme: ThemeTypes) -> None:
            Change the theme of the pixel.
    """
    def __init__(self, char: str = " ", themes: ThemeDict = ThemeDict()) -> None:
        """Initialize the pixel.

        Args:
            char (str, optional):
                The character of the pixel.
                Defaults to " ".
            themes (ThemeDict, optional):
                The colors of the pixel.
                Defaults to ThemeDict().
        """
        self._char = char
        self._themes = themes

        self._printable_str = f"{self._themes}{self._char}{Colors.END}"

    def __str__(self):
        return self.printable_str

    def __repr__(self):
        return self.printable_str

    @property
    def char(self) -> str:
        return self._char

    @property
    def themes(self) -> ThemeDict:
        return self._themes

    @property
    def printable_str(self) -> str:
        return f"{self._themes}{self._char}{Colors.END}"

    @char.setter
    def char(self, new_char: str) -> None:
        self._char = new_char
        self._printable_str = f"{self._themes}{new_char}{Colors.END}"

    @themes.setter
    def themes(self, new_theme: ThemeDict | None) -> None:
        self._themes = new_theme if new_theme else ThemeDict()
        self._printable_str = f"{self._themes}{self._char}{Colors.END}"

    def set(self, other: 'Pixel') -> None:
        """Set the pixel to have the values of another pixel.

        Args:
            other (Pixel):
                The other pixel.
        """
        self._char = other.char
        self._themes = other.themes

        self._printable_str = f"{self._themes}{self._char}{Colors.END}"

    def change_theme(self, theme: ThemeTypes) -> None:
        """Change the theme of the pixel.

        Args:
            theme (ThemeTypes):
                The theme to change to.
        """
        self._themes.current_theme_type = theme
        self._printable_str = f"{self._themes}{self._char}{Colors.END}"

    def __eq__(self, other: 'Pixel') -> bool:
        return self.char == other.char and self.themes == other.themes

    def __ne__(self, other: 'Pixel') -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.char, tuple(self.themes), Colors.END))

    def __copy__(self) -> 'Pixel':
        return Pixel(self.char, copy.deepcopy(self.themes))

    def __deepcopy__(self, memo: dict) -> 'Pixel':
        return Pixel(self.char, copy.deepcopy(self.themes))

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
        return Pixel(self.char + other.char, self.themes + other.themes)

    def __iadd__(self, other: 'Pixel') -> 'Pixel':
        self.char += other.char
        self.themes += other.themes
        return self
