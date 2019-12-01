import os

import pygame
from pygame.locals import Color

from sprite.animated import Animated
from game_objects.game_statics import frames
from utils.path_utils import harmonize_path
from sprite.sprite_animation import SpriteAnimation


class Coin(Animated):
    """
    The coin replaces the mouse cursor and has a spinning animation
    """

    SPRITE_WIDTH = 18  # width != height
    SPRITE_HEIGHT = 20

    def __init__(self):
        super().__init__()
        # x,y are assigned dynamically at mouse click event
        self.x = 0
        self.y = 0
        # coin width and height are just 1 to represent the mouse cursor at collision detection
        self.width = 3
        self.height = 3

        path = harmonize_path(os.path.join(os.path.dirname(__file__),  "../resources/sprites/spin_coin_big.png"))

        self.coin_spin_sprites = SpriteAnimation(path,
                                                 (0, 0, Coin.SPRITE_WIDTH, Coin.SPRITE_HEIGHT),
                                                 count=6,
                                                 colorkey=Color('black'),
                                                 loop=True,
                                                 frames=frames)

        self._sound = pygame.mixer.Sound("resources/sounds/coin_plink.wav")

        self._current_animation = self.coin_spin_sprites.iter()

    def play_plink_sound(self):
        """
        plays the coin "plink" sound
        """
        self._sound.play()
