"""
Functions for manipulating a terminal via ANSI escape codes.

`tput` is the implementation used by this module to obtain the strings that we
should send to the terminal.
"""

from dataclasses import dataclass
from functools import cache
from os import get_terminal_size
import subprocess


@dataclass
class Dimensions:
    columns: int
    lines: int


def get_dimensions() -> Dimensions:
    """Get the dimensions of the terminal."""
    columns, lines = get_terminal_size(0)
    return Dimensions(columns=columns, lines=lines)


@cache
# Cache every requested code since otherwise we repeatedly incur the penalty of
# looking up every cursor position
def escape_code(capability: str, *args: list[str]):
    """Get the code for the given capability."""
    return subprocess.run(
        ("tput", capability, *args),  # type: ignore
        capture_output=True,
        encoding="UTF-8",
    ).stdout


@dataclass
class TerminalCodes:
    """Strings to output to the terminal for each capability."""

    # Colour codes
    COLOUR_BLACK = 0
    COLOUR_RED = 1
    COLOUR_GREEN = 2
    COLOUR_YELLOW = 3
    COLOUR_BLUE = 4
    COLOUR_MAGENTA = 5
    COLOUR_CYAN = 6
    COLOUR_WHITE = 7

    # Terminal capability names (used internally)
    ENTER_ALTERNATE_SCREEN = "smcup"
    LEAVE_ALTERNATE_SCREEN = "rmcup"
    CURSOR_INVISIBLE = "civis"
    CURSOR_NORMAL = "cnorm"
    CLEAR_AND_HOME_CURSOR = "clear"
    CURSOR_ADDRESS = "cup"
    BOLD_TEXT = "bold"
    DIM_TEXT = "dim"
    REVERSE_TEXT = "rev"
    NORMAL_TEXT = "sgr0"
    SET_BACKGROUND_COLOUR = "setab"
    SET_FOREGROUND_COLOUR = "setaf"

    # The string for each capabilitiy
    enter_alternate_screen: str
    leave_alternate_screen: str
    cursor_invisible: str
    cursor_normal: str
    clear: str
    bold_text: str
    dim_text: str
    reverse_text: str
    normal_text: str

    def cursor_address(self, line: int, column: int) -> str:
        """Get the code to move the cursor to the given position."""
        return escape_code(self.CURSOR_ADDRESS, str(line), str(column))

    def background_colour(self, colour: int) -> str:
        """Get the code to set the text background colour."""
        return escape_code(self.SET_BACKGROUND_COLOUR, str(colour))

    def foreground_colour(self, colour: int) -> str:
        """Get the code to set the text foreground_colour colour."""
        return escape_code(self.SET_FOREGROUND_COLOUR, str(colour))

    @classmethod
    def from_tput(cls):
        """Factory to construct this for the current terminal."""
        return cls(
            enter_alternate_screen=escape_code(cls.ENTER_ALTERNATE_SCREEN),
            leave_alternate_screen=escape_code(cls.LEAVE_ALTERNATE_SCREEN),
            cursor_invisible=escape_code(cls.CURSOR_INVISIBLE),
            cursor_normal=escape_code(cls.CURSOR_NORMAL),
            clear=escape_code(cls.CLEAR_AND_HOME_CURSOR),
            bold_text=escape_code(cls.BOLD_TEXT),
            dim_text=escape_code(cls.DIM_TEXT),
            reverse_text=escape_code(cls.REVERSE_TEXT),
            normal_text=escape_code(cls.NORMAL_TEXT),
        )
