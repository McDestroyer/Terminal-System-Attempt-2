import system.objects.terminal_objects.base_object as obj
import system.objects.helper_objects.coordinate as coord
from system.objects.helper_objects import axis, pixel_grid


class CursorObject(obj.BaseObject):
    """The cursor object."""

    def __init__(self, cursor: pixel_grid.PixelGrid) -> None:
        """Initialize the cursor object.

        Args:
            cursor (PixelGrid):
                The pixel grid representing the cursor.
        """
        super().__init__(
            name="Mouse Cursor",
            description="A character-based representation of the mouse cursor used to indicate precisely which " +
                        "character the user is selecting.",
            initial_grid=cursor,
            z_index=9001,
            visible=True,
        )
