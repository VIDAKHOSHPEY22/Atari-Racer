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
from entities.powerup import PowerUp
from systems.sound import SoundManager
from systems.particle import ParticlePool
from systems.hud import HUD
from ui.button import Button
from ui.menus import MenuRenderer
from utils.helpers import get_combo_multiplier, level_threshold, clamp
from utils.persistence import load_high_score, load_progress, save_progress, save_high_score
from data.difficulty import DIFFICULTY
from data.skins import CAR_SKINS
from data.upgrades import upgrade_speed_cost, upgrade_life_cost

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("ATARI RACER - Refactored")
        self.clock = pg.time.Clock()
        self.running = True

        self.sound = SoundManager()
        self.particles = ParticlePool(150)
        self.fonts = self._get_fonts()
        self.hud = HUD(self.fonts)
        self.menu_renderer = MenuRenderer(self.fonts)

        self.high_score = load_high_score()
        self.wallet, self.upgrades = load_progress()
        self.selected_skin = 0
        self.selected_diff = "Medium"

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
        self.powerups = []
        self.score = 0
        self.run_coins = 0
        self.level = 1
        self.speed_pct = 100
        self.scroll_speed = 0
        self.obs_timer = 0.0
        self.obs_interval = 0.0
        self.coin_timer = 0.0
        self.powerup_timer = 0.0
        self.combo = 0
        self.multiplier = 1.0
        self.combo_timer = 0.0
        self.lives = 0
        self.base_lives = 0
        self.invincibility_timer = 0.0
        self.level_flash_timer = 0.0
        self.speed_blur_alpha = 0.0
        self.fb_text = ""
        self.fb_pos = (WIDTH // 2, HEIGHT // 2)
        self.fb_timer = 0.0
        self.coin_lane_history = []

        self._blur_surf = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self._prerender_blur_lines()
        self._gameplay_surf = pg.Surface((WIDTH, HEIGHT))

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

    def _prerender_blur_lines(self):
        self._blur_lines = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        for i in range(30):
            lx = ROAD_LEFT + (ROAD_RIGHT - ROAD_LEFT) * i // 30
            pg.draw.line(self._blur_lines, (255, 255, 255, 8), (lx, 0), (lx, HEIGHT), 2)

    def change_state(self, new_state):
        self.states[self.current_state].exit(self)
        self.current_state = new_state
        self.states[new_state].enter(self)

    def reset_game(self):
        diff = DIFFICULTY[self.selected_diff]
        skin = CAR_SKINS[self.selected_skin]
        speed_level = self.upgrades.get("speed", 0)
        life_level = self.upgrades.get("life", 0)

        self.base_lives = 3 + life_level
        self.player = Player(skin, speed_level=speed_level)
        self.road = Road(diff.base_speed)

        self.obs_cars.clear()
        self.obs_misc.clear()
        self.coins.clear()
        self.powerups.clear()
        self.particles.active.clear()
        self.coin_lane_history.clear()

        self.score = 0
        self.run_coins = 0
        self.level = 1
        self.speed_pct = 100
        self.scroll_speed = diff.base_speed
        self.obs_timer = 0.0
        self.obs_interval = diff.obs_interval
        self.coin_timer = 0.0
        self.powerup_timer = 0.0
        self.combo = 0
        self.multiplier = 1.0
        self.combo_timer = 0.0
        self.lives = self.base_lives
        self.invincibility_timer = 0.0
        self.level_flash_timer = 0.0
        self.speed_blur_alpha = 0.0
        self.fb_text = ""
        self.fb_timer = 0.0

    def try_boost(self):
        if self.score >= 50 and self.player.boost_timer <= 0:
            self.score -= 50
            self.player.apply_boost()
            self.set_feedback("BOOSTING!", 0.8)
            self.particles.spawn(
                self.player.x + Player.WIDTH // 2,
                self.player.y + Player.HEIGHT,
                random.uniform(-200, 200),
                random.uniform(-300, -100),
                ORANGE,
                0.8
            )
            self.sound.play("boost")
        else:
            self.set_feedback("50 PTS NEEDED!", 0.7)

    def set_feedback(self, text, duration):
        self.fb_text = text
        self.fb_pos = (int(self.player.x + Player.WIDTH // 2), int(self.player.y))
        self.fb_timer = duration

    def update_game(self, dt):
        self.invincibility_timer = max(0.0, self.invincibility_timer - dt)
        self.level_flash_timer = max(0.0, self.level_flash_timer - dt)

        self.player.update(dt, pg.key.get_pressed())

        freeze_factor = 0.3 if self.player.has_powerup(POWERUP_TIMEFREEZE) else 1.0
        base_speed_factor = self.player.get_speed_factor() * freeze_factor
        self.road.scroll_speed = self.scroll_speed * base_speed_factor
        self.road.update(dt)

        self.speed_pct = int(self.scroll_speed / DIFFICULTY[self.selected_diff].base_speed * 100)

        target_blur = clamp((self.scroll_speed - 250) / 350 * 180, 0, 180)
        self.speed_blur_alpha += (target_blur - self.speed_blur_alpha) * dt * 6

        diff = DIFFICULTY[self.selected_diff]
        effective_dt = dt * freeze_factor

        self.obs_timer += dt
        if self.obs_timer >= self.obs_interval:
            self.obs_timer = 0.0
            self._spawn_obstacle(diff)

        self.coin_timer += dt
        if self.coin_timer >= 1.2:
            self.coin_timer = 0.0
            self._spawn_coins()

        self.powerup_timer += dt
        if self.powerup_timer >= 8.0:
            self.powerup_timer = 0.0
            if random.random() < 0.55:
                kind = random.choice([POWERUP_SHIELD, POWERUP_TIMEFREEZE])
                self.powerups.append(
                    PowerUp(LANE_CENTERS[random.randint(0, 3)], self.scroll_speed * 0.85, kind)
                )

        invincible = self.invincibility_timer > 0
        player_rect = self.player.get_rect()

        for car in self.obs_cars[:]:
            if car.update(effective_dt):
                self.obs_cars.remove(car)
                self._on_obstacle_passed(2)
                continue

            if not invincible and not self.player.has_powerup(POWERUP_SHIELD):
                if car.get_rect().colliderect(player_rect):
                    self._on_hit()
                    return

        for obj in self.obs_misc[:]:
            if obj.update(effective_dt):
                self.obs_misc.remove(obj)
                self._on_obstacle_passed(1)
                continue

            if obj.get_rect().colliderect(player_rect):
                if isinstance(obj, OilSlick):
                    self.obs_misc.remove(obj)
                    if not self.player.has_powerup(POWERUP_SHIELD):
                        self.player.apply_oil()
                        self.set_feedback("SLIPPING!", 0.8)
                elif not invincible and not self.player.has_powerup(POWERUP_SHIELD):
                    self._on_hit()
                    return

        for coin in self.coins[:]:
            if coin.update(effective_dt):
                self.coins.remove(coin)
                continue
            if coin.get_rect().colliderect(player_rect):
                self.coins.remove(coin)
                self._on_coin(int(coin.x), int(coin.y))

        for pu in self.powerups[:]:
            if pu.update(effective_dt):
                self.powerups.remove(pu)
                continue
            if pu.get_rect().colliderect(player_rect):
                self.powerups.remove(pu)
                self._on_powerup(pu.kind, int(pu.x), int(pu.y))

        self.combo_timer += dt
        if self.combo_timer >= 2.5:
            self.combo_timer = 0.0
            if self.combo > 0:
                self.combo = max(0, self.combo - 1)
                self._recalc_multiplier()

        if self.fb_timer > 0:
            self.fb_timer -= dt

        if self.score >= level_threshold(self.level):
            self.level += 1
            self.scroll_speed = min(self.scroll_speed + diff.speed_inc, diff.base_speed * 2.5)
            self.obs_interval = max(0.6, self.obs_interval - 0.05)
            self.speed_pct = int(self.scroll_speed / diff.base_speed * 100)
            self.level_flash_timer = 1.0
            self.set_feedback(f"LEVEL {self.level}!", 1.0)
            self.sound.play("levelup")

            for _ in range(5):
                self.coins.append(
                    Coin(LANE_CENTERS[random.randint(0, 3)], self.scroll_speed * 0.9)
                )

    def _spawn_obstacle(self, diff):
        spd = random.uniform(*diff.obs_speed)
        occ = {c.lane for c in self.obs_cars}
        available_lanes = [i for i in range(4) if i not in occ] or list(range(4))
        lane = random.choice(available_lanes)
        lc = LANE_CENTERS[lane]

        roll = random.random()
        if roll < 0.60:
            self.obs_cars.append(ObstacleCar(lane, spd))
        elif roll < 0.92:
            self.obs_misc.append(Barrier(lc - Barrier.WIDTH // 2, spd))
        else:
            self.obs_misc.append(OilSlick(lc - OilSlick.WIDTH // 2, spd * 0.8))

    def _spawn_coins(self):
    recent = set(self.coin_lane_history[-4:])
    available = [lc for lc in LANE_CENTERS if lc not in recent]
    if not available:
        available = list(LANE_CENTERS)

    random.shuffle(available)
    count = random.randint(2, 4) if random.random() < 0.3 else 1
    count = min(count, len(available))
    chosen = available[:count]

    for lc in chosen:
        self.coins.append(Coin(lc, self.scroll_speed * 0.95))

    self.coin_lane_history.extend(chosen)
    if len(self.coin_lane_history) > 12:
        self.coin_lane_history = self.coin_lane_history[-12:]

    def _on_hit(self):
        self.lives -= 1
        self.combo = 0
        self._recalc_multiplier()
        self.set_feedback("-1 LIFE!", 1.0)

        self.particles.spawn(
            self.player.x + Player.WIDTH // 2,
            self.player.y + Player.HEIGHT // 2,
            random.uniform(-200, 200),
            random.uniform(-300, -100),
            RED,
            0.8
        )
        self.sound.play("hit")

        if self.lives <= 0:
            self._trigger_gameover()
            self.sound.play("explosion")
        else:
            self.invincibility_timer = 2.0

    def _on_obstacle_passed(self, base_points):
        self.combo += 1
        self._recalc_multiplier()
        self.score += int(base_points * self.multiplier)

    def _on_coin(self, x, y):
        self.combo += 1
        self._recalc_multiplier()
        gain = int(5 * self.multiplier)
        self.score += gain
        self.run_coins += gain

        self.fb_text = f"+{gain}"
        self.fb_pos = (x, y)
        self.fb_timer = 0.7

        self.particles.spawn(x, y, random.uniform(-100, 100), random.uniform(-200, -50), YELLOW, 0.5)
        self.sound.play("coin")

        if random.random() < 0.1 and self.player.boost_timer <= 0:
            self.player.apply_boost()
            self.set_feedback("BOOST!", 0.8)
            self.sound.play("boost")

    def _on_powerup(self, kind, x, y):
        col, _, _ = POWERUP_META[kind]
        self.particles.spawn(x, y, random.uniform(-150, 150), random.uniform(-250, -80), col, 0.6)
        self.sound.play("powerup")
        self.player.apply_powerup(kind)

        labels = {
            POWERUP_SHIELD: "SHIELD ON!",
            POWERUP_TIMEFREEZE: "TIME FREEZE!"
        }
        self.set_feedback(labels[kind], 1.0)

    def _recalc_multiplier(self):
        self.multiplier = get_combo_multiplier(self.combo)

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
        for obj in self.powerups:
            obj.draw(self._gameplay_surf)

        self.player.draw(self._gameplay_surf, pg.time.get_ticks())

        self.particles.update_and_draw(self._gameplay_surf, 1/60)

        if self.speed_blur_alpha > 4:
            alpha = int(self.speed_blur_alpha)
            self._blur_surf.fill((0, 0, 0, 0))
            self._blur_surf.blit(self._blur_lines, (0, 0))
            self._blur_surf.set_alpha(alpha)
            self._gameplay_surf.blit(self._blur_surf, (0, 0))

        screen.blit(self._gameplay_surf, (0, 0))

        self.hud.draw(
            screen, self.score, self.level, self.speed_pct,
            self.selected_diff, self.multiplier, self.lives, self.base_lives,
            self.player.boost_timer, self.player,
        )

        self.btn_pause.draw(screen, self.fonts[2])

        self._draw_feedback(screen)

        if self.score >= 50 and self.player.boost_timer <= 0:
            hint = self.fonts[2].render("SPACE = BOOST (50 pts)", True, (255, 200, 0))
            hint.set_alpha(128 + int(64 * abs(math.sin(pg.time.get_ticks() / 200))))
            screen.blit(hint, (WIDTH - 180, HEIGHT - 30))

        if self.level_flash_timer > 0:
            self._draw_level_flash(screen)

    def _draw_feedback(self, screen):
        if self.fb_timer <= 0 or not self.fb_text:
            return

        alpha = int(255 * (self.fb_timer / 0.8))
        y = self.fb_pos[1] - int((0.8 - self.fb_timer) * 80)

        surf = self.fonts[1].render(self.fb_text, True, YELLOW)
        surf.set_alpha(clamp(alpha, 0, 255))

        shadow = self.fonts[1].render(self.fb_text, True, BLACK)
        shadow.set_alpha(alpha // 2)

        screen.blit(shadow, (self.fb_pos[0] - surf.get_width() // 2 + 2, y + 2))
        screen.blit(surf, surf.get_rect(center=(self.fb_pos[0], y)))

    def _draw_level_flash(self, screen):
        alpha = int(clamp(self.level_flash_timer / 1.0 * 200, 0, 200))
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        s.fill((255, 255, 100, min(alpha // 4, 40)))
        screen.blit(s, (0, 0))

        t = self.fonts[0].render(f"LEVEL {self.level}!", True, YELLOW)
        t.set_alpha(alpha)
        y_offset = int(20 * math.sin(pg.time.get_ticks() / 100))
        screen.blit(t, t.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40 + y_offset)))

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

        for text, color, dy in [
            (f"SCORE: {self.score}", WHITE, 62),
            (f"LEVEL: {self.level}", CYAN, 90),
        ]:
            t = f_small.render(text, True, color)
            screen.blit(t, (cx - t.get_width() // 2, by + dy))

        if self.score >= self.high_score:
            hs_surf = f_small.render("NEW HIGH SCORE!", True, YELLOW)
        else:
            hs_surf = f_tiny.render(f"BEST: {self.high_score}", True, GRAY)
        screen.blit(hs_surf, (cx - hs_surf.get_width() // 2, by + 118))

        coins_surf = f_tiny.render(f"COINS EARNED: {self.run_coins}", True, YELLOW)
        screen.blit(coins_surf, (cx - coins_surf.get_width() // 2, by + 140))

        self._layout_overlay_buttons(by, include_quit=True)
        self.btn_restart.text = "RESTART"
        self.btn_menu.text = "MAIN MENU"
        self.btn_restart.draw(screen, f_small)
        self.btn_menu.draw(screen, f_small)
        self.btn_quit.draw(screen, f_small)

        hint = f_tiny.render("R restart", True, GRAY)
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

            self.states[self.current_state].handle_event(self, event)

    def _update(self, dt):
        self.states[self.current_state].update(self, dt)

    def _draw(self):
        self.states[self.current_state].draw(self, self.screen)
        pg.display.flip()
