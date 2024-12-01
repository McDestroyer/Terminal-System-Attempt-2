from system.inputs.button import Button
from system.inputs.generic_input import GenericInput as Input
from system.objects.helper_objects.axis import Axis

import system.inputs.keyboard_handler as keyboard
import system.inputs.mouse_handler as mouse
import system.inputs.clipboard_handler as clipboard
import system.inputs.binding_handler as binding


class InputHandler:
    """Collects mouse, keyboard, and (soon) gamepad inputs into a single place.

    Attributes:
        kb (keyboard.KeyboardHandler):
            The keyboard handler.
        mouse (mouse.MouseHandler):
            The mouse handler.
        clipboard (clipboard.Clipboard):
            The clipboard handler.
        binding_handler (binding.BindingHandler):
            The binding handler.
        screen_is_focused (bool):
            Whether the screen is focused or not.

    Methods:
        get_inputs() -> dict[str, Button | Axis | int | tuple]:
            Get the inputs from the keyboard and mouse.
    """

    def __init__(self, window_name: str) -> None:
        """Initialize the InputHandler object.

        Args:
            window_name (str):
                The name to set the window to. This is used for the mouse handler to check if the window is focused and
                for mapping the mouse to a relative position.
        """
        # Initialize the input classes.
        self.kb = keyboard.KeyboardHandler()
        self.mouse = mouse.MouseHandler(window_name)

        self.input_classes = [
            self.kb,
            self.mouse
        ]

        self.clipboard = clipboard.Clipboard()
        self.binding_handler = binding.BindingHandler()

        self.screen_is_focused = True

    def get_inputs(self) -> dict[Input, dict[str, Button | Axis | int | tuple]]:
        """Get the inputs from the keyboard and mouse.

        Returns:
            dict[Input, dict[str, Button | Axis | int | tuple]]:
                The inputs from the keyboard and mouse.
        """
        self.screen_is_focused = self.mouse.is_focused()

        # Update the inputs for all the input classes.
        for cls in self.input_classes:
            cls.update_inputs()

        if self.screen_is_focused:
            # Get the inputs from all the input classes and return them.
            input_map = {}
            for cls in self.input_classes:
                input_map[cls] = cls.get_inputs()
            return input_map

        return {}
