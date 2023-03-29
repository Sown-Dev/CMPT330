# NAME: Misha Smirnov
# FILENAME: HW4.py
# SUMMARY: Added 3 new powerups: invincibility, lives, and size rest.
# also added a new falling powerup that grants lives.
# In addition, added high score system with file and a lives UI element.

# vehicle assets from https://kenney.nl/assets/pixel-vehicle-pack
# block assets from https://kenney.nl/assets/sokoban
# tool assets from https://kenney.nl/assets/generic-items
# powerup diamond from https://kenney.nl/assets/puzzle-pack

import pygame
from random import randint, choice, random
from os.path import join
from glob import glob

SCREEN_W, SCREEN_H = 750, 450
FPS = 30


class Vehicle(pygame.sprite.Sprite):
    """
    A class for the player character (PC) sprite.
    """

    lives = 1
    size=1
    invintime = 0 #how much time you are invincible. decrements by 1 each frame
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # this is a subclass of the pygame.sprite.Sprite class
        # lots of this is stuff required for the sprite class to do it sstuff
        self.image = pygame.image.load(choice(glob(join('assets', 'vehicles', '*.png'))))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_W / 2) - (self.rect.width / 2)
        self.rect.y = (SCREEN_H - 1) - self.rect.height
        self.left = False  # boolean storing whether or not the vehicle is facing left or right
        self.dx = 6  # horizontal speed of car

    grow_scale = 1.5  # amount to increase/decrease sprite size by

    def grow(self):
        self.size*=self.grow_scale
        new_w = self.rect.width * self.grow_scale
        new_h = self.rect.height * self.grow_scale
        old_w, old_x = self.rect.width, self.rect.x
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.rect = self.image.get_rect()
        self.rect.x = old_x - 0.5 * (self.rect.width - new_w)  # need to adjust location so that it grows "in place"
        self.rect.y = (SCREEN_H - 1) - self.rect.height  # need to adjust location so that it grows "in place"

    def increase_speed(self):
        self.dx += 4

    def size_reset(self):

        grow_scale = 1/(self.size)
        self.size=1
        new_w = self.rect.width * grow_scale
        new_h = self.rect.height * grow_scale
        old_w, old_x = self.rect.width, self.rect.x
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.rect = self.image.get_rect()
        self.rect.x = old_x - 0.5 * (self.rect.width - new_w)  # need to adjust location so that it grows "in place"
        self.rect.y = (SCREEN_H - 1) - self.rect.height  # need to adjust location so that it grows "in place"
    def update(self, pressed_keys):
        if(self.invintime>0):
            self.invintime-=1
        if pressed_keys[pygame.K_a]:  # returns 1 if 'a' key is pressed, 0 if not pressed
            self.rect.x -= self.dx
            if self.left is False:  # flips car sprite horizointally once if still facing right
                self.image = pygame.transform.flip(self.image, True, False)
                self.left = True
        if pressed_keys[pygame.K_d]:  # returns 1 if 'd' key is pressed, 0 if not pressed
            self.rect.x += self.dx
            if self.left is True:  # flips car sprite horizointally once if still facing left
                self.image = pygame.transform.flip(self.image, True, False)
                self.left = False
        # checks if box is outside of screen, based on x and y (top-left corner coordinates of box)
        if self.rect.x <= 0:
            self.rect.x = 0
        elif (self.rect.x + self.rect.width) >= SCREEN_W:
            self.rect.x = SCREEN_W - self.rect.width


class FallingBlock(pygame.sprite.Sprite):
    """
    A class for falling blocks that end the game if they hit the user's vehicle.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(choice(glob(join('assets', 'blocks', '*.png'))))  # loads random block image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, SCREEN_W - self.rect.width)  # randomly starts in random x position fully on screen
        self.rect.y = 0  # starts visible at top of screen
        self.dy = randint(3, 9)  # random integer vertical speed makes game more interesting

    def update(self):
        # checks if box is outside of screen, based on x and y (top-left corner coordinates of box)
        self.rect.y += self.dy
        if self.rect.y >= SCREEN_W - self.rect.height:  # removes object if it goes off screen
            self.kill()  # removes object from lists, is no longer updated/drawn

class FallingPower(pygame.sprite.Sprite):
    """
    A class for falling power ups that add lives
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(choice(glob(join('assets', 'diamonds', 'element_yellow_diamond_glossy.png'))))  # loads random block image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, SCREEN_W - self.rect.width)  # randomly starts in random x position fully on screen
        self.rect.y = 0  # starts visible at top of screen
        self.dy = randint(2, 6)  # random integer vertical speed makes game more interesting

    def update(self):
        # checks if box is outside of screen, based on x and y (top-left corner coordinates of box)
        self.rect.y += self.dy
        if self.rect.y >= SCREEN_W - self.rect.height:  # removes object if it goes off screen
            self.kill()  # removes object from lists, is no longer updated/drawn


class LaunchedTool(pygame.sprite.Sprite):
    """
    A class for launched tools that fly using "physics" and make the vehicle larger because...video game logic.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(choice(glob(join('assets', 'tools', '*.png'))))
        shrink_scale = 0.25  # images are too big!
        smaller_w, smaller_h = int(self.image.get_width() * shrink_scale), int(self.image.get_height() * shrink_scale)
        # ^ need to use int() function since scale() function needs integer dimensions
        self.image = pygame.transform.scale(self.image, (smaller_w, smaller_h))
        self.rect = self.image.get_rect()
        self.rect.x = 0  # starts visible on screen left
        self.rect.y = randint(0, int((SCREEN_H * 0.75)) - self.rect.height)  # starts at random y position
        self.dx, self.dy = randint(2, 16), randint(3, 9)  # random vertical, horizontal speeds
        self.fly_frames = 0  # used for simulating physics

    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.dy  # upward velocity
        self.rect.y += 0.45 * self.fly_frames  # downward acceleration due to gravity
        self.fly_frames += 1  # more fly_frames ==> more time accelerating

        # checks if box is outside of screen, based on x and y (top-left corner coordinates of box)
        if self.rect.x >= SCREEN_W - self.rect.width or self.rect.y >= SCREEN_H - self.rect.height:
            self.kill()  # removes if off screen


class PowerUp(pygame.sprite.Sprite):
    """
    A class for random power-up blocks that make the vehicle go slightly faster.
    """
    ptype = 0 #integer that specifies what the power up does
    # 0 = speed, 1 = invincibility, 2 = size reset, 3 = lives
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ptype = randint(0, 3)
        #I love not having switch statements!!!! yipee!
        if (self.ptype >= 0):
            self.image = pygame.image.load(join('assets/diamonds', 'element_green_diamond_glossy.png'))
        if (self.ptype == 1):
            self.image = pygame.image.load(join('assets/diamonds', 'element_blue_diamond_glossy.png'))
        if (self.ptype == 2):
            self.image = pygame.image.load(join('assets/diamonds', 'element_red_diamond_glossy.png'))
        if (self.ptype == 3):
            self.image = pygame.image.load(join('assets/diamonds', 'element_yellow_diamond_glossy.png'))
        shrink_scale = 0.5
        smaller_w, smaller_h = int(self.image.get_width() * shrink_scale), int(self.image.get_height() * shrink_scale)
        self.image = pygame.transform.scale(self.image, (smaller_w, smaller_h))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, SCREEN_W - self.rect.width)
        self.rect.y = SCREEN_H - self.rect.height - 10
        self.going_up = True  # stores whether block is going up (True) or down (False)
        self.max_up_move = SCREEN_H - self.rect.height - 16  # furthest upward y location, helps with "animation"
        self.max_down_move = SCREEN_H - self.rect.height - 4  # furthest downward y location, helps with "animation"

    def update(self):
        # moves up if it hasn't reached its max upward location, otherwise it moves down (and vice versa)
        if (self.rect.y < self.max_up_move) or (self.rect.y > self.max_down_move):
            self.going_up = not self.going_up
        self.rect.y += (-1) ** int(self.going_up)  # clever maths, using (-1)^0 = 1 trick and fact that False=0, True=1


def game():
    pygame.init()
    bg = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SRCALPHA, 32)
    # sets the image background:
    bg_img = pygame.transform.scale(pygame.image.load(join('assets', 'sunset_bg.png')), (SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    pc = Vehicle()
    # dictionary of all sprite groups:
    sprite_groups = {gp: pygame.sprite.Group() for gp in ['all', 'blocks', 'tools', 'powerups', 'fallingpowerups']}
    # dictionary of helpul info on spawned objects (not player character)
    # info is current spawn timer, spawn timer max, constructor call, and pc function resulting from colliding w/object
    spawned_objects = {'blocks': [0, 1000, FallingBlock, "kill"], 'tools': [0, 750, LaunchedTool, "grow"],
                       'powerups': [0, 2500, PowerUp, "increase_speed"],
                       'fallingpowerups': [0, 3200, FallingPower, "increase_lives"]}
    #
    sprite_groups['all'].add(pc)  # initially only player character sprite exists
    font = pygame.font.Font(None, 38)
    time_score = 0

    while True:
        bg.blit(bg_img, (0, 0))
        time_inc = clock.tick(FPS)  # guarantees up to 30 FPS

        for st in spawned_objects.keys():
            spawned_objects[st][0] += time_inc
        time_score += time_inc

        for gp in spawned_objects.keys():  # loops over 'blocks', 'tools', and 'powerups'
            num_powerups = len(sprite_groups['powerups'].sprites())  # only want up to 3 powerups on screen!
            if spawned_objects[gp][0] > spawned_objects[gp][1]:
                # if more than max spawn time has passed since last spawn, spawn new instance of object
                new_obj = spawned_objects[gp][2]()  # create new object instance
                sprite_groups['all'].add(new_obj)  # add it to 'all' sprite group
                sprite_groups[gp].add(new_obj)  # add it to its own specific sprite group
                spawned_objects[gp][0] = 0  # reset spawn timer



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # cheat button for player to respawn with 'space' key
                    pc.kill()  # need to kill current sprite
                    pc = Vehicle()  # makes new sprite
                    sprite_groups['all'].add(pc)  # re-adds to all list
                    time_score = 0  # resets time score (can't cheat too much!)

        pc.update(pygame.key.get_pressed())  # updates pc based on currently pressed keys
        for gp in spawned_objects.keys():
            sprite_groups[gp].update()  # function updates all object in spawned object groups (blocks, tools, powerups)
            # TODO: need to check for object collisions!
            # collision detection:

            for go in sprite_groups[gp].sprites():
                #collisions with blocks
                if (not isinstance(go, FallingBlock)):
                    for bl in sprite_groups['blocks'].sprites():
                        if (pygame.sprite.collide_rect(go, bl)):
                            go.kill()
                #collisions with pc
                if (pygame.sprite.collide_rect(pc, go)):
                    if (isinstance(go,LaunchedTool)):
                        pc.grow()
                    if (isinstance(go,FallingBlock)):
                        if(pc.invintime<=0):
                            pc.lives -=1
                            if(pc.lives <=0):
                                pc.kill()
                    if (isinstance(go,PowerUp)):
                        if (go.ptype == 0):
                            pc.increase_speed()
                        if (go.ptype == 1):
                            #invincibility
                            pc.invintime+=150
                        if (go.ptype == 2):
                            # size reset
                            pc.size_reset()
                        if (go.ptype == 3):
                            #add lives
                            pc.lives+=1
                    if (isinstance(go, FallingPower)):
                        pc.lives += 1
                    go.kill()

        if len(sprite_groups['powerups'].sprites()) > 3:  # removes oldest powerup if there are more than 3 on screen
            sprite_groups['powerups'].sprites()[0].kill()

        score_printout = font.render(f'Score: {time_score // 1000}', True, (230, 230, 230))
        lives_printout = font.render(f'Lives: {pc.lives }', True, (230, 230, 230))

        bg.blit(lives_printout, (5, 5))
        bg.blit(score_printout, (SCREEN_W - score_printout.get_width() - 5, 5))
        sprite_groups['all'].draw(bg)

        # GAME OVER screen
        if not pc.alive():  # only true if pc object is not in any groups, happens if pc.kill() is called
            #high score functionality:
            file = open("hs.txt")
            hs = int(file.read())
            if((time_score // 1000)>hs):
                hs = time_score // 1000
                file = open("hs.txt", "w")
                file.write(str(hs))
                file.close()

            bg.fill((0, 0, 0))  # make black screen
            game_over = font.render(f'GAME OVER', True, (230, 230, 230))
            highscore= font.render(f'High Score: {hs}', True, (230, 230, 230))

            bg.blit(game_over, ((SCREEN_W / 2) - (game_over.get_width() / 2),
                                (SCREEN_H / 2) - (game_over.get_height() / 2)))  # draws text in top center of screen
            bg.blit(score_printout, ((SCREEN_W / 2) - (score_printout.get_width() / 2),
                                     (SCREEN_H / 2) - (score_printout.get_height() / 2) + 100))
            bg.blit(highscore, ((SCREEN_W / 2) - (highscore.get_width() / 2),
                                     (SCREEN_H / 2) - (highscore.get_height() / 2) + 150))
            pygame.display.update()
            pygame.time.delay(3500)
            exit()

        pygame.display.update()


def main():
    game()


if __name__ == '__main__':
    main()
