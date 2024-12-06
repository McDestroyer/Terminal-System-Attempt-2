from system.inputs.input_handler import InputHandler
from system.objects.helper_objects.pixel_objects import pixel_grid
from system.objects.helper_objects.ascii_text import Text
from system.objects.terminal_objects.base_object import BaseObject


class TextObject(BaseObject):
    def __init__(self, name: str, description: str, text: Text, initial_grid: pixel_grid.PixelGrid,
                 z_index: float = 0, visible: bool = True) -> None:
        """Initialize the TextObject object.

        Args:
            name (str):
                The name of the object.
            description (str):
                The description of the object.
            text (Text):
                The text to display.
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

        self._text = text

    @property
    def text(self) -> Text:
        """Get the text object."""
        return self._text

    @text.setter
    def text(self, value: Text) -> None:
        """Set the text object."""
        self._text = value
        self._text.update_text()

    def _draw_text(self) -> None:
        """Draw the image onto the grid."""
        self.grid.clear()
        self.grid.overlay(self._text)
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
        # if self._image.update_animation():
        self._text.update_text()
        self._draw_text()
