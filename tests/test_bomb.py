import importlib
import unittest

import pgstub

pgstub.install()
bullet = importlib.import_module("bullet")
config = importlib.import_module("config")


class BombTest(unittest.TestCase):
    def test_bomb_falls_and_disappears(self):
        b = bullet.Bomb((0, 0))
        start_y = b.rect.y
        b.update()
        self.assertGreater(b.rect.y, start_y)
        b.rect.top = config.SCREEN_HEIGHT + 1
        b.update()
        self.assertTrue(b.killed)


if __name__ == "__main__":
    unittest.main()
