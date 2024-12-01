"""A collection of little classes that perform useful functions.

Classes:
    Toggle:
        A simple class that toggles between True and False when called and returns the relevant mapped value when cast
        to a bool, printed, or called.
    ArgumentativeFunction:
        Describes a function and the arguments to be called with it. Can be called to execute the function.
"""
import time
from typing import Callable, Any


class Toggle:
    """A simple class that toggles between True and False when called and returns the relevant mapped value when cast
    to a bool, printed, or called.

    Attributes:
        state (bool):
            The current state of the Toggle.
    """
    def __init__(self, state: bool = False, true_value: Any = True, false_value: Any = False) -> None:
        """Initialize the Toggle object.

        Args:
            state (bool, optional):
                The initial state of the Toggle.
                Defaults to False.
            true_value (Any, optional):
                The value to return when the state is True.
                Defaults to True.
            false_value (Any, optional):
                The value to return when the state is False.
                Defaults to False.
        """
        self.state: bool = state
        self._value_options: dict[bool, Any] = {
            True: true_value,
            False: false_value
        }

    @property
    def true_value(self) -> Any:
        return self._value_options[True]

    @true_value.setter
    def true_value(self, value: Any) -> None:
        self._value_options[True] = value

    @property
    def false_value(self) -> Any:
        return self._value_options[False]

    @false_value.setter
    def false_value(self, value: Any) -> None:
        self._value_options[False] = value

    def __call__(self) -> bool | Any:
        self.state = not self.state
        return self._value_options[self.state]

    def __bool__(self) -> bool | Any:
        return self._value_options[self.state]

    def __repr__(self) -> bool | Any:
        return self._value_options[self.state]

    def __str__(self) -> str:
        return str(self._value_options[self.state])

    def __eq__(self, other: Any) -> bool:
        return self._value_options[self.state] == other

    def __ne__(self, other: Any) -> bool:
        return self._value_options[self.state] != other

    def __lt__(self, other: Any) -> bool:
        return self._value_options[self.state] < other

    def __le__(self, other: Any) -> bool:
        return self._value_options[self.state] <= other

    def __gt__(self, other: Any) -> bool:
        return self._value_options[self.state] > other

    def __ge__(self, other: Any) -> bool:
        return self._value_options[self.state] >= other


class ArgumentativeFunction:
    """Describes a function and the arguments to be called with it. Can be called to execute the function.

    Attributes:
        function (Callable[[...], object]):
            The function to be stored and called.
        args (tuple):
            The arguments to be passed to the function.
        kwargs (dict):
            The keyword arguments to be passed to the function.
    """

    def __init__(self, function: Callable, *args, **kwargs) -> None:
        """Initialize the ArgumentativeFunction object.

        Args:
            function (Callable[[...], object]):
                The function to be called.
            args (Any):
                The arguments to be passed to the function.
            kwargs (Any):
                The keyword arguments to be passed to the function.
        """
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs) -> object:
        return self.function(*(self.args + args), **(self.kwargs | kwargs))


class Cycler:
    """A simple class that cycles through a list of values when called. Can be called to get the next value in the list.
    Basically a complex version of the Toggle class. Can be reversed and moved in various different step sizes.
    Modifying the list of values should be done directly to the values attribute because I couldn't be bothered to
    implement a setter for it. Just make

    Attributes:
        values (list[Any]):
            The values to cycle through.
        index (int):
            The current index in the list.

    Methods:
        reverse():
            Reverse the order of the values.
        __call__(step_size: int = 1) -> Any:
            Get the next value in the list. The step_size can be used to skip values or go backwards.
    """

    def __init__(self, values: list[Any], start_index: int = 0) -> None:
        """Initialize the Cycler object.

        Args:
            values (list[Any]):
                The values to cycle through.
            start_index (int, optional):
                The index to start at.
                Defaults to 0.
        """
        self.values = values
        self.index = start_index

    def reverse(self) -> None:
        """Reverse the order of the values."""
        self.values = self.values[::-1]

    def __call__(self, step_size: int = 1) -> Any:
        self.index = (self.index + step_size) % len(self.values)
        return self.values[self.index]

    def __bool__(self) -> Any:
        self.index = self.index % len(self.values)
        return self.values[self.index]

    def __repr__(self) -> Any:
        self.index = self.index % len(self.values)
        return self.values[self.index]

    def __str__(self) -> str:
        self.index = self.index % len(self.values)
        return str(self.values[self.index])

    def __eq__(self, other: Any) -> bool:
        self.index = self.index % len(self.values)
        return self.values[self.index] == other

    def __ne__(self, other: Any) -> bool:
        self.index = self.index % len(self.values)
        return self.values[self.index] != other

    def __lt__(self, other: Any) -> bool:
        self.index = self.index % len(self.values)
        return self.values[self.index] < other

    def __le__(self, other: Any) -> bool:
        self.index = self.index % len(self.values)
        return self.values[self.index] <= other

    def __gt__(self, other: Any) -> bool:
        self.index = self.index % len(self.values)
        return self.values[self.index] > other

    def __ge__(self, other: Any) -> bool:
        self.index = self.index % len(self.values)
        return self.values[self.index] >= other


class RateLimiter:
    """A class that limits the rate at which a program runs by sleeping a dynamic amount of time when called."""

    def __init__(self, fps: float) -> None:
        """Initialize the RateLimiter object.

        Args:
            fps (float, optional):
                The number of times per second
        """
        self._fps = fps
        self._rate = 1.0 / fps
        self.last_call = 0.0

    @property
    def fps(self) -> float:
        return self._fps

    @fps.setter
    def fps(self, value: float) -> None:
        self._fps = value
        self._rate = 1.0 / value

    def __call__(self, *args, **kwargs) -> Any:
        remaining_time = self._rate - (time.time() - self.last_call)

        if remaining_time > 0:
            time.sleep(remaining_time)
            self.last_call = time.time()

        return remaining_time


if __name__ == "__main__":
    # Test the Toggle class
    func = ArgumentativeFunction(print, "Hello, world!", "Hi", end="!")
    func()
