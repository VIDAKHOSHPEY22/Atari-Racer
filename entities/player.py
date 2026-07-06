import pygame as pg
import math
import random
from core.settings import *
from utils.drawing import draw_car
from utils.helpers import clamp
from data.skins import Skin

class Player:
    WIDTH = 48
    HEIGHT = 88
    SPEED = 400
    
    def __init__(self, skin: Skin, speed_level=0):
        self.x = float(WIDTH // 2 - self.WIDTH // 2)
        self.y = float(HEIGHT - self.HEIGHT - 30)
        
        self.color = skin.color
        self.car_type = skin.type
        self.speed_bonus = skin.speed_bonus + speed_level * 0.04
        
        self.vel_x = 0.0
        self.tilt = 0.0
        self.boost_timer = 0.0
        self.boost_multiplier = 1.0
        self.slide_vel = 0.0
        self.slide_timer = 0.0
        self.hazard_lockout = 0.0
        
        self.powerups = {
            POWERUP_SHIELD: 0.0,
            POWERUP_TIMEFREEZE: 0.0
        }
        
        self.invincible = False
        self.invincible_timer = 0.0
        
        self._cache_surf = None
        self._cache_key = None
        self._prerender()
    
    def _prerender(self):
        key = (self.color, self.car_type)
        if self._cache_key != key:
            self._cache_surf = pg.Surface((self.WIDTH + 12, self.HEIGHT + 12), pg.SRCALPHA)
            draw_car(self._cache_surf, 6, 6, self.WIDTH, self.HEIGHT, 
                    self.color, CYAN, self.car_type, player=True)
            self._cache_key = key
    
    def apply_powerup(self, kind):
        _, _, duration = POWERUP_META[kind]
        self.powerups[kind] = duration
    
    def has_powerup(self, kind):
        return self.powerups.get(kind, 0) > 0
    
    def apply_boost(self):
        self.boost_timer = 1.5
        self.boost_multiplier = 1.8
    
    def apply_oil(self):
        if self.hazard_lockout > 0:
            return
        self.slide_vel = random.choice([-1, 1]) * self.SPEED * 1.2
        self.slide_timer = 1.0
        self.hazard_lockout = 1.0
    
    def apply_invincibility(self, duration):
        self.invincible = True
        self.invincible_timer = duration
    
    def update(self, dt, keys, rain_grip_penalty=0.0):
        self.boost_timer = max(0, self.boost_timer - dt)
        if self.boost_timer <= 0:
            self.boost_multiplier = 1.0
        
        for kind in self.powerups:
            self.powerups[kind] = max(0, self.powerups[kind] - dt)
        
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
        
        if self.hazard_lockout > 0:
            self.hazard_lockout -= dt
        
        if self.slide_timer > 0:
            self.slide_timer -= dt
            self.x += self.slide_vel * dt
            self.slide_vel *= (1 - dt * 3.0)
        else:
            grip = 1.0 - rain_grip_penalty
            accel = 1200 * grip
            decel = 800 * grip
            
            if keys[pg.K_LEFT]:
                self.vel_x = max(self.vel_x - accel * dt, -self.SPEED)
            elif keys[pg.K_RIGHT]:
                self.vel_x = min(self.vel_x + accel * dt, self.SPEED)
            else:
                if abs(self.vel_x) > 0:
                    self.vel_x -= math.copysign(min(decel * dt, abs(self.vel_x)), self.vel_x)
                    if abs(self.vel_x) < 1:
                        self.vel_x = 0
            
            self.x += self.vel_x * dt
        
        self.x = clamp(self.x, ROAD_LEFT + 2, ROAD_RIGHT - self.WIDTH - 2)
        
        target_tilt = (self.vel_x + self.slide_vel) / self.SPEED * 8
        self.tilt += (target_tilt - self.tilt) * 10 * dt
    
    def get_speed_factor(self):
        factor = self.speed_bonus
        if self.boost_timer > 0:
            factor *= self.boost_multiplier
        return factor
    
    def draw(self, surface, ticks):
        if self.invincible and (ticks // 60) % 2 == 0:
            return
        
        cx = int(self.x + self.WIDTH // 2)
        cy = int(self.y + self.HEIGHT // 2)
        
        if self.has_powerup(POWERUP_SHIELD):
            glow = pg.Surface((self.WIDTH + 28, self.HEIGHT + 28), pg.SRCALPHA)
            pg.draw.ellipse(glow, (80, 180, 255, 120), glow.get_rect())
            surface.blit(glow, (int(self.x) - 14, int(self.y) - 14))
            pg.draw.ellipse(surface, (80, 180, 255), 
                          (int(self.x) - 10, int(self.y) - 10, self.WIDTH + 20, self.HEIGHT + 20), 3)
        
        if self.boost_timer > 0:
            glow = pg.Surface((self.WIDTH + 20, self.HEIGHT + 20), pg.SRCALPHA)
            pg.draw.ellipse(glow, (255, 100, 0, 100), glow.get_rect())
            surface.blit(glow, (int(self.x) - 10, int(self.y) - 10))
        
        if abs(self.tilt) > 0.3:
            temp_surf = pg.Surface((self.WIDTH + 12, self.HEIGHT + 12), pg.SRCALPHA)
            temp_surf.blit(self._cache_surf, (0, 0))
            rot = pg.transform.rotate(temp_surf, -self.tilt)
            surface.blit(rot, rot.get_rect(center=(cx, cy)))
        else:
            surface.blit(self._cache_surf, (int(self.x) - 6, int(self.y) - 6))
    
    def get_rect(self):
        m = 6
        return pg.Rect(int(self.x) + m, int(self.y) + m, 
                      self.WIDTH - m * 2, self.HEIGHT - m * 2)
