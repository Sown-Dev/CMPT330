from typing import List

import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

from FinalProject.Ball import *
from FinalProject.Entity import Entity
from FinalProject.Paddle import *


FPS=60
TIMELIMIT = 60*2*FPS
def game():
    pygame.init()

    bg = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

    # Pymunk stuff:
    space = pymunk.Space()
    space.gravity = 0, 0
    space.collision_slop = 0.5  # Adjust the collision slop
    space.substeps = 10

    # Create a collision handler instance
    handler = space.add_collision_handler(3, 4)



    draw_options = pymunk.pygame_util.DrawOptions(bg)

    static: List[pymunk.Shape] = [
        pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 1),
        pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 1)
    ]



    for s in static:
        s.friction = 0
        s.group = 0
        s.elasticity= 1
    space.add( *static)
    #IDEA: Increase difficulty as time goes down

    pc = Paddle(True, False, (40,40))
    space.add(pc.body, pc.shape)

    enemy = Paddle(False, True, (WIDTH-40, HEIGHT-100))
    space.add(enemy.body, enemy.shape)


    ball = Ball(400,400, 4,space)
    space.add(ball.body, ball.shape)


    TimeRemaining=TIMELIMIT
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

    font = pygame.font.Font(None, 40)


    gameState = 1 # 1 = playing, 2 = endscreen

    #music
    pygame.mixer.music.play()


    #Game Loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


        bg.fill((0, 0, 0))

        clock.tick(FPS)

        if(gameState==1 and TimeRemaining<0):
            gameState=2

        if(gameState==1):
            bg.blit(BGIMG, (0, 0))



            TimeRemaining-=1







            pc.update(pygame.key.get_pressed(),ball, bg,space)  # update mouse based on keys, walls, and time
            enemy.update(pygame.key.get_pressed(),ball, bg,space)


            point = ball.update()

            if point:
                Score[1 if point == 1 else 0]+=1
                ball.reset(point)
            sprite_groups['all'].draw(bg)  # drawing updated sprites on screen
            #draw score and time:


            score_text = font.render(f'{Score[0]} - {Score[1]}', True, (230, 230, 230))
            time_text = font.render(f'{(int) ((TimeRemaining/60) / 60)}:{(int) ((TimeRemaining/60) % 60)}', True, (230, 230, 230))

            bg.blit(score_text, ((WIDTH / 2) - (score_text.get_width() / 2),
                                 2))
            bg.blit(time_text, ((WIDTH / 2) - (time_text.get_width() / 2),
                                 25))

            dt = 1.0 / FPS
            space.step(dt)

            # updating screen
            pygame.display.update()
            space.debug_draw(draw_options)

        if(gameState==2):
            pygame.mixer.music.load(join("Assets/Sounds", "Game Over.mp3"))
            pygame.mixer.music.play()
            #game end screen
            if(Score[0]>Score[1]):
                game_over = font.render(f'YOU WIN', True, (230, 230, 230))
            elif(Score[0]<Score[1]):
                game_over = font.render(f'YOU LOSE', True, (230, 230, 230))
            elif(Score[0 == Score[1]]):
                game_over = font.render(f'TIE GAME', True, (230, 230, 230))

            finalScore = font.render(f'Final Score:\n{Score[0]} - {Score[1]}', True, (230, 230, 230))

            bg.blit(game_over, ((WIDTH / 2) - (score_text.get_width() / 2),
                                 200))
            bg.blit(finalScore, ((WIDTH / 2) - (time_text.get_width() / 2),
                                325))

            pygame.display.update()
            pygame.time.delay(4000)
            exit()

def offset(mask1, mask2):
    return int(mask2.rect.x - mask1.rect.x), int(mask2.rect.y - mask1.rect.y)
def main():
    game()



if __name__ == '__main__':
    main()