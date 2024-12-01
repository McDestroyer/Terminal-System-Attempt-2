import system.objects.helper_objects.coordinate as coord
from system.inputs.input_handler import InputHandler
from system.objects.helper_objects import pixel_grid, axis


class BaseObject:
    def __init__(self, name: str, description: str, initial_grid: pixel_grid.PixelGrid,
                 z_index: float = 0, visible: bool = True) -> None:
        self.name = name
        self.description = description
        self.grid = initial_grid
        self.z_index = z_index
        self.visible = visible

        self.should_draw = True
        self.mouse_over = None

    def update(self, input_handler: InputHandler) -> None:
        """Update the object based on the inputs from the input handler.

        Args:
            input_handler (InputHandler):
                The input handler.
        """
        # TODO: Update mouse_over from outside the class when the mouse is moved. We can't do it here because of the
        #       idea of pixel grids containing other pixel grids causing the loss of the absolute position of the
        #       object.
        pass

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
