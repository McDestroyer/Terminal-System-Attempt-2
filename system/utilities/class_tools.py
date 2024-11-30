"""A collection of little classes that perform useful functions.

Classes:
    Toggle:
        A simple class that toggles between True and False when called and returns the current state when cast to a bool
        or printed.
    ArgumentativeFunction:
        Describes a function and the arguments to be called with it. Can be called to execute the function.
"""
from typing import Callable, Any


class Toggle:
    """A simple class that toggles between True and False when called and returns the current state when cast to a bool
    or printed.

    Attributes:
        state (bool):
            The current state of the Toggle.
    """
    def __init__(self, state: bool = False, value_map: dict[bool, Any] | None = None) -> None:
        """Initialize the Toggle object.

        Args:
            state (bool, optional):
                The initial state of the Toggle.
                Defaults to False.
            value_map (dict[bool, Any], optional):
                A dictionary mapping the state of the Toggle to a value.
                Defaults to {True: True, False: False} if not provided.
        """
        self.state = state
        self.value_options = value_map if value_map else {True: True, False: False}

    def __call__(self) -> bool | Any:
        self.state = not self.state
        return self.value_options[self.state]

    def __bool__(self) -> bool | Any:
        return self.value_options[self.state]

    def __repr__(self) -> bool | Any:
        return self.value_options[self.state]


class ArgumentativeFunction:
    """Describes a function and the arguments to be called with it. Can be called to execute the function.

    Attributes:
        func (Callable[[...], object]):
            The function to be called.
        args (tuple):
            The arguments to be passed to the function.
        kwargs (dict):
            The keyword arguments to be passed to the function.
    """

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        """Initialize the ArgumentativeFunction object.

        Args:
            func (Callable[[...], object]):
                The function to be called.
            args (Any):
                The arguments to be passed to the function.
            kwargs (Any):
                The keyword arguments to be passed to the function.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs) -> object:
        return self.func(*(self.args + args), **(self.kwargs | kwargs))


if __name__ == "__main__":
    # Test the Toggle class
    ArgumentativeFunction(print, "Hello, world!", "Hi", end="!")()
