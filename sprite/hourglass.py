import os
import time

from pygame.locals import Color

from sprite.animated import Animated
from game_objects.game_statics import frames
from sprite.sprite_animation import SpriteAnimation


class Hourglass(Animated):
    SPRITE_WIDTH = 99  # width != height
    SPRITE_HEIGHT = 128

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/sprites/hourglass 2.png")
        path = path.replace('/', os.sep)
        path = path.replace('\\', os.sep)

        self.hourglass_sprites = SpriteAnimation(filename=path,
                                                 rect=(0, 0, Hourglass.SPRITE_WIDTH, Hourglass.SPRITE_HEIGHT),
                                                 count=53, colorkey=Color('black'), loop=True,
                                                 frames=frames)

        self._current_animation = self.hourglass_sprites.iter()
