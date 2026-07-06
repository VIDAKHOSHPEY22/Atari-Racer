import pygame as pg
from core.settings import WHITE

class Button:
    def __init__(self, x, y, w, h, text, color=None):
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.base_color = color or (45, 165, 75)
        self.hover_color = tuple(min(c + 40, 255) for c in self.base_color)
        self.enabled = True
        self._text_cache = {}
    
    def draw(self, surface, font):
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        
        if not self.enabled:
            col = (60, 60, 60)
        else:
            col = self.hover_color if hovered else self.base_color
        
        if hovered and self.enabled:
            glow = pg.Surface((self.rect.w + 10, self.rect.h + 10), pg.SRCALPHA)
            pg.draw.rect(glow, (*col, 80), (0, 0, self.rect.w + 10, self.rect.h + 10), border_radius=10)
            surface.blit(glow, (self.rect.x - 5, self.rect.y - 5))
        
        pg.draw.rect(surface, (0, 0, 0), (self.rect.x + 3, self.rect.y + 4, 
                                          self.rect.w, self.rect.h), border_radius=8)
        
        pg.draw.rect(surface, col, self.rect, border_radius=8)
        pg.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        text_col = WHITE if self.enabled else (140, 140, 140)
        key = (id(font), self.text, text_col)
        if key not in self._text_cache:
            self._text_cache[key] = font.render(self.text, True, text_col)
        
        t = self._text_cache[key]
        surface.blit(t, t.get_rect(center=self.rect.center))
    
    def clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)
