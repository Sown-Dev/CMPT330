import math

import pygame
from os.path import join
from math import dist, inf
from random import choice

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


    def update(self, pressed_keys, ball):
        self.yPos += self.yVel * 0.2
        self.yVel *= 0.95

        if(self.pControlled):

            if pressed_keys[pygame.K_w]:
                self.yVel-=2.2
            if pressed_keys[pygame.K_s]:
                self.yVel+=2.2


        else:
            #AI stuff
            if(ball.rect.y>self.yPos+10):
                self.yVel+=2.2
            if (ball.rect.y < self.yPos - 10):
                self.yVel -= 2.2


        self.rect.x = int(self.xPos)
        self.rect.y = int(self.yPos)


            
    def shoot(self):
        print("bam!")


