import pygame as pg
import math
from utils.helpers import clamp

_particles = []

def spawn(x, y, vx, vy, color, lifetime):
    _particles.append([x, y, vx, vy, color, lifetime, lifetime])

def spawn_burst(x, y, color, count, speed, lifetime):
    import random
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        spd = random.uniform(speed * 0.4, speed)
        spawn(x, y, math.cos(angle) * spd, math.sin(angle) * spd, color, lifetime)

def update_and_draw(surface, dt):
    keep = []
    for p in _particles:
        p[0] += p[2] * dt
        p[1] += p[3] * dt
        p[5] -= dt
        if p[5] > 0:
            ratio = p[5] / p[6]
            alpha = int(255 * ratio)
            size = max(2, int(5 * ratio))
            r, g, b = p[4]
            s = pg.Surface((size * 2, size * 2), pg.SRCALPHA)
            pg.draw.circle(s, (r, g, b, alpha), (size, size), size)
            surface.blit(s, (int(p[0]) - size, int(p[1]) - size))
            keep.append(p)
    _particles.clear()
    _particles.extend(keep)

def clear():
    _particles.clear()
