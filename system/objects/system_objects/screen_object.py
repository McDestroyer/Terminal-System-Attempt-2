from system.inputs.input_handler import InputHandler
from system.objects.helper_objects.coordinate_objects.point import Point
from system.objects.helper_objects.pixel_objects.pixel_grid import PixelGrid
from system.objects.terminal_objects.base_object import BaseObject
from system.objects.terminal_objects.cursor_object import CursorObject


class Screen:
    """A screen object. This object is used to manage terminal objects on the screen.

    Attributes:
        name (str):
            The name of the screen.
        screen_grid (PixelGrid):
            The grid that represents the screen.
        terminal_objects (list[BaseObject]):
            The terminal objects on the screen.
        mouse (CursorObject | None):
            The cursor object.
        should_draw (bool):
            Whether the screen should be redrawn.

        Methods:
            update(input_handler: InputHandler) -> None:
                Update the screen objects based on the input handler.
            draw() -> None:
                Update the screen grid if needed.
            add_object(obj: BaseObject) -> None:
                Add an object to the screen.
            remove_object(obj: BaseObject) -> None:
                Remove an object from the screen.
            get_object_by_coordinates(coordinates: Point) -> BaseObject | None:
                Get an object by its coordinates.
            get_object_by_name(name: str) -> BaseObject | None:
                Get an object by its name.
    """

    def __init__(self, name: str, screen_grid: PixelGrid) -> None:
        """Initialize the Screen object.

        Args:
            name (str):
                The name of the screen.
        """
        self.name: str = name
        self.screen_grid: PixelGrid = screen_grid

        self.terminal_objects: list[BaseObject] = []

        self.mouse: CursorObject | None = None

        self.should_draw: bool = False

    def update(self, input_handler: InputHandler) -> None:
        """Update the screen objects based on the input handler.

        Args:
            input_handler (InputHandler):
                The input handler to get inputs from.
        """
        self._handle_mouse(input_handler)

        for obj in self.terminal_objects:
            obj.update(input_handler)
            if obj.should_draw:
                self.should_draw = True

    def draw(self) -> None:
        """Update the screen grid if needed."""
        if self.should_draw:
            self._refresh()

    def add_object(self, obj: BaseObject) -> None:
        """Add an object to the screen.

        Args:
            obj (obj.BaseObject):
                The object to add to the screen.
        """
        self.terminal_objects.append(obj)
        self.terminal_objects.sort(key=lambda x: x.z_index)
        self.should_draw = obj.visible

    def remove_object(self, obj: BaseObject) -> None:
        """Remove an object from the screen.

        Args:
            obj (obj.BaseObject):
                The object to remove from the screen.
        """
        self.should_draw = obj.visible
        self.terminal_objects.remove(obj)

    def _handle_mouse(self, input_handler: InputHandler) -> None:
        """Handle the mouse input.

        Args:
            input_handler (InputHandler):
                The input handler to get inputs from.
        """
        if self.mouse is not None:
            self.mouse.update(input_handler)
            if self.mouse.should_draw:
                self.should_draw = True

            cursor_pos = input_handler.get_inputs()[input_handler.mouse]["char_position"]

            if cursor_pos is not None:
                self.mouse.coordinates = cursor_pos
                self.mouse.visible = True
            else:
                self.mouse.visible = False

            hovered_obj: BaseObject = self.get_object_by_coordinates(cursor_pos)

            if hovered_obj is not None:
                hovered_obj.mouse_over = Point(
                    cursor_pos[0] - hovered_obj.grid.coordinates.char_y,
                    cursor_pos[1] - hovered_obj.grid.coordinates.char_x
                )

    def get_object_by_coordinates(self, coordinates: Point) -> BaseObject | None:
        """Get an object by its coordinates.

        Args:
            coordinates (Point):
                The coordinates to get the object at.

        Returns:
            BaseObject | None:
                The object at the specified coordinates, or None if there isn't one.
        """
        for obj in self.terminal_objects:
            if obj.grid.coordinates.char_y <= coordinates[0] < obj.grid.coordinates.char_y + obj.grid.height:
                if obj.grid.coordinates.char_x <= coordinates[1] < obj.grid.coordinates.char_x + obj.grid.width:
                    return obj
        return None

    def get_object_by_name(self, name: str) -> BaseObject | None:
        """Get an object by its name.

        Args:
            name (str):
                The name of the object to get.

        Returns:
            BaseObject | None:
                The object with the specified name, or None if it doesn't exist.
        """
        for obj in self.terminal_objects:
            if obj.name == name:
                return obj
        return None

    def _refresh(self) -> None:
        """Refresh the grid."""
        self.screen_grid.clear()
        for obj in self.terminal_objects:
            self.screen_grid.overlay(obj.grid)
            obj.should_draw = False
        self.should_draw = False

