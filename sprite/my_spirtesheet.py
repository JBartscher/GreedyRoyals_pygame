# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame


class Spritesheet(object):
    def __init__(self, filename):
        """
        It is mandatory to convert the sprite-base-image to RGBA Mode. If this is not done the Colors of the animation
        starts to "spill".
        Therefore you cant use pygame.image.load(<file>).convert() because .convert() creates the spill. Ive found two
        fixes for the issue:
            1. use the "pillow" (former PIL) library. to convert the image to RGBA mode

            def make_correct_pygame_image(filename):
                image = Image.open(filename)
                image = image.convert('RGBA')
                mode = image.mode
                size = image.size
                data = image.tobytes()

                return pygame.image.fromstring(data, size, mode)

            2. use the method convert_alpha() instead of .convert()

            def make_correct_pygame_image(filename):
                return pygame.image.load(filename).convert_alpha()

        If you use the convert_alpha() or make_correct_pygame_image() method pygame draws the background of the image too.
        For this Issues with transperency I generally fill the background of Spritesheets BLACK because white tends to
        have the "spill" issue. And just use convert().

        See:
            https://stackoverflow.com/questions/328061/how-to-make-a-surface-with-a-transparent-background-in-pygame
            https://nerdparadise.com/programming/pygameblitopacity

        :param filename: file which holds the sprite images.
        """
        try:
            py_image = pygame.image.load(filename).convert()
            self.sheet = py_image

        except pygame.error as message:
            print(f'Unable to load spritesheet image: {filename}')
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]

        return self.images_at(tups, colorkey)
