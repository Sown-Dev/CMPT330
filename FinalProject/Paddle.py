import math
import random

import pygame
from os.path import join
from math import dist, inf
from random import choice

import pymunk

from FinalProject.Bullet import Bullet
from FinalProject.Utils import WIDTH, HEIGHT


class Paddle(pygame.sprite.Sprite):

    yPos =0
    xPos =0
    flipped=False
    yVel=0

    def __init__(self, playerControlled, isflipped, spawnPos=(0,0) ):

        flipped = isflipped
        #call base
        pygame.sprite.Sprite.__init__(self)


        self.pControlled = playerControlled

        self.image = pygame.image.load(join('Assets/Sprites', 'paddle.png'))
        self.image = pygame.transform.flip(self.image, flipped, False)
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()
        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]
        self.xPos = self.rect.x
        self.yPos = self.rect.y


        #personal sprite groups:
        self.bullets = pygame.sprite.Group()

        self.shotLast = False

        self.body = pymunk.Body(1000, 100)
        self.body.position = (self.xPos, self.yPos)
        self.shape = pymunk.Circle(self.body, 25)
        self.shape.elasticity = 1
        self.shape.collision_type = 3

        self.shootdelay = 20

    def update(self, pressed_keys, ball, bg, space):
        self.shootdelay-=1

        for b in self.bullets:
            b.update(space,ball)

        self.bullets.draw(bg)


        self.yPos += self.yVel * 0.2
        self.yVel *= 0.95

        if(self.pControlled):

            if pressed_keys[pygame.K_w]:
                self.yVel-=2.2
            if pressed_keys[pygame.K_s]:
                self.yVel+=2.2

            if pressed_keys[pygame.K_SPACE]:
                if(not self.shotLast and self.shootdelay<0):
                    self.shootdelay = 30
                    self.shoot(space)
            else:
                self.shotLast=False


        else:
            #AI stuff
            if(random.random()< (abs(ball.rect.x-self.yPos)/WIDTH)+0.1):
                if(ball.rect.y<self.yPos+8 and ball.rect.y>self.yPos-8):
                    if(self.shootdelay<0):
                        self.shootdelay = 35
                        self.shoot(space)
                if(ball.rect.y>self.yPos+10):
                    self.yVel+=2.4
                if (ball.rect.y < self.yPos - 10):
                    self.yVel -= 2.4

        if(self.yPos <20):
            self.yPos=20
            self.yVel*= -0.4
        if(self.yPos >HEIGHT-20):
            self.yPos = HEIGHT-20
            self.yVel *=-0.4

        self.rect.x = int(self.xPos) - self.image.get_width()/2
        self.rect.y = int(self.yPos) - self.image.get_height()/2

        # update body to current position
        self.body.position = (self.xPos + (-24 if self.pControlled else 24), self.yPos)

    def shoot(self, space):
        bul = Bullet(self.flipped, (self.xPos,self.yPos), space)
        self.bullets.add(bul)


