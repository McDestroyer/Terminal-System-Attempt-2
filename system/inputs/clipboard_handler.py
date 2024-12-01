import pyperclip


class Clipboard:
    """A class to handle the clipboard

    Methods:
        paste: Get the text from the clipboard.
        copy: Copy text to the clipboard.
    """
    def __init__(self) -> None:
        self._clipboard_history = []

    @property
    def clipboard_history(self) -> list[str]:
        """Return the clipboard history."""
        return self._clipboard_history

    def paste(self, index: int | None = None) -> str:
        """Get the text from the clipboard.

        Args:
            index (int, optional):
                The index of the clipboard history to paste from. If None, paste from the active clipboard. Otherwise,
                paste from the clipboard history variable (does not include anything copied outside the program).
                Defaults to None.

        Returns:
            str: The text from the clipboard.
        """
        if index is not None:
            return self._clipboard_history[index]

        return pyperclip.paste()

    def copy(self, text: str) -> None:
        """Copy text to the clipboard.

        Args:
            text (str): The text to copy.
        """
        pyperclip.copy(text)
        self._clipboard_history.append(text)

    def clear_clipboard_history(self) -> None:
        """Clear the clipboard history."""
        self._clipboard_history = []

    @classmethod
    def clear_clipboard(cls) -> None:
        """Clear the clipboard."""
        pyperclip.copy("")


if __name__ == "__main__":
    clipboard = Clipboard()
    original_text = clipboard.paste()
    print(clipboard.paste())
    clipboard.copy("Hello, World!")
    print(clipboard.paste())
    clipboard.copy("Goodbye, World!")
    print(clipboard.paste())
    clipboard.copy(original_text)
    print(clipboard.paste())
