import system.inputs.input_handler as input_handler


class TerminalSystem:
    def __init__(self, name: str) -> None:
        self._name = name

        self.run = True

        self.input_handler = input_handler.InputHandler(self._name)

        self.inputs = {}

    def update(self) -> None:
        """Update the terminal objects and get inputs."""
        self.inputs = self.input_handler.get_inputs()

    def refresh_screen(self) -> None:
        """Print the terminal objects to the terminal."""
        pass

    def shutdown(self) -> None:
        """Stop the terminal system."""
        pass
