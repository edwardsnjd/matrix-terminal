import unittest

from main import Game


class TestGame(unittest.TestCase):
    def test_foo(self):
        game = Game()
        self.assertEqual(1, 1)
