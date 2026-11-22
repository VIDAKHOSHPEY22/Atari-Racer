import pygame as pg
import math
from core.settings import *
from data.skins import CAR_SKINS
from ui.button import Button
from utils.drawing import draw_car, draw_arrow
from utils.helpers import clamp

class MenuRenderer:
    def __init__(self, fonts):
        self.fonts = fonts
        self.selected_skin = 0
        self._init_buttons()
        self._grad_strip = pg.Surface((1, HEIGHT))
        self._grad_cache_key = None
        self._grad_surf = None

    def _init_buttons(self):
        btn_w = min(200, max(160, WIDTH // 5))
        cx = WIDTH // 2

        self.btn_play = Button(cx - 110, 490, 220, 52, "START RACE")
        self.btn_garage = Button(cx - 70, 552, 140, 36, "GARAGE", (60, 60, 110))
        self.btn_garage_back = Button(cx - btn_w // 2, 530, btn_w, 44, "BACK")

        self.btn_upgrade_speed = Button(cx - 180, 230, 360, 48, "")
        self.btn_upgrade_life = Button(cx - 180, 310, 360, 48, "")

        self._arrow_left_rect = pg.Rect(cx - 150, 330, 44, 44)
        self._arrow_right_rect = pg.Rect(cx + 106, 330, 44, 44)

    def _draw_bg(self, screen, elapsed):
        key = int(elapsed * 10)
        if key != self._grad_cache_key:
            self._grad_cache_key = key
            for y in range(HEIGHT):
                shade = clamp(10 + int(25 * math.sin(y / 30 + elapsed)), 0, 255)
                self._grad_strip.set_at((0, y), (shade, shade, min(shade + 10, 255)))
            self._grad_surf = pg.transform.scale(self._grad_strip, (WIDTH, HEIGHT))
        screen.blit(self._grad_surf, (0, 0))

    def _draw_divider(self, screen, y):
        pg.draw.line(screen, (80, 80, 100), (WIDTH // 2 - 260, y), (WIDTH // 2 + 260, y), 1)

    def draw_menu(self, screen, high_score, wallet):
        f_main, f_small, f_tiny = self.fonts
        elapsed = pg.time.get_ticks() / 1000
        cx = WIDTH // 2

        self._draw_bg(screen, elapsed)

        title = f_main.render("ATARI RACER", True, YELLOW)
        tx = cx - title.get_width() // 2
        for offset in range(3):
            glow = f_main.render("ATARI RACER", True, (100, 70 + offset * 20, 0))
            screen.blit(glow, (tx - offset, 18 - offset))
        screen.blit(title, (tx, 15))

        bg = pg.Surface((580, 530), pg.SRCALPHA)
        bg.fill((0, 0, 0, 190))
        pg.draw.rect(bg, (255, 255, 255, 40), (0, 0, 580, 530), 2, border_radius=15)
        screen.blit(bg, (cx - 290, 72))

        lbl = f_small.render("SELECT CAR", True, WHITE)
        screen.blit(lbl, (cx - lbl.get_width() // 2, 86))

        self._draw_divider(screen, 115)

        skin = CAR_SKINS[self.selected_skin]
        px, py = cx - 24, 190

        pbg = pg.Surface((110, 120), pg.SRCALPHA)
        pbg.fill((25, 25, 35, 220))
        pg.draw.rect(pbg, (255, 255, 255, 40), (0, 0, 110, 120), 1, border_radius=8)
        screen.blit(pbg, (px - 31, py - 10))
        draw_car(screen, px, py, 48, 88, skin, player=True)

        name_surf = f_small.render(skin.name, True, WHITE)
        screen.blit(name_surf, (cx - name_surf.get_width() // 2, 300))

        mouse = pg.mouse.get_pos()
        for rect, direction in [(self._arrow_left_rect, "left"), (self._arrow_right_rect, "right")]:
            col = GREEN if rect.collidepoint(mouse) else (70, 70, 75)
            if rect.collidepoint(mouse):
                pg.draw.rect(screen, (0, 200, 0, 60), rect.inflate(8, 8), border_radius=8)
            pg.draw.rect(screen, col, rect, border_radius=6)
            pg.draw.rect(screen, WHITE, rect, 1, border_radius=6)
            draw_arrow(screen, rect.centerx, rect.centery, 18, WHITE, direction)

        skin_dots_y = 368
        for i, _ in enumerate(CAR_SKINS):
            dot_x = cx - (len(CAR_SKINS) * 14) // 2 + i * 14 + 7
            col = WHITE if i == self.selected_skin else (60, 60, 60)
            pg.draw.circle(screen, col, (dot_x, skin_dots_y), 5)

        self._draw_divider(screen, 390)

        hs_text = f_small.render(f"BEST  {high_score}", True, YELLOW)
        coins_text = f_small.render(f"COINS  {wallet}", True, (200, 200, 60))
        screen.blit(hs_text, (cx - 120, 408))
        screen.blit(coins_text, (cx + 10, 408))

        self._draw_divider(screen, 448)

        self.btn_play.draw(screen, f_small)
        self.btn_garage.draw(screen, f_tiny)

        hint = f_tiny.render("ARROWS to steer   SPACE boost   P pause", True, GRAY)
        screen.blit(hint, (cx - hint.get_width() // 2, 578))

    def draw_garage(self, screen, wallet, upgrades):
        f_main, f_small, f_tiny = self.fonts
        elapsed = pg.time.get_ticks() / 1000
        cx = WIDTH // 2

        self._draw_bg(screen, elapsed)

        title = f_main.render("GARAGE", True, YELLOW)
        screen.blit(title, (cx - title.get_width() // 2, 35))

        self._draw_divider(screen, 85)

        coin_surf = f_small.render(f"COINS  {wallet}", True, YELLOW)
        screen.blit(coin_surf, (cx - coin_surf.get_width() // 2, 100))

        bg = pg.Surface((480, 320), pg.SRCALPHA)
        bg.fill((0, 0, 0, 190))
        pg.draw.rect(bg, (255, 255, 255, 40), (0, 0, 480, 320), 2, border_radius=15)
        screen.blit(bg, (cx - 240, 150))

        self._draw_divider(screen, 175)

        speed_lbl = f_small.render("TOP SPEED", True, CYAN)
        screen.blit(speed_lbl, (cx - speed_lbl.get_width() // 2, 185))

        speed_level = upgrades["speed"]
        from data.upgrades import UPGRADE_SPEED_MAX_LEVEL, upgrade_speed_cost
        if speed_level >= UPGRADE_SPEED_MAX_LEVEL:
            self.btn_upgrade_speed.text = "MAXED OUT"
            self.btn_upgrade_speed.enabled = False
        else:
            cost = upgrade_speed_cost(speed_level)
            self.btn_upgrade_speed.text = f"Lv {speed_level} → Lv {speed_level + 1}   {cost} coins"
            self.btn_upgrade_speed.enabled = wallet >= cost
        self.btn_upgrade_speed.draw(screen, f_small)

        info1 = f_tiny.render("+4% top speed per level", True, GRAY)
        screen.blit(info1, (cx - info1.get_width() // 2, 285))

        self._draw_divider(screen, 310)

        life_lbl = f_small.render("EXTRA LIFE", True, RED)
        screen.blit(life_lbl, (cx - life_lbl.get_width() // 2, 322))

        life_level = upgrades["life"]
        from data.upgrades import UPGRADE_LIFE_MAX_LEVEL, upgrade_life_cost
        if life_level >= UPGRADE_LIFE_MAX_LEVEL:
            self.btn_upgrade_life.text = "MAXED OUT"
            self.btn_upgrade_life.enabled = False
        else:
            cost = upgrade_life_cost(life_level)
            self.btn_upgrade_life.text = f"Lv {life_level} → Lv {life_level + 1}   {cost} coins"
            self.btn_upgrade_life.enabled = wallet >= cost
        self.btn_upgrade_life.draw(screen, f_small)

        info2 = f_tiny.render("+1 starting life per level", True, GRAY)
        screen.blit(info2, (cx - info2.get_width() // 2, 400))

        self._draw_divider(screen, 430)

        self.btn_garage_back.draw(screen, f_small)

    def handle_menu_click(self, pos):
        if self._arrow_left_rect.collidepoint(pos):
            self.selected_skin = (self.selected_skin - 1) % len(CAR_SKINS)
            return "skin_changed"

        if self._arrow_right_rect.collidepoint(pos):
            self.selected_skin = (self.selected_skin + 1) % len(CAR_SKINS)
            return "skin_changed"

        if self.btn_play.clicked(pos):
            return "play"

        if self.btn_garage.clicked(pos):
            return "garage"

        return None

    def handle_garage_click(self, pos, wallet, upgrades):
        if self.btn_garage_back.clicked(pos):
            return "back", wallet, upgrades

        from data.upgrades import UPGRADE_SPEED_MAX_LEVEL, UPGRADE_LIFE_MAX_LEVEL
        from data.upgrades import upgrade_speed_cost, upgrade_life_cost

        speed_level = upgrades["speed"]
        if speed_level < UPGRADE_SPEED_MAX_LEVEL and self.btn_upgrade_speed.clicked(pos):
            cost = upgrade_speed_cost(speed_level)
            if wallet >= cost:
                wallet -= cost
                upgrades["speed"] += 1
                return "upgrade", wallet, upgrades

        life_level = upgrades["life"]
        if life_level < UPGRADE_LIFE_MAX_LEVEL and self.btn_upgrade_life.clicked(pos):
            cost = upgrade_life_cost(life_level)
            if wallet >= cost:
                wallet -= cost
                upgrades["life"] += 1
                return "upgrade", wallet, upgrades

        return None, wallet, upgrades
