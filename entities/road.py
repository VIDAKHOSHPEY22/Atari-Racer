import pygame as pg
import random
import math
from core.settings import *
from utils.helpers import clamp

class Road:
    STRIPE_W = 10
    STRIPE_H = 60
    STRIPE_GAP = 100
    LANE_DIVIDERS = [
        LANE_CENTERS[0] - 8,
        LANE_CENTERS[1] - 8,
        LANE_CENTERS[2] - 8,
        LANE_CENTERS[3] - 8,
    ]
    RUMBLE_W = 18
    RUMBLE_PERIOD = 50
    
    _base_surf = None
    
    def __init__(self, scroll_speed):
        self.scroll = 0.0
        self.scroll_speed = scroll_speed
        
        if Road._base_surf is None:
            Road._base_surf = self._build_base()
        self._base = Road._base_surf
        self._stripe_surf = self._build_stripe_surf()
    
    @classmethod
    def _build_base(cls):
        if cls._base_surf is not None:
            return cls._base_surf
        
        grass = pg.Surface((ROAD_LEFT, HEIGHT))
        grass.fill(GRASS_COLOR)
        rng = random.Random(42)
        for _ in range(300):
            gx = rng.randint(0, ROAD_LEFT - 4)
            gy = rng.randint(0, HEIGHT - 6)
            shade = rng.randint(-20, 20)
            col = tuple(clamp(GRASS_COLOR[i] + shade, 0, 255) for i in range(3))
            pg.draw.rect(grass, col, (gx, gy, rng.randint(2, 6), rng.randint(3, 8)))
        
        s = pg.Surface((WIDTH, HEIGHT))
        s.blit(grass, (0, 0))
        s.blit(pg.transform.flip(grass, True, False), (ROAD_RIGHT, 0))
        
        pg.draw.rect(s, SHOULDER_COLOR, (ROAD_LEFT - 22, 0, 22, HEIGHT))
        pg.draw.rect(s, SHOULDER_COLOR, (ROAD_RIGHT, 0, 22, HEIGHT))
        
        road_w = ROAD_RIGHT - ROAD_LEFT
        road_surface = pg.Surface((road_w, HEIGHT))
        base_intensity = 35
        stripe_count = 10
        stripe_h = HEIGHT // stripe_count
        for i in range(stripe_count + 1):
            intensity = base_intensity + int(10 * math.sin(i / stripe_count * math.pi * 2))
            y0 = i * stripe_h
            y1 = min(y0 + stripe_h, HEIGHT)
            pg.draw.rect(road_surface, (intensity, intensity, intensity + 5), 
                        (0, y0, road_w, y1 - y0))
        
        s.blit(road_surface, (ROAD_LEFT, 0))
        
        pg.draw.line(s, (255, 255, 100), (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
        pg.draw.line(s, (255, 255, 100), (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)
        
        cls._base_surf = s
        return s
    
    def _build_stripe_surf(self):
        period = self.STRIPE_H + self.STRIPE_GAP
        s = pg.Surface((WIDTH, period), pg.SRCALPHA)
        
        for lx in self.LANE_DIVIDERS:
            glow = pg.Surface((self.STRIPE_W + 4, self.STRIPE_H), pg.SRCALPHA)
            pg.draw.rect(glow, (100, 100, 150, 80), (0, 0, self.STRIPE_W + 4, self.STRIPE_H), border_radius=3)
            s.blit(glow, (lx - 2, 0))
            
            pg.draw.rect(s, (180, 180, 200), (lx, 0, self.STRIPE_W, self.STRIPE_H), border_radius=2)
        
        return s
    
    def update(self, dt):
        period = self.STRIPE_H + self.STRIPE_GAP
        self.scroll = (self.scroll + self.scroll_speed * dt) % period
    
    def draw(self, surface):
        surface.blit(self._base, (0, 0))
        
        period = self.RUMBLE_PERIOD
        offset = self.scroll % period
        elapsed = pg.time.get_ticks() / 1000
        pulse = abs(math.sin(elapsed * 10))
        
        for i in range(HEIGHT // period + 2):
            ry = int(i * period - offset)
            col = RED if i % 2 == 0 else (255, 200, 100)
            bright_col = tuple(clamp(c + int(50 * pulse), 0, 255) for c in col)
            
            pg.draw.rect(surface, bright_col, 
                        (ROAD_LEFT - self.RUMBLE_W - 22, ry, self.RUMBLE_W, period // 2))
            pg.draw.rect(surface, bright_col, 
                        (ROAD_RIGHT + 22, ry, self.RUMBLE_W, period // 2))
        
        sp = self.STRIPE_H + self.STRIPE_GAP
        so = int(self.scroll % sp)
        y = -sp + so
        while y < HEIGHT:
            surface.blit(self._stripe_surf, (0, y))
            y += sp
