import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, loc, dim, grid_loc):
        """
        A class for tiles that make up the pieces of a grid object
        :param loc: (x,y) location of the tile
        :param dim: width and height (square) of tile
        :param grid_loc: grid location of tile
        """
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = loc
        self.dim = dim
        self.surf = pygame.Surface((self.dim, self.dim), pygame.SRCALPHA)
        self.visible = False
        self.wall = False
        self.intersection = False
        self.wall_color = (5, 75, 156)
        self.rect = pygame.Rect(self.x, self.y, self.dim, self.dim)
        self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        self.mask.fill()
        self.mid_x, self.mid_y = self.x + (self.dim / 2), self.y + (self.dim / 2)
        self.tile_x, self.tile_y = grid_loc

    def get_loc(self):
        return self.x, self.y

    def get_grid_loc(self):
        return self.tile_x, self.tile_y

    def get_dim(self):
        return self.dim

    def set_surf(self, new_surf, visible=None):  # lets you change surface of tile, set its visibility
        self.surf = new_surf
        if visible is not None:
            self.visible = visible

    def get_surf(self):
        if self.wall:
            self.surf.fill(self.wall_color)
        # if DEBUG and self.intersection:
        #     self.surf.fill((0, 160, 0, 100))
        return self.surf

    def is_visible(self):
        return self.visible

    def is_wall(self):
        return self.wall

    def set_wall(self, is_wall=True):  # changes wall parameter of a tile
        self.wall = is_wall
        if is_wall:
            self.visible = True

    def in_tile(self, sprite_mask):
        return pygame.mask.Mask.overlap(self.mask, sprite_mask, 0)

    def set_intersection(self, is_intersection=True):
        self.intersection = is_intersection

    def is_intersection(self):
        return self.intersection

    def get_rect(self):
        return self.rect
