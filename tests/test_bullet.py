import importlib
import unittest

import pgstub


pgstub.install()
bullet = importlib.import_module("bullet")


class BulletTest(unittest.TestCase):
    def test_bullet_moves_and_disappears(self):
        b = bullet.Bullet((0, 10))
        start_y = b.rect.y
        b.update()
        self.assertLess(b.rect.y, start_y)
        b.rect.bottom = -1
        b.update()
        self.assertTrue(b.killed)


if __name__ == '__main__':
    unittest.main()
