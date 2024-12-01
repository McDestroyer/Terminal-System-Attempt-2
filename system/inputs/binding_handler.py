import system.utilities.class_tools as tools


class Binding:
    def __init__(self, name: str, checking_function: tools.ArgumentativeFunction,
                 callback: tools.ArgumentativeFunction) -> None:
        """Initialize an instance of the class.

        Args:
            name (str):
                The unique name of the binding.
            checking_function (tools.ArgumentativeFunction):
                The function used to check if the binding should be triggered. The function should return a boolean.
            callback (tools.ArgumentativeFunction):
                The function to call when the key is pressed.
        """
        self.name = name
        self.checking_function = checking_function
        self.callback = callback

    def check(self):
        """Check if the binding should be triggered.

        Returns:
            bool:
                True if the binding should be triggered, False otherwise.
        """
        return self.checking_function()

    def __call__(self):
        self.callback()


class BindingHandler:

    def __init__(self):
        self._bindings = {}
        self._disabled = {}

    @property
    def bindings(self) -> dict[str, Binding]:
        return self._bindings

    @property
    def disabled_bindings(self) -> dict[str, Binding]:
        return self._disabled

    def trigger_bindings(self) -> None:
        """Check all bindings and trigger the ones that pass their check, calling their callback functions."""
        for binding in self._bindings.values():
            if binding.check():
                binding()

    def add_binding(self, name: str, checking_function: tools.ArgumentativeFunction,
                    callback: tools.ArgumentativeFunction) -> None:
        """Add a binding to the handler.

        Args:
            name (str):
                The unique name of the binding. Warning: If the name is not unique, the previous binding will be
                overwritten.
            checking_function (tools.ArgumentativeFunction):
                The function used to check if the binding should be triggered. The function should return a boolean.
            callback (tools.ArgumentativeFunction):
                The function to call when the key is pressed.
        """
        self._bindings[name] = Binding(name, checking_function, callback)

    def remove_binding(self, name: str) -> None:
        """Remove a binding from the handler.

        Args:
            name (str):
                The name of the binding to remove.
        """
        self._bindings.pop(name)

    def disable_binding(self, name: str) -> None:
        """Temporarily disable a binding.

        Args:
            name (str):
                The name of the binding to disable.
        """
        self._disabled[name] = self._bindings.pop(name)

    def enable_binding(self, name: str) -> None:
        """Re-enable a disabled binding.

        Args:
            name (str):
                The name of the binding to enable.
        """
        self._bindings[name] = self._disabled.pop(name)

    def disable_all_bindings(self) -> None:
        """Temporarily disable all bindings."""
        self._disabled.update(self._bindings)
        self._bindings.clear()

    def enable_all_bindings(self) -> None:
        """Re-enable all disabled bindings."""
        self._bindings.update(self._disabled)
        self._disabled.clear()

    def clear_bindings(self) -> None:
        """Clear all bindings."""
        self._bindings.clear()

    def clear_disabled_bindings(self) -> None:
        """Clear all disabled bindings."""
        self._disabled.clear()

    def clear_all(self) -> None:
        """Clear all bindings and disabled bindings."""
        self.clear_bindings()
        self.clear_disabled_bindings()

    def __getitem__(self, item: str) -> Binding:
        return self._bindings[item]

    def __setitem__(self, key: str, value: Binding) -> None:
        self._bindings[key] = value

    def __delitem__(self, key: str) -> None:
        self._bindings.pop(key)

    def __iter__(self):
        return iter(self._bindings)

    def __len__(self) -> int:
        return len(self._bindings)

    def __contains__(self, item: str) -> bool:
        return item in self._bindings

    def __str__(self) -> str:
        return str(self._bindings)

    def __repr__(self) -> str:
        return repr(self._bindings)

    def __bool__(self) -> bool:
        return bool(self._bindings)

    def __call__(self, *args, **kwargs):
        self.trigger_bindings()

    # TODO: These next two don't need to be here, they're just cool and should be copied into the utilities module
    #  eventually. They let you use the with statement to automatically create then destroy the object like so:
    #  with BindingHandler() as bh:
    #      bh.add_binding("name", function, function)
    #  .
    #  This is useless in this case, but it's a cool trick to know.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_all()
        return False

    def __del__(self):
        self.clear_all()
