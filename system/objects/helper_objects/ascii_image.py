from system.objects.helper_objects import pixel_grid


class Image(pixel_grid.PixelGrid):
    """The Image class for displaying an image on the terminal."""

    def __init__(self, width: int, height: int, image: list[list[str]]) -> None:
        """Initialize the Image object.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            image (list[list[str]]): The image to display.
        """
        super().__init__(width, height)
        self.image = image

        self._generate_image()

    def _generate_image(self) -> None:
        """Generate the image."""
        for y, row in enumerate(self.image):
            for x, pixel in enumerate(row):
                self.grid[y][x] = pixel

    def get_image(self) -> list[list[str]]:
        """Get the image."""
        return self.image
