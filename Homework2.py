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
    img2 = pygame.image.load("logo.png").convert_alpha()
    img3 = pygame.image.load("burger.png").convert()

    img3 = pygame.transform.smoothscale(img3, (200,200))

    surf.blit(img3,(10,250))
    surf.blit(img1, (110, 110))
    surf.blit(img2, (150, 210))

    #blur
    for i in range(1,img2.get_size()[0]-1):
        for j in range(1,img2.get_size()[1]-1):
            sumR=0
            sumG=0
            sumB=0
            for k in range(-1,2):
                for l in range(-1, 2):
                    sumR += img2.get_at((i+k, j+l))[0]
                    sumG += img2.get_at((i + k, j + l))[1]
                    sumB += img2.get_at((i + k, j + l))[2]
            avgcol = (sumR/9, sumG/9, sumB/9)
            img2.set_at((i,j),avgcol)

    surf.blit(img2, (150, 360))

    myfont = pygame.font.Font('freesansbold.ttf', 20)
    text = myfont.render('Press Space to Switch Screens', True, (255, 255, 255))
    text2 = myfont.render('I love pygame!!!!', True, (255, 20, 20))



    trect = text.get_rect()
    trect.center = (trect.w + 20, 500)
    surf.blit(text, trect)

    trect2 = text2.get_rect()
    trect2. center = (trect.w +70, 340)
    surf.blit(text2,trect2 )

    text3 = myfont.render('This image is blurred!!1!', True, (255, 120, 00))
    surf.blit(text3,( 150,420))




if __name__ == '__main__':
    main()