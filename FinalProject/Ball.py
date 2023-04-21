# Ball class
from os.path import join

import pygame

from FinalProject.Utils import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, posx, posy,  speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(join('Assets/Sprites', 'ball.png'))

        #scale x2
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 2), int(self.size[1] * 2)))

        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.rect = self.image.get_rect()

        self.posx = posx
        self.posy = posy
        self.speed = speed
        self.xFac = 1
        self.yFac = -1


        self.firstTime = 1


    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        self.rect.x = self.posx
        self.rect.y = self.posy

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and it
        # results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= -20 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH+20 and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    # Used to reset the position of the ball
    # to the center of the screen
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1



    def getRect(self):
        return self.rect