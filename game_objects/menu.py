import os

import pygame
import pygameMenu
from pygame import transform
from pygameMenu.config import TEXT_DRAW_X, TEXT_MARGIN

from game_objects.game_statics import WINDOW_SIZE, SCREENWIDTH, SCREENHEIGHT, FPS
from game_objects.highscore import Highscore
from utils.path_utils import harmonize_path


class Menu:
    """
    class which holds and administrate the game menus
    """
    BG_COLOR = (33, 33, 33)
    BG_TITLE_COLOR = (55, 66, 77)
    WHITE = (255, 255, 255)

    def __init__(self, surface, clock, start_game_function):
        self._surface = surface
        self._clock = clock

        path = harmonize_path(os.path.join(os.path.dirname(__file__), "../resources/sprites/cropped_floor.png"))
        self._background_image = pygame.image.load(path).convert()

        self.main_menu = pygameMenu.Menu(self._surface,
                                         bgfun=self.bg_func,
                                         color_selected=Menu.WHITE,  # ausgewähltes Menüelement
                                         font="resources/fonts/VCR_OSD_MONO_1.001.ttf",
                                         # pygameMenu.font.FONT_BEBAS,
                                         font_color=Menu.WHITE,
                                         font_size=50,
                                         menu_alpha=100,
                                         menu_color=Menu.BG_COLOR,
                                         menu_color_title=Menu.BG_TITLE_COLOR,
                                         menu_height=int(WINDOW_SIZE[1] * 0.8),
                                         menu_width=int(WINDOW_SIZE[0] * 0.9),
                                         onclose=pygameMenu.events.DISABLE_CLOSE,
                                         option_shadow=False,
                                         title='GREEDY ROYALS',
                                         window_height=WINDOW_SIZE[1],
                                         window_width=WINDOW_SIZE[0]
                                         )

        self.highscore_menu = pygameMenu.TextMenu(self._surface,
                                                  bgfun=self.bg_func,
                                                  font="resources/fonts/VCR_OSD_MONO_1.001.ttf",
                                                  font_color=Menu.WHITE,
                                                  font_size=50,
                                                  menu_alpha=100,
                                                  menu_color=Menu.BG_COLOR,
                                                  menu_color_title=Menu.BG_TITLE_COLOR,
                                                  menu_width=int(WINDOW_SIZE[0] * 0.8),
                                                  menu_height=int(WINDOW_SIZE[1] * 0.8),
                                                  title="Highscore",
                                                  option_shadow=False,
                                                  window_height=WINDOW_SIZE[1],
                                                  window_width=WINDOW_SIZE[0],
                                                  # TextMenu specific parameters
                                                  draw_text_region_x=TEXT_DRAW_X,
                                                  text_align=pygameMenu.locals.ALIGN_CENTER,
                                                  text_color=Menu.BG_TITLE_COLOR,
                                                  text_fontsize=20,
                                                  text_margin=TEXT_MARGIN, )

        # create DB if necessary and fill highscore list
        Highscore.create_db()
        self.fill_highscore_list()

        self.main_menu.add_option('Play', start_game_function)
        # main_menu.add_option('About', about_menu)
        self.main_menu.add_option('Highscore', self.highscore_menu)
        self.main_menu.add_option('Quit', pygameMenu.events.EXIT)

    def display_menu(self):
        """
        menu "game" loop which displays them menu until the game ist started or the application is closed
        """
        while True:

            self.main_menu.set_fps(FPS)
            # Tick
            self._clock.tick(FPS)

            # Application events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

            self.main_menu.mainloop(events, disable_loop=True)

            pygame.display.flip()

    def bg_func(self):
        """
        adds the tiled background to a menu background
        """
        self._surface.blit(transform.scale(self._background_image, WINDOW_SIZE), (0, 0))

    def fill_highscore_list(self):
        highscores = Highscore.select_top_five()
        for h in highscores:
            self.highscore_menu.add_line(f"{h[1]}. - {h[0]}")


if __name__ == "__main__":
    """
    Test
    """


    def start_function_stub():
        print("GAME START DUMMY")


    surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    clock = pygame.time.Clock()
    pygame.init()

    pygame.mouse.set_visible(False)  # cursor will be replaced with the coin

    m = Menu(surface=surface, clock=clock, start_game_function=start_function_stub)
    m.display_menu()
