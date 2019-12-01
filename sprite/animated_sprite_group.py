from pygame import transform
from pygame.sprite import Group

from game_objects.game_statics import SCREENWIDTH, SCREENHEIGHT
from sprite.king import King


class AnimatedGroup(Group):

    def __init__(self, *sprites):
        super().__init__(sprites)

    def draw(self, surface, transform_tuple=(64, 64)):
        """draw all sprites onto the surface

        Group.draw(surface): return None

        Draws all of the member sprites onto the given surface.
        """
        sprites = self.sprites()
        for spr in sprites:
            surface.blit(transform.scale(spr.get_image(), transform_tuple), spr.get_position())

    def reset(self):
        """ resets the sprite group and its sprites """
        self.spritedict = {}
        king1 = King(x=0, y=0)
        king2 = King(x=SCREENWIDTH, y=0)
        king3 = King(x=0, y=SCREENHEIGHT)
        king4 = King(x=SCREENWIDTH, y=SCREENHEIGHT)
        king5 = King(x=SCREENWIDTH / 2, y=SCREENHEIGHT / 2)

        self.add([king1, king2, king3, king4, king5])
