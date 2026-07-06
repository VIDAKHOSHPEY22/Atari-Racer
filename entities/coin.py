import pygame as pg
import random
import math
from core.settings import WIDTH, HEIGHT

class Coin:
    RADIUS = 11
    _cache = {}
    _MAX_CACHE = 64
    
    def __init__(self, x, speed):
        self.x = x
        self.y = float(-self.RADIUS * 2)
        self.speed = speed
        self.angle = random.uniform(0, math.pi * 2)
    
    def update(self, dt):
        self.y += self.speed * dt
        self.angle += 8.0 * dt
        return self.y > HEIGHT
    
    def draw(self, surface):
        w = max(4, int(self.RADIUS * 2 * abs(math.cos(self.angle))))
        
        key = w
        if key not in Coin._cache:
            if len(Coin._cache) >= Coin._MAX_CACHE:
                Coin._cache.pop(next(iter(Coin._cache)))
            
            h = self.RADIUS * 2
            s = pg.Surface((w, h), pg.SRCALPHA)
            
            pg.draw.ellipse(s, (220, 180, 30), (0, 0, w, h))
            pg.draw.ellipse(s, (255, 220, 70), (1, 1, w - 2, h - 2))
            pg.draw.ellipse(s, (255, 250, 150), (w // 4, 2, w // 2, h // 4))
            
            Coin._cache[key] = s
        
        surface.blit(Coin._cache[key], (self.x - w // 2, self.y - self.RADIUS))
    
    def get_rect(self):
        return pg.Rect(self.x - self.RADIUS, self.y - self.RADIUS, 
                      self.RADIUS * 2, self.RADIUS * 2)
