from abc import ABC, abstractmethod
import pygame as pg
from core.settings import *

class GameState(ABC):
    @abstractmethod
    def enter(self, game):
        pass
    
    @abstractmethod
    def exit(self, game):
        pass
    
    @abstractmethod
    def update(self, game, dt):
        pass
    
    @abstractmethod
    def draw(self, game, screen):
        pass
    
    @abstractmethod
    def handle_event(self, game, event):
        pass


class MenuState(GameState):
    def enter(self, game):
        game.menu_renderer.selected_skin = game.selected_skin
        game.menu_renderer.selected_diff = game.selected_diff
    
    def exit(self, game):
        game.selected_skin = game.menu_renderer.selected_skin
        game.selected_diff = game.menu_renderer.selected_diff
    
    def update(self, game, dt):
        pass
    
    def draw(self, game, screen):
        game.menu_renderer.draw_menu(screen, game.high_score, game.wallet)
    
    def handle_event(self, game, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            result = game.menu_renderer.handle_menu_click(event.pos)
            if result == "play":
                game.change_state("playing")
            elif result == "garage":
                game.change_state("garage")
            elif result == "diff_changed":
                game.selected_diff = game.menu_renderer.selected_diff
            elif result == "skin_changed":
                game.selected_skin = game.menu_renderer.selected_skin


class GarageState(GameState):
    def enter(self, game):
        pass
    
    def exit(self, game):
        pass
    
    def update(self, game, dt):
        pass
    
    def draw(self, game, screen):
        game.menu_renderer.draw_garage(screen, game.wallet, game.upgrades)
    
    def handle_event(self, game, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            result, wallet, upgrades = game.menu_renderer.handle_garage_click(
                event.pos, game.wallet, game.upgrades
            )
            if result == "back":
                game.change_state("menu")
            elif result == "upgrade":
                game.wallet = wallet
                game.upgrades = upgrades
                from utils.persistence import save_progress
                save_progress(game.wallet, game.upgrades)


class PlayingState(GameState):
    def enter(self, game):
        if not hasattr(game, 'player') or game.player is None:
            game.reset_game()
    
    def exit(self, game):
        pass
    
    def update(self, game, dt):
        if game.running:
            game.update_game(dt)
    
    def draw(self, game, screen):
        game.draw_gameplay(screen)
    
    def handle_event(self, game, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                game.change_state("paused")
            elif event.key == pg.K_SPACE:
                game.try_boost()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if game.btn_pause.clicked(event.pos):
                game.change_state("paused")


class PausedState(GameState):
    def __init__(self):
        self.confirm_pending = False
        self.confirm_action = None
    
    def enter(self, game):
        self.confirm_pending = False
        self.confirm_action = None
    
    def exit(self, game):
        pass
    
    def update(self, game, dt):
        pass
    
    def draw(self, game, screen):
        game.draw_gameplay(screen)
        game.draw_pause_overlay(screen, self.confirm_pending)
    
    def handle_event(self, game, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            if self.confirm_pending:
                self.confirm_pending = False
            else:
                game.change_state("playing")
            return
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not self.confirm_pending:
                if game.btn_restart.clicked(event.pos):
                    self.confirm_pending = True
                    self.confirm_action = "restart"
                elif game.btn_menu.clicked(event.pos):
                    self.confirm_pending = True
                    self.confirm_action = "menu"
                elif game.btn_pause.clicked(event.pos):
                    game.change_state("playing")
            else:
                if game.btn_pause_yes.clicked(event.pos):
                    from utils.persistence import save_progress, save_high_score
                    game.wallet += game.run_coins
                    save_progress(game.wallet, game.upgrades)
                    save_high_score(game.high_score)
                    
                    if self.confirm_action == "restart":
                        game.reset_game()
                        game.change_state("playing")
                    else:
                        game.reset_game()
                        game.change_state("menu")
                    
                    self.confirm_pending = False
                elif game.btn_pause_no.clicked(event.pos):
                    self.confirm_pending = False


class GameOverState(GameState):
    def enter(self, game):
        from utils.persistence import save_progress, save_high_score
        game.wallet += game.run_coins
        save_progress(game.wallet, game.upgrades)
        
        if game.score > game.high_score:
            game.high_score = game.score
            save_high_score(game.high_score)
    
    def exit(self, game):
        pass
    
    def update(self, game, dt):
        pass
    
    def draw(self, game, screen):
        game.draw_gameplay(screen)
        game.draw_game_over_overlay(screen)
    
    def handle_event(self, game, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            game.reset_game()
            game.change_state("playing")
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if game.btn_restart.clicked(event.pos):
                game.reset_game()
                game.change_state("playing")
            elif game.btn_menu.clicked(event.pos):
                game.reset_game()
                game.change_state("menu")
            elif hasattr(game, 'btn_quit') and game.btn_quit.clicked(event.pos):
                pg.quit()
                import sys
                sys.exit()
