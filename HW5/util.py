# NAME:
# FILENAME:
# SUMMARY:

import pygame
from os.path import join

DEBUG = False  # boolean to toggle "debug mode"
"""
Functionality from debug mode:
(1) shows gridlines
(2) game doesn't end if player dies
(3) cats show their current waypoint (same color as them)
(4) cats show current legal moves (same color as them)
(5) can force dog token mode by pressing the "Enter" key
(6+) anything you want to add!
"""

GRID_W = 28  # number of tiles in each row
GRID_H = 31  # number of tiles in each column
TILE_SIZE = 20  # note: your mileage may vary if you change this value (certain things are hard-coded for this value)
SCORE_MARGIN = 36  # amount of space in top for scores
SCREEN_W = TILE_SIZE * GRID_W + (GRID_W - 1)  # sets actual screen width in pixels
SCREEN_H = TILE_SIZE * GRID_H + (GRID_H - 1) + SCORE_MARGIN  # sets actual screen width in pixls
FPS = 30  # manually sets max frame rate

# starting tile locations for cats
BROWN_START = (1, 1)
BLACK_START = (26, 1)
ORANGE_START = (26, 29)
WHITE_START = (1, 29)

DOG_TIME_LEN = 4  # number of seconds that dog time lasts
CHEESE_RESPAWN_TIME = 15  # number of seconds for cheese to respawn
DOG_RESPAWN_TIME = 30  # number of seconds for dog to respawn

# loads in bmg but DOES NOT play it!  Playing should happen in game.py
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load(join("assets", "bgm.wav"))

# loads but DOES NOT play 3 requested sound effects
defeat_cat = pygame.mixer.Sound(join("assets", "defeat_cat.ogg"))
dog_bark = pygame.mixer.Sound(join("assets", "dog_bark.ogg"))
mouse_eat = pygame.mixer.Sound(join("assets", "mouse_eat.ogg"))


def manhattan_dist(pt_1, pt_2):
    # distance discussed in class, not used but here if you want to experiment
    return abs(pt_1[0] - pt_2[0]) + abs(pt_1[1] - pt_2[1])


def to_pix(loc):
    # converts an x,y pair from a grid location to a pixel location (top-left corner of corresponding tile)
    grid_x, grid_y = loc
    pixel_x = grid_x * (TILE_SIZE + 1)
    pixel_y = grid_y * (TILE_SIZE + 1)
    return pixel_x, pixel_y


def sign(x):
    # returns 1 if positive, -1 if negative, 0 if 0
    try:
        return x / abs(x)
    except:
        return 0
