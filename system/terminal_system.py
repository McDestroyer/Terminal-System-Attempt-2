import copy
import os
import time

from system.inputs.button import Button
from system.inputs.generic_input import GenericInput
from system.inputs.input_handler import InputHandler

from system.utilities.class_tools import RateLimiter

from system.objects.helper_objects.coordinate_objects.coordinate import Coordinate
from system.objects.helper_objects.coordinate_objects.axis import Axis
from system.objects.helper_objects.coordinate_objects.point import Point
from system.objects.helper_objects.pixel_objects.pixel_grid import PixelGrid

from system.objects.system_objects.display_manager import DisplayManager

from system.utilities import cursor
from system.utilities.color import Colors


class TerminalSystem:
    def __init__(
            self,
            name: str,
            minimum_screen_size=Point(50, 20),
            desired_fps=30,
            mouse_enabled=True,
            in_editor=True,
            ) -> None:
        """Initialize the terminal system.

        Args:
            name (str):
                The name of the terminal system.
            minimum_screen_size (Point, optional):
                The minimum screen size.
                Defaults to Point(50, 20).
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
        self._rate_limiter = RateLimiter(self.desired_fps)

        self.input_handler = InputHandler(self._name)

        screen_size = self._calibrate_screen_size()

        self._initial_pixel_grid = PixelGrid(
            coordinates=Coordinate(
                Axis(axis_size=screen_size.x),
                Axis(axis_size=screen_size.y)
            ),
            size=Coordinate(
                Axis(value=screen_size.x, axis_size=screen_size.x),
                Axis(value=screen_size.y, axis_size=screen_size.y)
            )
        )

        self.display_manager = DisplayManager(self._initial_pixel_grid)

        self._inputs: dict[GenericInput, dict[str, Button | Axis | int | Point]] = {}

        cursor.hide()

    def update(self) -> None:
        """Update the terminal objects and get inputs."""
        self.input_handler.update_inputs()
        self.inputs = self.input_handler.get_inputs()

        self.display_manager.update(self.input_handler)

    def refresh_screen(self) -> None:
        """Print the terminal objects to the terminal."""
        self.display_manager.refresh_screen()
        # self._rate_limiter()

    def shutdown(self) -> None:
        """Stop the terminal system."""
        cursor.show()
        pass

    def _calibrate_screen_size(self) -> Point:
        """Calibrate the screen size.

        Returns:
            Point: The screen size.
        """
        # Clear the screen.
        os.system("cls")

        x = 156
        y = 39

        first = True
        while True:
            # Get input
            self.input_handler.update_inputs()
            self.inputs = self.input_handler.get_inputs()

            kb = self.input_handler.kb

            up = self.inputs[kb]["up"].held
            down = self.inputs[kb]["down"].held
            left = self.inputs[kb]["left"].held
            right = self.inputs[kb]["right"].held
            finish = self.inputs[kb]["enter"].just_pressed or self.inputs[kb]["esc"].just_pressed

            # up = self.input_handler.kb.is_held("up")
            # down = self.input_handler.kb.is_held("down")
            # left = self.input_handler.kb.is_held("left")
            # right = self.input_handler.kb.is_held("right")
            # finish = self.input_handler.kb.is_newly_pressed("enter") or self.input_handler.kb.is_newly_pressed("esc")

            if finish:
                os.system("cls")
                break
            if up:
                y = max(y - 1, self._minimum_screen_size.y)
            if down:
                y += 1
            if left:
                x = max(x - 1, self._minimum_screen_size.x)
            if right:
                x += 1

            # Print
            if up or down or left or right or first:
                cursor.clear_screen()
                cursor.set_pos()
                for i in range(y):
                    if i != 0:
                        print()
                    if i == y - 1 or i == 0:
                        print(Colors.YELLOW + "█" * (x - 1) + Colors.BLUE + "█" + Colors.END, end="", flush=True)
                        continue
                    print(Colors.GREEN + "█" * (x - 1) + Colors.RED + "█" + Colors.END, end="", flush=True)
                print("x: " + str(x) + " y: " + str(y), end="", flush=True)

            first = False
            # Sleep to avoid excessive speed
            time.sleep(0.025)

        return Point(x, y + 1)

    @property
    def name(self) -> str:
        """Return the name of the terminal system.

        Returns:
            str: The name of the terminal system.
        """
        return self._name

    @property
    def minimum_screen_size(self) -> Point:
        """Return the minimum screen size.

        Returns:
            Point: The minimum screen size.
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
    def inputs(self) -> dict[GenericInput, dict[str, Button | Axis | int | Point]]:
        """Return the inputs.

        Returns:
            dict[GenericInput, dict[str, Button | Axis | int | Point]]: The inputs.
        """
        return self._inputs

    @inputs.setter
    def inputs(self, new_inputs: dict[GenericInput, dict[str, Button | Axis | int | Point]]) -> None:
        """Set the inputs.

        Args:
            new_inputs (dict[GenericInput, dict[str, Button | Axis | int | Point]]):
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
    # def minimum_screen_size(self, new_minimum_screen_size: Point) -> None:
    #     """Set the minimum screen size.
    #
    #     Args:
    #         new_minimum_screen_size (Point):
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

    @property
    def initial_pixel_grid(self) -> PixelGrid:
        """Return the initial pixel grid.

        Returns:
            PixelGrid: The initial pixel grid.
        """
        return copy.deepcopy(self._initial_pixel_grid)

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
