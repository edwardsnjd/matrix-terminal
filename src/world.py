from collections import deque
from dataclasses import dataclass
from lib import Dimensions
from random import choice, randint


CANDIDATES = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "1234567890"
    "!@#$%^&*("
    "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρςστυφχψωϑϒϖ"
)


def get_random_character():
    return choice(CANDIDATES)


@dataclass
class Drop:
    """
    A single drop of rain.

    The main data structure is a list of characters, with the last character of
    that representing the head of the drop, and the precending characters a
    tail.
    """

    chars: deque[str]
    column: int
    line: int

    def tick(self):
        self.line += 1
        # NB. `deque#append` will discard earlier characters if required
        self.chars.append(get_random_character())

    @classmethod
    def create(cls, dimensions: Dimensions):
        """Create a new random rain drop."""
        # These semi-tuned params try to make a visually pleasing
        # distribution of new drops
        max_length = randint(8, max(8, dimensions.lines * 2 // 3))
        return cls(
            chars=deque([get_random_character()], maxlen=max_length),
            column=randint(0, dimensions.columns - 1),
            line=max(0, randint(-5, dimensions.lines // 3)),
        )


class World:
    """The core program loop logic that manages all the rain drops."""

    def __init__(self, target: int = 60):
        self.rain: list[Drop] = []
        self.target: int = target

    def update(self, view: Dimensions):
        # Update existing raindrops
        for drop in self.rain:
            drop.tick()

        # Cull raindrops that have left the view
        self.rain = [drop for drop in self.rain if self.in_view(view, drop)]

        # Add raindrops if needed
        while len(self.rain) < self.target:
            new_drop = Drop.create(dimensions=view)
            self.rain.append(new_drop)

    def in_view(self, view: Dimensions, drop: Drop):
        threshold = view.lines + len(drop.chars) - 1
        return 0 <= drop.column <= view.columns and drop.line <= threshold
