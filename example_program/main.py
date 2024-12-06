from system.objects.helper_objects.coordinate_objects.point import Point
from system.terminal_system import TerminalSystem


class Main:
    """Main class for the example program."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""
        self.run = True

        self._terminal = TerminalSystem(
            name="Example Program",
            minimum_screen_size=Point(50, 20),
            desired_fps=30,
            mouse_enabled=True,
            in_editor=True,
        )

        # Add the code to set up the first screen here.

        # Add the code to initialize here.

    def loop(self) -> None:
        """Run the program."""
        while self.run:
            self._terminal.update()

            # Add the code to run here.

            self._terminal.refresh_screen()

    def shutdown(self) -> None:
        """Stop the program."""
        self._terminal.shutdown()
