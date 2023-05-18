import math

import pygame
from os.path import join
from math import dist, inf
from random import choice

import pymunk

from FinalProject.GameMan import offset


class Bullet(pygame.sprite.Sprite):
    yPos = 0
    xPos = 0
    flipped = False
    yVel = 0
    xVel=0

    def __init__(self, flipped, spawnPos , space):

        # call base
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(join('Assets/Sprites', 'bullet.png'))
        self.image = pygame.transform.flip(self.image, flipped, False)
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()
        self.flipped = flipped
        self.xVel = -80 if flipped else 80;

        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]
        self.xPos = self.rect.x
        self.yPos = self.rect.y

        self.body = pymunk.Body(0.8, 100)
        self.body.position = (self.xPos, self.yPos)
        self.shape = pymunk.Circle(self.body, 3)
        self.shape.elasticity = 1
        self.shape.collision_type = 4

        self.body.velocity = -320 if flipped else 320,0
        space.add(self.body, self.shape)

        self.timeLeft = 130 #120/30 = 4 seconds
    def update(self,space, ball):
       self.rect.x = self.body.position.x
       self.rect.y= self.body.position.y
       self.timeLeft -= 1
       if(self.timeLeft==0):
           space.remove(self.body, self.shape)
           self.kill()

       if (pygame.mask.Mask.overlap(ball.mask, self.mask, offset(ball,self))):
           self.timeLeft=4



