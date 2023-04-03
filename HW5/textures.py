# NAME:
# FILENAME:
# SUMMARY:

import pygame


class Texture:
    def __init__(self, img_path, dim):
        """
        A (perhaps overkill?) class for storing/computing/running textures in pygame
        As-is, this only repeats a SINGLE texture
        :param img_path: path to image for texture
        :param dim: width of the base image within the texture
        """
        self.image = pygame.image.load(img_path)
        self.dim = dim  # dimension of each square of the texture (e.g., 28x28, so a big image would have several)
        self.image = pygame.transform.scale(self.image, (self.dim, self.dim))
        self.image.set_alpha(85)

    def tiled(self, max_width, max_height):
        tiled_surf = pygame.Surface((max_width, max_height))
        for x in range(0, max_width + 1, self.dim):
            for y in range(0, max_height + 1, self.dim):
                tiled_surf.blit(self.image, (x, y))  # these makes a 1 surface made of several tiles of self.image
        return tiled_surf
