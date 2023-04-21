import math

import pygame
from os.path import join
from math import dist, inf
from random import choice


class Bullet(pygame.sprite.Sprite):
    yPos = 0
    xPos = 0
    flipped = False
    yVel = 0

    def __init__(self, playerControlled):

        # call base
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(join('Assets/Sprites', 'bullet.png'))
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()

    def update(self):
        self.yPos += self.yVel * 0.2
        self.yVel *= 0.9


