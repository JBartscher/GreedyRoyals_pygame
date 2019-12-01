from pygame.sprite import Sprite


class Animated(Sprite):

    def __int__(self, x=None, y=None, width=None, height=None):
        super().__init__()
        self._current_animation = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_image(self):
        """
        gets the next image in the animation.

        :return: enxt image in the animation
        """
        return self._current_animation.next()

    def get_position(self):
        """
        returns the current position of the Object

        :return: x and y position
        """
        return self.x, self.y
