import system.terminal_system.helper_objects.pixel as pixel
import system.terminal_system.helper_objects.coordinate as coord


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
            The grid of the PixelGrid

    Methods:
        clear() -> None:
            Clear the PixelGrid. Set all pixels to the default pixel.
        fill(fill_pixel: Pixel) -> None:
            Fill the PixelGrid with the given pixel.
        overlay(other: PixelGrid) -> None:
            Overlay the other PixelGrid onto this PixelGrid based on the other's coordinates.

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
                 default_pixel: pixel.Pixel = pixel.Pixel()) -> None:
        """Initialize the PixelGrid object.

        Args:
            coordinates (Coordinate):
                The coordinates of the PixelGrid.
            size (Coordinate):
                The size of the PixelGrid.
            default_pixel (Pixel, optional):
                The default pixel of the PixelGrid.
                Defaults to Pixel().
        """
        self._coordinates: coord.Coordinate = coordinates
        self._size: coord.Coordinate = size
        self._default_pixel: pixel.Pixel = default_pixel

        self._grid: list[list[pixel.Pixel]] = [[default_pixel for _ in range(size.x_char)] for _ in range(size.y_char)]

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

    def overlay(self, other: "PixelGrid") -> None:
        """Overlay the other PixelGrid onto this PixelGrid based on the other's coordinates.

        Args:
            other (PixelGrid):
                The other PixelGrid.
        """
        # Update the other's size's screen size to match the size of this PixelGrid.
        other.size.screen_size = (self.size.x_char, self.size.y_char)

        offset = other._coordinates

        for y, row in enumerate(other._grid):
            for x, pix in row:
                # Skip the pixel if it'd be out of bounds.
                if y + offset.y_char < 0 or x + offset.x_char < 0:
                    continue
                if y + offset.y_char >= self._size.y_char or x + offset.x_char >= self._size.x_char:
                    continue

                # Overlay the pixel.
                self._grid[y + offset.y_char][x + offset.x_char] = pix

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
