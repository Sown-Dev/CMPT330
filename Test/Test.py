import sys

import pygame
import pymunk

pygame.init()
screen = pygame.display.set_mode((640, 480))

# Create a Space object and set the gravity
space = pymunk.Space()
space.gravity = (0, 100)

# Create a static body to represent the ground
ground = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground, (0, 400), (640, 400), 5)
space.add(ground, ground_shape)

# Create a dynamic body to represent a falling ball
ball_body = pymunk.Body(1, 100)
ball_body.position = (320, 0)
ball_shape = pymunk.Circle(ball_body, 20)
space.add(ball_body, ball_shape)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Step the simulation and update the positions of the objects
    dt = 1.0 / 60.0
    space.step(dt)

    # Clear the screen and draw the objects
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), (0, 400), (640, 400), 5)
    pygame.draw.circle(screen, (255, 0, 0), ball_body.position, 20)

    pygame.display.update()
    clock.tick(60)
