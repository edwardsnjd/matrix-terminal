import unittest

from world import Drop
from collections import namedtuple

Dimensions = namedtuple("Dimensions", "columns lines")


class TestDrop(unittest.TestCase):
    def build(self):
        dimensions = Dimensions(columns=10, lines=5)
        return Drop.create(dimensions)

    def test_create_drop_length(self):
        drop = self.build()

        self.assertEqual(len(drop.chars), 1)

    def test_drop_falls_each_tick(self):
        drop = self.build()
        start_position = drop.line

        drop.tick()
        drop.tick()

        self.assertEqual(drop.line, start_position + 2)

    def test_drop_grows_each_tick(self):
        drop = self.build()
        start_chars = "".join(drop.chars)

        drop.tick()
        drop.tick()

        end_chars = "".join(drop.chars)
        self.assertEqual(len(end_chars), len(start_chars) + 2)

    def test_drop_has_max_length(self):
        drop = self.build()

        for i in range(1000):
            drop.tick()

        end_chars = "".join(drop.chars)
        self.assertLess(len(end_chars), 1000)
