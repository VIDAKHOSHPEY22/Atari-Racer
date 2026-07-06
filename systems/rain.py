import pygame as pg
import random
from core.settings import WIDTH, HEIGHT
from utils.helpers import clamp

class RainPool:
    def __init__(self, size=120):
        self.drops = []
        self.active_count = 0
        
        for _ in range(size):
            self.drops.append({
                'x': random.uniform(0, WIDTH),
                'y': random.uniform(-HEIGHT, 0),
                'speed': random.uniform(600, 900)
            })
    
    def set_active(self, count):
        self.active_count = clamp(count, 0, len(self.drops))
    
    def reset_drop(self, idx):
        drop = self.drops[idx]
        drop['x'] = random.uniform(0, WIDTH)
        drop['y'] = random.uniform(-HEIGHT, 0)
        drop['speed'] = random.uniform(600, 900)
    
    def update_and_draw(self, surface, dt, intensity=1.0):
        if self.active_count <= 0:
            return
        
        color = (180, 200, 220, int(140 * intensity))
        
        for i in range(self.active_count):
            drop = self.drops[i]
            
            drop['y'] += drop['speed'] * dt
            
            if drop['y'] > HEIGHT:
                self.reset_drop(i)
                drop = self.drops[i]
            
            pg.draw.line(surface, color, 
                        (drop['x'], drop['y']), 
                        (drop['x'] - 4, drop['y'] + 14), 2)
