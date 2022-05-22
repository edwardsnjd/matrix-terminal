from random import choice, randint
from dataclasses import dataclass


CANDIDATES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*("


def get_random_character():
    return choice(CANDIDATES)


@dataclass
class Drop:
    """A single drop of rain"""

    age: int
    chars: list[str]
    max_length: int
    x: int
    y: int

    def tick(self):
        self.age += 1
        self.y += 1
        self.chars.append(get_random_character())
        self.chars = self.chars[-self.max_length:]

    @classmethod
    def create(cls, width: int):
        return cls(
            age=0,
            chars=[get_random_character()],
            max_length=randint(5, 35),
            x=randint(0, width - 1),
            y=randint(-5, 5),
        )
