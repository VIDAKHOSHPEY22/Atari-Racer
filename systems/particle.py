import pygame as pg
import random
from core.settings import WIDTH, HEIGHT

class ParticlePool:
    def __init__(self, size=150):
        self.pool = []
        self.active = []
        self._cache = {}
        self._max_cache = 128
        
        for _ in range(size):
            self.pool.append({
                'alive': False,
                'x': 0, 'y': 0,
                'vx': 0, 'vy': 0,
                'color': (255, 255, 255),
                'life': 0,
                'max_life': 0
            })
    
    def spawn(self, x, y, vx, vy, color, lifetime):
        for p in self.pool:
            if not p['alive']:
                p.update({
                    'alive': True,
                    'x': x, 'y': y,
                    'vx': vx, 'vy': vy,
                    'color': color,
                    'life': lifetime,
                    'max_life': lifetime
                })
                self.active.append(p)
                return
        
        p = {
            'alive': True,
            'x': x, 'y': y,
            'vx': vx, 'vy': vy,
            'color': color,
            'life': lifetime,
            'max_life': lifetime
        }
        self.pool.append(p)
        self.active.append(p)
    
    def update_and_draw(self, surface, dt):
        keep = []
        for p in self.active:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['life'] -= dt
            
            if p['life'] > 0:
                self._draw_particle(surface, p)
                keep.append(p)
            else:
                p['alive'] = False
        
        self.active = keep
    
    def _draw_particle(self, surface, p):
        ratio = p['life'] / p['max_life']
        alpha = int(255 * ratio)
        size = max(2, int(6 * ratio))
        
        key = (size, p['color'], alpha)
        if key not in self._cache:
            if len(self._cache) >= self._max_cache:
                self._cache.pop(next(iter(self._cache)))
            
            s = pg.Surface((size * 2, size * 2), pg.SRCALPHA)
            pg.draw.circle(s, (*p['color'], alpha), (size, size), size)
            self._cache[key] = s
        
        surface.blit(self._cache[key], (int(p['x'] - size), int(p['y'] - size)))
