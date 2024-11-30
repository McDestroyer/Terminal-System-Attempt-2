import os
import time

import mouse
from pynput import mouse as mouse_suppressor
# import win32gui  # TODO: Find a way to make this work on python 3.13 and above.
import pywinctl

import system.inputs.button as button
import system.utilities.class_tools as tools
from system.utilities import rect


class MouseHandler:
    def __init__(self, window_name: str = "TerminalSystem", in_editor: bool = False) -> None:
        """Initialize an instance of the class.

        Args:
            window_name (str, optional):
                The name of the window to get inputs from.
                Defaults to "TerminalSystem".
            in_editor (bool, optional):
                Whether the program is running in the editor. WARNING: The program will crash if this is set to False
                and the program is running in the editor because the window name will not be found.
                Defaults to False.
        """
        self._window_name = window_name
        self._in_editor = in_editor

        self._window = self._get_window()

        # Get mouse inputs.
        self._wheel_delta = 0
        self._wheel_position = 0

        self._position = (0, 0)

        self._buttons = {}
        self._button_states = {}
        self._is_clicked = False

        self._inputs = {}

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
        self.listener = mouse_suppressor.Listener(win32_event_filter=self.win32_event_filter)
        self.listener.start()

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]):
        mouse.move(value[0], value[1])
        self._position = value

    def get_left_click(self) -> bool:
        return self._is_clicked

    def is_focused(self) -> bool:
        return self._window == pywinctl.getActiveWindow()

    def update_inputs(self) -> None:
        if self.is_focused():
            # Suppress the mouse if the window is focused.
            self._suppress_mouse = True
            self._is_focused = True
            self._update_window_rect()
            self._position = mouse.get_position()

            # Update the mouse inputs
            self._inputs = {
                "wheel": self._wheel_position,
                "wheel_delta": self._wheel_delta,
                "position": self._position,
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

    def get_inputs(self) -> dict[str, button.Button | int | tuple[int, int]]:
        """Get the input dictionary.

        Returns:
            dict[str, button.Button | int | tuple[int, int]]: The buttons, mouse position, wheel position/delta.
        """
        return self._inputs

    def _get_window(self) -> pywinctl.Window | None:
        """Get the window object.

        Returns:
            pywinctl.Window: The window object.
            None: If the program is running in the editor.
        """
        # If the program is running in the editor, return None because the window will not be found.
        if self._in_editor:
            return None

        # Get the windows with the name given.
        window_list = pywinctl.getWindowsWithTitle(self._window_name)

        # If there are no windows with the name, set the title of the window to the name.
        if len(window_list) == 0:
            os.system("title " + self._window_name)

        # If there is already one or more windows with the same name, append a number to the end of the name and try
        # again repeatedly until a unique name is found.
        else:
            window_name_mod = 1
            while len(window_list) > 0:
                window_name_mod += 1
                window_list = pywinctl.getWindowsWithTitle(self._window_name + str(window_name_mod))

            # Set the window name to the new name.
            self._window_name = self._window_name + " " + str(window_name_mod)
            os.system("title " + self._window_name)

        # Get the window itself.
        return window_list[0]

    def _update_window_rect(self) -> None:
        """Update the size and position of the window."""
        if self._in_editor:
            self._window_rect.set_bounds(0, 0, 0, 0)
            return

        # Update the window rect and offset the edges to account for the window border and scroll bars.
        self._window_rect.set_bounds(
            left=self._window.rect.left + self._window_rect_offsets.left,
            top=self._window.rect.top + self._window_rect_offsets.top,
            right=self._window.rect.right + self._window_rect_offsets.right,
            bottom=self._window.rect.bottom + self._window_rect_offsets.bottom,
        )

    def win32_event_filter(self, msg, _) -> bool:
        # Suppress Left click
        if (msg == 513 or msg == 514) and self._window_rect and (
                self._window_rect.left < self._position[0] < self._window_rect.right and
                self._window_rect.top < self._position[1] < self._window_rect.bottom
        ):
            self._is_clicked = True if msg == 513 else False
            self.listener.suppress_event()
        return True

    def _mouse_hook(self, event) -> None:
        """Handle the mouse events. Specifically, the wheel events."""
        if type(event) is mouse.WheelEvent:
            self._wheel_delta += event.delta
            self._wheel_position += event.delta


if __name__ == '__main__':
    m = MouseHandler()
    while True:
        time.sleep(.2)
