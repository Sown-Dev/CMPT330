from os.path import join

import pygame
from pymunk import Vec2d

WIDTH = 900;
HEIGHT = 600;
BGIMG = pygame.image.load(join('Assets/Sprites', 'BG.png'))

WIDTH = BGIMG.get_width();
HEIGHT = BGIMG.get_height();

BGIMG = pygame.transform.scale(BGIMG, (WIDTH, HEIGHT))


#AUDIO
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load(join("Assets/Sounds", "Music.mp3"))

shoot = pygame.mixer.Sound(join("Assets/Sounds", "Fire 3.mp3"))
hit = pygame.mixer.Sound(join("Assets/Sounds", "Hit 1.mp3"))
gameover = pygame.mixer.Sound(join("Assets/Sounds", "Game Over.mp3"))

def flipy(p):
    """Convert pymunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)