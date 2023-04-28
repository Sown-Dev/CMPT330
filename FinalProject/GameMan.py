from typing import List

import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

from FinalProject.Ball import *
from FinalProject.Paddle import *


FPS=60

def game():
    pygame.init()

    bg = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

    # Pymunk stuff:
    space = pymunk.Space()
    space.gravity = 0, 10

    draw_options = pymunk.pygame_util.DrawOptions(bg)

    static: List[pymunk.Shape] = [
        pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5),
        pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 5),
        pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5),
        pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5),
    ]

    b2 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    static.append(pymunk.Circle(b2, 30))
    b2.position = 300, 200

    for s in static:
        s.friction = 1.0
        s.group = 1
    space.add(b2, *static)


    pc = Paddle(True, False, (40,40))
    enemy = Paddle(False, True, (WIDTH-40, HEIGHT-100))

    ball = Ball(400,400, 4,space)

    TimeRemaining=0
    Score= [0,0]

    #Sprite Groups
    sprite_groups = {gp: pygame.sprite.Group() for gp in ['all', 'ball', 'bullets', 'pc', 'enemy', 'col']}
    sprite_groups['all'].add(pc)
    sprite_groups['all'].add(enemy)
    sprite_groups['all'].add(ball)
    sprite_groups['col'].add(pc)
    sprite_groups['col'].add(enemy)
    sprite_groups['enemy'].add(enemy)

    sprite_groups['pc'].add(pc)

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 48)



    #Game Loop
    while True:
        bg.fill((0, 0, 0))
        bg.blit(BGIMG, (0, 0))

        dt = 1.0 / FPS
        space.step(dt)
        clock.tick(FPS)


        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                exit()





        pc.update(pygame.key.get_pressed(),ball, bg)  # update mouse based on keys, walls, and time
        enemy.update(pygame.key.get_pressed(),ball, bg)
        #check colliders
        for collider in sprite_groups['col']:
            if pygame.mask.Mask.overlap(ball.mask, collider.mask, offset(ball,collider)):
                ball.hit()
                if type(collider) is Paddle:
                    ball.speed+=0.05

        point = ball.update()

        if point:
            Score[1 if point == 1 else 0]+=1
            ball.reset()

        sprite_groups['all'].draw(bg)  # drawing updated sprites on screen
        #draw score and time:

        score_text = font.render(f'{Score[0]} - {Score[1]}', True, (230, 230, 230))
        bg.blit(score_text, ((WIDTH / 2) - (score_text.get_width() / 2),
                                 10))

        # updating screen
        pygame.display.update()
        space.debug_draw(draw_options)










def offset(mask1, mask2):
    return int(mask2.rect.x - mask1.rect.x), int(mask2.rect.y - mask1.rect.y)
def main():
    game()


if __name__ == '__main__':
    main()