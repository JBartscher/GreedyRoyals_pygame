import copy
import os
import time
from random import randint

from pygame.locals import Color

from game_objects.game_statics import frames, SCREENHEIGHT, SCREENWIDTH
from sprite.animated import Animated
from sprite.sprite_animation import SpriteAnimation
from utils.collision_util import intersects
from utils.path_utils import harmonize_path
from utils.vector_translation_utils import *


class King(Animated):
    """
    Model Class for the King. A Game Entity, which is moved across the Gamescreen in an
    "random" pattern
    """
    SPRITE_SHEET = "./sprites/characters"
    SPRITE_SIZE = 32  # width == height

    def __init__(self, x=0, y=0, speed=1):

        super().__init__()

        self.x = x
        self.y = y
        self.width = King.SPRITE_SIZE
        self.height = King.SPRITE_SIZE

        self._speed = speed

        path = harmonize_path(os.path.join(os.path.dirname(__file__), "../resources/sprites/characters_black.png"))

        self.move_right_sprites = SpriteAnimation(path,
                                                  (0, King.SPRITE_SIZE, King.SPRITE_SIZE, King.SPRITE_SIZE),
                                                  count=5, colorkey=Color('black'),
                                                  loop=True, frames=frames)
        self.move_left_sprites = SpriteAnimation(path,
                                                 (0, King.SPRITE_SIZE, King.SPRITE_SIZE, King.SPRITE_SIZE),
                                                 count=5, colorkey=Color('black'),
                                                 loop=True, frames=frames).flip()

        self.move_down_sprites = self.move_right_sprites  # looks the same

        path = harmonize_path(os.path.join(os.path.dirname(__file__), "../resources/sprites/king_up_black.png"))
        self.move_up_sprites = SpriteAnimation(path,
                                               (0 * King.SPRITE_SIZE, 0 * King.SPRITE_SIZE, King.SPRITE_SIZE,
                                                King.SPRITE_SIZE),
                                               count=5,
                                               colorkey=Color('black'), loop=True,
                                               frames=frames)

        self._current_animation = None
        self._current_waypoint = self._create_new_waypoint()
        self._move_vector = self._calculate_movement_vector()
        self._select_movement_direction()

    def get_speed(self):
        """
        gets the current speed
        :return: speed value
        """
        return self._speed

    def set_king_speed(self, speed=1):
        """
        set the speed of the king. the speed is the value which the king travels in one gameloop iteration. The default
        speed is 1.
        :param speed: speed at which the king figure travels
        """
        self._speed = speed

    def _select_movement_direction(self):
        """
        calculates the current direction in degrees (from x-axis) and selects the right sprite animation for
        that movement.

        the up movement looks fishy if used in a far "down" angle so just 30° ( 75° till 105°) are counted as
        up movement.
        """
        self.__start_time = time.time()
        v = self._current_waypoint
        u = np.array([self.x, self.y])
        delta = v - u
        delta[1] = delta[1] * -1  # y-axis needs to be flipped to get correct degree
        degree = calculate_vector_angle_in_degree(delta)

        if degree > 75 and degree < 105:
            # Up
            self._current_animation = self.move_up_sprites.iter()

        elif degree >= 105 and degree < 270:
            # Left
            self._current_animation = self.move_left_sprites.iter()

        elif degree >= 270 or degree <= 75:
            # Right
            self._current_animation = self.move_down_sprites.iter()

    def _check_waypoint(self):
        """ generates a new waypoint after x seconds"""

        if time.time() - self.__start_time > 1:
            self._current_waypoint = self._create_new_waypoint()
            self._move_vector = self._calculate_movement_vector()
            self._select_movement_direction()
            self.__start_time = time.time()
        """
        if compare_2d_array(np.array([self.x, self.y]), self._current_waypoint):
            self._current_waypoint = self._create_new_waypoint()
            self._move_vector = self._calculate_movement_vector()
            self._select_movement_direction()
        """

    def _create_new_waypoint(self):
        """
        select a random point on the game screen and creates a vector to that point.
        "interploates" further points on that path and returns them as a list.
        :return: a point to which the King walks
        """
        return np.array([randint(0, SCREENWIDTH - King.SPRITE_SIZE),
                         randint(0, SCREENHEIGHT - King.SPRITE_SIZE)])

    def collides_with(self, other):
        """
        the kings pos and size does not represent his collision box, so a dummy Animated object is created to check if
        the objects collide.

        :param other: the other object which may or may not collide with this king entity
        :return: True or False
        """

        collision_dummy = copy.copy(self)

        collision_dummy.x = collision_dummy.x + (King.SPRITE_SIZE / 2)
        collision_dummy.y = collision_dummy.y + (4 + King.SPRITE_SIZE / 2)
        collision_dummy.height = collision_dummy.height + 12

        return intersects(other, collision_dummy)

    def update(self, *args):
        """
        method which is called by the SpriteGroup and wraps the kings move method
        """
        self.__move()

    def __move(self):
        """ moves the king to its current waypoint by a movement vector"""

        self.x += self._move_vector[0]
        self.y += self._move_vector[1]
        self._check_waypoint()

    def _calculate_movement_vector(self):
        """
        calculates the movement vector for the current waypoint.
        This method is intended to be called in every gameloop iteration.
        The normal vector is "longer" when the speed is high eg. the king moves faster.
        """
        v1 = np.array([self.x, self.y])
        v2 = self._current_waypoint
        delta = v2 - v1
        return normalize_vector(delta, norm=self._speed)
