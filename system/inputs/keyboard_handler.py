import string
import time

import keyboard

import system.inputs.button as button
import system.utilities.class_tools as tools
from system.inputs.generic_input import GenericInput


class KeyboardHandler(GenericInput):
    """Handles the keyboard inputs for the system.

    Implements:
        GenericInput

    Properties:
        buttons (dict[str, button.Button]): The buttons.

    Methods:
        update_inputs(): Update the inputs and store the values.
        get_inputs(): Get the inputs.
        block_all(): Block all keys so that they don't do anything in the background by accident.
        unblock_all(): Unblock all keys so that they do something in the background.
    """

    # This is to get rid of a warning about the canonical names being private. I couldn't find a way to get around it.
    # noinspection PyProtectedMember
    def __init__(self):
        # Get all the button names from the keyboard module.
        button_names = list(keyboard._canonical_names.canonical_names.values())
        button_names += list(keyboard._canonical_names.canonical_names.keys())
        button_names += list(string.ascii_lowercase + string.ascii_uppercase)

        # Create a dictionary of buttons.
        self._buttons = {}

        for btn_name in button_names:

            # Check if the button is valid.
            try:
                keyboard.is_pressed(btn_name)
            except ValueError:
                continue

            # Create a getter function for the button's state.
            getter = tools.ArgumentativeFunction(keyboard.is_pressed, btn_name)
            self._buttons[btn_name] = button.Button(btn_name, getter)
            self._buttons[btn_name].update()

        # Unblockable keys.
        self._unblockable_keys = ['esc', 'tab', 'shift', 'ctrl', 'alt', 'win', 'command', 'left win', 'windows',
                                  'left windows', 'right win', 'right windows', 'right command', 'right alt',
                                  'right ctrl', 'left alt', 'left ctrl', 'option', 'right option', 'left option',
                                  'menu', 'right menu', 'left menu', 'left command', 'left control', 'right control',
                                  'control', 'escape', 'shift']
        # Weed out the unblockable keys that aren't in the button names.
        self._unblockable_keys = list(set(self._unblockable_keys).intersection(self._buttons.keys()))
        self._keys_blocked = False

        self.block_all()

    @property
    def buttons(self) -> dict[str, button.Button]:
        """Return the buttons.

        Returns:
            dict[str, button.Button]: The buttons.
        """
        return self._buttons

    @buttons.setter
    def buttons(self, value: dict[str, button.Button]) -> None:
        """Set the buttons.

        Args:
            value (dict[str, button.Button]): The buttons.
        """
        self._buttons = value

    def update_inputs(self) -> None:
        """Update the inputs and store the values."""
        # Update the buttons.
        for btn_name, btn in self._buttons.items():
            btn.update()

        # Check if any of the unblockable keys are pressed. If they are, unblock all keys in case the user is trying to
        # use a keybind.
        for key in self._unblockable_keys:
            if self._buttons[key].just_pressed:
                self.unblock_all()
                return
            if self._buttons[key].pressed:
                return

        if not self._keys_blocked:
            self.block_all()

    def get_inputs(self) -> dict[str, button.Button]:
        """Get the inputs.

        Returns:
            dict[str, button.Button]: A mapping of the button names to the button objects.
        """
        return self._buttons

    def block_all(self) -> None:
        """Block all keys so that they don't do anything in the background by accident."""
        # Get all the keys.
        keys = self.get_inputs()

        # Block all the keys.
        for key in keys:
            # Skip the unblockable keys.
            if key in self._unblockable_keys:
                continue

            keyboard.block_key(key)

        # Set the keys to blocked to avoid blocking them again unnecessarily.
        self._keys_blocked = True

    def unblock_all(self) -> None:
        """Unblock all keys so that they do something in the background."""
        # Get all the keys.
        keys = self.get_inputs()

        # Unblock all the keys.
        for key in keys:
            try:
                # This is to get rid of an incorrect warning that I found annoying.
                # noinspection PyTypeChecker
                keyboard.unblock_key(key)
            except KeyError:
                pass

        # Set the keys to unblocked to avoid unblocking them again unnecessarily.
        self._keys_blocked = False


# Test the keyboard handler.
if __name__ == "__main__":
    time.sleep(1)

    handler = KeyboardHandler()

    values = handler.get_inputs()

    while True:
        time.sleep(.01)
        handler.update_inputs()
        values = handler.get_inputs()

        for name, bttn in values.items():
            if bttn.just_pressed:
                print(f"{name}: {bttn.just_pressed}")
