from unittest import TestCase

import pygame

from game_objects.game_statics import SCREENHEIGHT, SCREENWIDTH
from sprite.king import King


class TestKing(TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode([SCREENHEIGHT, SCREENWIDTH])

        self.king = King()

    def test_set_king_speed(self):
        """
        test if the speed of the King object is setted right
        :return:
        """
        self.king.set_king_speed(3)
        self.assertEqual(self.king._speed, 3)
        self.king.set_king_speed()
        self.assertEqual(self.king._speed, 1)


    def test__select_movement_direction(self):
        self.king._select_movement_direction()
        pass

    def test__check_waypoint(self):
        self.king
        pass
        # self.fail()

    def test__create_new_waypoint(self):
        pass
        # self.fail()

    def test_move(self):
        pass
        # self.fail()
