import math

import pygame as pg
import pymunk as pm
from pymunk import Vec2d


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)


class Entity(pg.sprite.Sprite):

    def __init__(self, pos, space):
        super().__init__()
        self.image = pg.Surface((46, 52), pg.SRCALPHA)
        pg.draw.polygon(self.image, (0, 50, 200),
                        [(0, 0), (48, 0), (48, 54), (24, 54)])
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft=pos)
        vs = [(-23, 26), (23, 26), (23, -26), (0, -26)]
        mass = 1
        moment = pm.moment_for_poly(mass, vs)
        self.body = pm.Body(mass, moment)
        self.shape = pm.Poly(self.body, vs)
        self.shape.friction = .9
        self.body.position = pos
        self.space = space
        self.space.add(self.body, self.shape)

    def update(self, dt):
        pos = flipy(self.body.position)
        self.rect.center = pos
        self.image = pg.transform.rotate(
            self.orig_image, math.degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        # Remove sprites that have left the screen.
        if pos.x < 20 or pos.y > 560:
            self.space.remove(self.body, self.shape)
            self.kill()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.body.angular_velocity = 5.5
            elif event.key == pg.K_w:
                self.body.apply_impulse_at_local_point(Vec2d(0, 900))

