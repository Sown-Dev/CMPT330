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
    xVel=0

    def __init__(self, flipped, spawnPos ):

        # call base
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(join('Assets/Sprites', 'bullet.png'))
        self.image = pygame.transform.flip(self.image, flipped, False)
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()
        self.flipped = flipped
        self.xVel = 80 if flipped else -80;

        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]
        self.xPos = self.rect.x
        self.yPos = self.rect.y
    def update(self):
        self.xPos = self.xVel*0.2
        self.xVel *=0.99


        self.rect.x = int(self.xPos)
        self.rect.y = int(self.yPos)


