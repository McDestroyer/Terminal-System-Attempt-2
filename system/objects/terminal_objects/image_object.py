from system.inputs.input_handler import InputHandler
from system.objects.helper_objects.pixel_objects import pixel_grid
from system.objects.helper_objects.ascii_image import Image
from system.objects.terminal_objects.base_object import BaseObject


class ImageObject(BaseObject):
    def __init__(self, name: str, description: str, image: Image, initial_grid: pixel_grid.PixelGrid,
                 z_index: float = 0, visible: bool = True) -> None:
        """Initialize the ImageObject object.

        Args:
            name (str):
                The name of the object.
            description (str):
                The description of the object.
            image (Image):
                The image to display.
            initial_grid (PixelGrid):
                The initial grid to display the image on.
            z_index (float, optional):
                The z-index of the object.
                Defaults to 0.
            visible (bool, optional):
                Whether the object is visible.
                Defaults to True.
        """
        super().__init__(
            name=name,
            description=description,
            initial_grid=initial_grid,
            z_index=z_index,
            visible=visible,
        )

        self._image = image

    def _draw_image(self) -> None:
        """Draw the image onto the grid."""
        self.grid.overlay(self._image)
        self.should_draw = True

    def update(self, input_handler: InputHandler) -> None:
        """Update the object based on the inputs from the input handler.

        Args:
            input_handler (InputHandler):
                The input handler.
        """
        # This should be called first in this method in any child classes of BaseObject.
        super().update(input_handler)

        # Update the image animation and draw it if it has changed.
        if self._image.update_animation():
            self._draw_image()


