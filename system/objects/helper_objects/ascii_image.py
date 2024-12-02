import copy
import time

from system.objects.helper_objects import pixel_grid, pixel, coordinate as coord, axis
from system.utilities.color import Colors


class Image(pixel_grid.PixelGrid):
    """The Image class for displaying an image on the terminal."""

    def __init__(self, position: coord.Coordinate, image_frames: list[list[list[pixel.Pixel]]] | str) -> None:
        """Initialize the Image object.

        Args:
            position (coord.Coordinate):
                The position of the image.
            image_frames (list[list[list[pixel.Pixel]]] | str):
                The image frames to display. If a string is passed, it will be assumed to be a path to an image file.
        """
        self._given_image_frames = image_frames

        # Initialize the frame handling variables.
        self._frame_count = 1
        self._fps = 0
        self._frame_delay = 0

        self._current_frame = 0
        self._last_frame_time = time.time()

        # Check if the frames are a string or a list. If it's a string, create the image from the file.
        if isinstance(self._given_image_frames, str):
            self._frames: list[list[list[pixel.Pixel]]] = self._get_grids_from_file(self._given_image_frames)
        else:
            self._frames: list[list[list[pixel.Pixel]]] = self._given_image_frames

        # Get the size of the first frame to set the size of the image.
        size = coord.Coordinate(
            axis.Axis(len(self._frames[0][0]), axis_size=position.screen_size[0]),
            axis.Axis(len(self._frames[0]), axis_size=position.screen_size[1]),
        )

        # Initialize the PixelGrid object with the coordinates, size, and grid of the image.
        super().__init__(position, size)

        # Set the grid to the first frame.
        self.grid = self._frames[self._current_frame]

    @property
    def frame_count(self) -> int:
        """The number of frames in the image."""
        return self._frame_count

    @property
    def fps(self) -> float:
        """The frames per second of the image."""
        return self._fps

    @property
    def frame_delay(self) -> float:
        """The delay between frames in seconds."""
        return self._frame_delay

    @property
    def current_frame(self) -> int:
        """The current frame of the image."""
        return self._current_frame

    @property
    def frames(self) -> list[list[list[pixel.Pixel]]]:
        """The frames of the image."""
        return self._frames

    @property
    def given_image_frames(self) -> list[list[list[pixel.Pixel]]] | str:
        """The given image frames."""
        return self._given_image_frames

    @pixel_grid.PixelGrid.size.setter
    def size(self, new_size: coord.Coordinate) -> None:
        """Set the size of the image.

        Args:
            new_size (coord.Coordinate):
                The new size of the image.
        """
        pass

    def update_animation(self) -> bool:
        """Check if the frame should be updated and update it if necessary.

        Returns:
            bool:
                True if the frame was updated, False otherwise. Used to determine if the image should be redrawn.
        """
        if self._frame_count == 1:
            return False

        # Get the current time.
        current_time = time.time()

        # If the current time minus the last frame time is greater than the frame delay, increment the current frame and
        # set the last frame time to the current time.
        if current_time - self._last_frame_time >= self._frame_delay:
            self._current_frame = (self._current_frame + 1) % self._frame_count
            self._last_frame_time = current_time

            # Update the grid with the new frame.
            self.grid = self._frames[self._current_frame]

            return True

        return False

    def _get_grids_from_file(self, image_path: str) -> list[list[list[pixel.Pixel]]]:
        """Create an image from a file.

        Args:
            image_path (str):
                The path to the image file.

        Returns:
            list[pixel_grid.PixelGrid]:
                The image.

        Raises:
            FileNotFoundError:
                If the file is not found.
            ValueError:
                If the file type is not supported.
        """
        # Check if the file path is a string and ends with .AI or .AAI.
        if not image_path:
            raise FileNotFoundError(f"File path {image_path} is empty.")

        file_type = image_path.strip().split(".")[-1]

        if file_type not in ["AI", "AAI"]:
            raise ValueError(f"File type {file_type} is not supported. Supported types are AI and AAI.")

        # Get the contents of the file if it exists.
        file_contents = _get_file_contents(image_path)

        # Check if the file is empty.
        if not file_contents:
            raise FileNotFoundError(f"File {image_path} not found.")

        # Get the metadata from the file.
        try:
            metadata = _extract_metadata(file_contents)
        except IndexError:
            raise ValueError(f"File is missing metadata or metadata is invalid.")

        self._frame_count = metadata["frame_count"]
        self._fps = metadata["fps"]
        self._frame_delay = 1 / self._fps

        # Get the image pixel grids from the file contents.
        image_frames: list[list[list[pixel.Pixel]]] = _assemble_image_frames(file_contents, metadata)

        return image_frames


def _get_file_contents(file_path: str) -> list[str]:
    """Get the contents of a file.

    Args:
        file_path (str):
            The path to the file.

    Returns:
        list[str]:
            The contents of the file.
    """
    with open(file_path, "r", encoding="UTF-16") as file:
        contents = copy.deepcopy(file.readlines())

    return contents


def _extract_metadata(file_contents: list[str]) -> dict[str, int | list[str]]:
    """Extract the metadata from the file contents.

    Args:
        file_contents (list[str]):
            The contents of the file.

    Returns:
        dict[str, int | list[str]]:
            The height, width, base colors, frame count, and frame time.
    """
    metadata = file_contents[0].strip().split(":")

    # Copy the metadata into the variables. If the metadata is missing, set the values to defaults. Also, fix the escape
    # sequences for the base colors.
    height: int = int(metadata[0])
    width: int = int(metadata[1])
    base_colors: str = metadata[-1].replace("\\033", "\033")

    if not base_colors:
        base_colors = "\033[0m"

    if len(metadata) == 3:
        frame_count = 1
        fps = 0.0
    else:
        frame_count = int(metadata[2])
        fps = float(metadata[3])

    vals = {
        "height": height,
        "width": width,
        "base_colors": base_colors,
        "frame_count": frame_count,
        "fps": fps
    }

    return vals


def _get_pixel_row(row: str, width: int, base_colors: list[str]) -> list[pixel.Pixel]:
    """Get the pixel row from the image line.

    Args:
        row (str):
            The row of the image.
        width (int):
            The width of the image.
        base_colors (list[str]):
            The base colors of the image.

    Returns:
        list[pixel.Pixel]:
            The pixel row.
    """
    pixel_row: list[pixel.Pixel] = []

    char_count = 0

    # Prep to take in color codes.
    color_list = []
    color_string = ""

    # Get the pixel characters from the row.
    for char in row:
        # If the color string isn't empty, we're in the middle of building a color code. Add the character to the color
        # code string.
        if color_string:
            color_string += char

            # If the character is an "m", the color code is complete. Add it to the color list and reset the color code
            # string, unless the color code is the clear color code. If it is, clear the color list because it has the
            # same effect as the clear color code with less overhead.
            if char == "m":
                if color_string == Colors.END:
                    color_list.clear()
                else:
                    color_list.append(color_string)
                    color_string = ""

            # We'll just continue here because the other stuff won't apply.
            continue

        # If the color string is empty and the character is a color code escape sequence, add it to the color code
        # string to begin building the color code and continue to the next character.
        elif char == "\033":
            color_string += char
            continue

        # If the character made it this far, it's a regular character and will be converted to a pixel.
        # Add it to the pixel row.
        else:
            char_count += 1
            pixel_row.append(pixel.Pixel(char, base_colors + color_list))

        # If the character count is equal to the width of the image, break out of the loop.
        if char_count == width:
            break

    return pixel_row


def _assemble_image_frames(file_contents: list[str], metadata: dict[str, int | str]) -> list[list[list[pixel.Pixel]]]:
    """Assemble the image frames from the file contents.

    Args:
        file_contents (list[str]):
            The contents of the file.
        metadata (dict[str, int | str]):
            The metadata of the image.

    Returns:
        list[list[list[pixel.Pixel]]]:
            The image frames.

    Raises:
        ValueError:
            If the metadata is missing.
    """
    # Get the image pixel grids from the file contents.
    image_frames: list[list[list[pixel.Pixel]]] = []

    for frame_num in range(metadata["frame_count"]):
        frame_grid = []

        # Get the line offset in the file for the frame, making sure to account for the metadata line and the
        # blank lines between frames.
        line_offset = 2 + (metadata["height"] + 1) * frame_num

        # To verify typing.
        colors: str = metadata["base_colors"]

        # Assemble the frame grid from the file contents.
        for row in file_contents[line_offset:line_offset + metadata["height"]]:
            frame_grid.append(_get_pixel_row(row, metadata["width"], [colors]))

        # Add the frame grid to the list of image frames.
        image_frames.append(frame_grid)

    return image_frames


if __name__ == "__main__":
    # Create an image object.
    img = Image(coord.Coordinate(), "C:\\Users\\dafan\\OneDrive\\Desktop\\CS\\Side Project Games and Apps\\Terminal System Attempt 2\\system\\assets\\images\\flashing_logo.AAI")

    # Update the image.
    img.update_animation()

    # Print the image to the terminal.
    print(img.grid)

    time.sleep(1)

    # Update the image.
    img.update_animation()

    # Print the image to the terminal.
    print(img.grid)

    while True:
        img.update_animation()
        print(img.to_string())
        print("\n----------\n")
        time.sleep(.5)
