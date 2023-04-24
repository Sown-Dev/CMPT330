from os.path import join

import pygame

WIDTH = 900;
HEIGHT = 600;
BGIMG = pygame.image.load(join('Assets/Sprites', 'BG.png'))

WIDTH = BGIMG.get_width();
HEIGHT = BGIMG.get_height();

BGIMG = pygame.transform.scale(BGIMG, (WIDTH, HEIGHT))