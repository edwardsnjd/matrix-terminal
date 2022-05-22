#!/usr/bin/env python3

"""
A matrix rain clone using `tput` to control the terminal.
"""

from contextlib import contextmanager
from terminal import TerminalCodes, cursor_address
from time import sleep
from rain import Drop


def main():
    with terminal_view() as view:
        game = Game()
        while True:
            game.update(view)
            view.display(game)
            sleep(0.1)


def loop(n: int):
    with terminal_view() as view:
        game = Game()

        for _ in range(n):
            game.update(view)
            view.display(game)


class Game:
    def __init__(self):
        self.rain = []
        self.target = 40

    def update(self, view):
        # Update existing raindrops
        for drop in self.rain:
            drop.tick()

        # Cull raindrops that are out of the view
        self.rain = [drop for drop in self.rain if self.in_view(view, drop)]

        # Add raindrops if needed
        while len(self.rain) < self.target:
            new_drop = Drop.create(width=view.width)
            self.rain.append(new_drop)

    def in_view(self, view, drop):
        threshold = view.height + drop.max_length - 1
        return 0 <= drop.x <= view.width and drop.y <= threshold


class View:
    def __init__(self, codes, width, height):
        self.codes = codes
        self.width = width
        self.height = height

    def display(self, game):
        cmd = "".join(self.render(game))
        print(cmd, end=None)

    def render(self, game):
        yield self.codes.clear

        for drop in game.rain:
            column = drop.x
            total = len(drop.chars)
            for i, char in enumerate(drop.chars):
                row = drop.y - total + i + 1
                if 0 <= row < self.height - 1:
                    yield cursor_address(row, column)
                    if i == total - 1:
                        yield self.codes.bold_text
                        yield char
                        yield self.codes.normal_text
                    else:
                        yield char


@contextmanager
def terminal_view():
    codes = TerminalCodes.from_tput()
    width, height = TerminalCodes.get_dimensions()

    v = View(codes, width, height)

    try:
        print(codes.enter_alternate_screen)
        print(codes.cursor_invisible)
        yield v
    finally:
        print(codes.cursor_normal)
        print(codes.leave_alternate_screen)



if __name__ == "__main__":
    main()
