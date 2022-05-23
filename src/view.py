from contextlib import contextmanager
from terminal import TerminalCodes, get_dimensions
from world import World


class NaiveTerminalView:
    """
    A view that naively renders by concatenating all the escape codes for
    each tick.
    """

    def __init__(self, codes: TerminalCodes, columns: int, lines: int):
        self.codes = codes
        self.columns = columns
        self.lines = lines

    def display(self, game: World):
        cmd = "".join(self.render(game))
        print(cmd, end=None)

    def render(self, game: World):
        yield self.codes.clear

        for drop in game.rain:
            column = drop.column
            total = len(drop.chars)
            for i, char in enumerate(drop.chars):
                line = drop.line - total + i + 1
                if 0 <= line < self.lines - 1:
                    yield self.codes.cursor_address(line, column)
                    if i == total - 1:
                        yield self.codes.foreground_colour(self.codes.COLOUR_WHITE)
                        yield self.codes.bold_text
                        yield char
                        yield self.codes.normal_text
                    else:
                        yield self.codes.foreground_colour(self.codes.COLOUR_GREEN)
                        yield char
                        yield self.codes.normal_text


@contextmanager
def terminal_view():
    """Context manager switches to and from the alternate screen mode."""
    codes = TerminalCodes.from_tput()
    dimensions = get_dimensions()
    view = NaiveTerminalView(codes, dimensions.columns, dimensions.lines)

    try:
        print(codes.enter_alternate_screen)
        print(codes.cursor_invisible)
        yield view
    finally:
        print(codes.cursor_normal)
        print(codes.leave_alternate_screen)
