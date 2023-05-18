# Ball class
from enum import Enum
from os.path import join
from random import random

import pygame
import pymunk

from FinalProject.Utils import *

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
class Ball(pygame.sprite.Sprite):


    body= pymunk.Body(1, 100)
    shape = pymunk.Circle(body, 20)
    def __init__(self, posx, posy,  speed,space, difficulty = Difficulty.EASY, ):

        """
        self.mass = 10
        self.radius = 25
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(self.mass, self.inertia)
        self.body.position = self.x, 200
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        self.shape.elasticity = 0.95
        self.shape.friction = 0.9
        space.add(self.body, self.shape)
        #_balls.append(self.shape)
        """

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(join('Assets/Sprites', 'ball.png'))

        #scale x2
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 2), int(self.size[1] * 2)))

        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()

        self.speed = speed
        self.xFac = 1
        self.yFac = -1
        self.dif = difficulty

        self.firstTime = 1

        self.body.position = (posx,posy)
        self.shape = pymunk.Circle(self.body, 16)
        self.shape.elasticity = 1
        self.shape.collision_type = 3

        self.reset(-1)

    def update(self):

        """ Code for having constant speed
        direction = self.body.velocity.normalized()
        new_velocity = direction * (self.speed* 40)
        self.body.velocity = new_velocity"""

        self.posx = self.body.position[0]
        self.posy= self.body.position[1]

        self.rect.x = self.posx-self.image.get_width()/2
        self.rect.y = self.posy-self.image.get_height()/2

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and it
        # results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= -20 and self.firstTime:
            return 1
        elif self.posx >= WIDTH+20 and self.firstTime:
            return -1
        else:
            return 0

    # Used to reset the position of the ball
    # to the center of the screen
    def reset(self, point):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.body.position = (self.posx,self.posy)

        self.body.velocity = (100, -100)

        if(point == 1):
            self.body.velocity = (100, -100)

        if(point == -1):
            self.body.velocity = (-100, -100)


    # Used to reflect the ball along the X-axis

    hitcooldown=0
    def hit(self):
        if(self.hitcooldown<=0):
            self.hitcooldown=10
            self.xFac *= -1



    def getRect(self):
        return self.rect