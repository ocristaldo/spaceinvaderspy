import sys
import types


class FakeRect:
    def __init__(self, *args, **kwargs):
        if args:
            self.left, self.top, self.width, self.height = (
                args + (0, 0, 0, 0)
            )[:4]
            self.x = self.left
            self.y = self.top
        else:
            pos = (
                kwargs.get('midbottom')
                or kwargs.get('midtop')
                or kwargs.get('topleft')
                or kwargs.get('center')
                or (0, 0)
            )
            self.x, self.y = pos
            self.left = self.x
            self.top = self.y
            self.width = kwargs.get('width', 0)
            self.height = kwargs.get('height', 0)
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    def clamp_ip(self, rect):
        self.x = min(max(self.x, rect.left), rect.left + rect.width)
        self.y = min(max(self.y, rect.top), rect.top + rect.height)
        self.left = self.x
        self.right = self.x
        self.top = self.y
        self.bottom = self.y


class FakeSurface:
    def __init__(self, size):
        pass

    def fill(self, color):
        pass

    def get_rect(self, **kwargs):
        return FakeRect(**kwargs)


class FakeSprite:
    def __init__(self):
        self.killed = False

    def kill(self):
        self.killed = True


def install():
    pygame_stub = types.SimpleNamespace(
        Surface=FakeSurface,
        sprite=types.SimpleNamespace(Sprite=FakeSprite),
        Rect=FakeRect,
        K_LEFT='left',
        K_RIGHT='right',
    )
    sys.modules['pygame'] = pygame_stub
    return pygame_stub
