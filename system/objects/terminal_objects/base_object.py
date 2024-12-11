import system.objects.helper_objects.coordinate_objects.coordinate as coord
from system.inputs.input_handler import InputHandler
from system.objects.helper_objects.pixel_objects import pixel_grid
from system.objects.helper_objects.coordinate_objects.point import Point


class BaseObject:
    def __init__(self, name: str, description: str, initial_grid: pixel_grid.PixelGrid,
                 z_index: float = 0, visible: bool = True) -> None:
        """Initialize the object.

        Args:
            name (str):
                The name of the object.
            description (str):
                The description of the object.
            initial_grid (PixelGrid):
                The initial grid of the object.
            z_index (float, optional):
                The z-index of the object.
                Defaults to 0.
            visible (bool, optional):
                Whether the object is visible.
                Defaults to True.
        """
        self.name = name
        self.description = description
        self._grid = initial_grid
        self._z_index = z_index
        self.visible = visible

        self.should_draw = True
        self._mouse_over: Point | None = None

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value: pixel_grid.PixelGrid):
        self._grid = value
        self.should_draw = True

    @property
    def z_index(self):
        return self._z_index

    @z_index.setter
    def z_index(self, value: float):
        self._z_index = value
        self.should_draw = True

    @property
    def mouse_over(self):
        return self._mouse_over

    @mouse_over.setter
    def mouse_over(self, value: Point | None):
        self._mouse_over = value

    def update(self, input_handler: InputHandler) -> bool:
        """Update the object based on the inputs from the input handler.

        Args:
            input_handler (InputHandler):
                The input handler.
        """
        # TODO: Update mouse_over from outside the class when the mouse is moved. We can't do it here because of the
        #       idea of pixel grids containing other pixel grids causing the loss of the absolute position of the
        #       object.
        return self.should_draw

    def move(self, new_position: coord.Coordinate) -> None:
        """Move the object to the new position.

        Args:
            new_position (Coordinate):
                The new position of the object.
        """
        self.grid.coordinates = new_position
        self.should_draw = True

    def resize(self, new_size: coord.Coordinate) -> None:
        """Resize the object to the new size.

        Args:
            new_size (Coordinate):
                The new size of the object.
        """
        self.grid.size = new_size
        self.should_draw = True

    def draw(self) -> pixel_grid.PixelGrid:
        """Return the grid of the object and set should_draw to False.

        Returns:
            PixelGrid: The grid of the object.
        """
        self.should_draw = False
        return self.grid

    def __str__(self):
        return f"{self.name} is {self.description} at {self.grid.coordinates} with size {self.grid.size}."

    def __repr__(self):
        return f"{self.name} is {self.description} at {self.grid.coordinates} with size {self.grid.size}."

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return self.grid != other.grid

    def __lt__(self, other):
        return self.z_index < other.z_index

    def __le__(self, other):
        return self.z_index <= other.z_index

    def __gt__(self, other):
        return self.z_index > other.z_index

    def __ge__(self, other):
        return self.z_index >= other.z_index

    def __copy__(self):
        return BaseObject(self.name, self.description, self.grid, self.z_index, self.visible)

    def __deepcopy__(self, memo_dict):
        return BaseObject(self.name, self.description, self.grid, self.z_index, self.visible)

    def __call__(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def __hash__(self):
        return hash(self.grid)

    def __bool__(self):
        return self.visible
