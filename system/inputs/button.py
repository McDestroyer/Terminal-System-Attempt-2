import time

import keyboard

import system.utilities.class_tools as tools


class Button:
    def __init__(self, name: str, read_func: tools.ArgumentativeFunction,
                 hold_delay: float = 0.25, negated: bool = False) -> None:
        """Initialize the Button object.

        Args:
            name (str):
                The name of the button.
            read_func (class_tools.ArgumentativeFunction):
                The function to call to read the button.
            hold_delay (float, optional):
                The time in seconds to wait before the button is considered held.
                Defaults to 0.25.
            negated (bool, optional):
                Whether to invert the button state.
                Defaults to False.
        """
        self._name = name
        self._read_func = read_func
        self._hold_delay = hold_delay
        self._negated = negated

        # Initialize the button states.
        self._pressed = False
        self._held = False
        self._released = False
        self._just_pressed = False
        self._just_released = False
        self._toggled = False

        self._last_press_time = 0.0

    def update(self) -> None:
        """Update the button states."""
        # Get the current state of the button.
        state = self._read_func()

        # If the button is negated, invert the state.
        if self._negated:
            state = not state

        # Update the button states.

        # The button is considered just pressed if it was not pressed in the previous loop but is pressed now. The
        # opposite is true for just released.
        self._just_pressed = state and not self._pressed
        self._just_released = not state and self._pressed

        # Now, update whether the button is pressed, held, or released.
        self._pressed = self._read_func()
        self._released = not self._pressed

        # The button is considered held if it is pressed and the time since the last press is greater than the hold
        # delay. This is similar to pressing a key on a keyboard and holding it down to get the key repeat.
        self._held = self._pressed and (time.time() - self._last_press_time) > self._hold_delay

        # Finally, update the last press time if the button was just pressed so that the hold delay can be calculated
        # correctly.
        if self._just_pressed:
            self._toggled = not self._toggled
            self._last_press_time = time.time()

    @property
    def name(self) -> str:
        """Return the name of the button.

        Returns:
            str: The name of the button.
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Set the name of the button.

        Args:
            new_name (str):
                The new name of the button.
        """
        self._name = new_name

    @property
    def read_func(self) -> tools.ArgumentativeFunction:
        """Return the read function of the button.

        Returns:
            class_tools.ArgumentativeFunction: The read function of the button.
        """
        return self._read_func

    @read_func.setter
    def read_func(self, new_read_func: tools.ArgumentativeFunction) -> None:
        """Set the read function of the button.

        Args:
            new_read_func (class_tools.ArgumentativeFunction):
                The new read function of the button.
        """
        self._read_func = new_read_func

    @property
    def hold_delay(self) -> float:
        """Return the hold delay of the button.

        Returns:
            float: The hold delay of the button.
        """
        return self._hold_delay

    @hold_delay.setter
    def hold_delay(self, new_hold_delay: float) -> None:
        """Set the hold delay of the button.

        Args:
            new_hold_delay (float):
                The new hold delay of the button.
        """
        self._hold_delay = new_hold_delay

    @property
    def pressed(self) -> bool:
        """Return whether the button is pressed.

        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return self._pressed

    @property
    def held(self) -> bool:
        """Return whether the button is held.

        Returns:
            bool: True if the button is held, False otherwise.
        """
        return self._held

    @property
    def released(self) -> bool:
        """Return whether the button is released.

        Returns:
            bool: True if the button is released, False otherwise.
        """
        return self._released

    @property
    def just_pressed(self) -> bool:
        """Return whether the button was just pressed.

        Returns:
            bool: True if the button was just pressed, False otherwise.
        """
        return self._just_pressed

    @property
    def just_released(self) -> bool:
        """Return whether the button was just released.

        Returns:
            bool: True if the button was just released, False otherwise.
        """
        return self._just_released

    @property
    def toggled(self) -> bool:
        """Return whether the button was toggled.

        Returns:
            bool: True if the button was toggled, False otherwise.
        """
        return self._toggled

    @toggled.setter
    def toggled(self, new_toggled: bool) -> None:
        """Set whether the button was toggled.

        Args:
            new_toggled (bool):
                The new toggled state of the button.
        """
        self._toggled = new_toggled

    def __call__(self, *args, **kwargs) -> None:
        self.update()


if __name__ == '__main__':
    btn_a = Button("a", tools.ArgumentativeFunction(keyboard.is_pressed, "a"))

    while True:
        time.sleep(0.025)
        btn_a.update()
        if btn_a.held:
            print(btn_a.held)
