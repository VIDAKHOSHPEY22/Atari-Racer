import pygame as pg
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

def draw_car(surface, x, y, w, h, skin, player=False):
    body = skin.body
    roof = skin.roof
    window = skin.window
    wheel = skin.wheel
    accent = skin.accent
    car_type = skin.type

    shadow = pg.Surface((w + 6, h // 3), pg.SRCALPHA)
    pg.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
    surface.blit(shadow, (x - 3, y + h - h // 6))

    hi = clamp_color(body[0] + 45, body[1] + 45, body[2] + 45)
    sh = clamp_color(body[0] - 35, body[1] - 35, body[2] - 35)

    pg.draw.rect(surface, sh, (x + 2, y + 4, w - 4, h - 4), border_radius=5)
    pg.draw.rect(surface, body, (x, y, w, h), border_radius=5)

    if car_type == "sedan":
        roof_rect = pg.Rect(x + 8, y + 10, w - 16, h // 2 - 4)
        pg.draw.rect(surface, roof, roof_rect, border_radius=4)
        pg.draw.rect(surface, window, (x + 10, y + 13, w - 20, 16), border_radius=3)
        pg.draw.rect(surface, window, (x + 10, y + 34, w - 20, 14), border_radius=3)
        pg.draw.line(surface, sh, (x + 10, y + 30), (x + w - 10, y + 30), 2)
        pg.draw.rect(surface, accent, (x + 2, y + h - 10, w - 4, 6), border_radius=2)
        pg.draw.rect(surface, accent, (x, y + h // 2, 4, h // 3), border_radius=2)
        pg.draw.rect(surface, accent, (x + w - 4, y + h // 2, 4, h // 3), border_radius=2)
    elif car_type == "suv":
        roof_rect = pg.Rect(x + 6, y + 8, w - 12, h // 2)
        pg.draw.rect(surface, roof, roof_rect, border_radius=4)
        pg.draw.rect(surface, window, (x + 8, y + 11, w - 16, 14), border_radius=3)
        pg.draw.rect(surface, window, (x + 8, y + 30, (w - 20) // 2, 14), border_radius=3)
        pg.draw.rect(surface, window, (x + w // 2 + 2, y + 30, (w - 20) // 2, 14), border_radius=3)
        pg.draw.line(surface, sh, (x + w // 2, y + 30), (x + w // 2, y + 44), 2)
        pg.draw.rect(surface, accent, (x + 2, y + h - 10, w - 4, 6), border_radius=2)
        pg.draw.rect(surface, accent, (x, y + h // 3, 4, h // 2), border_radius=2)
        pg.draw.rect(surface, accent, (x + w - 4, y + h // 3, 4, h // 2), border_radius=2)

    rim = clamp_color(wheel[0] + 60, wheel[1] + 60, wheel[2] + 60)
    for wx, wy in [(x - 5, y + 10), (x + w - 8, y + 10), (x - 5, y + h - 22), (x + w - 8, y + h - 22)]:
        pg.draw.rect(surface, wheel, (wx, wy, 13, 13), border_radius=3)
        pg.draw.rect(surface, rim, (wx + 3, wy + 3, 7, 7), border_radius=2)

    if player:
        headlight = clamp_color(accent[0] + 80, accent[1] + 80, accent[2] + 80)
        for lx in [x + 5, x + w - 13]:
            pg.draw.ellipse(surface, headlight, (lx, y - 5, 8, 5))
        pg.draw.rect(surface, accent, (x + 5, y + h - 4, w - 10, 4), border_radius=2)
