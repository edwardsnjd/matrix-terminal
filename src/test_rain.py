import unittest

from rain import Drop


class TestRain(unittest.TestCase):
    def test_create_drop_length(self):
        drop = Drop.create(width=10)

        self.assertEqual(len(drop.chars), 1)

    def test_drop_ages_each_tick(self):
        drop = Drop.create(width=10)
        start_age = drop.age

        drop.tick()
        drop.tick()

        self.assertEqual(drop.age, start_age + 2)
        self.assertEqual(drop.age, start_age + 2)

    def test_drop_falls_each_tick(self):
        drop = Drop.create(width=10)
        start_position = drop.y

        drop.tick()
        drop.tick()

        self.assertEqual(drop.y, start_position + 2)

    def test_drop_grows_each_tick(self):
        drop = Drop.create(width=10)
        start_chars = "".join(drop.chars)

        drop.tick()
        drop.tick()

        end_chars = "".join(drop.chars)
        self.assertEqual(len(end_chars), len(start_chars) + 2)

    def test_drop_has_max_length(self):
        drop = Drop.create(width=10)
        max_length = drop.max_length

        for i in range(100):
            drop.tick()

        end_chars = "".join(drop.chars)
        self.assertEqual(len(end_chars), max_length)
