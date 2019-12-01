import time

import pygame
from pygame.font import Font
from pygame.locals import Color


class GuiTextElement:
    """
    GUI Parent Class for Text Gui Elements
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.font = Font("resources/fonts/VCR_OSD_MONO_1.001.ttf", 30)  # pygame.font.SysFont('Comic Sans MS', 30)  #
        self._text = self.font.render("", True, Color("white"), Color("black"))
        self._text_rect = self._text.get_rect()

    def get_text(self):
        """
        get the text string of the current gui element

        :return: the text string of the current gui element
        """
        return self._text

    def get_pos(self):
        """
        return position of the GUI Element

        :return: position of the GUI Element
        """
        return self.x, self.y

    def update_text(self, new_text, color=Color("white")):
        """
        updates the text of the GUI Element in a specific color

        :param new_text: the text that should be displayed in the GUI element
        :param color: color of text
        """
        self._text = self.font.render(new_text, True, color, None)
        self._text_rect = self._text.get_rect()


class Countdown(GuiTextElement):
    """ game countdown """

    def __init__(self, x=0, y=0, initial_time=15):
        super().__init__(x, y)
        self._initial_time = initial_time
        self._time_left = initial_time
        self._end_time = time.time() + initial_time

        self.red = 150
        self.yellow = 150

    async def start_timer(self):
        """
        restarts the timer from initial time property
        """
        self._end_time = time.time() + self._initial_time
        self._time_left = self._end_time - time.time()
        # return self._time_left

    async def tick(self):
        """
        async ticks from the timeleft and updates the time left property
        """

        countdown_time = 10

        # In the last 10 seconds the color of the countdown will strive more and more to red
        if self._time_left < countdown_time:
            pygame.mixer.music.fadeout(countdown_time * 1000)  # s -> ms
            if self.red < 255:
                self.red = self.red + 0.1
            if self.yellow > 0:
                self.yellow = self.yellow - 0.1
            color = (self.red, self.yellow, 25)

            self.update_text(str(abs(round(self._time_left, 1))), color)
        else:
            self.update_text(str(abs(round(self._time_left, 1))))

        self._time_left = self._end_time - time.time()

    def get_time_left(self):
        """
        returns remaining time

        :return: the time left in seconds
        """
        # print(self._time_left)
        return self._time_left

    async def end_timer(self):
        """ "hard" end of timer"""
        self._time_left = 0


class Score(GuiTextElement):
    """
    game score
    """

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self._score = 0
        self.update_text(f'Score: {str(self._score)}')

    def add_to_score(self, score):
        """
        adds an amount to the current score

        :param score: the amount that is added to the score
        """
        self._score += score
        self.update_text(f'Score: {str(self._score)}')

    def get_score(self):
        """
        return the current score

        :return: current score
        """
        return self._score

    def reset_score(self):
        """
        resets the score to zero
        """
        self._score = 0
        self.update_text(f'Score: {str(self._score)}')
