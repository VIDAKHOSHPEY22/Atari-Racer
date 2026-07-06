import pygame as pg
import math
from core.settings import *

class PowerUp:
    RADIUS = 14
    _labels = {}
    
    def __init__(self, x, speed, kind):
        self.x = x
        self.y = float(-self.RADIUS * 2)
        self.speed = speed
        self.kind = kind
        self.angle = 0.0
        
        if not PowerUp._labels:
            f = pg.font.Font(None, 16)
            PowerUp._labels = {
                k: f.render(meta[1][0], True, WHITE)
                for k, meta in POWERUP_META.items()
            }
        self._label_surf = PowerUp._labels[kind]
    
    def update(self, dt):
        self.y += self.speed * dt
        self.angle += 3.0 * dt
        return self.y > HEIGHT
    
    def draw(self, surface):
        col, label, _ = POWERUP_META[self.kind]
        pulse = abs(math.sin(self.angle))
        r = int(self.RADIUS + 4 * pulse)
        
        glow = pg.Surface((r * 2 + 8, r * 2 + 8), pg.SRCALPHA)
        pg.draw.circle(glow, (*col, 80), (r + 4, r + 4), r + 4)
        surface.blit(glow, (int(self.x) - r - 4, int(self.y) - r - 4))
        
        pg.draw.circle(surface, col, (int(self.x), int(self.y)), r)
        pg.draw.circle(surface, WHITE, (int(self.x), int(self.y)), r, 2)
        
        surface.blit(self._label_surf, 
                    self._label_surf.get_rect(center=(int(self.x), int(self.y))))
    
    def get_rect(self):
        return pg.Rect(self.x - self.RADIUS, self.y - self.RADIUS, 
                      self.RADIUS * 2, self.RADIUS * 2)
