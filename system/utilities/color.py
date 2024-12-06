"""A mapping between colors and escape codes for use in the text function"""
from enum import Enum
from typing import NamedTuple

import colorama

colorama.init()


class ColorType(Enum):
    FORE: str = 'foreground'
    BACK: str = 'background'
    STYLE: str = 'style'
    OTHER: str = 'other'


class Color:

    def __init__(self, color: str, color_type: ColorType) -> None:
        self.color = color
        self.color_type = color_type

    def __str__(self) -> str:
        return self.color

    def __repr__(self) -> str:
        return self.color

    def __add__(self, other: str) -> str:
        return self.color + other

    def __radd__(self, other: str) -> str:
        return other + self.color

    def __mul__(self, other: int) -> str:
        return self.color * other

    def __rmul__(self, other: int) -> str:
        return other * self.color

    def __iadd__(self, other: 'Color') -> str:
        return self.color + other

    def __imul__(self, other: int) -> str:
        return self.color * other

    def __len__(self) -> int:
        return len(self.color)

    def __getitem__(self, key: int) -> str:
        return self.color[key]

    def __contains__(self, item: str) -> bool:
        return item in self.color

    def __eq__(self, other: 'Color') -> bool:
        return self.color == other

    def __ne__(self, other: 'Color') -> bool:
        return self.color != other

    def __lt__(self, other: 'Color') -> bool:
        return self.color < other.color

    def __le__(self, other: 'Color') -> bool:
        return self.color <= other.color

    def __gt__(self, other: 'Color') -> bool:
        return self.color > other.color

    def __ge__(self, other: 'Color') -> bool:
        return self.color >= other.color

    def __hash__(self) -> int:
        return hash(self.color)

    def __bool__(self) -> bool:
        return bool(self.color)

    def __format__(self, format_spec: str) -> str:
        return self.color.__format__(format_spec)

    def __iter__(self):
        return iter(self.color)

    def __reversed__(self):
        return reversed(self.color)


class Colors:
    """A mapping between colors and escape codes for use in coloring text.

    Attributes:
        BOLD (Color): Bold text.
        FAINT (Color): Faint text.
        ITALIC (Color): Italic text.
        UNDERLINE (Color): Underlined text.
        BLINKING (Color): Blinking text.
        INVERSE (Color): Inverse text.
        HIDDEN (Color): Hidden text.
        STRIKETHROUGH (Color): Strikethrough text.

        BLACK (Color): Black text.
        RED (Color): Red text.
        GREEN (Color): Green text.
        YELLOW (Color): Yellow text.
        BLUE (Color): Blue text.
        PURPLE (Color): Purple text.
        CYAN (Color): Cyan text.
        WHITE (Color): White text.

        BRIGHT_BLACK (Color): Bright black text.
        BRIGHT_RED (Color): Bright red text.
        BRIGHT_GREEN (Color): Bright green text.
        BRIGHT_YELLOW (Color): Bright yellow text.
        BRIGHT_BLUE (Color): Bright blue text.
        BRIGHT_PURPLE (Color): Bright purple text.
        BRIGHT_CYAN (Color): Bright cyan text.
        BRIGHT_WHITE (Color): Bright white text.

        DEFAULT_COLOR (Color): Default text color.

        BACKGROUND_BLACK (Color): Black background.
        BACKGROUND_RED (Color): Red background.
        BACKGROUND_GREEN (Color): Green background.
        BACKGROUND_YELLOW (Color): Yellow background.
        BACKGROUND_BLUE (Color): Blue background.
        BACKGROUND_PURPLE (Color): Purple background.
        BACKGROUND_CYAN (Color): Cyan background.
        BACKGROUND_WHITE (Color): White background.

        BACKGROUND_BRIGHT_BLACK (Color): Bright black background.
        BACKGROUND_BRIGHT_RED (Color): Bright red background.
        BACKGROUND_BRIGHT_GREEN (Color): Bright green background.
        BACKGROUND_BRIGHT_YELLOW (Color): Bright yellow background.
        BACKGROUND_BRIGHT_BLUE (Color): Bright blue background.
        BACKGROUND_BRIGHT_PURPLE (Color): Bright purple background.
        BACKGROUND_BRIGHT_CYAN (Color): Bright cyan background.
        BACKGROUND_BRIGHT_WHITE (Color): Bright white background.

        BACKGROUND_DEFAULT_COLOR (Color): Default background color.

        ERROR (Color): Error text color.

        WARN (Color): Warning symbol.
        BELL (Color): Play a bell sound.

        END (Color): End coloring

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

    BOLD: Color = Color('\033[1m', ColorType.STYLE)
    FAINT: Color = Color('\033[2m', ColorType.STYLE)
    ITALIC: Color = Color('\033[3m', ColorType.STYLE)
    UNDERLINE: Color = Color('\033[4m', ColorType.STYLE)
    BLINKING: Color = Color('\033[5m', ColorType.STYLE)
    INVERSE: Color = Color('\033[7m', ColorType.STYLE)
    HIDDEN: Color = Color('\033[8m', ColorType.STYLE)
    STRIKETHROUGH: Color = Color('\033[9m', ColorType.STYLE)

    DOUBLE_UNDERLINE: Color = Color('\033[21m', ColorType.STYLE)  # Not supported in all terminals.

    RESET_BOLD: Color = Color('\033[22m', ColorType.STYLE)
    RESET_FAINT: Color = Color('\033[22m', ColorType.STYLE)
    RESET_ITALIC: Color = Color('\033[23m', ColorType.STYLE)
    RESET_UNDERLINE: Color = Color('\033[24m', ColorType.STYLE)
    RESET_BLINKING: Color = Color('\033[25m', ColorType.STYLE)
    RESET_INVERSE: Color = Color('\033[27m', ColorType.STYLE)
    RESET_HIDDEN: Color = Color('\033[28m', ColorType.STYLE)
    RESET_STRIKETHROUGH: Color = Color('\033[29m', ColorType.STYLE)

    # Colors:

    BLACK: Color = Color('\033[30m', ColorType.FORE)
    RED: Color = Color('\033[31m', ColorType.FORE)
    GREEN: Color = Color('\033[32m', ColorType.FORE)
    YELLOW: Color = Color('\033[33m', ColorType.FORE)
    BLUE: Color = Color('\033[34m', ColorType.FORE)
    PURPLE: Color = Color('\033[35m', ColorType.FORE)
    CYAN: Color = Color('\033[36m', ColorType.FORE)
    WHITE: Color = Color('\033[37m', ColorType.FORE)

    BRIGHT_BLACK: Color = Color('\033[90m', ColorType.FORE)
    BRIGHT_RED: Color = Color('\033[91m', ColorType.FORE)
    BRIGHT_GREEN: Color = Color('\033[92m', ColorType.FORE)
    BRIGHT_YELLOW: Color = Color('\033[93m', ColorType.FORE)
    BRIGHT_BLUE: Color = Color('\033[94m', ColorType.FORE)
    BRIGHT_PURPLE: Color = Color('\033[95m', ColorType.FORE)
    BRIGHT_CYAN: Color = Color('\033[96m', ColorType.FORE)
    BRIGHT_WHITE: Color = Color('\033[97m', ColorType.FORE)

    DEFAULT_COLOR: Color = Color('\033[39m', ColorType.FORE)

    # Background colors:

    BACKGROUND_BLACK: Color = Color('\033[40m', ColorType.BACK)
    BACKGROUND_RED: Color = Color('\033[41m', ColorType.BACK)
    BACKGROUND_GREEN: Color = Color('\033[42m', ColorType.BACK)
    BACKGROUND_YELLOW: Color = Color('\033[43m', ColorType.BACK)
    BACKGROUND_BLUE: Color = Color('\033[44m', ColorType.BACK)
    BACKGROUND_PURPLE: Color = Color('\033[45m', ColorType.BACK)
    BACKGROUND_CYAN: Color = Color('\033[46m', ColorType.BACK)
    BACKGROUND_WHITE: Color = Color('\033[47m', ColorType.BACK)

    BACKGROUND_BRIGHT_BLACK: Color = Color('\033[100m', ColorType.BACK)
    BACKGROUND_BRIGHT_RED: Color = Color('\033[101m', ColorType.BACK)
    BACKGROUND_BRIGHT_GREEN: Color = Color('\033[102m', ColorType.BACK)
    BACKGROUND_BRIGHT_YELLOW: Color = Color('\033[103m', ColorType.BACK)
    BACKGROUND_BRIGHT_BLUE: Color = Color('\033[104m', ColorType.BACK)
    BACKGROUND_BRIGHT_PURPLE: Color = Color('\033[105m', ColorType.BACK)
    BACKGROUND_BRIGHT_CYAN: Color = Color('\033[106m', ColorType.BACK)
    BACKGROUND_BRIGHT_WHITE: Color = Color('\033[107m', ColorType.BACK)

    BACKGROUND_DEFAULT_COLOR: Color = Color('\033[49m', ColorType.BACK)

    # Specific use colors:

    ERROR: Color = Color('\033[38;2;255;140;25m', ColorType.FORE)

    # Symbols:

    WARN: Color = Color('⚠ ', ColorType.OTHER)

    # Sounds:

    BELL: Color = Color('\a', ColorType.OTHER)

    # Remove formatting:

    END: Color = Color('\033[0m', ColorType.OTHER)

    @classmethod
    def color_id(cls, code: int, back: bool = False) -> Color:
        """Give a text or background modification color code based off of a specific escape code.

        Args:
            code (int):
                The code of the desired modification. This must be between 0 and 255.
            back (bool, optional):
                If True gives the code for modifying the background instead of the foreground.
                Defaults to False.

        Returns:
            Color: The modification escape code ready to be input to text.

        Raises:
            ValueError: If the code is not between 0 and 255.
        """
        # Verify it is a valid color code.
        if code < 0 or code > 255:
            raise ValueError('Color code must be between 0 and 255.')

        # Return the correct color code.
        if back:
            return Color(f'\033[48;5;{code}m', ColorType.BACK)
        else:
            return Color(f'\033[38;5;{code}m', ColorType.FORE)

    @classmethod
    def rgb(cls, red: int = 0, green: int = 0, blue: int = 0, back: bool = False) -> Color:
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
            Color: The modification escape code ready to be input to text.

        Raises:
            ValueError: If any of the color values are not between 0 and 255.
        """
        # Verify the color values are valid.
        if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
            raise ValueError('Color values must be between 0 and 255.')

        # Return the correct color code.
        if back:
            return Color(f'\033[48;2;{red};{green};{blue}m', ColorType.BACK)
        else:
            return Color(f'\033[38;2;{red};{green};{blue}m', ColorType.FORE)

    @classmethod
    def rgb_hex(cls, red_hex: str = "00", green_hex: str = "00", blue_hex: str = "00", back: bool = False) -> Color:
        """Give a text or background modification color code based off of a hex RGB input. The hex string must be 2
        characters long.

        Args:
            red_hex (str, optional):
                Red value of the text (00-FF).
                Defaults to "00".
            green_hex (str, optional):
                Green value of the text (00-FF).
                Defaults to "00".
            blue_hex (str, optional):
                Blue value of the text (00-FF).
                Defaults to "00".
            back (bool, optional):
                If True gives the code for modifying the background instead of the foreground.
                Defaults to False.

        Returns:
            Color: The modification escape code ready to be input to text.

        Raises:
            ValueError: If any of the color values are not between 00 and FF.
        """
        red = int(red_hex, 16)
        green = int(green_hex, 16)
        blue = int(blue_hex, 16)

        return cls.rgb(red, green, blue, back)

    @classmethod
    def rgb_hex_string(cls, hex_string: str, back: bool = False) -> Color:
        """Give a text or background modification color code based off of a hex RGB input string.

        Args:
            hex_string (str):
                The hex string to get the color from.
            back (bool, optional):
                If True gives the code for modifying the background instead of the foreground.
                Defaults to False.

        Returns:
            Color: The modification escape code ready to be input to text.

        Raises:
            ValueError: If the hex string is not a valid hex color string.
        """
        # Remove the hash if it is there.
        if hex_string.startswith('#'):
            hex_string = hex_string[1:]

        # Check the length of the hex string.
        if len(hex_string) == 6:
            return cls.rgb_hex(hex_string[:2], hex_string[2:4], hex_string[4:], back)
        elif len(hex_string) == 3:
            return cls.rgb_hex(hex_string[0] * 2, hex_string[1] * 2, hex_string[2] * 2, back)
        else:
            raise ValueError('Hex string must be either 3 or 6 characters long.')

    @classmethod
    def color_from_code(cls, color_str: str, color_type: ColorType = ColorType.OTHER) -> Color:
        """Get the color from the given color code if possible.

        Args:
            color_str (str):
                The color to get. This must be a valid escape code.
            color_type (ColorType, optional):
                The type of color being input (foreground, background, style, or other) if known. Ignored if not known
                or found in the attribute list.
                Defaults to ColorType.OTHER.

        Returns:
            Color: The color.

        Raises:
            ValueError: If the color code is not a valid escape code.
        """

        # Check if the color is an escape code.
        if not color_str.startswith('\033['):
            raise ValueError('Color code must be a valid name or start with an escape code.')

        # Check if the color is an RGB or 0-255 color ID escape code.
        if color_str.startswith('\033[38;'):
            return Color(color_str, ColorType.FORE)
        elif color_str.startswith('\033[48;'):
            return Color(color_str, ColorType.BACK)

        return Color(color_str, color_type)


if __name__ == '__main__':

    print(Colors.UNDERLINE + 'Hello, underline!' + Colors.END)
    print(Colors.DOUBLE_UNDERLINE + 'Hello, double underline!' + Colors.END)

    # color_list: list[Color] = [
    #     Colors.BOLD,
    #     Colors.RED,
    #     Colors.BACKGROUND_BLUE,
    #     Colors.rgb(255, 0, 0),
    #     Colors.rgb_hex('FF', '00', '00'),
    #     Colors.color_id(255),
    #     Colors.color_id(255, True),
    #     Colors.UNDERLINE,
    #     Colors.END,
    # ]
    #
    # for c in color_list:
    #     print((c == Colors.END))
    # print()
    # print((Colors.END == Colors.BOLD))
    # print((Colors.END == Colors.END))
    # print((Colors.END == "Colors.RED"))
    # print("RED == RED.color", str(Colors.RED == str(Colors.RED)))
    # print("RED == RED", str(Colors.RED == Colors.RED))

    # print(Colors.BOLD + 'Hello, bold!' + Colors.END)
    # print(Colors.FAINT + 'Hello, faint!' + Colors.END)
    # print(Colors.ITALIC + 'Hello, italic!' + Colors.END)
    # print(Colors.UNDERLINE + 'Hello, underline!' + Colors.END)
    # print(Colors.BLINKING + Colors.RED + 'Hello, blinking!' + Colors.END)
    # print(Colors.INVERSE + 'Hello, inverse!' + Colors.END)
    # print(Colors.HIDDEN + 'Hello, hidden!' + Colors.END)
    # print(Colors.STRIKETHROUGH + 'Hello, strikethrough!' + Colors.END)
    #
    # print(Colors.BOLD + Colors.ITALIC + Colors.UNDERLINE + Colors.BLINKING + Colors.INVERSE +
    #       Colors.STRIKETHROUGH + Colors.RED + 'Hello, all!' + Colors.END)
    #
    # # Italic
    # print(Colors.ITALIC + 'Hello, italic!' + Colors.END)
    # # Bold
    # print(Colors.BOLD + 'Hello, bold!' + Colors.END)
    # # Bold and italic
    # print(Colors.BOLD + Colors.ITALIC + 'Hello, bold and italic!' + Colors.END)

