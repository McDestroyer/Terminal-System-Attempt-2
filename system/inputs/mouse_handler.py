class MouseHandler:
    """A class to handle mouse input."""

    def __init__(self, window_manager: WindowManager) -> None:
        """Initialize the MouseHandler.

        Args:
            window_manager (WindowManager): The window manager.
        """
        self._window_manager = window_manager
        self._mouse = None
        self._mouse_down = False

    def handle_mouse(self, mouse: Mouse) -> None:
        """Handle mouse input.

        Args:
            mouse (Mouse): The mouse input.
        """
        self._mouse = mouse
        if mouse.left_button:
            self._mouse_down = True
        else:
            self._mouse_down = False

    def update(self) -> None:
        """Update the mouse."""
        if self._mouse is not None:
            if self._mouse_down:
                self._window_manager.current_screen.handle_mouse_down(self._mouse)
            else:
                self._window_manager.current_screen.handle_mouse_up(self._mouse)
            self._mouse = None