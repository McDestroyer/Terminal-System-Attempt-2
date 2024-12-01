from system.objects.terminal_objects import base_object as obj, cursor_object
from system.objects.helper_objects import pixel_grid, coordinate as coord, axis


class Screen:
    """A screen object."""

    def __init__(self, name: str) -> None:
        """Initialize the Screen object.

        Args:
            name (str):
                The name of the screen.
        """
        self.name: str = name

        self.terminal_objects: list[obj.BaseObject] = []

        cursor_grid = pixel_grid.PixelGrid(
            coordinates=coord.Coordinate(
                axis.Axis(1),
            ),
        )

        self.cursor_object: cursor_object.CursorObject = cursor_object.CursorObject(cursor_grid)
