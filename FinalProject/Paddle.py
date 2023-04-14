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

    def __init__(self, playerControlled ):

        #call base
        pygame.sprite.Sprite.__init__(self)


        self.pControlled = playerControlled

        self.image = pygame.image.load(join('Assets/Sprites', 'paddle.png'))
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()


    def update(self, pressed_keys):
        if(self.pControlled):
            self.yPos += self.yVel*0.2
            self.yVel*=0.9

            if pressed_keys[pygame.K_w]:
                self.yVel-=2
            if pressed_keys[pygame.K_s]:
                self.yVel+=2


            self.rect.x = int(self.xPos)
            self.rect.y = int(self.yPos)

            
    def shoot(self):
        print("bam!")


