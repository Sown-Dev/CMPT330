# NAME: Misha Smirnov
# FILENAME: Homework3.py
# SUMMARY:
# I kind of redid a lot of the game. I started by adding physics based movement by having velocity and drag,
# and by having boxes move every frame based on velocity. Then I decided to add shooting, and with that I added a gun
# Afterwards I knew I needed enemies, so I implemented that along with damage, health, and hit detection, and to finish the project, I added reloading and burst fire
# to satisfy the requirements


import math
import random
import pygame

SCREEN_W, SCREEN_H = 750, 450
FPS = 30 #Sets game fps


class Enemy:
    health=100
    mx = 0
    my = 0
    drag = 3
    damagecooldown=8 #used to delay attacks.
    # Doesn't start at zero so that enemies spawned on player don't immediately do damage

    def __init__(self, dim=24, color=(176, 82, 94)):
        self.dim = dim
        self.x, self.y = random.random()* SCREEN_W-50,random.random()* SCREEN_H -50
        self.color = color

    def get_x(self):
        return self.x

    def increment_x(self, dx):
        self.mx += dx

    def get_y(self):
        return self.y

    def increment_y(self, dy):
        self.my += dy

    def get_center(self):
        return self.x + (0.5 * self.dim), self.y + (0.5 * self.dim)

    def doPhysics(self):
        self.x += self.mx/FPS
        self.y += self.my/FPS
        self.my -= (self.my * self.drag)/FPS
        self.mx -= (self.mx * self.drag)/FPS

    def resetMomentum(self):
        self.mx =0
        self.my = 0
    def get_rect_params(self):
        # returns tuple in format pygame often uses for rectangle parameters
        return self.x, self.y, self.dim, self.dim

class Box:
    #Add physics to box (momentumx, momentumy)
    mx=0;
    my=0;
    drag=2; #How much the object decelerates per second as a multiple of velocity
    rotation = 0 #rotation of gun

    # Class holding info of box "character"
    def __init__(self, dim=36, color=(16, 132, 194)):
        self.dim = dim
        self.x, self.y = (SCREEN_W / 2) - (self.dim / 2), (SCREEN_H / 2) - (self.dim / 2)
        self.color = color

    def update_loc(self, x, y):
        self.x, self.y = x, y

    def surrounds(self, mouse_loc):
        # returns True if x and y are within box region, otherwise False
        mouse_x, mouse_y = mouse_loc
        return self.x - self.dim < mouse_x < self.x + self.dim and self.y - self.dim < mouse_y < self.y + self.dim

    def respawn(self):
        # resets box to center of screen
        self.x, self.y = (SCREEN_W / 2) - (self.dim / 2), (SCREEN_H / 2) - (self.dim / 2)

    def get_x(self):
        return self.x

    def increment_x(self, dx):
        self.mx += dx

    def get_y(self):
        return self.y

    def increment_y(self, dy):
        self.my += dy

    def get_center(self):
        return self.x + (0.5 * self.dim), self.y + (0.5 * self.dim)

    def set_center(self, x=None, y=None):
        if x is not None:
            self.x = x - (0.5 * self.dim)
        if y is not None:
            self.y = y - (0.5 * self.dim)

    def get_dim(self):
        return self.dim

    def check_out_of_bounds(self):
        # checks if box is outside of screen, based on x and y (top-left corner coordinates of box)
        if self.x <= 0:
            self.x = 0
        elif (self.x + self.dim) >= SCREEN_W:
            self.x = SCREEN_W - self.dim
        if self.y <= 0:
            self.y = 0
        elif (self.y + self.dim) >= SCREEN_H:
            self.y = SCREEN_H - self.dim

    def get_rect_params(self):
        # returns tuple in format pygame often uses for rectangle parameters
        return self.x, self.y, self.dim, self.dim

    def get_color(self):
        return self.color

    def set_color(self, c):
        self.color = c

    def intersects_with(self, other_box):
        this_box = pygame.Rect(self.x, self.y, self.dim, self.dim)
        other_box = pygame.Rect(other_box.get_x(), other_box.get_y(), other_box.get_dim(), other_box.get_dim())
        return this_box.colliderect(other_box)

    def doPhysics(self):
        self.x += self.mx/FPS
        self.y += self.my/FPS
        self.my -= (self.my * self.drag)/FPS
        self.mx -= (self.mx * self.drag)/FPS

    def resetMomentum(self):
        self.mx =0
        self.my = 0

def game():
    respawnTime = 60 # How often enemies spawn


    dx, dy = 8, 8  # setting speed for box movement
    big_box = Box(color=(16, 132, 194))  # creating main box object
    pygame.init()
    bg = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SRCALPHA, 32)
    pygame.display.set_caption('Box Invasion')
    clock = pygame.time.Clock()
    flags = {'up': False, 'down': False,'left': False,'right': False, 'mouse_loc': (),'right_click': False, 'left_click': False,
             'line_start': (), 'line_end': (), 'on_line': False}  # creating dictionary of flags for ease of access
    #NOTE: renamed left_click to box drag, now left click is generally used if left mouse is pressed
    mouse_loc, line_start, line_end = (), (), ()  # initalizing location variables
    font = pygame.font.Font(None, 38)


    #Images
    gun = pygame.image.load("gunhr.png").convert_alpha()
    char= pygame.image.load("char.png").convert_alpha()
    char =  pygame.transform.scale(char, (36,36)) #scale beforehand
    #New Stuff
    maxammo=30  #used for reloading with right click
    ammo=maxammo
    health=100
    score =0
    shotalpha=0
    shootpos = [0,0]
    enemyList = [Enemy()]
    spawnTimer=0
    spawnTimer2 = respawnTime/2
    while True:
        clock.tick(FPS)  # guarantees up to 30 FPS
        spawnTimer+=1
        big_box.doPhysics() #do box physics before drawing box


        bg.fill((0, 0, 0))  # reset bg to black
        # checking for events

        flags['left_click'] = False #reset flag
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    flags['up'] = True
                elif event.key == pygame.K_s:
                    flags['down'] = True
                elif event.key == pygame.K_a:
                    flags['left'] = True
                elif event.key == pygame.K_d:
                    flags['right'] = True
                elif event.key == pygame.K_SPACE:
                    big_box.respawn()  # SPACE lets the box go back to center, feel free to remove
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    flags['up'] = False
                elif event.key == pygame.K_s:
                    flags['down'] = False
                elif event.key == pygame.K_a:
                    flags['left'] = False
                elif event.key == pygame.K_d:
                    flags['right'] = False
                elif event.key == pygame.K_r:
                    ammo= maxammo #reload
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    flags['right_click'] = True
                elif event.button == 1:
                    flags['left_click'] = True


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    flags['right_click'] = False
            elif event.type == pygame.MOUSEMOTION:
                shootpos = event.pos

        # makes the big (blue) box white while it's intersecting with the smaller (orange) box


        # If box is "on the line" (user clicked endpt and released), then calculate movement
        if flags['on_line']:
            # rate of change of x, y for movement
            rise, run = line_end[1] - line_start[1], line_end[0] - line_start[0]
            # the try/except stuff below just makes sure that we can work with 100% vertical/horizontal lines
            try:
                rise_sign = rise / abs(rise)
            except ZeroDivisionError:
                rise_sign = 0
            try:
                run_sign = run / abs(run)
            except ZeroDivisionError:
                run_sign = 0
            try:
                slope = (rise / run)
            except ZeroDivisionError:
                slope = 1
            big_box.increment_x(dx * run_sign)
            if run_sign == 0:
                big_box.increment_y(dy * slope * rise_sign)
            else:
                big_box.increment_y(dy * slope * run_sign)
            # once we reach our goal x value, stop there
            if run_sign * big_box.get_center()[0] > run_sign * (line_end[0]):
                big_box.set_center(x=line_end[0])
                flags['on_line'] = False
            # once we reach our goal y value, stop there
            if rise_sign * big_box.get_center()[1] > rise_sign * (line_end[1]):
                big_box.set_center(y=line_end[1])
                flags['on_line'] = False
        big_box.increment_y(flags['up'] * -dy + flags['down'] * dy)
        big_box.increment_x(flags['left'] * -dx + flags['right'] * dx)
        # move box back to 100% in the screen movement caused it to leave bounds
        big_box.check_out_of_bounds()


        #Shooting Logic:

        # I know this is a stupid way of doing this, but it works and I don't want to convert from rads
        v1 = pygame.math.Vector2(0,0)
        v2 = pygame.math.Vector2(pygame.mouse.get_pos()[0]-big_box.x, pygame.mouse.get_pos()[1] - big_box.y)
        big_box.rotation = v1.angle_to(v2)
        tempgun = pygame.transform.scale(gun, (120,60))
        tempgun = pygame.transform.rotate(tempgun, -big_box.rotation);

        if (flags['left_click']  and ammo > 0):
            shotalpha = 6
            ammo -= 1

        if ( flags['right_click'] and ammo > 0 and shotalpha==0):
            shotalpha = 6
            ammo -= 1

        bg.blit(tempgun, (big_box.x-40, big_box.y-35))
        if(shotalpha>5): #Initialize line position in the first frame of shooting
            lStart = big_box.get_center()
            lEnd = (shootpos[0] + random.randint(-5, 5), shootpos[1] + random.randint(-10, 10))  # add random spread

        if(shotalpha>0):
            shotalpha-=1
            colora = shotalpha/6
            #create line and raycast
            pygame.draw.line(bg, width=3,color = (240*colora,240*colora,0),start_pos=lStart, end_pos=lEnd)

            #check for collisions:
            for e in enemyList:
                if pygame.Rect(e.get_rect_params()).clipline( lStart, lEnd) != ():
                    enemyList.remove(e)
                    score+=1



        # ENEMY LOGIC:

        gothit=False #reset hit indicator

        #Iterate through enemies
        for e in enemyList:

            #Movement:

            #get direction to player
            dir = pygame.math.Vector2(e.x-big_box.x, e.y-big_box.y).normalize()
            #add momentum
            e.increment_x(dir.x*-6)
            e.increment_y(dir.y*-6)

            #Collision Detection & Damage

            if(e.damagecooldown>0): #decrement cooldown if greater than 0
                e.damagecooldown-=1

            if(pygame.Rect(e.get_rect_params()).colliderect(big_box.get_rect_params()) and e.damagecooldown<1):
                gothit=True
                health-=10

                e.damagecooldown=30


            #Physics Step:
            e.doPhysics()


        # Enemy Spawn Logic
        if spawnTimer > respawnTime:
            enemyList.append(Enemy())
            spawnTimer = 0
            respawnTime -= 1  # keeps increasing difficulty over time
        #Instead of redoing timing system, I added a second spawn timer so that multiple enemies could be spawned every frame
        if spawnTimer2 > respawnTime:
            enemyList.append(Enemy())
            spawnTimer2=0




        # Drawing:

        score_surf = font.render(f'Score: {score}', True, (230, 230, 230))
        health_surf = font.render(f'Health: {health}', True, (230, 230, 230))
        ammo_surf = font.render(f'Ammo: {ammo}/{maxammo}', True, (230, 230, 230))

        if(gothit):
            pygame.draw.ellipse(bg, rect=big_box.get_rect_params(), color=(200,0,0))
        bg.blit(char, big_box.get_rect_params())
        bg.blit(score_surf, (((SCREEN_W / 2) - (score_surf.get_width() / 2)), 10))  # draws text in top center of screen
        bg.blit(health_surf, (((SCREEN_W / 2) - (health_surf.get_width() / 2) + health_surf.get_width()+20), 10))  # draws text in top center of screen
        bg.blit(ammo_surf, (((SCREEN_W / 2) - (ammo_surf.get_width() / 2) - health_surf.get_width()-40), 10))  # draws text in top center of screen

        for e in enemyList:
            pygame.draw.rect(bg, (100,200,80), e.get_rect_params())

        pygame.display.update()


        #check game over:
        if (health <= 0):
            pygame.quit()







def main():
    game()


if __name__ == '__main__':
    main()
