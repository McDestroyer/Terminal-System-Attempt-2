import copy

import system.objects.helper_objects.pixel_objects.pixel as pixel
import system.objects.helper_objects.coordinate_objects.coordinate as coord
import system.objects.helper_objects.pixel_objects.pixel_theme as theme
from system.objects.helper_objects.coordinate_objects.point import Point


class PixelGrid:
    """A grid of pixels.

    Properties:
        coordinates (Coordinate):
            The coordinates of the PixelGrid.
        size (Coordinate):
            The size of the PixelGrid.
        default_pixel (Pixel):
            The default pixel of the PixelGrid.
        grid (list[list[Pixel]]):
            The grid of the PixelGrid.

    Methods:
        clear() -> None:
            Clear the PixelGrid. Set all pixels to the default pixel.
        fill(fill_pixel: Pixel) -> None:
            Fill the PixelGrid with the given pixel.
        overlay(other: PixelGrid) -> None:
            Overlay the other PixelGrid onto this PixelGrid based on the other's coordinates.
        to_string() -> str:
            Return the printable string representation of the PixelGrid.
        change_pixel(new_pixel: Pixel, coordinates: Coordinate) -> None:
            Change the pixel at the given coordinates.

            Theme Methods:

        change_overall_theme(theme_name: ThemeTypes) -> None:
            Set the theme of all the pixels in the PixelGrid.
        update_overall_theme(themes: dict[ThemeTypes, PixelTheme] | ThemeDict) -> None:
            Update the values of the theme of all the pixels in the PixelGrid.
        change_theme(theme_name: ThemeTypes, coordinates: Coordinate) -> None:
            Set the theme of the pixel at the given coordinates.
        update_theme(themes: dict[ThemeTypes, PixelTheme] | ThemeDict, coordinates: Coordinate) -> None:
            Update the values of the theme of the pixel at the given coordinates.
        change_pixel_theme_area(theme_name: ThemeTypes, start: Coordinate, end: Coordinate) -> None:
            Change the theme of the pixels in the area.
        update_pixel_theme_area(themes: dict[ThemeTypes, PixelTheme] | ThemeDict, start: Coordinate, end: Coordinate) -> None:
            Update the values of the theme of the pixels in the area.

    Possible Improvements:
        - Add a method to get a subgrid of the PixelGrid.
        - Add a method to copy the PixelGrid.
        - Add a method to get a pixel at a given coordinate.
        - Add a method to set a pixel at a given coordinate.
        - Add a method to get a row of the PixelGrid.
        - Add a method to get a column of the PixelGrid.
        - Add a method to rotate the PixelGrid.
        - Add a method to flip the PixelGrid.
        - Add a method to invert the PixelGrid.
        - Add a method to shift the PixelGrid.
        - Add a method to crop the PixelGrid.
        - Add a method to scale the PixelGrid.
        - Add a method to blend the PixelGrid.
    """

    def __init__(self, coordinates: coord.Coordinate, size: coord.Coordinate,
                 default_pixel: pixel.Pixel = pixel.Pixel(),
                 overall_themes: theme.ThemeDict = theme.ThemeDict()) -> None:
        """Initialize the PixelGrid object.

        Args:
            coordinates (Coordinate):
                The coordinates of the PixelGrid.
            size (Coordinate):
                The size of the PixelGrid.
            default_pixel (Pixel, optional):
                The default pixel of the PixelGrid.
                Defaults to Pixel().
            overall_themes (ThemeDict, optional):
                The overall themes of the PixelGrid.
                Defaults to a new ThemeDict().
        """
        self._coordinates: coord.Coordinate = coordinates
        self._size: coord.Coordinate = size
        self._default_pixel: pixel.Pixel = default_pixel
        self._overall_themes: theme.ThemeDict = overall_themes

        # Create the grid of pixels.
        self._grid: list[list[pixel.Pixel]] = [[default_pixel for _ in range(size.x_char)] for _ in range(size.y_char)]

        # Set the themes of the pixels.
        for row in self._grid:
            for pix in row:
                pix.themes = copy.deepcopy(self._overall_themes)

    @property
    def coordinates(self) -> coord.Coordinate:
        """Return the coordinates of the PixelGrid.

        Returns:
            Coordinate:
                The coordinates of the PixelGrid.
        """
        return self._coordinates

    @property
    def size(self) -> coord.Coordinate:
        """Return the size of the PixelGrid.

        Returns:
            Coordinate:
                The size of the PixelGrid.
        """
        return self._size

    @property
    def default_pixel(self) -> pixel.Pixel:
        """Return the default pixel of the PixelGrid.

        Returns:
            Pixel:
                The default pixel of the PixelGrid.
        """
        return self._default_pixel

    @property
    def grid(self) -> list[list[pixel.Pixel]]:
        """Return the grid of the PixelGrid.

        Returns:
            list[list[Pixel]]:
                The grid of the PixelGrid.
        """
        return self._grid

    @property
    def screen_size(self) -> Point:
        """Return the screen size of the PixelGrid.

        Returns:
            Point:
                The screen size of the PixelGrid.
        """
        return self._size.screen_size

    @property
    def overall_themes(self) -> theme.ThemeDict:
        """Return the overall themes of the PixelGrid.

        Returns:
            ThemeDict:
                The overall themes of the PixelGrid.
        """
        return self._overall_themes

    @overall_themes.setter
    def overall_themes(self, new_overall_themes: theme.ThemeDict) -> None:
        """Set the overall themes of the PixelGrid.

        Args:
            new_overall_themes (ThemeDict):
                The new overall themes of the PixelGrid.
        """
        self._overall_themes = new_overall_themes

        # Set the themes of the pixels.
        for row in self._grid:
            for pix in row:
                pix.themes = copy.deepcopy(self._overall_themes)

    @screen_size.setter
    def screen_size(self, new_screen_size: Point) -> None:
        """Set the screen size of the PixelGrid.

        Args:
            new_screen_size (Point):
                The new screen size of the PixelGrid.
        """
        self._size.screen_size = new_screen_size
        self._coordinates.screen_size = new_screen_size

    @coordinates.setter
    def coordinates(self, new_coordinates: coord.Coordinate) -> None:
        """Set the coordinates of the PixelGrid.

        Args:
            new_coordinates (Coordinate):
                The new coordinates of the PixelGrid.
        """
        self._coordinates = new_coordinates

    @size.setter
    def size(self, new_size: coord.Coordinate) -> None:
        """Set the size of the PixelGrid.

        Args:
            new_size (Coordinate):
                The new size of the PixelGrid.
        """
        self._size = new_size

        self._grid = [[self._default_pixel for _ in range(new_size.x_char)] for _ in range(new_size.y_char)]

    @default_pixel.setter
    def default_pixel(self, new_default_pixel: pixel.Pixel) -> None:
        """Set the default pixel of the PixelGrid.

        Args:
            new_default_pixel (Pixel):
                The new default pixel of the PixelGrid.
        """
        self._default_pixel = new_default_pixel

    @grid.setter
    def grid(self, new_grid: list[list[pixel.Pixel]]) -> None:
        """Set the grid of the PixelGrid.

        Args:
            new_grid (list[list[Pixel]]):
                The new grid of the PixelGrid.
        """
        self._grid = new_grid

        self._size.x_char = len(new_grid[0])
        self._size.y_char = len(new_grid)

    def change_overall_theme(self, theme_name: theme.ThemeTypes) -> None:
        """Set the theme of all the pixels in the PixelGrid.

        Args:
            theme_name (theme.ThemeTypes):
                The name of the theme to set.
        """
        for row in self._grid:
            for pix in row:
                pix.change_theme(theme_name)

    def update_overall_theme(self, themes: dict[theme.ThemeTypes, theme.PixelTheme] | theme.ThemeDict) -> None:
        """Update the values of the theme of all the pixels in the PixelGrid.

        Args:
            themes (dict[theme.ThemeTypes, theme.PixelTheme]):
                The theme dictionary to update the values of the theme with. Only values listed will be changed.
        """
        # Make sure the theme is in the right format and make a copy of the themes to avoid changing the original.
        if isinstance(themes, dict):
            theme_dict = theme.ThemeDict(themes)
        else:
            theme_dict = themes

        for row in self._grid:
            for pix in row:
                pix.themes = copy.deepcopy(theme_dict)

    def change_theme(self, theme_name: theme.ThemeTypes, coordinates: coord.Coordinate) -> None:
        """Set the theme of the pixel at the given coordinates.

        Args:
            theme_name (theme.ThemeTypes):
                The name of the theme to set.
            coordinates (Coordinate):
                The coordinates of the pixel to change the theme of.
        """
        self._grid[coordinates.y_char][coordinates.x_char].change_theme(theme_name)

    def update_theme(self, themes: dict[theme.ThemeTypes, theme.PixelTheme] | theme.ThemeDict,
                     coordinates: coord.Coordinate) -> None:
        """Update the values of the theme of the pixel at the given coordinates.

        Args:
            themes (dict[theme.ThemeTypes, theme.PixelTheme] | ThemeDict):
                The theme dictionary to update the values of the theme with. Only values listed will be changed.
            coordinates (Coordinate):
                The coordinates of the pixel to change the theme of.
        """
        if isinstance(themes, dict):
            theme_dict = theme.ThemeDict(themes)
        else:
            theme_dict = themes

        self._grid[coordinates.y_char][coordinates.x_char].themes = copy.deepcopy(theme_dict)

    def change_pixel(self, new_pixel: pixel.Pixel, coordinates: coord.Coordinate) -> None:
        """Change the pixel at the given coordinates.

        Args:
            new_pixel (Pixel):
                The new pixel to set.
            coordinates (Coordinate):
                The coordinates of the pixel to change.
        """
        self._grid[coordinates.y_char][coordinates.x_char] = copy.deepcopy(new_pixel)

    def change_pixel_theme_area(self, theme_name: theme.ThemeTypes, start: coord.Coordinate,
                                end: coord.Coordinate) -> None:
        """Change the theme of the pixels in the area.

        Args:
            theme_name (theme.ThemeTypes):
                The name of the theme to set.
            start (Coordinate):
                The starting coordinates of the area.
            end (Coordinate):
                The ending coordinates of the area.
        """
        for y in range(start.y_char, end.y_char + 1):
            for x in range(start.x_char, end.x_char + 1):
                self._grid[y][x].change_theme(theme_name)

    def update_pixel_theme_area(self, themes: dict[theme.ThemeTypes, theme.PixelTheme] | theme.ThemeDict,
                                start: coord.Coordinate, end: coord.Coordinate) -> None:
        """Update the values of the theme of the pixels in the area.

        Args:
            themes (dict[theme.ThemeTypes, theme.PixelTheme] | ThemeDict):
                The theme dictionary to update the values of the theme with. Only values listed will be changed.
            start (Coordinate):
                The starting coordinates of the area.
            end (Coordinate):
                The ending coordinates of the area.
        """
        # Make sure the theme is in the right format.
        if isinstance(themes, dict):
            theme_dict = theme.ThemeDict(themes)
        else:
            theme_dict = themes

        # Update the theme of the pixels in the area.
        for y in range(start.y_char, end.y_char + 1):
            for x in range(start.x_char, end.x_char + 1):
                self._grid[y][x].themes = copy.deepcopy(theme_dict)

    def clear(self) -> None:
        """Clear the PixelGrid. Set all pixels to the default pixel."""
        for pix in self:
            pix.set(self._default_pixel)

    def fill(self, fill_pixel: pixel.Pixel) -> None:
        """Fill the PixelGrid with the given pixel.

        Args:
            fill_pixel (Pixel):
                The pixel to fill the PixelGrid with.
        """
        for pix in self:
            pix.set(fill_pixel)

    def overlay(self, other: "PixelGrid") -> bool:
        """Overlay the other PixelGrid onto this PixelGrid based on the other's coordinates.

        Args:
            other (PixelGrid):
                The other PixelGrid.

        Returns:
            bool: Whether the overlay changed anything.
        """
        # Update the other's size's screen size to match the size of this PixelGrid.
        other.size.screen_size = (self.size.x_char, self.size.y_char)

        # Prep a variable to return whether anything changed.
        something_changed = False

        # Get the offset of the other PixelGrid.
        offset = other._coordinates

        # Overlay the other PixelGrid onto this PixelGrid.
        for y, row in enumerate(other._grid):
            for x, pix in row:
                # Skip the pixel if it'd be out of bounds.
                if y + offset.y_char < 0 or x + offset.x_char < 0:
                    continue
                if y + offset.y_char >= self._size.y_char or x + offset.x_char >= self._size.x_char:
                    continue

                # Check if the pixel is different.
                if str(self._grid[y + offset.y_char][x + offset.x_char]) != str(pix):
                    something_changed = True

                # Overlay the pixel.
                self._grid[y + offset.y_char][x + offset.x_char] = pix

        return something_changed

    def to_string(self) -> str:
        """Return the printable string representation of the PixelGrid.

        Returns:
            str: The printablestring representation of the PixelGrid.
        """
        return "\n".join(["".join([str(pix) for pix in row]) for row in self._grid])

    def __str__(self) -> str:
        """Return the string representation of the PixelGrid.

        Returns:
            str: The string representation of the PixelGrid.
        """
        return "\n".join(["".join([str(pix) for pix in row]) for row in self._grid])

    def __repr__(self) -> str:
        """Return the string representation of the PixelGrid.

        Returns:
            str: The string representation of the PixelGrid.
        """
        return self.__str__()

    def __len__(self) -> int:
        """Return the length of the PixelGrid.

        Returns:
            int: The length of the PixelGrid.
        """
        return len(self._grid)

    def __iter__(self) -> pixel.Pixel:
        """Return the iterator of the PixelGrid.

        Returns:
            Pixel: The iterator of the PixelGrid.
        """
        for row in self._grid:
            for pix in row:
                yield pix

    def __contains__(self, item: pixel.Pixel) -> bool:
        """Return whether the PixelGrid contains the given pixel.

        Args:
            item (Pixel):
                The pixel to check for.

        Returns:
            bool: Whether the PixelGrid contains the given pixel.
        """
        return item in self._grid

    def __getitem__(self, key: coord.Coordinate) -> pixel.Pixel:
        """Get the pixel at the given coordinates.

        Args:
            key (Coordinate):
                The coordinates of the pixel.

        Returns:
            Pixel: The pixel at the given coordinates.
        """
        return self._grid[key.y_char][key.x_char]

    def __setitem__(self, key: coord.Coordinate, value: pixel.Pixel) -> None:
        """Set the pixel at the given coordinates.

        Args:
            key (Coordinate):
                The coordinates of the pixel.
            value (Pixel):
                The pixel to set.
        """
        self._grid[key.y_char][key.x_char] = value
