import pygame

from FinalProject.Ball import *
from FinalProject.Paddle import *


FPS=60

def game():
    pygame.init()

    bg = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

    pc = Paddle(True, False)
    enemy = Paddle(False, True, (WIDTH-60, HEIGHT))

    ball = Ball(400,400, 4)

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
        time_inc = clock.tick(FPS)  # guarantees up to 30 FPS

        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                exit()

        pc.update(pygame.key.get_pressed(),ball)  # update mouse based on keys, walls, and time
        enemy.update(pygame.key.get_pressed(),ball)
        #check colliders
        for collider in sprite_groups['col']:
            if pygame.mask.Mask.overlap(ball.mask, collider.mask, offset(ball,collider)):
                ball.hit()
                if type(collider) is Paddle:
                    print("test")
                    ball.speed+=1

        point = ball.update()

        if point:
            Score[1 if point == 1 else 0]+=1
            ball.reset()

        sprite_groups['all'].draw(bg)  # drawing updated sprites on screen
        #draw score and time:

        score_text = font.render(f'{Score[0]} - {Score[1]}', True, (230, 230, 230))
        bg.blit(score_text, ((WIDTH / 2) - (score_text.get_width() / 2),
                                 100))

        # updating screen
        pygame.display.update()









def offset(mask1, mask2):
    return int(mask2.rect.x - mask1.rect.x), int(mask2.rect.y - mask1.rect.y)
def main():
    game()


if __name__ == '__main__':
    main()