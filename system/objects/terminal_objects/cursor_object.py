import system.objects.terminal_objects.image_object as obj
from system.objects.helper_objects.ascii_image import Image
from system.objects.helper_objects.pixel_objects.pixel_grid import PixelGrid


class CursorObject(obj.ImageObject):
    """The cursor object."""

    def __init__(self, cursor: Image) -> None:
        """Initialize the cursor object.

        Args:
            cursor (Image):
                The ascii image representing the cursor.
        """
        super().__init__(
            name="Mouse Cursor",
            description="A character-based representation of the mouse cursor used to indicate precisely which " +
                        "character the user is selecting.",
            initial_grid=PixelGrid(cursor.coordinates, cursor.size),
            image=cursor,
            z_index=9001,
            visible=True,
        )


