import importlib
import unittest

import pgstub

pgstub.install()
bunker = importlib.import_module("bunker")


class BunkerTest(unittest.TestCase):
    def test_damage_and_destroy(self):
        b = bunker.Bunker((0, 0))
        for _ in range(3):
            b.damage()
            self.assertFalse(b.killed)
        b.damage()
        self.assertTrue(b.killed)


if __name__ == "__main__":
    unittest.main()
