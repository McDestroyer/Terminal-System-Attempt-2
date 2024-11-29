from system.inputs.button import Button
from system.terminal_system.helper_objects.axis import Axis


class InputHandler:

    def __init__(self, window_name: str) -> None:
        self.kb = KeyboardInput()
        self.mouse = MouseInput(window_name)
        self.clipboard = Clipboard()

        self.screen_is_focused = True

        self.keyboard_states = None
        self.mouse_states = None

    def get_inputs(self) -> dict[str, Button | Axis | Mouse]:
        self.screen_is_focused = self.mouse.is_focused()

        if self.screen_is_focused:
            self.kb.update_inputs()
            self.keyboard_states = self.kb.get_inputs(self.screen_is_focused)
            self.mouse_states = self.mouse.update_inputs(self.screen_is_focused)
            return {**self.keyboard_states, **self.mouse_states}
