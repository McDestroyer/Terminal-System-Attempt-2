import copy

from system.objects.helper_objects.formatted_text import FormattedText
from system.objects.helper_objects.pixel_objects.pixel import Pixel
from system.objects.helper_objects.pixel_objects.pixel_grid import PixelGrid
from system.objects.helper_objects.coordinate_objects.coordinate import Coordinate
from system.objects.helper_objects.pixel_objects.pixel_theme import ThemeDict

from system.utilities.color import Colors, Color


class Text(PixelGrid):
    """A class for displaying text on the terminal."""

    def __init__(self, coordinates: Coordinate, size: Coordinate, text: FormattedText = FormattedText(),
                 default_pixel: Pixel = Pixel(),
                 overall_themes: ThemeDict = ThemeDict()) -> None:
        """Initialize the PixelGrid object.

        Args:
            coordinates (Coordinate):
                The coordinates of the PixelGrid.
            size (Coordinate):
                The size of the PixelGrid.
            text (FormattedText, optional):
                The text to display.
                Defaults to FormattedText().
            default_pixel (Pixel, optional):
                The default pixel of the PixelGrid.
                Defaults to Pixel().
            overall_themes (ThemeDict, optional):
                The overall themes of the PixelGrid.
                Defaults to a new ThemeDict().
        """
        super().__init__(coordinates, size, default_pixel, overall_themes)

        self._text = text

        self._text_pixels = self._get_text_pixel_list()

        self.grid = self._get_text_pixel_grid_word_wrap() if self._text.wrap_words else self._get_text_pixel_grid()

        self.should_draw = True

    @PixelGrid.size.setter
    def size(self, new_size: Coordinate) -> None:
        """Set the size of the PixelGrid.

        Args:
            new_size (Coordinate):
                The new size of the PixelGrid.
        """
        self._size = new_size

        self._grid = [[self._default_pixel for _ in range(new_size.x_char)] for _ in range(new_size.y_char)]

        self.should_draw = True

    @PixelGrid.overall_themes.setter
    def overall_themes(self, new_overall_themes: ThemeDict) -> None:
        """Set the overall themes of the PixelGrid.

        Args:
            new_overall_themes (ThemeDict):
                The new overall themes of the PixelGrid.
        """
        self._overall_themes = new_overall_themes

        # Set the themes of the pixels.
        for row in self._grid:
            for pix in row:
                pix.themes = copy.deepcopy(self._overall_themes)

        self.should_draw = True

    @property
    def text(self) -> FormattedText:
        """Return the text.

        Returns:
            FormattedText: The text.
        """
        return self._text

    @text.setter
    def text(self, new_text: FormattedText) -> None:
        """Set the text.

        Args:
            new_text (FormattedText):
                The new text.
        """
        self._text = new_text
        self.should_draw = True

    def update_text(self) -> bool:
        """Update the text grid and pixel list.

        Returns:
            bool: Whether the text was updated and should be redrawn.
        """
        if self.should_draw:
            self.should_draw = False

            pixel_list = self._get_text_pixel_list()

            if self._text_pixels != pixel_list:
                self._text_pixels = pixel_list

                if self._text.wrap_words:
                    self.grid = self._get_text_pixel_grid_word_wrap()
                else:
                    self.grid = self._get_text_pixel_grid()

            return True

        return False

    def _get_text_pixel_list(self) -> list[Pixel]:
        """Get the pixels for the text.

        Returns:
            list[Pixel]: The pixels for the text.
        """
        # Replace the escape characters in the text if needed.
        for chunk in self._text:
            chunk[0].replace("\\033", "\033")
            chunk[0].replace("\\n", "\n")

        text_pixels = []

        # Create the properly formatted text pixels in a single list.
        for chunk in self._text:
            for char in chunk[0]:
                text_pixels.append(Pixel(char, self._overall_themes + copy.deepcopy(chunk[1])))

        return text_pixels

    def _get_text_pixel_grid_word_wrap(self) -> list[list[Pixel]]:
        """Get the pixels for the text.

        Returns:
            list[list[Pixel]]: The pixels for the text.
        """
        text_pixels = self._get_text_pixel_list()

        # TODO: MAke this into a function by itself.
        # Create the 2D list of text pixels, splitting the text into rows and pulling out escape characters.
        text_pixel_grid = [[]]
        word: list[Pixel] = []
        word_breakers: list[str] = ["\n", "\033", " ", "-", ":", ";", ",", ".", ">", "<", "/", "\\", "|", "=", "+", "*"]

        color_list: list[Color] = []
        color_string: str = ""

        for pix in text_pixels:
            # Handle extracting the color codes.
            if color_string:
                color_string += pix.char
                # If the character is 'm', add the color code to the list and clear the color string.
                if pix.char == "m":
                    # If the color code is the end code, clear the color list.
                    if color_string == str(Colors.END):
                        color_list = []
                    color_list.append(Colors.color_from_code(color_string))
                    color_string = ""
                continue

            # Check for word breakers and handle them.
            if pix.char in word_breakers:
                # If adding the word will make the row too long
                if len(word) + len(text_pixel_grid[-1]) > self._size.x_char:
                    # If the length of the word is greater than the row length, split the word into multiple rows.
                    if len(word) > self._size.x_char:
                        # If the row is empty, add the first part of the word to the row. Otherwise, start a new row.
                        # Then, remove the part of the word that was added to the row so the loop can work properly.
                        if len(text_pixel_grid[-1]) == 0:
                            text_pixel_grid.append(word[:self._size.x_char])
                            word = word[self._size.x_char:]
                        else:
                            text_pixel_grid.append([])
                            text_pixel_grid[-1].extend(word[:self._size.x_char - len(text_pixel_grid[-1])])
                            word = word[self._size.x_char - len(text_pixel_grid[-1]):]

                        # Add the rest of the word to the rows.
                        for i in range((len(word) // self._size.x_char) + 1):
                            text_pixel_grid.append(word[i * self._size.x_char:(i + 1) * self._size.x_char])

                    # If the word is too long to fit on the row, but not longer than a full row, start a new row.
                    else:
                        text_pixel_grid.append([])
                        text_pixel_grid[-1].extend(word)

                # If the word is not too long, add it to the row.
                else:
                    text_pixel_grid[-1].extend(word)

                # Regardless of any complications in adding the word, clear the word.
                word = []

            # Check for color codes.
            if pix.char == "\033":
                text_pixel_grid[-1].extend(word)
                color_string = pix.char
                continue

            # If the character is a newline, start a new row.
            if pix.char == "\n":
                text_pixel_grid.append([])
                continue

            # If nothing prevents us from reaching here, add the current color list to the pixel and add the pixel to
            # the word.
            pix.themes[pix.themes.current_theme_type].add_colors(color_list)
            word.append(pix)

            # Finally, check to see if there are too many rows and add the cut off the text if so.
            if len(text_pixel_grid) > self._size.y_char:
                text_pixel_grid = text_pixel_grid[:self._size.y_char]
                text_pixel_grid[-1] = text_pixel_grid[-1][:max(self._size.x_char + len(self._text.cutoff_ending[0]), 0)]

                # Convert the cutoff ending to pixels and add it to the end of the row.
                for i in range(len(self._text.cutoff_ending[:self._size.x_char])):
                    for j in range(len(self._text.cutoff_ending[i][0])):
                        end_pix = Pixel(self._text.cutoff_ending[i][0][j],
                                        copy.deepcopy(self._text.cutoff_ending[i][1]))
                        end_pix.themes[end_pix.themes.current_theme_type].add_colors(color_list)

                        text_pixel_grid[-1].append(end_pix)

                break

        return text_pixel_grid

    def _get_text_pixel_grid(self) -> list[list[Pixel]]:
        """Get the pixels for the text.

        Returns:
            list[list[Pixel]]: The pixels for the text.
        """
        text_pixels = self._get_text_pixel_list()

        # Create the 2D list of text pixels, splitting the text into rows and pulling out escape characters.
        text_pixel_grid = [[]]

        color_list: list[Color] = []
        color_string: str = ""

        for pix in text_pixels:
            # Handle extracting the color codes.
            if color_string:
                color_string += pix.char
                # If the character is 'm', add the color code to the list and clear the color string.
                if pix.char == "m":
                    # If the color code is the end code, clear the color list.
                    if color_string == str(Colors.END):
                        color_list = []
                    color_list.append(Colors.color_from_code(color_string))
                    color_string = ""
                continue

            # Check for color codes.
            if pix.char == "\033":
                color_string = pix.char
                continue

            # If the character is a newline, start a new row.
            if pix.char == "\n":
                text_pixel_grid.append([])
                continue

            # If nothing prevents us from reaching here, add the current color list to the pixel and add the pixel to
            # the word.
            pix.themes[pix.themes.current_theme_type].add_colors(color_list)

            if len(text_pixel_grid[-1]) >= self._size.x_char:
                text_pixel_grid.append([])

            text_pixel_grid[-1].append(pix)

            # Finally, check to see if there are too many rows and add the cut off the text if so.
            if len(text_pixel_grid) > self._size.y_char:
                text_pixel_grid = text_pixel_grid[:self._size.y_char]
                try:
                    text_pixel_grid[-1] = text_pixel_grid[-1][
                        :max(self._size.x_char + len(self._text.cutoff_ending[0]), 0)
                    ]
                except IndexError:
                    pass

                # Convert the cutoff ending to pixels and add it to the end of the row.
                for i in range(len(self._text.cutoff_ending[:self._size.x_char])):
                    for j in range(len(self._text.cutoff_ending[i][0])):
                        end_pix = Pixel(self._text.cutoff_ending[i][0][j],
                                        copy.deepcopy(self._text.cutoff_ending[i][1]))
                        end_pix.themes[end_pix.themes.current_theme_type].add_colors(color_list)

                        text_pixel_grid[-1].append(end_pix)

                break

        return text_pixel_grid
