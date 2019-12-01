from unittest import TestCase

import pygame

from game_objects.gui_elements import GuiTextElement, Score


class TestGuiTextElement(TestCase):

    def test_get_text(self):
        pygame.init()
        g = GuiTextElement(3, 5)
        self.assertIsNotNone(g.get_text())

    def test_get_pos(self):
        pygame.init()
        g = GuiTextElement(3, 5)
        self.assertIsNotNone(g.get_pos())


class TestScore(TestCase):

    def test(self):
        pass

    def test_add_to_score(self):
        pygame.init()
        t = Score(1, 3)
        t.add_to_score(420)
        self.assertEqual(t.get_score(), 420)

    def test_get_score(self):
        pygame.init()
        t = Score(1,43)
        self.assertEqual(t.get_score(), 0)
