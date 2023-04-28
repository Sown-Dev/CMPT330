from os.path import join

import pygame
from pymunk import Vec2d

WIDTH = 900;
HEIGHT = 600;
BGIMG = pygame.image.load(join('Assets/Sprites', 'BG.png'))

WIDTH = BGIMG.get_width();
HEIGHT = BGIMG.get_height();

BGIMG = pygame.transform.scale(BGIMG, (WIDTH, HEIGHT))


def flipy(p):
    """Convert pymunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)