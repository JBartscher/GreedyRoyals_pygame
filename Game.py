import asyncio
import os
from random import randint

import pygame
from pygame import transform
from pygame.locals import *

from sprite.animated_sprite_group import AnimatedGroup
from sprite.coin import Coin
from game_objects.game_statics import SCREENWIDTH, SCREENHEIGHT, INITIAL_TIME, FPS, WINDOW_SIZE
from game_objects.gui_elements import Countdown, Score
from game_objects.highscore import Highscore
from sprite.hourglass import Hourglass
from sprite.king import King
from game_objects.menu import Menu
from sprite.my_spirtesheet import Spritesheet

# Pygame Setup
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('GREEDY ROYALS')

icon_sprite = Spritesheet(os.path.dirname(__file__) + '/resources/sprites/characters_black.png')
icon = icon_sprite.image_at((6 * 32, 32, 32, 32), colorkey=Color('black'))
pygame.display.set_icon(icon)

# Sprites
floor = py_image = pygame.image.load(os.path.dirname(__file__) + '/resources/sprites/cropped_floor.png').convert()
coin = Coin()
hourglass = Hourglass()
king_sprites = AnimatedGroup()

# GUI Elements
score = Score(x=0, y=0)
countdown = Countdown(x=SCREENWIDTH - 100, y=0, initial_time=INITIAL_TIME)


def blit_alpha(target, source, location, opacity):
    """
    changes the alpha channel of an surface Object

    :param target: the game surface (here: screen)
    :param source: the surface object which will be manipulated
    :param location: where we want to blit
    :param opacity: opacity that should set
    :return:
    """
    x = location[0]
    y = location[1]
    _ = pygame.Surface((source.get_width(), source.get_height())).convert()
    _.blit(target, (-x, -y))
    _.blit(source, (0, 0))
    _.set_alpha(opacity)
    target.blit(_, location)


def replace_king_with_faster_king(old_king: King):
    """
    takes the collided king and replaces him with a new faster one which is placed randomly on the display
    :param old_king: king which has collided with the mouse cursor on click
    """
    speed = old_king.get_speed()
    king_sprites.remove(old_king)
    # create new king at random position
    faster_king = King(randint(0, SCREENWIDTH), randint(0, SCREENHEIGHT), speed + 0.25)
    king_sprites.add(faster_king)


async def update():
    for e in pygame.event.get():
        # exit application
        if e.type == pygame.QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            pygame.quit()
            quit(1)

        if e.type == MOUSEBUTTONDOWN:
            coin.x, coin.y = pygame.mouse.get_pos()
            for king in king_sprites:
                # collision with mouse is detected -> new faster king and points for the player
                if king.collides_with(coin):
                    score.add_to_score(1 * king.get_speed())
                    replace_king_with_faster_king(old_king=king)
                    coin.play_plink_sound()

    # GUI Elements
    screen.blit(transform.scale(floor, WINDOW_SIZE), (0, 0))  # floor image
    blit_alpha(screen, transform.scale(hourglass.get_image(), (40, 54)), (SCREENWIDTH - 40, 8), 150)  # hourglass
    screen.blit(transform.scale(countdown.get_text(), (64, 64)), countdown.get_pos())  # countdown
    screen.blit(transform.scale(score.get_text(), (128, 64)), score.get_pos())  # score

    # Game Objects
    king_sprites.update()
    king_sprites.draw(surface=screen)
    # coin cursor is blitted separately to ensure that it is always "on top"
    m_pos = pygame.mouse.get_pos()
    screen.blit(transform.scale(coin.get_image(), (16, 16)), (m_pos[0]-8, m_pos[1]-8))

    pygame.display.flip()

    clock.tick(FPS)


def start_game():
    """
    method which starts the actual game
    """
    # if the game is stated over the king sprites need to be reinitialized
    pygame.mouse.set_visible(False)  # cursor will be replaced with the coin
    king_sprites.reset()

    # start music
    pygame.mixer.music.load("resources/sounds/bugle_call_rag.ogg")
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(1.5)  # skip "mute" start

    # start of the actual game loop

    loop = asyncio.get_event_loop()
    loop.run_until_complete(countdown.start_timer())

    # async processing of game logic and the game counter
    while countdown.get_time_left() >= 0:
        loop.run_until_complete(countdown.tick())
        loop.run_until_complete(update())
    # game ended. Add game score to highscores and (re)start of the main menu
    Highscore.add_highscore(score.get_score())
    start_main_menu()


def start_main_menu():
    """
    method which creates and displays the main menu
    """
    pygame.mouse.set_visible(False)
    score.reset_score()

    menu = Menu(surface=screen, clock=clock, start_game_function=start_game)
    menu.display_menu()


if __name__ == "__main__":
    start_main_menu()
