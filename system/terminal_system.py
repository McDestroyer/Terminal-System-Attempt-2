from system.inputs.input_handler import InputHandler
import system.utilities.class_tools as tools
from system.objects.helper_objects import pixel_grid, coordinate as coord, axis
from system.objects.system_objects.display_manager import DisplayManager


class TerminalSystem:
    def __init__(
            self,
            name: str,
            minimum_screen_size=(50, 20),
            desired_fps=30,
            mouse_enabled=True,
            in_editor=True,
            ) -> None:
        """Initialize the terminal system.

        Args:
            name (str):
                The name of the terminal system.
            minimum_screen_size (tuple[int, int], optional):
                The minimum screen size.
                Defaults to (50, 20).
            desired_fps (int, optional):
                The desired FPS.
                Defaults to 30.
            mouse_enabled (bool, optional):
                True if the mouse is enabled, False otherwise.
                Defaults to True.
            in_editor (bool, optional):
                True if the terminal system is in the editor, False otherwise. This disables certain features like
                the mouse.
                Defaults to True.
        """
        self._name = name
        self._minimum_screen_size = minimum_screen_size
        self._desired_fps = desired_fps
        self._mouse_enabled = mouse_enabled
        self._in_editor = in_editor

        self.run: bool = True
        self._rate_limiter = tools.RateLimiter(self.desired_fps)

        self._initial_pixel_grid = pixel_grid.PixelGrid(
            coordinates=coord.Coordinate(
                axis.Axis(axis_size=minimum_screen_size[0]),
                axis.Axis(axis_size=minimum_screen_size[1])
            ),
            size=coord.Coordinate(
                axis.Axis(value=minimum_screen_size[0], axis_size=minimum_screen_size[0]),
                axis.Axis(value=minimum_screen_size[1], axis_size=minimum_screen_size[1])
            )
        )

        self.input_handler = InputHandler(self._name)
        self.display_manager = DisplayManager(self._initial_pixel_grid)

        self._inputs = {}

    def update(self) -> None:
        """Update the terminal objects and get inputs."""
        self.inputs = self.input_handler.get_inputs()
        self.display_manager.update()

    def refresh_screen(self) -> None:
        """Print the terminal objects to the terminal."""
        # TODO: Implement actually printing stuff here.
        self._rate_limiter()

    def shutdown(self) -> None:
        """Stop the terminal system."""
        pass

    @property
    def name(self) -> str:
        """Return the name of the terminal system.

        Returns:
            str: The name of the terminal system.
        """
        return self._name

    @property
    def minimum_screen_size(self) -> tuple[int, int]:
        """Return the minimum screen size.

        Returns:
            tuple[int, int]: The minimum screen size.
        """
        return self._minimum_screen_size

    @property
    def desired_fps(self) -> int:
        """Return the desired FPS.

        Returns:
            int: The desired FPS.
        """
        return self._desired_fps

    @property
    def mouse_enabled(self) -> bool:
        """Return whether the mouse is enabled.

        Returns:
            bool: True if the mouse is enabled, False otherwise.
        """
        return self._mouse_enabled

    @property
    def in_editor(self) -> bool:
        """Return whether the terminal system is in the editor.

        Returns:
            bool: True if the terminal system is in the editor, False otherwise.
        """
        return self._in_editor

    @property
    def inputs(self) -> dict[str, str]:
        """Return the inputs.

        Returns:
            dict[str, str]: The inputs.
        """
        return self._inputs

    @inputs.setter
    def inputs(self, new_inputs: dict[str, str]) -> None:
        """Set the inputs.

        Args:
            new_inputs (dict[str, str]):
                The new inputs.
        """
        self._inputs = new_inputs

    # TODO: Implement these.
    # @name.setter
    # def name(self, new_name: str) -> None:
    #     """Set the name of the terminal system.
    #
    #     Args:
    #         new_name (str):
    #             The new name of the terminal system.
    #     """
    #     self._name = new_name
    #
    #     self.input_handler.mouse._window_name = new_name

    # @minimum_screen_size.setter
    # def minimum_screen_size(self, new_minimum_screen_size: tuple[int, int]) -> None:
    #     """Set the minimum screen size.
    #
    #     Args:
    #         new_minimum_screen_size (tuple[int, int]):
    #             The new minimum screen size.
    #     """
    #     self._minimum_screen_size = new_minimum_screen_size
    #
    @desired_fps.setter
    def desired_fps(self, new_desired_fps: int) -> None:
        """Set the desired FPS.

        Args:
            new_desired_fps (int):
                The new desired FPS.
        """
        self._desired_fps = new_desired_fps
        self._rate_limiter.fps = self._desired_fps

    @mouse_enabled.setter
    def mouse_enabled(self, new_mouse_enabled: bool) -> None:
        """Set whether the mouse is enabled.

        Args:
            new_mouse_enabled (bool):
                True if the mouse is enabled, False otherwise.
        """
        self._mouse_enabled = new_mouse_enabled
        self.input_handler.mouse.enabled = self._mouse_enabled
        # TODO: Implement this.

    # This should never be modified by the user after being set.
    # @in_editor.setter
    # def in_editor(self, new_in_editor: bool) -> None:
    #     """Set whether the terminal system is in the editor.
    #
    #     Args:
    #         new_in_editor (bool):
    #             True if the terminal system is in the editor, False otherwise.
    #     """
    #     self._in_editor = new_in_editor
