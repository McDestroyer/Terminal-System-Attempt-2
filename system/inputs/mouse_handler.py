import os
import time

import subprocess
import socket

import mouse
# from pynput import mouse as mouse_suppressor
# import win32gui  # TODO: Find a way to make this work on python 3.13 and above or the the editor.
# from pywinctl import Window, getWindowsWithTitle, getActiveWindow
from pygetwindow import Window, getWindowsWithTitle, getActiveWindowTitle

from system.inputs.generic_input import GenericInput
import system.inputs.button as button
import system.utilities.class_tools as tools
import system.utilities.rect as rect
import system.objects.helper_objects.coordinate_objects.coordinate as coord
import system.objects.helper_objects.coordinate_objects.axis as axis
from system.objects.helper_objects.coordinate_objects.point import Point


class MouseHandler(GenericInput):
    """Handles the mouse inputs.

    Implements:
        GenericInput

    Properties:
        position (Point): The position of the mouse.

    Methods:
        get_left_click: Get the state of the left click.
        is_focused: Whether the window is focused or not.
        update_inputs: Update the inputs dictionary and refresh the window rect.
        get_inputs: Get the input dictionary.

    """
    def __init__(self, window_name: str = "TerminalSystem", screen_size: coord.Coordinate = coord.Coordinate(),
                 in_editor: bool = False) -> None:
        """Initialize an instance of the class.

        Args:
            window_name (str, optional):
                The name of the window to get inputs from.
                Defaults to "TerminalSystem".
            screen_size (coord.Coordinate, optional):
                The size of the screen. Used to calculate the position of the mouse in characters. Only ignored if the
                program is running in the editor.
            in_editor (bool, optional):
                Whether the program is running in the editor. WARNING: The program will crash if this is set to False
                and the program is running in the editor because the window name will not be found.
                Defaults to False.
        """
        self._window_name = window_name
        self._screen_size = screen_size
        self._in_editor = in_editor

        self._window = self._get_window()

        # Get mouse inputs.
        self._wheel_delta = 0
        self._wheel_position = 0

        self._absolute_position = Point(0, 0)
        self._mouse_char_position = coord.Coordinate(
            axis.Axis(0, axis_size=self._screen_size.x_char),
            axis.Axis(0, axis_size=self._screen_size.y_char)
        )

        self._buttons = {}
        self._button_states = {}
        self._is_clicked = False

        self._inputs: dict[str, button.Button | int | Point] = {}

        # Create the buttons.
        for btn in [mouse.RIGHT, mouse.MIDDLE, mouse.X, mouse.X2]:
            func = tools.ArgumentativeFunction(mouse.is_pressed, btn)
            self._buttons[btn] = button.Button(btn, func)

        # The left click is a special case because it is blocked by the click suppressor.
        self._buttons[mouse.LEFT] = button.Button(mouse.LEFT, tools.ArgumentativeFunction(self.get_left_click))

        # Deal with the window.
        self._is_focused = False
        self._window_rect: rect.Rect = rect.Rect(0, 0, 0, 0)
        self._window_rect_offsets: rect.Rect = rect.Rect(10, 40, -35, -30)
        self._update_window_rect()

        # Suppress the mouse.
        self._suppress_mouse = False
        self._was_suppressed = False
        # self.listener = mouse_suppressor.Listener(win32_event_filter=self._win32_event_filter)
        # self.listener.start()

        # Start the mouse listener in a different Python version
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'prototype_mouse_blocker.py')
        self._suppressor_process = subprocess.Popen(
            args=['python', path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # time.sleep(1)
        # Create a persistent socket connection
        self._suppressor_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._suppressor_connection.connect(('localhost', 65432))

    def send_command(self, cmd: str) -> None:
        """Send a command to the mouse suppressor.

        Args:
            cmd (str): The command to send.
        """
        self._suppressor_connection.sendall(cmd.encode())

    def receive_response(self) -> str:
        """Receive a response from the mouse suppressor.

        Returns:
            str: The response.
        """
        return self._suppressor_connection.recv(1024).decode()

    @property
    def position(self) -> Point:
        return self._absolute_position

    @position.setter
    def position(self, value: Point):
        mouse.move(value.x, value.y)
        self._absolute_position = value

    def get_left_click(self) -> bool:
        return self._is_clicked

    def is_focused(self) -> bool:
        """Whether the window is focused or not.

        Returns:
            bool: Whether the window is focused or not.
        """
        return self._window.title == getActiveWindowTitle()

    def _get_mouse_relative_position(self) -> Point:
        """Get the mouse position relative to the window.

        Returns:
            Point: The mouse position relative to the window.
        """
        return Point(
            self._absolute_position.x - self._window_rect.left,
            self._absolute_position.y - self._window_rect.top
        )

    def _get_mouse_char_position(self) -> coord.Coordinate:
        """Get the mouse position in characters.

        Returns:
            coord.Coordinate: The mouse position in characters.
        """
        # Get the position of the mouse relative to the window.
        rel_pos = self._get_mouse_relative_position()

        # Get the screen width and height in simplified terms.
        pixel_width = self._window_rect.right - self._window_rect.left
        pixel_height = self._window_rect.bottom - self._window_rect.top

        char_width = self._mouse_char_position.screen_size[0]
        char_height = self._mouse_char_position.screen_size[1]

        # Get the normalized position.
        normal_x = float(rel_pos[0]) / float(pixel_width)
        normal_y = float(rel_pos[1]) / float(pixel_height)

        # Get the character position.
        char_pos_x = int(normal_x * char_width)
        char_pos_y = int(normal_y * char_height)

        # Convert to axes.
        self._mouse_char_position.x_axis.value = char_pos_x
        self._mouse_char_position.y_axis.value = char_pos_y

        return self._mouse_char_position

    def update_inputs(self) -> None:
        """Update the inputs dictionary and refresh the window rect."""
        if self.is_focused():
            # Suppress the mouse if the window is focused.
            self._suppress_mouse = True
            self._is_focused = True
            self._update_window_rect()
            self._absolute_position = Point(mouse.get_position())

            # Update the mouse inputs
            self._inputs = {
                "wheel": self._wheel_position,
                "wheel_delta": self._wheel_delta,
                "position": self._absolute_position,
                "char_position": self._get_mouse_char_position()
            }

            for btn in self._buttons:
                self._buttons[btn].update()
                self._inputs[btn] = self._buttons[btn]

            # Reset the wheel delta after the inputs have been updated.
            self._wheel_delta = 0
        else:
            self._suppress_mouse = False
            self._is_focused = False

            # Empty the inputs if the window is not focused.
            self._inputs = {}

            # Update the buttons anyway.
            for btn in self._buttons:
                self._buttons[btn].update()

            # Reset the wheel delta after the inputs have been updated.
            self._wheel_delta = 0

        self._update_suppressor()

    def _update_suppressor(self) -> None:
        """Update the mouse suppressor."""
        if self._suppress_mouse and not self._was_suppressed:
            self.send_command("start")
        elif not self._suppress_mouse and self._was_suppressed:
            self.send_command("stop")
        self._was_suppressed = self._suppress_mouse

        self.send_command("update_window_rect: " + str(self._window_rect.left) + " " + str(self._window_rect.top) + " "
                          + str(self._window_rect.right) + " " + str(self._window_rect.bottom))
        self.send_command("update_mouse_position: " + str(self._absolute_position.x) + " " +
                          str(self._absolute_position.y))

        response = self.receive_response().lower().strip()
        if response.startswith("mouse_clicked"):
            if response.endswith("true"):
                self._is_clicked = True
            elif response.endswith("false"):
                self._is_clicked = False
            else:
                raise ValueError("Unexpected response from mouse suppressor.")
        else:
            raise ValueError("Unexpected response from mouse suppressor.")

    def get_inputs(self) -> dict[str, button.Button | int | Point]:
        """Get the input dictionary.

        Returns:
            dict[str, button.Button | int | Point]: The buttons, mouse position, wheel position/delta.
        """
        return self._inputs

    def _get_window(self) -> Window | None:
        """Get the window object.

        Returns:
            Window: The window object.
            None: If the program is running in the editor.
        """
        # If the program is running in the editor, return None because the window will not be found.
        if self._in_editor:
            return None

        # Get the windows with the name given.
        window_list = getWindowsWithTitle(self._window_name)

        # If there are no windows with the name, set the title of the window to the name.
        if len(window_list) == 0:
            os.system("title " + self._window_name)

        # If there is already one or more windows with the same name, append a number to the end of the name and try
        # again repeatedly until a unique name is found.
        else:
            window_name_mod = 1
            while len(window_list) > 0:
                window_name_mod += 1
                window_list = getWindowsWithTitle(self._window_name + str(window_name_mod))

            # Set the window name to the new name.
            self._window_name = self._window_name + " " + str(window_name_mod)
            os.system("title " + self._window_name)

        # Get the window itself.
        window_list = getWindowsWithTitle(self._window_name)

        return window_list[0]

    def _update_window_rect(self) -> None:
        """Update the size and position of the window."""
        if self._in_editor:
            self._window_rect.set_bounds(0, 0, 0, 0)
            return

        # Update the window rect and offset the edges to account for the window border and scroll bars.
        self._window_rect.set_bounds(
            left=self._window.left + self._window_rect_offsets.left,
            top=self._window.top + self._window_rect_offsets.top,
            right=self._window.right + self._window_rect_offsets.right,
            bottom=self._window.bottom + self._window_rect_offsets.bottom,
        )

    # def _win32_event_filter(self, msg, _) -> bool:
    #     """Filter the win32 events.
    #
    #     Args:
    #         msg (int):
    #             The message of the event.
    #         _ (int):
    #             The data of the event.
    #
    #     Returns:
    #         bool: Whether the event was filtered or not.
    #     """
    #     # Suppress Left click
    #     if (msg == 513 or msg == 514) and self._window_rect and (
    #             self._window_rect.left < self._absolute_position[0] < self._window_rect.right and
    #             self._window_rect.top < self._absolute_position[1] < self._window_rect.bottom
    #     ):
    #         self._is_clicked = True if msg == 513 else False
    #         self.listener.suppress_event()
    #     return True

    def _mouse_hook(self, event) -> None:
        """Handle the mouse events. Specifically, the wheel events."""
        if type(event) is mouse.WheelEvent:
            self._wheel_delta += event.delta
            self._wheel_position += event.delta

    def shutdown(self) -> None:
        """Shutdown the mouse handler."""
        # self.listener.stop()
        # Close the connection to the mouse listener
        self.send_command("exit")
        self._suppressor_connection.close()

        self._suppressor_process.kill()
        mouse.unhook_all()

    def __del__(self) -> None:
        self.shutdown()


if __name__ == '__main__':
    m = MouseHandler()
    while True:
        time.sleep(.2)
