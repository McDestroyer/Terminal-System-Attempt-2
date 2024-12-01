"""A mapping between colors and escape codes for use in the text function"""
from enum import Enum
import colorama

colorama.init()


class Colors(Enum):
    """A mapping between colors and escape codes for use in coloring text.

    Attributes:
        BOLD (str): Bold text.
        FAINT (str): Faint text.
        ITALIC (str): Italic text.
        UNDERLINE (str): Underlined text.
        BLINKING (str): Blinking text.
        INVERSE (str): Inverse text.
        HIDDEN (str): Hidden text.
        STRIKETHROUGH (str): Strikethrough text.

        BLACK (str): Black text.
        RED (str): Red text.
        GREEN (str): Green text.
        YELLOW (str): Yellow text.
        BLUE (str): Blue text.
        PURPLE (str): Purple text.
        CYAN (str): Cyan text.
        WHITE (str): White text.

        BRIGHT_BLACK (str): Bright black text.
        BRIGHT_RED (str): Bright red text.
        BRIGHT_GREEN (str): Bright green text.
        BRIGHT_YELLOW (str): Bright yellow text.
        BRIGHT_BLUE (str): Bright blue text.
        BRIGHT_PURPLE (str): Bright purple text.
        BRIGHT_CYAN (str): Bright cyan text.
        BRIGHT_WHITE (str): Bright white text.

        DEFAULT_COLOR (str): Default text color.

        BACKGROUND_BLACK (str): Black background.
        BACKGROUND_RED (str): Red background.
        BACKGROUND_GREEN (str): Green background.
        BACKGROUND_YELLOW (str): Yellow background.
        BACKGROUND_BLUE (str): Blue background.
        BACKGROUND_PURPLE (str): Purple background.
        BACKGROUND_CYAN (str): Cyan background.
        BACKGROUND_WHITE (str): White background.

        BACKGROUND_BRIGHT_BLACK (str): Bright black background.
        BACKGROUND_BRIGHT_RED (str): Bright red background.
        BACKGROUND_BRIGHT_GREEN (str): Bright green background.
        BACKGROUND_BRIGHT_YELLOW (str): Bright yellow background.
        BACKGROUND_BRIGHT_BLUE (str): Bright blue background.
        BACKGROUND_BRIGHT_PURPLE (str): Bright purple background.
        BACKGROUND_BRIGHT_CYAN (str): Bright cyan background.
        BACKGROUND_BRIGHT_WHITE (str): Bright white background.

        BACKGROUND_DEFAULT_COLOR (str): Default background color.

        ERROR (str): Error text color.

        WARN (str): Warning symbol.

        END (str): End coloring

    Methods:
        custom(cls, code: int, back: bool = False) -> str:
            Give a text or background modification color code based off of a specific escape code.
        rgb(cls, red: int = 0, green: int = 0, blue: int = 0, back: bool = False) -> str:
            Give a text or background modification color code based off of a decimal RGB input.
        rgb_hex(cls, red: str = 0, green: str = 0, blue: str = 0, back: bool = False) -> str:
            Give a text or background modification color code based off of a hex RGB

    Notes:
        BLINKING, FAINT, and HIDDEN are not supported in all terminals, and even if they are supported, they may
        interfere with each other.
    """

    # Formatting:

    BOLD = '\033[1m'
    FAINT = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINKING = '\033[5m'
    INVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

    # Colors:

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_PURPLE = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    DEFAULT_COLOR = '\033[39m'

    # Background colors:

    BACKGROUND_BLACK = '\033[40m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_YELLOW = '\033[43m'
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_PURPLE = '\033[45m'
    BACKGROUND_CYAN = '\033[46m'
    BACKGROUND_WHITE = '\033[47m'

    BACKGROUND_BRIGHT_BLACK = '\033[100m'
    BACKGROUND_BRIGHT_RED = '\033[101m'
    BACKGROUND_BRIGHT_GREEN = '\033[102m'
    BACKGROUND_BRIGHT_YELLOW = '\033[103m'
    BACKGROUND_BRIGHT_BLUE = '\033[104m'
    BACKGROUND_BRIGHT_PURPLE = '\033[105m'
    BACKGROUND_BRIGHT_CYAN = '\033[106m'
    BACKGROUND_BRIGHT_WHITE = '\033[107m'

    BACKGROUND_DEFAULT_COLOR = '\033[49m'

    # Specific use colors:

    ERROR = '\033[38;2;255;140;25m'

    # Symbols:

    WARN = "⚠ "

    # Remove formatting:

    END = '\033[0m'

    @classmethod
    def custom(cls, code: int, back: bool = False) -> str:
        """Give a text or background modification color code based off of a specific escape code.

        Args:
            code (int): The code of the desired modification.
            back (bool, optional):
                If True gives the code for modifying the background instead of the foreground.
                Defaults to False.

        Returns:
            str: The modification escape code ready to be input to text.
        """
        return f'\033[38;5;{code}m' if not back else f'\033[48;5;{code}m'

    @classmethod
    def rgb(cls, red: int = 0, green: int = 0, blue: int = 0, back: bool = False) -> str:
        """Give a text or background modification color code based off of a decimal RGB input.

        Args:
            red (int, optional):
                Red value of the text (0-255).
                Defaults to 0.
            green (int, optional):
                Green value of the text (0-255).
                Defaults to 0.
            blue (int, optional):
                Blue value of the text (0-255).
                Defaults to 0.
            back (bool, optional):
                If True gives the code for modifying the background instead of the foreground.
                Defaults to False.

        Returns:
            str: The modification escape code ready to be input to text.
        """
        return (f'\033[38;2;{red};{green};{blue}m' if not back
                else f'\033[48;2;{red};{green};{blue}m')

    @classmethod
    def rgb_hex(cls, red: str = 0, green: str = 0, blue: str = 0, back: bool = False) -> str:
        """Give a text or background modification color code based off of a hex RGB input.

        Args:
            red (str, optional):
                Red value of the text (00-FF).
                Defaults to 0.
            green (str, optional):
                Green value of the text (00-FF).
                Defaults to 0.
            blue (str, optional):
                Blue value of the text (00-FF).
                Defaults to 0.
            back (bool, optional):
                If True gives the code for modifying the background instead of the foreground.
                Defaults to False.

        Returns:
            str: The modification escape code ready to be input to text.
        """
        return (f'\033[38;2;{int(red, 16)};{int(green, 16)};{int(blue, 16)}m' if not back
                else f'\033[48;2;{red};{green};{blue}m')

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def __add__(self, other: str) -> str:
        return self.value + other

    def __radd__(self, other: str) -> str:
        return other + self.value

    def __mul__(self, other: int) -> str:
        return self.value * other

    def __rmul__(self, other: int) -> str:
        return other * self.value

    def __iadd__(self, other: str) -> str:
        return self.value + other

    def __imul__(self, other: int) -> str:
        return self.value * other

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, key: int) -> str:
        return self.value[key]

    def __contains__(self, item: str) -> bool:
        return item in self.value

    def __eq__(self, other: str) -> bool:
        return self.value == other

    def __ne__(self, other: str) -> bool:
        return self.value != other

    def __lt__(self, other: str) -> bool:
        return self.value < other

    def __le__(self, other: str) -> bool:
        return self.value <= other

    def __gt__(self, other: str) -> bool:
        return self.value > other

    def __ge__(self, other: str) -> bool:
        return self.value >= other

    def __hash__(self) -> int:
        return hash(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __format__(self, format_spec: str) -> str:
        return self.value.__format__(format_spec)

    def __iter__(self):
        return iter(self.value)

    def __reversed__(self):
        return reversed(self.value)


if __name__ == '__main__':
    print(Colors.BOLD + 'Hello, bold!' + Colors.END)
    print(Colors.FAINT + 'Hello, faint!' + Colors.END)
    print(Colors.ITALIC + 'Hello, italic!' + Colors.END)
    print(Colors.UNDERLINE + 'Hello, underline!' + Colors.END)
    print(Colors.BLINKING + Colors.RED + 'Hello, blinking!' + Colors.END)
    print(Colors.INVERSE + 'Hello, inverse!' + Colors.END)
    print(Colors.HIDDEN + 'Hello, hidden!' + Colors.END)
    print(Colors.STRIKETHROUGH + 'Hello, strikethrough!' + Colors.END)

    print(Colors.BOLD + Colors.ITALIC + Colors.UNDERLINE + Colors.BLINKING + Colors.INVERSE +
          Colors.STRIKETHROUGH + Colors.RED + 'Hello, all!' + Colors.END)

    # Italic
    print(Colors.ITALIC + 'Hello, italic!' + Colors.END)
    # Bold
    print(Colors.BOLD + 'Hello, bold!' + Colors.END)
    # Bold and italic
    print(Colors.BOLD + Colors.ITALIC + 'Hello, bold and italic!' + Colors.END)

