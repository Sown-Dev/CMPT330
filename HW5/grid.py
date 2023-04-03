# NAME:
# FILENAME:
# SUMMARY:

import pygame as pygame
from os.path import join
import csv
from math import dist

from util import *
from tile import *


class Grid:
    def __init__(self, width, height, tile_dim):
        """
        A class used to store/compute/etc. the game grid
        :param width: number of tiles horizontally
        :param height: number of tiles vertically
        :param tile_dim: pixel size (width, height) of each tile
        """
        self.width = width
        self.height = height
        self.tile_dim = tile_dim
        self.pixel_width = self.width * (self.tile_dim + 1)  # need a few extra pixels bc grid lines/spacing
        self.pixel_height = self.height * (self.tile_dim + 1)
        self.visible = False  # lets you toggle the visibility of the grid
        self.tiles, self.tile_rects = self.generate_tiles()  # creates a 2D list of tile objects that grid object holds
        self.surf = pygame.Surface((self.pixel_width + 1, self.pixel_height + 1), pygame.SRCALPHA)  # grid's surface
        self.intersections = []

    def toggle_visible(self):
        self.visible = not self.visible  # makes visible opposite of current one

    def generate_tiles(self):
        tiles, tile_rects = [], []
        for y in range(self.height):
            grid_y = y
            y *= (self.tile_dim + 1)  # need +1 for to account for gridlines/spacing
            row = []
            for x in range(self.width):
                grid_x = x
                x *= (self.tile_dim + 1)  # makes each tile 1 pixel wide (adds "gap")
                curr_tile = Tile((x + 1, y + 1), self.tile_dim, (grid_x, grid_y))
                row.append(curr_tile)
                tile_rects.append(pygame.Rect(curr_tile.get_loc()[0], curr_tile.get_loc()[1],
                                              self.tile_dim, self.tile_dim))
            tiles.append(row)
        return tiles, tile_rects

    def get_tile(self, grid_loc):  # returns tile at (x,y) location
        tile_x, tile_y = grid_loc
        return self.tiles[tile_y][tile_x]

    def get_tile_rect(self, grid_loc):  # returns the rectangle object of tile at (x,y) location
        tile_x, tile_y = grid_loc
        return self.tile_rects[(tile_y * self.width) + tile_x]

    def set_tile(self, grid_loc, new_surf, tile_vis):  # can allow you to overwrite a tile with any surface
        # new_surf should be the same size as self.tile_dim
        tile_x, tile_y = grid_loc
        self.tiles[tile_y][tile_x].set_surf(new_surf, tile_vis)

    def get_surf(self):
        if self.visible:  # draws gridlines if self.visible is true
            for y in range(self.height + 1):
                y *= (self.tile_dim + 1)
                pygame.draw.line(self.surf, (80, 243, 7), (0, y), (self.width * (self.tile_dim + 1) + 1, y))
            for x in range(self.width + 1):
                x *= (self.tile_dim + 1)
                pygame.draw.line(self.surf, (80, 243, 7), (x, 0), (x, self.height * (self.tile_dim + 1) + 1))
        for y in range(self.height):  # draws each tile on surface if it's visible (i.e., if it's a wall)
            for x in range(self.width):
                if self.tiles[y][x].is_visible():
                    self.surf.blit(self.tiles[y][x].get_surf(), self.tiles[y][x].get_loc())
        return self.surf

    def refresh(self):  # resets surface to empty, see-through (0 alpha)
        self.surf.fill((0, 0, 0, 0))

    def import_map(self, fn):
        #  lets you use a CSV (with google sheets or excel) to easily customize maps
        #  link to google sheets template: https://bit.ly/41KWbmu
        cheese_tiles = []
        dog_tiles = []
        with open(fn) as f:
            rows = csv.reader(f)
            grid = [[x for x in row] for row in rows]
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                if grid[y][x] == 'W':  # W's are walls
                    self.tiles[y][x].set_wall()
                if grid[y][x] == 'C':  # C's are the cheese tiles
                    cheese_tiles.append(to_pix((x, y)))
                elif grid[y][x] == 'D':  # D's are dog tiles
                    dog_tiles.append(to_pix((x, y)))
                elif grid[y][x] == 'IC':  # IC's are intersections AND cheeses
                    self.tiles[y][x].set_intersection()
                    cheese_tiles.append(to_pix((x, y)))
        return cheese_tiles, dog_tiles

    def get_open_tiles(self):  # returns a list of tiles without walls (could have items though)
        open_tiles = []
        for r in self.tiles:
            for t in r:
                if not t.is_wall():
                    open_tiles.append(t)
        return open_tiles

    def get_walls(self):  # returns list of only tiles with walls
        walls = []
        for r in self.tiles:
            for t in r:
                if t.is_wall():
                    walls.append(t)
        return walls

    def overlaps_wall(self, sprite_mask):  # function tests mask sprite overlap with wall and input sprite
        for wall in self.get_walls():
            if wall.in_tile(sprite_mask):  # awkwardly defined but it works ¯\_(ツ)_/¯
                return True
        return False

    def pix_to_tile(self, pix_loc):  # gives approximate grid location based on pixel location
        loc_x, loc_y = pix_loc
        closest_tile_x, closest_tile_y = None, None
        closest_tile_dist = float('inf')
        pix_rect = pygame.Rect(loc_x, loc_y, self.tile_dim, self.tile_dim)
        for idx, tile in enumerate(self.tile_rects):
            # finds tile_x, tile_y
            tile_x = idx % self.width
            tile_y = idx // self.width
            # if pixel (as a tile) would intersect tile AND distance is closer, keep track of it
            if pygame.Rect.colliderect(tile, pix_rect) and dist(tile.center, pix_rect.center) < closest_tile_dist:
                closest_tile_x, closest_tile_y = tile_x, tile_y
                closest_tile_dist = dist(tile.center, pix_rect.center)
        return closest_tile_x, closest_tile_y

    def highlight_tile(self, grid_loc, rgb=(255, 0, 255, 50)):  # sets a tile to show up as a specific color
        indicator_tile = pygame.Surface((self.tile_dim, self.tile_dim), pygame.SRCALPHA)
        indicator_tile.fill(rgb)
        self.set_tile(grid_loc, indicator_tile, True)

    def reset_tile(self, grid_loc):  # sets tile back to only showing background texture
        reset_tile = pygame.Surface((self.tile_dim, self.tile_dim), pygame.SRCALPHA)
        reset_tile.fill((0, 0, 0, 0))
        self.set_tile(grid_loc, reset_tile, False)

    def get_neighbor_tiles(self, grid_loc):  # returns list of neighbor tiles
        neighbors = []
        tx, ty = grid_loc
        for tile_x, tile_y, move_val in [(tx, ty - 1, -1), (tx, ty + 1, 1), (tx - 1, ty, -2), (tx + 1, ty, 2)]:
            if 0 <= tile_x <= (self.width - 1) and 0 <= tile_y <= (self.height - 1):
                neighbors.append([self.tiles[tile_y][tile_x], move_val])
        return neighbors


if __name__ == '__main__':
    # I was using this to test grids & tiles out -- it looks super pretty if you run just this file!
    pygame.init()
    test_tile_dim = 28
    grid_w, grid_h = 28, 32
    disp_w, disp_h = (test_tile_dim + 1) * grid_w + 1, (test_tile_dim + 1) * grid_h + 1
    bg = pygame.display.set_mode((disp_w, disp_h), pygame.SRCALPHA, 32)
    from textures import Texture

    bg_texture = Texture(join('assets', 'carpet_tile.jpg'), test_tile_dim + 1)
    bg_img = bg_texture.tiled(disp_w, disp_h)
    clock = pygame.time.Clock()
    ex_grid = Grid(grid_w, grid_h, test_tile_dim)
    ex_grid.toggle_visible()
    for x in range(grid_w):
        for y in range(grid_h):
            new_surf = pygame.Surface((test_tile_dim, test_tile_dim))
            new_surf.fill((x * 8, y * 8, (x + y) * 4))
            ex_grid.set_tile((x, y), new_surf, True)
    while True:
        bg.blit(bg_img, (0, 0))
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        bg.blit(ex_grid.get_surf(), (0, 0))
        pygame.display.update()
