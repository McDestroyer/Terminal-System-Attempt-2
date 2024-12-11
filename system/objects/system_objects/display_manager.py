from system.inputs.input_handler import InputHandler

from system.objects.helper_objects.coordinate_objects.axis import Axis
from system.objects.helper_objects.coordinate_objects.coordinate import Coordinate
from system.objects.helper_objects.ascii_image import Image
from system.objects.helper_objects.pixel_objects.pixel_grid import PixelGrid

from system.objects.system_objects.display import Display
from system.objects.system_objects.screen_object import Screen

from system.objects.terminal_objects.cursor_object import CursorObject


class DisplayManager:
    def __init__(self, display_grid: PixelGrid) -> None:
        """Initialize an instance of the DisplayManager (formerly WindowManager) class.

        Args:
            display_grid (PixelGrid):
                The basic grid defining the display.
        """
        self._display_grid = display_grid

        self._display: Display = Display(self._display_grid)
        self._screens: dict[str, Screen] = {}
        self._current_screen: Screen | None = None

        self.mouse = None

    def add_screen(self, screen: Screen) -> None:
        self._screens[screen.name] = screen

    def set_current_screen(self, screen_name: str) -> None:
        self._current_screen = self._screens[screen_name]

    def get_current_screen(self) -> Screen:
        return self._current_screen

    def get_screen(self, screen_name: str) -> Screen:
        return self._screens[screen_name]

    def set_up_mouse(self, cursor_image: str | list[PixelGrid] | Image) -> None:
        """Set up the mouse cursor.

        Args:
            cursor_image (str | PixelGrid | Image):
                The image to use as the cursor.
        """
        if not isinstance(cursor_image, Image):
            cursor_image = Image(
                Coordinate(
                    Axis(0, axis_size=self._display_grid.screen_size.x),
                    Axis(0, axis_size=self._display_grid.screen_size.y)
                ),
                cursor_image
            )
        self.mouse = CursorObject(cursor_image)

        self._current_screen.mouse = self.mouse

    def refresh_screen(self) -> None:
        """Refresh the screen."""
        if self._current_screen is not None:
            self._current_screen.draw()

            self._display.update_display_grid(self._current_screen.screen_grid)

    def update(self, input_handler: InputHandler) -> None:
        """Update the screen and all of its objects.

        Args:
            input_handler (InputHandler):
                The input handler to use.
        """
        if self._current_screen is not None:
            self._current_screen.update(input_handler)
