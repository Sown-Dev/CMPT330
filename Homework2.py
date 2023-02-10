import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption('Homework 2')

    draw1(screen)


    screenT=1;
    x=5;
    y=5;

    keepGameRunning=True
    while keepGameRunning:
        pygame.draw.rect(screen,rect=((x*10,y*10),(20,20)), color=(250,250,100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGameRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x -= 1;
                if event.key == pygame.K_d:
                    x += 1;
                if event.key == pygame.K_w:
                    y -= 1;
                if event.key == pygame.K_s:
                    y += 1;

                if event.key == pygame.K_SPACE:
                    screen.fill((0,0,0))
                    if(screenT==1):
                        screenT=0
                        draw2(screen)
                    else:
                        screenT=1
                        draw1(screen)


def draw1(surf):
    pygame.draw.rect(surf, color=(255,0,0), rect=(10,10, 140,180) )
    pygame.draw.circle(surf, width=10, radius =100, color=(0,200,230), center=(110,130))
    pygame.draw.arc(surf, width=5,rect=(250,390, 200,100), color=(120,250,90), start_angle=0.8, stop_angle=6 )
    pygame.draw.line(surf, width=9, start_pos=(0,400), end_pos=(480,20), color=(8,250,0))
    pygame.draw.polygon(surf, color=(200,100,255), points=[(100,400),(200,440),(280,390),(200,320), (120, 420)])
    myfont = pygame.font.Font('freesansbold.ttf', 20)
    text = myfont.render('Press Space to Switch Screens', True, (255, 255, 255))
    trect = text.get_rect()
    trect.center = (trect.w + 20, 520)
    surf.blit(text, trect)
def draw2(surf):
    pygame.draw.circle(surf, width=10, radius =10, color=(25,100,0), center=(80,30))

    img1 = pygame.image.load("walk2.png").convert()
    surf.blit(img1, (110, 110))

    myfont = pygame.font.Font('freesansbold.ttf', 20)
    text = myfont.render('Press Space to Switch Screens', True, (255, 255, 255))
    trect = text.get_rect()
    trect.center = (trect.w + 20, 500)
    surf.blit(text, trect)




if __name__ == '__main__':
    main()