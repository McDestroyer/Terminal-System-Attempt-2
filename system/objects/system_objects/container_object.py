import copy

from system.inputs.input_handler import InputHandler
from system.objects.helper_objects.pixel_objects import pixel_grid
from system.objects.helper_objects.coordinate_objects.point import Point
from system.objects.terminal_objects.base_object import BaseObject
from system.utilities.rect import Rect


class ContainerObject(BaseObject):
    def __init__(self, name: str, description: str, objects: list[BaseObject], initial_grid: pixel_grid.PixelGrid,
                 z_index: float = 0, visible: bool = True) -> None:
        """Initialize the ImageObject object.

        Args:
            name (str):
                The name of the object.
            description (str):
                The description of the object.
            objects (list[BaseObject]):
                The objects to display on the container.
            initial_grid (PixelGrid):
                The initial grid to display the image on.
            z_index (float, optional):
                The z-index of the object.
                Defaults to 0.
            visible (bool, optional):
                Whether the object is visible.
                Defaults to True.
        """
        super().__init__(
            name=name,
            description=description,
            initial_grid=initial_grid,
            z_index=z_index,
            visible=visible,
        )

        self._objects = copy.deepcopy(objects)

        self._update_grid()

    @property
    def objects(self) -> list[BaseObject]:
        """The objects in the container.

        Returns:
            list[BaseObject]:
                The objects in the container.
        """
        return self._objects

    @objects.setter
    def objects(self, value: list[BaseObject]) -> None:
        """Set the objects in the container.

        Args:
            value (list[BaseObject]):
                The objects to set in the container.
        """
        self._objects = value
        self._update_grid()

    @objects.deleter
    def objects(self) -> None:
        """Delete the objects in the container."""
        self._objects = []
        self._update_grid()

    @BaseObject.mouse_over.setter
    def mouse_over(self, value: Point | None) -> None:
        """Set the mouse over state of the object.

        Args:
            value (Point | None):
                The new mouse over state.
        """
        self._mouse_over = value

        # Sort the objects by z-index so that they are checked in the correct order.
        self._objects.sort(key=lambda x: x.z_index)

        # If the value is None, set all objects to have the mouse over state as None.
        if value is None:
            for obj in self._objects:
                obj.mouse_over = value
            return

        # Check if the mouse is over any of the objects, and set the mouse over state of the object to the first object
        # that the mouse is over.
        hovered_obj = False

        for obj in self._objects:
            if not hovered_obj and obj.visible and obj.grid:
                obj_rect = Rect(
                    left=obj.grid.coordinates.x_char,
                    right=obj.grid.coordinates.x_char + obj.grid.size.x_char,
                    top=obj.grid.coordinates.y_char,
                    bottom=obj.grid.coordinates.y_char + obj.grid.size.y_char,
                )

                if obj_rect.inside(int(self._mouse_over.x), int(self._mouse_over.y)):
                    obj.mouse_over = value

            else:
                obj.mouse_over = None

    def add_object(self, obj: BaseObject) -> None:
        """Add an object to the container.

        Args:
            obj (BaseObject):
                The object to add.
        """
        self._objects.append(obj)
        self._update_grid()

    def remove_object(self, obj: BaseObject) -> None:
        """Remove an object from the container.

        Args:
            obj (BaseObject):
                The object to remove.
        """
        self._objects.remove(obj)
        self._update_grid()

    def _update_grid(self) -> None:
        """Update the grid to display the contained objects."""
        # If no objects are visible or have changed, there is no need to update the grid.
        should_update = False

        for obj in self._objects:
            if obj.visible and obj.should_draw:
                should_update = True

        if not should_update:
            return

        # Sort the objects by z-index so that they are drawn in the correct order.
        self._objects.sort(key=lambda x: x.z_index)

        # Create a copy of the grid to have something to compare the new grid to.
        initial_grid = copy.deepcopy(self.grid)

        # Clear the grid.
        self.grid.clear()

        # Overlay the objects on the grid.
        for obj in self._objects:
            if obj.visible:
                self.grid.overlay(obj.grid)

        # Check if the grid has changed. We can't just check if any pixels changed as they are overlayed because adding
        # an object to the container will change the grid even if adding another later would put it back to how it was
        # before.
        if self.grid != initial_grid:
            self.should_draw = True

    def update(self, input_handler: InputHandler) -> None:
        """Update the object based on the inputs from the input handler.

        Args:
            input_handler (InputHandler):
                The input handler.
        """
        # This should be called first in this method in any child classes of BaseObject.
        super().update(input_handler)

        # Update all sub-objects.
        for obj in self._objects:
            obj.update(input_handler)

        # Make sure the grid is updated for printing.
        self._update_grid()
