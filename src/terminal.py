from dataclasses import dataclass
import subprocess
from os import get_terminal_size
from functools import cache


@cache
def cursor_address(row: int, col: int):
    cmd = ("tput", "cup", str(row), str(col))
    return subprocess.run(
        cmd, capture_output=True, encoding="UTF-8"
    ).stdout


@dataclass
class TerminalCodes:
    """Strings to output to the terminal for each capability."""

    # Terminal capability names
    ENTER_ALTERNATE_SCREEN = "smcup"
    LEAVE_ALTERNATE_SCREEN = "rmcup"
    CURSOR_INVISIBLE = "civis"
    CURSOR_NORMAL = "cnorm"
    CLEAR_AND_HOME_CURSOR = "clear"
    CURSOR_ADDRESS = "cup"
    BOLD_TEXT = "bold"
    NORMAL_TEXT = "sgr0"

    # The string for each capabilitiy
    enter_alternate_screen: str
    leave_alternate_screen: str
    cursor_invisible: str
    cursor_normal: str
    clear: str
    bold_text: str
    normal_text: str

    @classmethod
    def from_tput(cls):
        """Factory to construct this for the current terminal."""
        return cls(
            enter_alternate_screen=cls.escape_code(cls.ENTER_ALTERNATE_SCREEN),
            leave_alternate_screen=cls.escape_code(cls.LEAVE_ALTERNATE_SCREEN),
            cursor_invisible=cls.escape_code(cls.CURSOR_INVISIBLE),
            cursor_normal=cls.escape_code(cls.CURSOR_NORMAL),
            clear=cls.escape_code(cls.CLEAR_AND_HOME_CURSOR),
            bold_text=cls.escape_code(cls.BOLD_TEXT),
            normal_text=cls.escape_code(cls.NORMAL_TEXT),
        )

    @classmethod
    def escape_code(self, capability, *args: list[str]):
        """Get the code for the given capability."""
        cmd = ("tput", capability, *args)
        return subprocess.run(
            cmd, capture_output=True, encoding="UTF-8"
        ).stdout

    @staticmethod
    def get_dimensions():
        return get_terminal_size(0)
