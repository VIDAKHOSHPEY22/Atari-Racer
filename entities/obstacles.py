import pygame as pg
import random
import math
from core.settings import *
from utils.drawing import draw_car
from utils.helpers import clamp

class ObstacleCar:
    _cache = {}
    _MAX_CACHE = 64
    
    def __init__(self, lane, speed):
        self.width = 48
        self.height = random.choice([82, 88, 94])
        self.x = float(LANE_CENTERS[lane] - self.width // 2)
        self.y = float(-self.height - 10)
        self.speed = speed
        self.color = random.choice([
            (255, 80, 80), (80, 255, 80), (255, 180, 60),
            (200, 80, 255), (80, 150, 255), (255, 220, 60)
        ])
        self.car_type = random.choice(["sedan", "suv", "truck"])
        self.lane = lane
        
        key = (self.color, self.car_type, self.width, self.height)
        if key not in ObstacleCar._cache:
            if len(ObstacleCar._cache) >= ObstacleCar._MAX_CACHE:
                ObstacleCar._cache.pop(next(iter(ObstacleCar._cache)))
            s = pg.Surface((self.width + 8, self.height + 8), pg.SRCALPHA)
            draw_car(s, 4, 4, self.width, self.height, self.color, (100, 100, 120), self.car_type)
            ObstacleCar._cache[key] = s
        self._surf = ObstacleCar._cache[key]
    
    def update(self, dt):
        self.y += self.speed * dt
        return self.y > HEIGHT
    
    def draw(self, surface):
        surface.blit(self._surf, (int(self.x) - 4, int(self.y) - 4))
    
    def get_rect(self):
        return pg.Rect(int(self.x) + 4, int(self.y) + 4, self.width - 8, self.height - 8)


class Barrier:
    WIDTH, HEIGHT = 60, 20
    _surf = None
    
    def __init__(self, x, speed):
        self.x = x
        self.y = float(-self.HEIGHT)
        self.speed = speed
        if Barrier._surf is None:
            Barrier._surf = self._build_surf()
    
    @classmethod
    def _build_surf(cls):
        s = pg.Surface((cls.WIDTH, cls.HEIGHT), pg.SRCALPHA)
        pg.draw.rect(s, (200, 200, 210), (0, 0, cls.WIDTH, cls.HEIGHT), border_radius=3)
        for i in range(3):
            pg.draw.rect(s, ORANGE, (i * 20 + 2, 2, 14, cls.HEIGHT - 4), border_radius=2)
        return s
    
    def update(self, dt):
        self.y += self.speed * dt
        return self.y > HEIGHT
    
    def draw(self, surface):
        surface.blit(self.__class__._surf, (self.x, int(self.y)))
    
    def get_rect(self):
        return pg.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)


class OilSlick:
    WIDTH, HEIGHT = 54, 28
    _surf_outer = None
    _surf_inner = None
    
    def __init__(self, x, speed):
        self.x = x
        self.y = float(-self.HEIGHT)
        self.speed = speed
        self.angle = 0.0
        
        if OilSlick._surf_outer is None:
            OilSlick._surf_outer = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)
            OilSlick._surf_inner = pg.Surface((self.WIDTH - 10, self.HEIGHT - 6), pg.SRCALPHA)
    
    def update(self, dt):
        self.y += self.speed * dt
        self.angle += dt * 2.0
        return self.y > HEIGHT
    
    def draw(self, surface):
        t = self.angle
        
        c0 = (
            clamp(int(100 + 80 * math.sin(t)), 0, 255),
            clamp(int(50 + 80 * math.sin(t + 2.1)), 0, 255),
            clamp(int(150 + 80 * math.sin(t + 4.2)), 0, 255),
            200,
        )
        c1 = (
            clamp(int(200 + 80 * math.sin(t + 1.0)), 0, 255),
            clamp(int(100 + 80 * math.sin(t + 3.1)), 0, 255),
            clamp(int(50 + 80 * math.sin(t + 5.2)), 0, 255),
            180,
        )
        
        OilSlick._surf_outer.fill((0, 0, 0, 0))
        pg.draw.ellipse(OilSlick._surf_outer, c0, OilSlick._surf_outer.get_rect())
        surface.blit(OilSlick._surf_outer, (self.x, self.y))
        
        OilSlick._surf_inner.fill((0, 0, 0, 0))
        pg.draw.ellipse(OilSlick._surf_inner, c1, OilSlick._surf_inner.get_rect())
        surface.blit(OilSlick._surf_inner, (self.x + 5, self.y + 3))
    
    def get_rect(self):
        return pg.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
