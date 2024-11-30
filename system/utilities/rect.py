class Rect:

    def __init__(self, left: int, top: int, right: int, bottom: int) -> None:
        """Initialize the Rect object.

        Args:
            left (int):
                The left of the rectangle.
            top (int):
                The top of the rectangle.
            right (int):
                The right of the rectangle.
            bottom (int):
                The bottom of the rectangle.
        """
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def set_bounds(self, left: int, top: int, right: int, bottom: int) -> None:
        """Set the boundaries of the rectangle.

        Args:
            left (int):
                The left of the rectangle.
            top (int):
                The top of the rectangle.
            right (int):
                The right of the rectangle.
            bottom (int):
                The bottom of the rectangle.
        """
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def inside(self, x: int, y: int) -> bool:
        """Return whether the point is inside the rectangle.

        Args:
            x (int):
                The x-coordinate of the point.
            y (int):
                The y-coordinate of the point.

        Returns:
            bool:
                Whether the point is inside the rectangle.
        """
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def intersect(self, other: "Rect") -> bool:
        """Return whether the rectangles intersect.

        Args:
            other (Rect):
                The other rectangle.

        Returns:
            bool:
                Whether the rectangles intersect.
        """
        if not isinstance(other, Rect):
            raise TypeError("The other object must be a Rect object.")

        if (self.left < other.right and
                self.right > other.left and
                self.top < other.bottom and
                self.bottom > other.top):
            return True
        return False

    def move(self, dx: int, dy: int) -> None:
        """Move the rectangle.

        Args:
            dx (int):
                The amount to move the rectangle in the x-direction.
            dy (int):
                The amount to move the rectangle in the y-direction.
        """
        self.left += dx
        self.right += dx
        self.top += dy
        self.bottom += dy

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"Rect({self.top}, {self.left}, {self.right}, {self.bottom})"
