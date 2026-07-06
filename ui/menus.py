import pygame as pg
import math
from core.settings import *
from data.skins import CAR_SKINS
from data.difficulty import DIFFICULTY
from ui.button import Button
from utils.drawing import draw_car, draw_arrow
from utils.helpers import clamp

class MenuRenderer:
    def __init__(self, fonts):
        self.fonts = fonts
        self.selected_skin = 0
        self.selected_diff = "Medium"
        self._init_buttons()
    
    def _init_buttons(self):
        btn_w = min(200, max(160, WIDTH // 5))
        
        self.btn_play = Button(WIDTH // 2 - 100, 490, 200, 52, "START RACE")
        self.btn_garage = Button(WIDTH // 2 - 100, 552, 200, 36, "GARAGE", (60, 60, 110))
        self.btn_garage_back = Button(WIDTH // 2 - btn_w // 2, 530, btn_w, 44, "BACK")
        
        self.btn_upgrade_speed = Button(WIDTH // 2 - 170, 220, 340, 46, "")
        self.btn_upgrade_life = Button(WIDTH // 2 - 170, 290, 340, 46, "")
        
        self._diff_rects = {
            d: pg.Rect(WIDTH // 2 - 90, 148 + i * 46, 180, 36)
            for i, d in enumerate(["Easy", "Medium", "Hard"])
        }
        
        self._arrow_left_rect = pg.Rect(WIDTH // 2 - 145, 365, 40, 40)
        self._arrow_right_rect = pg.Rect(WIDTH // 2 + 105, 365, 40, 40)
    
    def draw_menu(self, screen, high_score, wallet):
        f_main, f_small, f_tiny = self.fonts
        elapsed = pg.time.get_ticks() / 1000
        
        for y in range(HEIGHT):
            shade = clamp(10 + int(25 * math.sin(y / 30 + elapsed)), 0, 255)
            pg.draw.line(screen, (shade, shade, min(shade + 10, 255)), (0, y), (WIDTH, y))
        
        title = f_main.render("ATARI RACER", True, YELLOW)
        tx = WIDTH // 2 - title.get_width() // 2
        for offset in range(3):
            glow = f_main.render("ATARI RACER", True, (100, 70 + offset * 20, 0))
            screen.blit(glow, (tx - offset, 38 - offset))
        screen.blit(title, (tx, 35))
        
        sub = f_tiny.render("EXTREME EDITION", True, ORANGE)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 85))
        
        bg = pg.Surface((460, 480), pg.SRCALPHA)
        bg.fill((0, 0, 0, 190))
        pg.draw.rect(bg, (255, 255, 255, 40), (0, 0, 460, 480), 2, border_radius=15)
        screen.blit(bg, (WIDTH // 2 - 230, 115))
        
        lbl = f_small.render("DIFFICULTY", True, WHITE)
        screen.blit(lbl, (WIDTH // 2 - lbl.get_width() // 2, 122))
        
        for d, r in self._diff_rects.items():
            sel = d == self.selected_diff
            col = GREEN if sel else (70, 70, 75)
            if sel:
                pg.draw.rect(screen, (0, 200, 0, 80), r.inflate(10, 10), border_radius=8)
            pg.draw.rect(screen, col, r, border_radius=7)
            pg.draw.rect(screen, WHITE, r, 2 if sel else 1, border_radius=7)
            t = f_small.render(d, True, WHITE)
            screen.blit(t, t.get_rect(center=r.center))
        
        lbl2 = f_small.render("CAR SKIN", True, WHITE)
        screen.blit(lbl2, (WIDTH // 2 - lbl2.get_width() // 2, 310))
        
        skin = CAR_SKINS[self.selected_skin]
        px, py = WIDTH // 2 - 24, 345
        
        pbg = pg.Surface((100, 110), pg.SRCALPHA)
        pbg.fill((25, 25, 35, 220))
        pg.draw.rect(pbg, (255, 255, 255, 40), (0, 0, 100, 110), 1, border_radius=8)
        screen.blit(pbg, (px - 26, py - 5))
        
        draw_car(screen, px, py, 48, 88, skin.color, CYAN, skin.type, player=True)
        
        mouse = pg.mouse.get_pos()
        for rect, direction in [(self._arrow_left_rect, "left"), (self._arrow_right_rect, "right")]:
            col = GREEN if rect.collidepoint(mouse) else (70, 70, 75)
            if rect.collidepoint(mouse):
                pg.draw.rect(screen, (0, 200, 0, 80), rect.inflate(10, 10), border_radius=8)
            pg.draw.rect(screen, col, rect, border_radius=6)
            pg.draw.rect(screen, WHITE, rect, 1, border_radius=6)
            draw_arrow(screen, rect.centerx, rect.centery, 18, WHITE, direction)
        
        bonus_val = skin.speed_bonus
        bonus_text = f_tiny.render(
            f"{skin.name} - {'+' if bonus_val > 1 else ''}{int((bonus_val - 1) * 100)}% SPEED",
            True, GREEN if bonus_val >= 1 else ORANGE,
        )
        screen.blit(bonus_text, (WIDTH // 2 - bonus_text.get_width() // 2, 445))
        
        hs_text = f"HIGH SCORE: {high_score}    COINS: {wallet}"
        screen.blit(f_tiny.render(hs_text, True, YELLOW), 
                   (WIDTH // 2 - f_tiny.size(hs_text)[0] // 2, 465))
        
        self.btn_play.draw(screen, f_small)
        self.btn_garage.draw(screen, f_tiny)
        
        hint = f_tiny.render("   Move  |  SPACE to boost  |  P - Pause  |  R - Restart", True, GRAY)
        text_x = WIDTH // 2 - hint.get_width() // 2
        MARGIN = 20
        al_x = text_x - 22
        ar_x = text_x - 4
        if al_x < MARGIN:
            shift = MARGIN - al_x
            al_x += shift
            ar_x += shift
            text_x += shift
        screen.blit(hint, (text_x, 555))
        draw_arrow(screen, al_x, 560, 14, GRAY, "left")
        draw_arrow(screen, ar_x, 560, 14, GRAY, "right")
    
    def draw_garage(self, screen, wallet, upgrades):
        f_main, f_small, f_tiny = self.fonts
        elapsed = pg.time.get_ticks() / 1000
        
        for y in range(HEIGHT):
            shade = clamp(10 + int(25 * math.sin(y / 30 + elapsed)), 0, 255)
            pg.draw.line(screen, (shade, shade, min(shade + 10, 255)), (0, y), (WIDTH, y))
        
        title = f_main.render("GARAGE", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 35))
        
        coin_text = f_small.render(f"COINS: {wallet}", True, YELLOW)
        screen.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, 95))
        
        bg = pg.Surface((460, 380), pg.SRCALPHA)
        bg.fill((0, 0, 0, 190))
        pg.draw.rect(bg, (255, 255, 255, 40), (0, 0, 460, 380), 2, border_radius=15)
        screen.blit(bg, (WIDTH // 2 - 230, 140))
        
        speed_level = upgrades["speed"]
        from data.upgrades import UPGRADE_SPEED_MAX_LEVEL, upgrade_speed_cost
        if speed_level >= UPGRADE_SPEED_MAX_LEVEL:
            self.btn_upgrade_speed.text = "TOP SPEED - MAXED"
            self.btn_upgrade_speed.enabled = False
        else:
            cost = upgrade_speed_cost(speed_level)
            self.btn_upgrade_speed.text = f"TOP SPEED  Lv{speed_level} -> Lv{speed_level + 1}   ({cost} coins)"
            self.btn_upgrade_speed.enabled = wallet >= cost
        self.btn_upgrade_speed.draw(screen, f_tiny)
        
        life_level = upgrades["life"]
        from data.upgrades import UPGRADE_LIFE_MAX_LEVEL, upgrade_life_cost
        if life_level >= UPGRADE_LIFE_MAX_LEVEL:
            self.btn_upgrade_life.text = "EXTRA LIFE - MAXED"
            self.btn_upgrade_life.enabled = False
        else:
            cost = upgrade_life_cost(life_level)
            self.btn_upgrade_life.text = f"EXTRA LIFE  Lv{life_level} -> Lv{life_level + 1}   ({cost} coins)"
            self.btn_upgrade_life.enabled = wallet >= cost
        self.btn_upgrade_life.draw(screen, f_tiny)
        
        info1 = f_tiny.render("Permanently +4% top speed per level", True, GRAY)
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 270))
        info2 = f_tiny.render("Permanently +1 starting life per level", True, GRAY)
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 340))
        
        self.btn_garage_back.draw(screen, f_small)
    
    def handle_menu_click(self, pos):
        for d, r in self._diff_rects.items():
            if r.collidepoint(pos):
                self.selected_diff = d
                return "diff_changed"
        
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
