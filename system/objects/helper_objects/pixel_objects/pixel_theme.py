from enum import Enum

from system.utilities.color import Colors, Color, ColorType


class PixelTheme:
    """A class to hold the theme of the terminal."""

    def __init__(self, color_list: list[Color] | None = None) -> None:
        """Initialize the theme object.

        Args:
            color_list (list[Color] | None, optional):
                The color scheme of the theme.
                Defaults to None.
        """
        self._color_list: list[Color] = color_list if color_list is not None else []

        self._foreground_color: Color | None = None
        self._background_color: Color | None = None
        self._style_colors: list[Color] = []
        self._other_colors: list[Color] = []

        self._str_value = ""

        # Use the color scheme setter to update the colors.
        self.color_scheme = self._color_list

    @property
    def color_scheme(self) -> list[Color]:
        return self._color_list

    @color_scheme.setter
    def color_scheme(self, value: list[Color]) -> None:
        self._color_list = value
        self._list_to_theme()
        self._str_value = self._to_str()

    @property
    def foreground_color(self) -> Color | None:
        return self._foreground_color

    @property
    def background_color(self) -> Color | None:
        return self._background_color

    @property
    def style_colors(self) -> list[Color]:
        return self._style_colors

    @property
    def other_colors(self) -> list[Color]:
        return self._other_colors

    @property
    def color_list(self) -> list[Color]:
        return self._color_list

    @property
    def str_value(self) -> str:
        return self._str_value

    def _to_str(self) -> str:
        """Convert the theme to a string.

        Returns:
            str: The string representation of the theme.
        """
        color_string = ""

        # Add the colors to the string.
        for other_color in self._other_colors:
            color_string += str(other_color)
        for style_color in self._style_colors:
            color_string += str(style_color)
        if self._foreground_color is not None:
            color_string += str(self._foreground_color)
        if self._background_color is not None:
            color_string += str(self._background_color)

        return color_string

    def _list_to_theme(self) -> None:
        """Convert color list to the theme."""

        # Set the colors of the theme based on the color list.
        for color in self._color_list:
            if type(color) is not Color:
                raise ValueError(f"Invalid color in color scheme: {color}")

            # If the color is a reset code, reset all colors.
            if color == Colors.END:
                self._foreground_color = None
                self._background_color = None
                self._style_colors = []
                self._other_colors = []

            # Otherwise, match its color type to the appropriate variable or list.
            match color.color_type:
                case ColorType.FORE:
                    self._foreground_color = color
                case ColorType.BACK:
                    self._background_color = color
                case ColorType.STYLE:
                    self._style_colors.append(color)
                case ColorType.OTHER:
                    self._other_colors.append(color)
                case _:
                    raise ValueError(f"Invalid color type in color scheme: {color.color_type}")

    def add_colors(self, colors: list[Color]) -> None:
        """Add colors to the theme.

        Args:
            colors (list[Color]):
                The colors to add to the theme.
        """
        self._color_list += colors
        self.color_scheme = self._color_list

    def __str__(self) -> str:
        return self._str_value

    def __repr__(self) -> str:
        return self._str_value

    def __getitem__(self, index: int) -> Color:
        return self._color_list[index]

    def __len__(self) -> int:
        return len(self._color_list)

    def __iter__(self):
        return iter(self._color_list)

    def __contains__(self, item: Color) -> bool:
        return item in self._color_list

    def __eq__(self, other: 'PixelTheme') -> bool:
        return self._color_list == other._color_list

    def __ne__(self, other: 'PixelTheme') -> bool:
        return self._color_list != other._color_list

    def __add__(self, other: 'PixelTheme') -> 'PixelTheme':
        return PixelTheme(self._color_list + other._color_list)

    def __iadd__(self, other: 'PixelTheme') -> 'PixelTheme':
        self.color_scheme += other._color_list
        return self

    def __mul__(self, other: int) -> 'PixelTheme':
        return PixelTheme(self._color_list * other)

    def __imul__(self, other: int) -> 'PixelTheme':
        self._color_list *= other
        return self

    def __rmul__(self, other: int) -> 'PixelTheme':
        return PixelTheme(self._color_list * other)


class ThemeTypes(Enum):
    """An enumeration of theme types."""
    DEFAULT = "default"
    HIGHLIGHTED = "highlighted"
    SELECTED = "selected"
    HOVERED = "hovered"
    DISABLED = "disabled"
    PRESSED = "pressed"
    ERROR = "error"
    WARNING = "warning"


class ThemeDict:

    def __init__(self, themes: dict[ThemeTypes, PixelTheme] | None = None,
                 unspecified_theme: PixelTheme = PixelTheme(), initial_theme: ThemeTypes = ThemeTypes.DEFAULT) -> None:
        """Initialize the theme dictionary.

        Args:
            themes (dict[ThemeTypes, PixelTheme], optional):
                The themes to initialize the dictionary with.
                Defaults to None.
            unspecified_theme (PixelTheme, optional):
                The theme to use if a theme is not specified.
                Defaults to PixelTheme().
        """
        # Set the themes to the specified themes or the default themes.
        self._themes: dict[ThemeTypes, PixelTheme] = themes if themes is not None else {
            ThemeTypes.DEFAULT: unspecified_theme,
            ThemeTypes.HIGHLIGHTED: unspecified_theme,
            ThemeTypes.SELECTED: unspecified_theme,
            ThemeTypes.HOVERED: unspecified_theme,
            ThemeTypes.DISABLED: unspecified_theme,
            ThemeTypes.PRESSED: unspecified_theme,
            ThemeTypes.ERROR: unspecified_theme,
            ThemeTypes.WARNING: unspecified_theme,
        }

        # If a theme is not specified, set it to the unspecified theme.
        if themes is not None:
            for item in ThemeTypes:
                try:
                    self._themes[item]
                except KeyError:
                    self._themes[item] = unspecified_theme

        # Set the current theme to the initial theme.
        self._current_theme: ThemeTypes = initial_theme

    @property
    def themes(self) -> dict[ThemeTypes, PixelTheme]:
        return self._themes

    @property
    def current_theme_type(self) -> ThemeTypes:
        return self._current_theme

    @current_theme_type.setter
    def current_theme_type(self, value: ThemeTypes) -> None:
        self._current_theme = value

    def update_themes(self, themes: dict[ThemeTypes, PixelTheme]) -> None:
        """Set the themes of the dictionary.

        Args:
            themes (dict[ThemeTypes, PixelTheme]):
                The themes to set the dictionary to. Only themes that are in the dictionary will be changed.
        """
        self._themes.update(themes)

    def __getitem__(self, item: ThemeTypes) -> PixelTheme:
        return self._themes[item]

    def __setitem__(self, key: ThemeTypes, value: PixelTheme) -> None:
        self._themes[key] = value

    def __len__(self) -> int:
        return len(self._themes)

    def __iter__(self):
        return iter(self._themes)

    def __contains__(self, item: ThemeTypes) -> bool:
        return item in self._themes

    def __eq__(self, other: 'ThemeDict') -> bool:
        return self._themes == other._themes

    def __ne__(self, other: 'ThemeDict') -> bool:
        return self._themes != other._themes

    def __add__(self, other: 'ThemeDict') -> 'ThemeDict':
        return ThemeDict({**self._themes, **other._themes})

    def __iadd__(self, other: 'ThemeDict') -> 'ThemeDict':
        self._themes.update(other._themes)
        return self

    def __mul__(self, other: int) -> 'ThemeDict':
        return ThemeDict({key: value * other for key, value in self._themes.items()})

    def __imul__(self, other: int) -> 'ThemeDict':
        self._themes = {key: value * other for key, value in self._themes.items()}
        return self

    def __rmul__(self, other: int) -> 'ThemeDict':
        return ThemeDict({key: value * other for key, value in self._themes.items()})

    def __str__(self) -> str:
        return str(self._themes[self._current_theme])

    def __repr__(self) -> str:
        return repr(self._themes[self._current_theme])
