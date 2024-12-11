import copy
import sys
from copy import deepcopy

import system.utilities.cursor as cursor

import system.objects.helper_objects.pixel_objects.pixel_grid as pixel_grid
import system.objects.helper_objects.coordinate_objects.coordinate as coord
import system.objects.helper_objects.coordinate_objects.axis as ax
from system.objects.helper_objects.coordinate_objects.point import Point


class Display:

    def __init__(self, display_grid: pixel_grid.PixelGrid) -> None:
        """Initialize the display.

        Args:
            display_grid (pixel_grid.PixelGrid):
                The display grid to use.
        """
        self._display_size = copy.deepcopy(display_grid.size)

        self._display_pixel_grid = pixel_grid.PixelGrid(
            coord.Coordinate(
                ax.Axis(value=0, axis_size=self._display_size.x_char),
                ax.Axis(value=0, axis_size=self._display_size.y_char),
            ),
            self._display_size,
            default_pixel=copy.deepcopy(display_grid.default_pixel),
        )
        self._previous_pixel_grid = copy.deepcopy(self._display_pixel_grid)

        self._display_string = self._display_pixel_grid.to_string()

        self.refresh_display()

    # Display functions.

    def clear_display(self) -> None:
        """Clear the display array and refresh. NOT the same as cursor.clear_screen()!!!"""
        self._display_pixel_grid.clear()

        self.refresh_display()

    def refresh_display(self) -> None:
        """Refresh the display with the most recent display string. Fast, but may cause flashing."""
        # cursor.clear_screen()

        self._display_string = self._display_pixel_grid.to_string()
        print(self._display_string, end="", flush=True)

        self._previous_pixel_grid = deepcopy(self._display_pixel_grid)

    def anti_flash_refresh_display(self) -> None:
        """Refresh the display with the most recent display string, only updating the parts that are different. Slower,
        but prevents flashing."""
        # Skip if there have been no changes.
        # if self._display_pixel_grid == self._previous_pixel_grid:
        #     return

        # If the previous display array is a different size than the current one, clear the screen and print the whole
        # thing. Usually should only occur when changing display sizes.
        if self._previous_pixel_grid.size != self._display_pixel_grid.size:
            self.refresh_display()
            return

        # if len(self._display_pixel_grid.grid) != len(self._previous_pixel_grid.grid):
        #     print("Display size mismatch.")
        #     return

        # Cycle through the display array and print the characters that have changed.
        for y, row in enumerate(self._display_pixel_grid.grid):

            string_buffer = ""
            buffer_start: Point | None = None

            for x, pixel in enumerate(row):
                if pixel != self._previous_pixel_grid.grid[y][x]:
                    if buffer_start is None:
                        buffer_start = Point(x, y)
                    string_buffer += pixel.printable_str
                elif buffer_start is not None:
                    cursor.set_pos(buffer_start.y, buffer_start.x)
                    print(string_buffer, end="", flush=False)

                    string_buffer = ""
                    buffer_start = None

        # Finish by resetting the cursor to the top left and flushing the print queue.
        cursor.set_pos(0, 0)
        print("", end="", flush=True)

        # Update the previous display grid.
        self._previous_pixel_grid = deepcopy(self._display_pixel_grid)

    def update_display_grid(self, new_display_grid: pixel_grid.PixelGrid) -> None:
        """Update the display grid.

        Args:
            new_display_grid (pixel_grid.PixelGrid):
                The new display grid.
        """
        # if new_display_grid != self._display_pixel_grid:
            # self._display_pixel_grid = deepcopy(new_display_grid)
        self._display_pixel_grid = new_display_grid
        self.anti_flash_refresh_display()

    @property
    def display_array(self) -> pixel_grid.PixelGrid:
        """Return the display array.

        Returns:
            pixel_grid.PixelGrid: The display array.
        """
        return self._display_pixel_grid

    @property
    def display_string(self) -> str:
        """Return the display string.

        Returns:
            str: The display string.
        """
        return self._display_string

    @property
    def display_size(self) -> coord.Coordinate:
        """Return the display size.

        Returns:
            coord.Coordinate: The display size.
        """
        return self._display_size

    @property
    def previous_display_array(self) -> pixel_grid.PixelGrid:
        """Return the previous display array.

        Returns:
            pixel_grid.PixelGrid: The previous display array.
        """
        return self._previous_pixel_grid

    @previous_display_array.setter
    def previous_display_array(self, new_previous_pixel_grid: pixel_grid.PixelGrid) -> None:
        """Set the previous display array.

        Args:
            new_previous_pixel_grid (pixel_grid.PixelGrid):
                The new previous display array.
        """
        self._previous_pixel_grid = deepcopy(new_previous_pixel_grid)

    @display_array.setter
    def display_array(self, new_display_array: pixel_grid.PixelGrid) -> None:
        """Set the display array.

        Args:
            new_display_array (pixel_grid.PixelGrid):
                The new display array.
        """
        self._display_pixel_grid = deepcopy(new_display_array)
        self.anti_flash_refresh_display()

    @display_string.setter
    def display_string(self, new_display_string: str) -> None:
        """Set the display string.

        Args:
            new_display_string (str):
                The new display string.
        """
        self._display_string = deepcopy(new_display_string)
        self.refresh_display()

    @display_size.setter
    def display_size(self, new_display_size: coord.Coordinate) -> None:
        """Set the display size.

        Args:
            new_display_size (coord.Coordinate):
                The new display size.
        """
        self._display_size = deepcopy(new_display_size)
        self._display_pixel_grid.size = self._display_size

        self.refresh_display()


if __name__ == "__main__":
    # display = Display()
    pass
