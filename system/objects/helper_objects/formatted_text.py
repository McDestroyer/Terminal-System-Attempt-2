from system.objects.helper_objects.pixel_objects.pixel_theme import ThemeDict


class FormattedText:
    """A class to hold a list of strings and their themes. Allows for text to have different themes in a single line."""
    def __init__(self, text_list: list[tuple[str, ThemeDict]] = None, center_text_horizontally: bool = False,
                 center_text_vertically: bool = False, wrap_words: bool = True,
                 cutoff_ending: list[tuple[str, ThemeDict]] = None) -> None:
        """Initialize the class.

        Args:
            text_list (list[tuple[str, ThemeDict]], optional):
                The list of text chunks and their themes. All text chunks will be concatenated together with no spaces.
                Defaults to [["", ThemeDict()]].
            center_text_horizontally (bool, optional):  # TODO: Implement this
                Whether to center the text horizontally.
                Defaults to False.
            center_text_vertically (bool, optional):  # TODO: Implement this
                Whether to center the text vertically.
                Defaults to False.
            wrap_words (bool, optional):
                Whether to wrap words to the next line if they are too long.
                Defaults to True.
            cutoff_ending (list[tuple[str, ThemeDict]], optional):
                The text to cut off the end of the text with if it is too long. Should not include color codes because
                I couldn't be bothered to make that work. Should not include newlines because this will only show if the
                text ran out of lines and that would be stupid. Warning: If the text is too long, it may scroll off the
                grid or be cut off itself.
                Defaults to [["...", ThemeDict()]].
        """
        self._text_list = text_list if text_list is not None else [["", ThemeDict()]]
        self.center_text_horizontally = center_text_horizontally
        self.center_text_vertically = center_text_vertically
        self.wrap_words = wrap_words
        self.cutoff_ending = cutoff_ending if cutoff_ending is not None else [["...", ThemeDict()]]

    def _get_string(self) -> str:
        return "".join([text[0][0] for text in self._text_list])

    def __str__(self) -> str:
        return self._get_string()

    def __repr__(self) -> str:
        return self._get_string()

    def __len__(self) -> int:
        return len(self._text_list)

    def __getitem__(self, index: int) -> tuple[str, ThemeDict]:
        return self._text_list[index]

    def __setitem__(self, index: int, value: tuple[str, ThemeDict]) -> None:
        self._text_list[index] = value

    def __delitem__(self, index: int) -> None:
        del self._text_list[index]

    def __iter__(self):
        return iter(self._text_list)

