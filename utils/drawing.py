import pygame as pg
from core.settings import RED, CYAN, BLACK, WHITE
from utils.helpers import clamp_color

def draw_heart(surface, cx, cy, size, color):
    r = size // 2
    pg.draw.circle(surface, color, (cx - r // 2, cy), r // 2)
    pg.draw.circle(surface, color, (cx + r // 2, cy), r // 2)
    pg.draw.polygon(surface, color, [(cx - r, cy), (cx + r, cy), (cx, cy + int(r * 1.2))])

def draw_arrow(surface, cx, cy, size, color, direction):
    h = size // 2
    if direction == "left":
        pts = [(cx + h, cy - h), (cx + h, cy + h), (cx - h, cy)]
    else:
        pts = [(cx - h, cy - h), (cx - h, cy + h), (cx, cy)]
    pg.draw.polygon(surface, color, pts)

def draw_car(surface, x, y, w, h, body_color, window_color, car_type, player=False):
    shadow = pg.Surface((w + 6, h // 3), pg.SRCALPHA)
    pg.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
    surface.blit(shadow, (x - 3, y + h - h // 6))
    
    r, g, b = body_color
    hi = clamp_color(r + 50, g + 50, b + 50)
    sh = clamp_color(r - 40, g - 40, b - 40)
    
    pg.draw.rect(surface, sh, (x + 2, y + 4, w - 4, h - 4), border_radius=5)
    pg.draw.rect(surface, body_color, (x, y, w, h), border_radius=5)
    pg.draw.rect(surface, hi, (x + 3, y + 3, w - 6, 8), border_radius=3)
    
    if car_type == "sedan":
        pg.draw.rect(surface, window_color, (x + 6, y + 12, w - 12, 20), border_radius=3)
        pg.draw.rect(surface, window_color, (x + 6, y + 38, w - 12, 18), border_radius=3)
        pg.draw.line(surface, (0, 0, 0), (x + 6, y + 23), (x + w - 6, y + 23), 1)
    elif car_type == "truck":
        pg.draw.rect(surface, window_color, (x + 8, y + 8, w - 16, 18), border_radius=3)
        pg.draw.rect(surface, sh, (x + 4, y + 35, w - 8, h - 42), border_radius=2)
        pg.draw.line(surface, hi, (x + 4, y + 34), (x + w - 4, y + 34), 1)
    else:  # suv
        pg.draw.rect(surface, window_color, (x + 6, y + 10, w - 12, 30), border_radius=3)
        pg.draw.line(surface, (0, 0, 0), (x + w // 2, y + 10), (x + w // 2, y + 40), 1)
    
    wheel_col, rim_col = (30, 30, 35), (120, 120, 130)
    for wx, wy in [(x - 4, y + 8), (x + w - 9, y + 8), (x - 4, y + h - 20), (x + w - 9, y + h - 20)]:
        pg.draw.rect(surface, wheel_col, (wx, wy, 13, 13), border_radius=3)
        pg.draw.rect(surface, rim_col, (wx + 3, wy + 3, 7, 7), border_radius=2)
    
    if player:
        for lx in [x + 4, x + w - 12]:
            pg.draw.ellipse(surface, (255, 255, 100), (lx, y - 5, 8, 6))
        pg.draw.rect(surface, RED, (x + 4, y + h - 4, w - 8, 4), border_radius=2)
