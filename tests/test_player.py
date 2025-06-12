import importlib
import unittest

import pgstub

pgstub.install()
player_mod = importlib.import_module("player")
config = importlib.import_module("config")


class Pressed(dict):
    def __getitem__(self, key):
        return self.get(key, False)


class PlayerTest(unittest.TestCase):
    def test_player_stays_on_screen(self):
        p = player_mod.Player()
        p.rect.x = -10
        p.update(Pressed({}))
        self.assertGreaterEqual(p.rect.x, 0)
        p.rect.x = config.SCREEN_WIDTH + 10
        p.update(Pressed({}))
        self.assertLessEqual(p.rect.x, config.SCREEN_WIDTH)


if __name__ == "__main__":
    unittest.main()
