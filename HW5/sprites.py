# NAME:
# FILENAME:
# SUMMARY:
import math

import pygame
from os.path import join
from math import dist, inf
from util import *
from random import choice


class Mouse(pygame.sprite.Sprite):
    def __init__(self, start_tile):
        """
        Mouse class for the player character's sprite.
        :param start_tile: Tile() object at which the mouse starts the game.
        """
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load(join('assets', 'rat.png'))  # loads rat spritesheet
        self.frames = {}  # creates the frames dictionary where each key holds a list of 3 frames in correct order
        self.load_animation_frames()  # fills the frames with images (surfaces)
        self.image = self.frames['down'][1]  # starter frame
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.masks = {}  # same as .frames but for masks
        self.load_animation_masks()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_tile.get_loc()
        self.float_x, self.float_y = float(self.rect.x), float(self.rect.y)  # using floats for easier fluid movement
        self.dx = self.dy = (TILE_SIZE + 1) / 8  # fractional amount of movement
        self.move_left, self.move_right, self.move_up, self.move_right = False, False, False, False  # movement bools
        self.dog_timer = 0  # timer for when you pick up a dog item (causes cats to be scared like in pac-man)
        self.dog_timer_max = DOG_TIME_LEN * 1000  # maximum time limit (DOG_TIME_LEN) for dog, defined in util.py
        self.dog_active = False  # boolean flag for whether dog is active
        self.curr_tile = start_tile  # beginning current tile is start tile
        self.left_teleport = True  # weird boolean to help with teleport move

        # new vars:
        self.total_frames = 0
        self.frame_timing_mod = 3
        self.frame_num = 0

    def load_animation_frames(self):
        """
        Fills frames dictionary with lists of frames per movement direction
        """
        x_vals = [0, 32, 64]
        y_off = {'up': 0, 'right': 32, 'down': 64, 'left': 96}
        ss_w, ss_h = self.sprite_sheet.get_width(), self.sprite_sheet.get_height()
        empty = pygame.Surface((ss_w, ss_h + 32), pygame.SRCALPHA, 32)
        empty.blit(self.sprite_sheet, (0, 0))  # gives some extra space to help with cropping below
        self.sprite_sheet = empty.copy()

        # sets initial values of frames to cropped portions of sprite sheet
        for move_dir in y_off.keys():
            self.frames[move_dir] = [pygame.Surface.subsurface(self.sprite_sheet, (i, 0 + y_off[move_dir], 32, 48)) for
                                     i in x_vals]

        # crops each direction's frames based on image specifics, NOTE: these are hard-coded, do not change theses!
        # this makes the sprites as large as possible while keeping proportions
        self.frames['up'] = [pygame.Surface.subsurface(t, (3, 5, 27, 27)) for t in self.frames['up']]
        self.frames['right'] = [pygame.Surface.subsurface(t, (0, 6, 32, 32)) for t in self.frames['right']]
        self.frames['down'] = [pygame.Surface.subsurface(t, (3, 4, 26, 26)) for t in self.frames['down']]
        self.frames['left'] = [pygame.Surface.subsurface(t, (0, 6, 32, 32)) for t in self.frames['left']]

        # This part scales each frame back to (TILE_SIZE, TILE_SIZE) size at most (keeps side proportions the same)
        for k in ['up', 'down']:
            scale = TILE_SIZE / self.frames[k][0].get_height()  # taller image --> width scaled based on height
            self.frames[k] = [pygame.transform.scale(t, (scale * t.get_width(), TILE_SIZE)) for t in self.frames[k]]
        for k in ['left', 'right']:
            scale = TILE_SIZE / self.frames[k][0].get_width()  # wider image --> height scaled based on width
            self.frames[k] = [pygame.transform.scale(t, (TILE_SIZE, scale * t.get_height())) for t in self.frames[k]]

    def load_animation_masks(self):
        """
        Creates masks dictionary with a mask for each surface in the frames dictionary.
        """
        for k in self.frames.keys():
            self.masks[k] = [pygame.mask.from_surface(t) for t in self.frames[k]]

    def check_bounds(self, grid):
        """
        Makes sure that the player stays in bounds.  May be unneeded now?
        :param grid: the current game's grid
        :return:
        """
        if self.rect.x <= 0:  # too far left
            self.float_x = 0.0
            self.rect.x = 0
        elif (self.rect.x + self.rect.width) >= SCREEN_W:  # too far right
            self.float_x = float(SCREEN_W - self.rect.width)
            self.rect.x = SCREEN_W - self.rect.width
        if self.rect.y <= 0:  # too far up
            self.float_y = 0.0
            self.rect.y = 0
        elif (self.rect.y + self.rect.height) >= SCREEN_H:  # too far down
            self.float_y = float(SCREEN_H - self.rect.height)
            self.rect.y = SCREEN_H - self.rect.height
        if self.curr_tile.get_grid_loc() == (0, 14) and self.left_teleport is True:  # left tile ==> teleport to right
            self.curr_tile = grid.get_tile((27, 14))
            self.rect.x, self.rect.y = self.curr_tile.get_loc()
            self.float_x, self.float_y = float(self.rect.x), float(self.rect.y)
            self.left_teleport = False
        elif self.curr_tile.get_grid_loc() == (27, 14) and self.left_teleport is True:  # right tile ==> teleport left
            self.curr_tile = grid.get_tile((0, 14))
            self.rect.x, self.rect.y = self.curr_tile.get_loc()
            self.float_x, self.float_y = float(self.rect.x), float(self.rect.y)
            self.left_teleport = False
        elif self.curr_tile.get_grid_loc() not in [(0, 14), (27, 14)]:  # prevents teleportation loop
            self.left_teleport = True

    def toggle_dog_active(self):
        self.dog_active = not self.dog_active  # reverses dog boolean

    def force_dog_active(self):  # used for debugging to manually turn on dog mode
        self.dog_active = True

    def get_dog_active(self):  # returns dog boolean
        return self.dog_active

    def get_curr_tile(self):  # returns object for currently-located tile
        return self.curr_tile

    def update(self, pressed_keys, grid, timer):
        """
        Important update function for mouse.
        :param pressed_keys: list of booleans indicating if button is (true) or isn't (false) pressed
        :param grid: grid object for current game
        :param timer: current time in game (from pygame)
        """
        self.move_left, self.move_right, self.move_up, self.move_down = False, False, False, False
        self.total_frames = (self.total_frames + 1) % self.frame_timing_mod


        if pressed_keys[pygame.K_a]:
            self.move_left = True
            self.image = self.frames['left'][self.frame_num]
            self.mask = self.masks['left'][self.frame_num]
            if (self.total_frames % self.frame_timing_mod) == 0:
                self.frame_num = (self.frame_num + 1) % len(self.frames['left'])

        if pressed_keys[pygame.K_d]:
            self.move_right = True
            self.image = self.frames['right'][self.frame_num]
            self.mask = self.masks['right'][self.frame_num]
            if (self.total_frames % self.frame_timing_mod) == 0:
                self.frame_num = (self.frame_num + 1) % len(self.frames['right'])
        if pressed_keys[pygame.K_w]:
            self.move_up = True
            self.image = self.frames['up'][self.frame_num]
            self.mask = self.masks['up'][self.frame_num]
            if (self.total_frames % self.frame_timing_mod) == 0:
                self.frame_num = (self.frame_num + 1) % len(self.frames['up'])
        if pressed_keys[pygame.K_s]:
            self.move_down = True
            self.image = self.frames['down'][self.frame_num]
            self.mask = self.masks['down'][self.frame_num]
            if (self.total_frames % self.frame_timing_mod) == 0:
                self.frame_num = (self.frame_num + 1) % len(self.frames['down'])

        if DEBUG and pressed_keys[pygame.K_RETURN]:  # can force
            self.force_dog_active()

        # updates location based on button(s) pressed
        x_move = (self.move_left * -1 * self.dx) + (self.move_right * self.dx)
        y_move = (self.move_up * -1 * self.dy) + (self.move_down * self.dy)
        self.float_x += x_move
        self.float_y += y_move
        self.rect.x = int(self.float_x)
        self.rect.y = int(self.float_y)

        # checks for collisions with any walls
        if pygame.sprite.spritecollideany(self, pygame.sprite.Group(grid.get_walls())):
            self.float_x -= x_move  # undoes movement (before rendering) if it would result in collision
            self.float_y -= y_move
            self.rect.x = int(self.float_x)
            self.rect.y = int(self.float_y)
        self.check_bounds(grid)  # makes sure it's not in an incorrect spot
        if self.dog_active:
            self.dog_timer += timer
            if self.dog_timer > self.dog_timer_max:
                self.dog_timer = 0  # need to reset timer to 0 once done
                self.dog_active = False  # need to reset flag to false once done

        approx_grid_loc = grid.pix_to_tile((self.rect.x, self.rect.y))
        self.curr_tile = grid.get_tile(approx_grid_loc)


class Cat(pygame.sprite.Sprite):
    def __init__(self, start_tile, start_wp_idx, grid):
        """
        A class holding all the information for the stars of the show -- the cat opponents!  These
        are like the ghosts in Pac-Man.
        :param start_tile: starting tile of cat (in grid)
        :param start_wp_idx: starting waypoint index (probably want to remove later)
        :param grid: the grid object for the game map
        """
        pygame.sprite.Sprite.__init__(self)
        self.color = None
        self.color_rgb = (128, 128, 128)
        self.sprite_sheet = pygame.image.load(join('assets', 'cat.png'))
        self.xoff = 0  # horizontal offset for processing spritesheet
        self.frames = {}  # frames dictionary
        self.load_animation_frames()  # frames loading function
        self.total_frames = 0  # total number of frames experienced (helps with animation)
        self.frame_num = 0  # current frame number (in relation to list of frames)
        self.frame_timing_mod = 3  # helps slow down the visible "speed" of the cat animations
        self.image = self.frames['-1'][1]  # setting the "current" image to the normal (non-scared) one
        self.image_hidden = self.image.copy()  # making a copy of starting image for hidden (invisible)
        self.image_hidden.set_alpha(0)  # making the hidden copy invisible by setting alpha = 0
        self.rect = self.image.get_rect()  # need to get rectangle from image for pygame sprite
        self.rect.x, self.rect.y = start_tile.get_loc()
        self.float_x, self.float_y = float(self.rect.x), float(self.rect.y)  # float_x,y help with fractional movement
        self.mask = pygame.mask.from_surface(self.image)  # extracting mask for better collisions
        self.masks = {}  # masks dictioanry
        self.load_animation_masks()  # loads dictionary full of masks for each frame for each move
        self.scared_frames = {}  # scared frames dictionary
        self.load_scared_frames()  # loads dictionary of scared (negative) version each frame for each move
        self.dx = self.dy = (TILE_SIZE + 1) / 10  # slightly slower speed than PC
        self.move_left, self.move_right, self.move_up, self.move_down = False, False, False, False
        self.curr_dir = 6  # non-standard starting value (will be -1, -2, 1, or 2 once the game starts)
        self.waypoints = [grid.get_tile((1, 1)), grid.get_tile((26, 1)),  # waypoints for default cat settings
                          grid.get_tile((26, 29)), grid.get_tile((1, 29))]
        self.waypoint_idx = start_wp_idx  # index into waypoints list for default cat settings
        self.waypoint = self.waypoints[self.waypoint_idx]  # sets initial waypoint for default cat scenario
        if DEBUG:  # highlights waypoint tile when debugging
            grid.highlight_tile(self.waypoint.get_grid_loc(), self.color_rgb)
        self.scared = False  # flag for if cat is scared
        self.visible = True  # flag for if cat is visible
        self.refresh_timer = 0  # timer for when cat dies
        self.respawn_min = 10000  # time limit for cat to respond after dying
        self.curr_tile = start_tile  # sets curr_tile to starting tile
        self.scared_waypoint = start_tile  # sets scared waypoint to starting waypoint bc it is in an extreme corner
        self.state_change = False  # allows for going backwards when state is changed
        self.waypoint_on_pause = None  # var for holding current waypoint when it is temporarily being replaced

    def load_animation_frames(self):
        """
        Fills frames dictionary with lists of frames per movement direction
        """
        x_vals = [0, 32, 64]
        # sets initial frames
        self.frames['2'] = [pygame.Surface.subsurface(self.sprite_sheet, (i + self.xoff, 0, 32, 32)) for i in x_vals]
        self.frames['-1'] = [pygame.Surface.subsurface(self.sprite_sheet, (i + self.xoff, 32, 32, 32)) for i in x_vals]
        self.frames['1'] = [pygame.Surface.subsurface(self.sprite_sheet, (i + self.xoff, 64, 32, 32)) for i in x_vals]
        self.frames['-2'] = [pygame.Surface.subsurface(self.sprite_sheet, (i + self.xoff, 96, 32, 32)) for i in x_vals]

        # crops frames for better size/clarity
        for k in ['2', '-2']:
            self.frames[k] = [pygame.Surface.subsurface(t, (3, 6, 26, 22)) for t in self.frames[k]]  # left, right
        for k in ['1', '-1']:
            self.frames[k] = [pygame.Surface.subsurface(t, (4, 2, 26, 26)) for t in self.frames[k]]  # up, down

        # rescales frames to be as large as possible in tile
        scale = TILE_SIZE / self.frames['-1'][0].get_height()
        self.frames['-1'] = [pygame.transform.scale(t, (scale * t.get_width(), TILE_SIZE)) for t in self.frames['-1']]
        self.frames['2'] = [pygame.transform.scale(t, (scale * t.get_width(), TILE_SIZE)) for t in self.frames['2']]
        self.frames['-2'] = [pygame.transform.scale(t, (scale * t.get_width(), TILE_SIZE)) for t in self.frames['-2']]
        self.frames['1'] = [pygame.transform.scale(t, (scale * t.get_width(), TILE_SIZE)) for t in self.frames['1']]

    def load_scared_frames(self):
        for k in ['2', '-2', '1', '-1']:
            self.scared_frames[k] = []
            for t in self.frames[k]:
                scared_t = t.copy()
                for y in range(self.frames[k][0].get_height()):
                    for x in range(self.frames[k][0].get_width()):
                        # sets color of frame to negative, where each channel c becomes negative = 255-c
                        scared_r = 255 - t.get_at((x, y))[0]
                        scared_g = 255 - t.get_at((x, y))[1]
                        scared_b = 255 - t.get_at((x, y))[2]
                        scared_t.set_at((x, y), (scared_r, scared_g, scared_b, t.get_at((x, y))[3]))
                self.scared_frames[k].append(scared_t)

    def load_animation_masks(self):
        for k in self.frames.keys():
            self.masks[k] = [pygame.mask.from_surface(t) for t in self.frames[k]]

    def check_bounds(self):  # keeps sprite in map / on screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif (self.rect.x + self.rect.width) >= SCREEN_W:
            self.rect.x = SCREEN_W - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif (self.rect.y + self.rect.height) >= SCREEN_H:
            self.rect.y = SCREEN_H - self.rect.height

    def check_waypoint(self, grid, mouse):
        # roughly estimates how close waypoint is, switches to next if sufficiently close
        if dist((self.float_x, self.float_y), self.waypoint.get_loc()) < 1:
            grid.reset_tile(self.waypoint.get_grid_loc())
            self.waypoint_idx = (self.waypoint_idx + 1) % len(self.waypoints)
            self.waypoint = self.waypoints[self.waypoint_idx]

    def at_tile_midpoint(self):
        return self.rect.center == self.curr_tile.get_rect().center

    def best_move_toward_waypoint(self, neighbors, legal_moves):
        # searches list of legal moves for one that brings sprite closer to its current waypoint
        legal_moves = [lm[1] for lm in legal_moves]
        if len(legal_moves) == 0:
            if (-1 * self.curr_dir) in [n[1] for n in neighbors if not n[0].is_wall()]:
                return -1 * self.curr_dir
        best_move = (0, inf)
        for lm in legal_moves:
            if lm == -2:  # left
                self.move_left, self.move_right = True, False
                self.move_up, self.move_down = False, False
            elif lm == 2:  # right
                self.move_left, self.move_right = False, True
                self.move_up, self.move_down = False, False
            elif lm == -1:  # up
                self.move_left, self.move_right = False, False
                self.move_up, self.move_down = True, False
            elif lm == 1:  # down
                self.move_left, self.move_right = False, False
                self.move_up, self.move_down = False, True
            temp_float_x = self.rect.centerx + (self.move_left * -1 * self.dx) + (self.move_right * self.dx)
            temp_float_y = self.rect.centery + (self.move_up * -1 * self.dy) + (self.move_down * self.dy)
            proposed_dist = dist((temp_float_x, temp_float_y), self.waypoint.get_rect().center)
            if proposed_dist < best_move[1]:
                best_move = (lm, proposed_dist)
        return best_move[0]

    def set_scared(self, scared):
        # sets scared attribute to given input, adjusting its image as needed
        self.scared = scared
        self.state_change = True
        # if scared:
        #     # self.image = self.image_scared  # changes to "scared" image (an eyeball with small pupil)
        #     self.mask = pygame.mask.from_surface(self.image)
        # else:
        #     self.image = self.image_normal
        #     self.mask = pygame.mask.from_surface(self.image)

    def get_visible(self):
        return self.visible

    def move_sprite(self, neighbors):
        if self.at_tile_midpoint():
            if self.state_change:
                legal_moves = [n for n in neighbors if (not n[0].is_wall())]
                self.state_change = False
            else:
                legal_moves = [n for n in neighbors if (not n[0].is_wall()) and (self.curr_dir / n[1]) != -1]
            legal_move_vals = [lm[1] for lm in legal_moves]
            if self.curr_tile.is_intersection() or self.curr_dir == 6 or self.curr_dir not in legal_move_vals:
                self.curr_dir = self.best_move_toward_waypoint(neighbors, legal_moves)  # find next move

        self.total_frames = (self.total_frames + 1) % self.frame_timing_mod
        self.move_left, self.move_right, self.move_up, self.move_down = False, False, False, False
        move_to_attr = {'-2': 'move_left', '2': 'move_right', '-1': 'move_up', '1': 'move_down'}
        for move_dir in [-2, -1, 1, 2]:
            if self.curr_dir == int(move_dir):
                setattr(self, move_to_attr[str(move_dir)], True)
                if self.visible:
                    self.image = self.frames[str(move_dir)][self.frame_num]
                    self.mask = self.masks[str(move_dir)][self.frame_num]
                    if self.scared:
                        self.image = self.scared_frames[str(move_dir)][self.frame_num]
                if (self.total_frames % self.frame_timing_mod) == 0:
                    self.frame_num = (self.frame_num + 1) % len(self.frames[str(move_dir)])

        self.float_x += (self.move_left * -1 * self.dx) + (self.move_right * self.dx)
        self.float_x = round(self.float_x, 2)
        self.rect.x = int(self.float_x)
        self.float_y += (self.move_up * -1 * self.dy) + (self.move_down * self.dy)
        self.float_y = round(self.float_y, 2)
        self.rect.y = int(self.float_y)

    def update(self, grid, mouse, timer):
        if DEBUG:
            grid.reset_tile(self.waypoint.get_grid_loc())
        self.check_waypoint(grid, mouse)
        if DEBUG:
            grid.highlight_tile(self.waypoint.get_grid_loc(), self.color_rgb + (100,))
        if DEBUG and not grid.get_tile(self.waypoint.get_grid_loc()).is_visible():
            grid.highlight_tile(self.waypoint.get_grid_loc(), self.color_rgb + (100,))
        # if DEBUG and
        if mouse.get_dog_active() and not self.scared and self.visible:
            # if mouse currently has dog powerup running and sprite is visible, it should become scared
            self.set_scared(True)
            self.waypoint_on_pause = self.waypoint
        elif not mouse.get_dog_active() and self.scared and self.visible:
            # if dog powerup is not active and it's scared and visible, it should no longer be scared
            self.set_scared(False)
            self.waypoint = self.waypoint_on_pause
            self.waypoint_on_pause = None
        if self.scared:
            self.waypoint = self.scared_waypoint
        neighbors = grid.get_neighbor_tiles(self.curr_tile.get_grid_loc())
        if DEBUG:
            for n in neighbors:
                if not n[0].is_wall():
                    grid.reset_tile(n[0].get_grid_loc())

        self.move_sprite(neighbors)

        ret_score = 0  # value for tracking if player got points from gobbling up a cat
        if self.scared and self.visible and pygame.sprite.collide_mask(self, mouse):
            # if cat is scared and visible and collides with player, it is defeated!
            ret_score += 100  # player will gain 100 points (which function returns)
            self.image = self.image_hidden  # since it's "dead", make it invisible
            self.mask = pygame.mask.from_surface(self.image)  # readjust mask
            self.visible = False  # set visible flag to false
            defeat_cat.play()
        elif not DEBUG and self.visible and not self.scared and pygame.sprite.collide_mask(self, mouse):
            # if cat is visible and not scared and collides with the player, then PC is "killed" (game over)
            mouse.kill()
        if not self.visible:
            # if cat is not visible (dead), increment timer for becoming visible!  (respawning)
            self.refresh_timer += timer
            if self.refresh_timer > self.respawn_min:
                # if more than 10 seconds have passed, refresh timer, become visible and not scared
                # and start in the middle of the map with normal image
                self.refresh_timer = 0
                self.visible = True
                self.scared = False
                respawn_tile = choice([(grid.get_tile((13, 11)), -2), (grid.get_tile((14, 11)), 2)])
                self.rect.center = respawn_tile[0].rect.center
                self.float_x, self.float_y = self.rect.x, self.rect.y
                self.curr_dir = respawn_tile[1]
                self.mask = pygame.mask.from_surface(self.image)

        self.check_bounds()

        approx_grid_loc = grid.pix_to_tile((self.rect.x, self.rect.y))
        self.curr_tile = grid.get_tile(approx_grid_loc)

        for n in grid.get_neighbor_tiles(self.curr_tile.get_grid_loc()):
            if not n[0].is_wall() and (self.curr_dir / n[1]) != -1 and DEBUG:
                grid.highlight_tile(n[0].get_grid_loc(), self.color_rgb + (100,))

        return ret_score  # this is useful in game.py


class BlackCat(Cat):
    """
    Subclass of Cat class specifically for black cat.  Same below for white, orange, and brown cats.
    """

    def __init__(self, start_tile, grid):
        Cat.__init__(self, start_tile, 1, grid)
        pygame.sprite.Sprite.__init__(self)
        self.color = 'black'
        # self.color_rgb = (75, 68, 76)
        self.color_rgb = (112, 102, 113)
        self.xoff = 384
        self.frames = {}
        self.load_animation_frames()
        self.load_animation_masks()
        self.load_scared_frames()

    def check_waypoint(self, grid, mouse):
        # sets waypoint to current location of mouse
        self.waypoint = mouse.get_curr_tile()


class BrownCat(Cat):

    def __init__(self, start_tile, grid):
        Cat.__init__(self, start_tile, 1, grid)
        pygame.sprite.Sprite.__init__(self)  # initializes with Cat() object and THen STS ITS WN
        self.color = 'brown'
        self.color_rgb = (143, 68, 38)
        self.xoff = 256
        self.load_animation_frames()
        self.load_animation_masks()
        self.load_scared_frames()
        self.refreshWP = self.waypoint  # waypoint that refrehes
        self.timeElapsed = 0  # tracks time elapsed for counting

    # orange cat will move to a waypoint that updates to player position every 5 seconds

    def check_waypoint(self, grid, mouse):
        self.timeElapsed += 1;
        if (self.timeElapsed > 150):  # 5 seconds = 150 frames
            self.timeElapsed = 0
            self.refreshWP = mouse.get_curr_tile()

        self.waypoint = self.refreshWP


class OrangeCat(Cat):
    def __init__(self, start_tile, grid):
        Cat.__init__(self, start_tile, 3, grid)
        pygame.sprite.Sprite.__init__(self)
        self.color = 'orange'
        self.color_rgb = (217, 183, 92)
        self.xoff = 128
        self.load_animation_frames()
        self.load_animation_masks()
        self.load_scared_frames()

        # follows player if it is within 5 blocks of its position

    def check_waypoint(self, grid, mouse):
        distance = manhattan_dist(self.curr_tile.get_loc(), mouse.get_curr_tile().get_loc())
        if (distance < 5):
            super().check_waypoint(grid, mouse)
        else:
            self.waypoint = mouse.get_curr_tile()

    # def update(self, grid, mouse, timer):
    #     super().update(grid, mouse, timer)  # calls base class update, remove if overriding
    #     # can add additional functionality AFTER original update function here


class WhiteCat(Cat):
    def __init__(self, start_tile, grid):
        Cat.__init__(self, start_tile, 0, grid)
        pygame.sprite.Sprite.__init__(self)
        self.color = 'white'
        self.color_rgb = (239, 233, 231)
        self.xoff = 0
        self.load_animation_frames()
        self.load_animation_masks()
        self.load_scared_frames()

        # follows mouse by going 5 blocks under its position (if possible)

    def check_waypoint(self, grid, mouse):
        toPos = list(mouse.get_curr_tile().get_loc())
        toPos[1] += 5
        # if out of bounds, use default waypoint
        try:
            self.waypoint = grid.get_tile(tuple(toPos))
        except:
            super().check_waypoint(grid, mouse)

    # def update(self, grid, mouse, timer):
    #     super().update(grid, mouse, timer)  # calls base class update, remove if overriding
    #     # can add additional functionality AFTER original update function here


class Cheese(pygame.sprite.Sprite):
    def __init__(self, loc=None):
        """
        A class for the cheese items in the game.
        Most stuff here is about the same as (or simpler than) the Cat class.
        :param loc: starting (x,y) location of cheese sprite
        """
        pygame.sprite.Sprite.__init__(self)
        self.image_visible = pygame.image.load(join('assets', 'cheese.png'))  # loads sprite
        self.image_visible = pygame.transform.scale(self.image_visible, (TILE_SIZE, TILE_SIZE))  # scales to TILE_SIZE
        self.image_hidden = self.image_visible.copy()  # sets up ability to hide cheese
        self.image_hidden.set_alpha(0)  # makes image see-through
        self.image = self.image_visible  # starting image is visible image
        self.rect = self.image.get_rect()  # needed to link function to page
        self.rect.x, self.rect.y = loc
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = True
        self.refresh_timer = 0
        self.respawn_min = CHEESE_RESPAWN_TIME * 1000  # CHEESE_RESPAWN_TIME set in util.py

    def show_cheese(self):
        self.image = pygame.image.load(join('assets', 'cheese.png'))
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def update(self, mouse, timer):
        ret_val = 0  # this value is +1 point for player if they gobble up the cheese
        if self.visible and pygame.sprite.collide_mask(self, mouse):
            # if cheese is visible and player interacts with it, the cheese disappears and player gets 1 point
            self.image = self.image_hidden
            self.mask = pygame.mask.from_surface(self.image)
            self.visible = False
            ret_val += 1
            mouse_eat.play()
        if not self.visible:
            # if cheese is currently invisible, increment timer and become visible if enough time has passed
            self.refresh_timer += timer
            if self.refresh_timer > self.respawn_min:
                self.refresh_timer = 0
                self.visible = True
                self.image = self.image_visible
                self.mask = pygame.mask.from_surface(self.image)
        return ret_val


class Dog(pygame.sprite.Sprite):
    def __init__(self, loc=None):
        """
        A class for the dog items.  Similar to Cheese, most stuff here is similar to or simpler than the Cat class.
        :param loc:
        """
        pygame.sprite.Sprite.__init__(self)
        self.image_visible = pygame.image.load(join('assets', 'pug.png'))
        self.image_visible = pygame.Surface.subsurface(self.image_visible, (32, 64, 32, 32))
        self.image_visible = pygame.transform.scale(self.image_visible, (TILE_SIZE, TILE_SIZE))
        self.image = self.image_visible
        self.image_hidden = self.image_visible.copy()
        self.image_hidden.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = loc
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = True
        self.refresh_timer = 0
        self.respawn_min = DOG_RESPAWN_TIME * 1000

    def update(self, mouse, timer):
        if self.visible and pygame.sprite.collide_mask(self, mouse):
            # if dog is visible and player collides with it, activate "dog mode" and make token disappear!
            self.image = self.image_hidden
            self.mask = pygame.mask.from_surface(self.image)
            self.visible = False
            mouse.toggle_dog_active()
            dog_bark.play()
        if not self.visible:
            self.refresh_timer += timer
            if self.refresh_timer > self.respawn_min:
                self.visible = True
                self.image = self.image_visible
                self.mask = pygame.mask.from_surface(self.image)
        return 0  # needs to return 0 since this is called the same way a Cheese token is (will create errors otherwise)
