#!/usr/bin/env python3

"""
A matrix rain clone.
"""

from time import sleep
from world import World
from view import terminal_view


def main():
    """Main loop, displays the rain"""
    with terminal_view() as view:
        game = World(target=view.columns * 2 // 3)
        while True:
            game.update(view)
            view.display(game)
            sleep(0.15)


def loop(n: int):
    """Loop for profiling, displays rain"""
    with terminal_view() as view:
        game = World()
        for _ in range(n):
            game.update(view)
            view.display(game)


if __name__ == "__main__":
    main()
