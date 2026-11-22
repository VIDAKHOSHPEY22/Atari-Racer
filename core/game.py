import pygame as pg
import sys
import random
import math
from core.settings import *
from core.state import MenuState, GarageState, PlayingState, PausedState, GameOverState
from entities.player import Player
from entities.road import Road
from entities.obstacles import ObstacleCar, Barrier, OilSlick
from entities.coin import Coin
from systems.sound import SoundManager
import systems.particle as particle
from systems.hud import HUD
from systems.achievements import AchievementManager
from ui.button import Button
from ui.menus import MenuRenderer
from utils.helpers import level_threshold, clamp, get_time_multiplier
from utils.persistence import load_high_score, load_progress, save_progress, save_high_score
from data.skins import CAR_SKINS
from data.upgrades import upgrade_speed_cost, upgrade_life_cost

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("ATARI RACER")
        self.clock = pg.time.Clock()
        self.running = True

        self.sound = SoundManager()
        self.fonts = self._get_fonts()
        self.hud = HUD(self.fonts)
        self.menu_renderer = MenuRenderer(self.fonts)
        self.achievements = AchievementManager()

        self.high_score = load_high_score()
        self.wallet, self.upgrades = load_progress()
        self.selected_skin = 0

        self._init_buttons()

        self.states = {
            "menu": MenuState(),
            "garage": GarageState(),
            "playing": PlayingState(),
            "paused": PausedState(),
            "gameover": GameOverState()
        }
        self.current_state = "menu"
        self.states[self.current_state].enter(self)

        self.player = None
        self.road = None
        self.obs_cars = []
        self.obs_misc = []
        self.coins = []
        self.score = 0
        self.run_coins = 0
        self.level = 1
        self.scroll_speed = 0
        self.obs_timer = 0.0
        self.obs_interval = OBS_BASE_INTERVAL
        self.coin_timer = 0.0
        self.lives = 0
        self.base_lives = 0
        self.invincibility_timer = 0.0
        self.level_flash_timer = 0.0
        self.hit_flash_timer = 0.0
        self.fb_text = ""
        self.fb_pos = (WIDTH // 2, HEIGHT // 2)
        self.fb_timer = 0.0
        self.time_survived = 0.0
        self.multiplier = 1.0
        self.clean_run = True
        self.coins_spent = 0

        self.toast_ach = None
        self.toast_timer = 0.0
        self.toast_max = 3.0

        self._gameplay_surf = pg.Surface((WIDTH, HEIGHT), 0, self.screen)

    def _get_fonts(self):
        return (
            pg.font.Font(None, 48),
            pg.font.Font(None, 32),
            pg.font.Font(None, 24)
        )

    def _init_buttons(self):
        btn_w = min(200, max(160, WIDTH // 5))

        self.btn_pause = Button(WIDTH - 115, 10, 100, 36, "PAUSE", (60, 60, 80))
        self.btn_restart = Button(WIDTH // 2 - btn_w // 2, 0, btn_w, 46, "RESTART")
        self.btn_menu = Button(WIDTH // 2 - btn_w // 2, 0, btn_w, 46, "MAIN MENU", (60, 80, 160))
        self.btn_quit = Button(WIDTH // 2 - btn_w // 2, 0, btn_w, 46, "QUIT", (160, 50, 50))
        self.btn_pause_yes = Button(WIDTH // 2 - 95, 0, 85, 42, "YES", (160, 50, 50))
        self.btn_pause_no = Button(WIDTH // 2 + 10, 0, 85, 42, "NO", (45, 165, 75))

        self._overlay_btn_w = btn_w

    def _layout_overlay_buttons(self, by, include_quit=False):
        bw = self._overlay_btn_w
        bx = WIDTH // 2 - bw // 2
        self.btn_restart.rect = pg.Rect(bx, by + 148, bw, 46)
        self.btn_menu.rect = pg.Rect(bx, by + 200, bw, 46)
        if include_quit:
            self.btn_quit.rect = pg.Rect(bx, by + 252, bw, 46)

    def change_state(self, new_state):
        self.states[self.current_state].exit(self)
        self.current_state = new_state
        self.states[new_state].enter(self)

    def reset_game(self):
        skin = CAR_SKINS[self.selected_skin]
        speed_level = self.upgrades.get("speed", 0)
        life_level = self.upgrades.get("life", 0)

        self.base_lives = 3 + life_level
        self.player = Player(skin, speed_level=speed_level)
        self.road = Road(300)

        self.obs_cars.clear()
        self.obs_misc.clear()
        self.coins.clear()
        particle.clear()

        self.score = 0
        self.run_coins = 0
        self.level = 1
        self.scroll_speed = 300
        self.obs_timer = 0.0
        self.obs_interval = OBS_BASE_INTERVAL
        self.coin_timer = 0.0
        self.lives = self.base_lives
        self.invincibility_timer = 0.0
        self.level_flash_timer = 0.0
        self.hit_flash_timer = 0.0
        self.fb_text = ""
        self.fb_timer = 0.0
        self.time_survived = 0.0
        self.multiplier = 1.0
        self.clean_run = True

        self.achievements.record("runs_played")

    def _get_obs_speed(self):
        t = self.time_survived
        base_lo, base_hi = OBS_BASE_SPEED
        ramp = min(t / 60.0, 3.0) * OBS_SPEED_RAMP
        return (base_lo + ramp, base_hi + ramp)

    def _get_obs_interval(self):
        t = self.time_survived
        ramp = min(t / 60.0, 3.0) * OBS_INTERVAL_RAMP
        return max(OBS_MIN_INTERVAL, OBS_BASE_INTERVAL - ramp)

    def try_boost(self):
        if self.score >= 100 and self.player.boost_timer <= 0:
            self.score -= 100
            self.player.apply_boost()
            self.set_feedback("BOOST!", 0.8)
            self.sound.play("boost")
            self.achievements.record("boosts_used")
        else:
            self.set_feedback("100 PTS NEEDED", 0.7)

    def set_feedback(self, text, duration):
        self.fb_text = text
        self.fb_pos = (int(self.player.x + Player.WIDTH // 2), int(self.player.y))
        self.fb_timer = duration

    def update_game(self, dt):
        self.time_survived += dt
        self.invincibility_timer = max(0.0, self.invincibility_timer - dt)
        self.level_flash_timer = max(0.0, self.level_flash_timer - dt)
        self.hit_flash_timer = max(0.0, self.hit_flash_timer - dt)

        self.multiplier = get_time_multiplier(self.time_survived)

        self.player.update(dt, pg.key.get_pressed())

        self.scroll_speed = 300 + min(self.time_survived / 60.0, 3.0) * 200
        self.road.scroll_speed = self.scroll_speed * self.player.get_speed_factor()
        self.road.update(dt)

        self.obs_interval = self._get_obs_interval()
        self.obs_timer += dt
        if self.obs_timer >= self.obs_interval:
            self.obs_timer = 0.0
            self._spawn_obstacle()

        self.coin_timer += dt
        if self.coin_timer >= 1.4:
            self.coin_timer = 0.0
            self._spawn_coins()

        invincible = self.invincibility_timer > 0
        player_rect = self.player.get_rect()

        for car in self.obs_cars[:]:
            if car.update(dt):
                self.obs_cars.remove(car)
                continue
            if not invincible and car.get_rect().colliderect(player_rect):
                self._on_hit(car.get_rect().clip(player_rect))
                return

        for obj in self.obs_misc[:]:
            if obj.update(dt):
                self.obs_misc.remove(obj)
                continue
            if obj.get_rect().colliderect(player_rect):
                if isinstance(obj, OilSlick):
                    self.obs_misc.remove(obj)
                    self.player.apply_oil()
                    self.set_feedback("SLIPPING!", 0.8)
                elif not invincible:
                    self._on_hit(obj.get_rect().clip(player_rect))
                    return

        for coin in self.coins[:]:
            if coin.update(dt):
                self.coins.remove(coin)
                continue
            if coin.get_rect().colliderect(player_rect):
                self.coins.remove(coin)
                self._on_coin(int(coin.x), int(coin.y))

        if self.fb_timer > 0:
            self.fb_timer -= dt

        if self.toast_timer > 0:
            self.toast_timer -= dt
        else:
            ach = self.achievements.pop_pending()
            if ach:
                self.toast_ach = ach
                self.toast_timer = self.toast_max

        if self.score >= level_threshold(self.level):
            self.level += 1
            self.level_flash_timer = 1.0
            self.set_feedback(f"LEVEL {self.level}!", 1.0)
            self.sound.play("levelup")
            self.achievements.set_stat("best_level", self.level)

        self.achievements.set_stat("best_survival", int(self.time_survived))

    def _spawn_obstacle(self):
        spd_lo, spd_hi = self._get_obs_speed()
        spd = random.uniform(spd_lo, spd_hi)
        occ = {c.lane for c in self.obs_cars}
        available = [i for i in range(4) if i not in occ] or list(range(4))
        lane = random.choice(available)
        lc = LANE_CENTERS[lane]

        roll = random.random()
        if roll < 0.60:
            self.obs_cars.append(ObstacleCar(lane, spd))
        elif roll < 0.88:
            self.obs_misc.append(Barrier(lc - Barrier.WIDTH // 2, spd))
        else:
            self.obs_misc.append(OilSlick(lc - OilSlick.WIDTH // 2, spd * 0.8))

    def _spawn_coins(self):
        available = list(LANE_CENTERS)
        random.shuffle(available)
        count = random.randint(1, 3)
        for lc in available[:count]:
            self.coins.append(Coin(lc, self.scroll_speed * 0.9))

    def _on_hit(self, contact_rect=None):
        self.lives -= 1
        self.clean_run = False
        self.set_feedback("-1 LIFE!", 1.0)

        if contact_rect and contact_rect.width > 0:
            cx, cy = contact_rect.center
        else:
            cx = self.player.x + Player.WIDTH // 2
            cy = self.player.y + Player.HEIGHT // 2

        particle.spawn_burst(cx, cy, RED, 8, 220, 0.6)

        self.hit_flash_timer = 0.25
        self.sound.play("hit")

        if self.lives <= 0:
            if self.level == 1:
                self.achievements.record("died_at_level_1")
            self._trigger_gameover()
            self.sound.play("explosion")
        else:
            self.invincibility_timer = 2.0

    def _on_coin(self, x, y):
        gain = int(COIN_BASE_VALUE * self.multiplier)
        self.score += gain
        self.run_coins += gain

        self.fb_text = f"+{gain}"
        self.fb_pos = (x, y)
        self.fb_timer = 0.6

        particle.spawn_burst(x, y, YELLOW, 5, 120, 0.4)
        self.sound.play("coin")
        self.achievements.record("coins_collected")

        if random.random() < 0.08 and self.player.boost_timer <= 0:
            self.player.apply_boost()
            self.set_feedback("FREE BOOST!", 0.8)
            self.sound.play("boost")

    def _trigger_gameover(self):
        self.change_state("gameover")

    def draw_gameplay(self, screen):
        self._gameplay_surf.fill(BLACK)

        self.road.draw(self._gameplay_surf)

        for obj in self.obs_cars:
            obj.draw(self._gameplay_surf)
        for obj in self.obs_misc:
            obj.draw(self._gameplay_surf)
        for obj in self.coins:
            obj.draw(self._gameplay_surf)

        self.player.draw(self._gameplay_surf, pg.time.get_ticks())

        particle.update_and_draw(self._gameplay_surf, 1 / 60)

        screen.blit(self._gameplay_surf, (0, 0))

        self.hud.draw(
            screen, self.score, self.level, self.time_survived,
            self.multiplier, self.lives, self.base_lives,
            self.player.boost_timer,
        )

        self.btn_pause.draw(screen, self.fonts[2])

        self._draw_feedback(screen)

        if self.score >= 100 and self.player.boost_timer <= 0:
            hint = self.fonts[2].render("SPACE = BOOST (100 pts)", True, (255, 200, 0))
            hint.set_alpha(160 + int(60 * abs(math.sin(pg.time.get_ticks() / 200))))
            screen.blit(hint, (WIDTH - 200, HEIGHT - 30))

        if self.level_flash_timer > 0:
            self._draw_level_flash(screen)

        if self.hit_flash_timer > 0:
            self._draw_hit_flash(screen)

        if self.toast_timer > 0 and self.toast_ach:
            self.hud.draw_achievement_toast(screen, self.toast_ach, self.toast_timer, self.toast_max)

    def _draw_feedback(self, screen):
        if self.fb_timer <= 0 or not self.fb_text:
            return

        alpha = int(255 * min(self.fb_timer / 0.5, 1.0))
        y = self.fb_pos[1] - int((0.8 - min(self.fb_timer, 0.8)) * 60)

        surf = self.fonts[1].render(self.fb_text, True, YELLOW)
        surf.set_alpha(clamp(alpha, 0, 255))
        screen.blit(surf, surf.get_rect(center=(self.fb_pos[0], y)))

    def _draw_level_flash(self, screen):
        alpha = int(clamp(self.level_flash_timer / 1.0 * 180, 0, 180))
        t = self.fonts[0].render(f"LEVEL {self.level}!", True, YELLOW)
        t.set_alpha(alpha)
        screen.blit(t, t.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

    def _draw_hit_flash(self, screen):
        alpha = int(clamp(self.hit_flash_timer / 0.25 * 180, 0, 180))
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pg.draw.rect(s, (255, 0, 0, alpha), (0, 0, WIDTH, HEIGHT), 14)
        screen.blit(s, (0, 0))

    def draw_overlay(self, screen, title_text, title_color, box_h, box_border_color):
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))

        bx, by = WIDTH // 2 - 200, HEIGHT // 2 - box_h // 2
        box = pg.Surface((400, box_h), pg.SRCALPHA)
        box.fill((20, 20, 30, 250))
        pg.draw.rect(box, box_border_color, (0, 0, 400, box_h), 3, border_radius=15)
        screen.blit(box, (bx, by))

        t = self.fonts[0].render(title_text, True, title_color)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, by + 18))

        return by

    def draw_pause_overlay(self, screen, confirm_pending):
        if not confirm_pending:
            by = self.draw_overlay(screen, "PAUSED", YELLOW, 180, (255, 255, 255, 60))
            self._layout_overlay_buttons(by)
            self.btn_restart.text = "RESTART"
            self.btn_menu.text = "MAIN MENU"
            self.btn_restart.draw(screen, self.fonts[1])
            self.btn_menu.draw(screen, self.fonts[1])
            hint = self.fonts[2].render("P to resume", True, GRAY)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, by + 120))
        else:
            by = self.draw_overlay(screen, "ARE YOU SURE?", YELLOW, 150, (255, 255, 255, 60))
            cx = WIDTH // 2
            self.btn_pause_yes.rect = pg.Rect(cx - 95, by + 90, 85, 42)
            self.btn_pause_no.rect = pg.Rect(cx + 10, by + 90, 85, 42)
            self.btn_pause_yes.draw(screen, self.fonts[1])
            self.btn_pause_no.draw(screen, self.fonts[1])

    def draw_game_over_overlay(self, screen):
        by = self.draw_overlay(screen, "GAME OVER", RED, 340, (200, 30, 30, 100))

        f_small, f_tiny = self.fonts[1], self.fonts[2]
        cx = WIDTH // 2

        mins = int(self.time_survived) // 60
        secs = int(self.time_survived) % 60

        for text, color, dy in [
            (f"SCORE   {self.score}", WHITE, 62),
            (f"LEVEL   {self.level}", CYAN, 90),
            (f"TIME    {mins:01d}:{secs:02d}", WHITE, 118),
        ]:
            t = f_small.render(text, True, color)
            screen.blit(t, (cx - t.get_width() // 2, by + dy))

        if self.score >= self.high_score:
            hs_surf = f_small.render("NEW HIGH SCORE!", True, YELLOW)
        else:
            hs_surf = f_tiny.render(f"BEST  {self.high_score}", True, GRAY)
        screen.blit(hs_surf, (cx - hs_surf.get_width() // 2, by + 148))

        coins_surf = f_tiny.render(f"COINS EARNED  {self.run_coins}", True, YELLOW)
        screen.blit(coins_surf, (cx - coins_surf.get_width() // 2, by + 170))

        self._layout_overlay_buttons(by, include_quit=True)
        self.btn_restart.text = "RESTART"
        self.btn_menu.text = "MAIN MENU"
        self.btn_restart.draw(screen, f_small)
        self.btn_menu.draw(screen, f_small)
        self.btn_quit.draw(screen, f_small)

        hint = f_tiny.render("R to restart", True, GRAY)
        screen.blit(hint, (cx - hint.get_width() // 2, by + 308))

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self._handle_events()
            self._update(dt)
            self._draw()
        pg.quit()
        sys.exit()

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                save_progress(self.wallet, self.upgrades)
                save_high_score(self.high_score)
                self.achievements.save()
            self.states[self.current_state].handle_event(self, event)

    def _update(self, dt):
        self.states[self.current_state].update(self, dt)

    def _draw(self):
        self.states[self.current_state].draw(self, self.screen)
        pg.display.flip()
