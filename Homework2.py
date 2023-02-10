import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((500,500))

    draw1(screen)



    keepGameRunning=True
    while keepGameRunning:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGameRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.fill((0,0,0))
                    draw2(screen)

def draw1(surf):
    pygame.draw.rect(surf, color=(255,0,0), rect=(10,10, 20,80) )
def draw2(surf):
    pygame.draw.circle(surf, width=10, radius =10, color=(25,100,0), center=(80,30))



if __name__ == '__main__':
    main()