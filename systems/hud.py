import pygame as pg
import math
from core.settings import *
from utils.drawing import draw_heart
from utils.helpers import clamp, clamp_color

class HUD:
    def __init__(self, fonts):
        self.small = fonts[1]
        self.tiny = fonts[2]
        self.surf = pg.Surface((260, 160), pg.SRCALPHA)
        self._text_cache = {}

    def _render(self, font, text, color):
        surf = font.render(text, True, color)
        return surf

    def draw(self, surface, score, level, time_survived, multiplier, lives, max_lives, boost_timer):
        self.surf.fill((0, 0, 0, 170))
        pg.draw.rect(self.surf, (255, 255, 255, 35), (0, 0, 260, 160), 2, border_radius=10)

        pulse = int(8 * abs(math.sin(pg.time.get_ticks() / 300)))
        self._blit(f"SCORE  {score}", (255, 220, 50 + pulse), 12, 10)
        self._blit(f"LEVEL  {level}", CYAN, 12, 38)

        mins = int(time_survived) // 60
        secs = int(time_survived) % 60
        self._blit(f"TIME   {mins:01d}:{secs:02d}", WHITE, 12, 66)

        if multiplier > 1.0:
            col = YELLOW if multiplier >= 2.0 else (160, 230, 160)
            self._blit(f"MULT   x{multiplier:.1f}", col, 12, 94)
        else:
            self._blit("MULT   x1.0", GRAY, 12, 94)

        if boost_timer > 0:
            boost_fill = int(120 * (boost_timer / 1.5))
            pg.draw.rect(self.surf, (60, 30, 0), (12, 118, 120, 7), border_radius=3)
            pg.draw.rect(self.surf, ORANGE, (12, 118, boost_fill, 7), border_radius=3)
            self._blit("BOOST", ORANGE, 138, 114, tiny=True)

        for i in range(max_lives):
            draw_heart(self.surf, 22 + i * 22, 143, 14, RED if i < lives else (60, 60, 60))

        surface.blit(self.surf, (10, 10))

    def draw_achievement_toast(self, surface, ach, timer, max_timer):
        alpha = 255
        if timer < 0.5:
            alpha = int(255 * (timer / 0.5))
        elif timer > max_timer - 0.4:
            alpha = int(255 * ((max_timer - timer) / 0.4))
        alpha = clamp(alpha, 0, 255)

        box_w, box_h = 340, 64
        bx = WIDTH // 2 - box_w // 2
        by = 20

        box = pg.Surface((box_w, box_h), pg.SRCALPHA)
        box.fill((25, 20, 5, 220))
        pg.draw.rect(box, (255, 215, 0, 200), (0, 0, box_w, box_h), 3, border_radius=10)

        title = self.small.render("ACHIEVEMENT UNLOCKED", True, YELLOW)
        box.blit(title, (box_w // 2 - title.get_width() // 2, 8))

        name = self.small.render(ach["name"], True, WHITE)
        box.blit(name, (box_w // 2 - name.get_width() // 2, 34))

        box.set_alpha(alpha)
        surface.blit(box, (bx, by))

    def _blit(self, text, color, x, y, tiny=False):
        if isinstance(color, tuple):
            color = tuple(int(clamp(c, 0, 255)) for c in color)
        font = self.tiny if tiny else self.small
        surface = font.render(text, True, color)
        self.surf.blit(surface, (x, y))
