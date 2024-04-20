import pygame
import sys
import random
import os
from themes.manager import ThemeManager
from src.logic import GameLogic
from src.ai import MinimaxAI
from src.renderer import Renderer

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display = pygame.Surface((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")
        
        self.theme_manager = ThemeManager()
        self.logic = GameLogic()
        self.ai = MinimaxAI(self.logic.check_win_state)
        self.renderer = Renderer(self.screen_width, self.screen_height)
        
        self.shake_timer = 0
        self.shake_intensity = 0
        
        try:
            self.click_sfx = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
            self.win_sfx = pygame.mixer.Sound(os.path.join("assets", "win.wav"))
        except:
            self.click_sfx = None
            self.win_sfx = None

        self.state = 'MENU'
        self.ai_timer = 0
        self.clicked = False
        
        self.apply_theme()

    def apply_theme(self):
        theme_name = self.theme_manager.get_current_theme_name()
        self.theme_config = self.theme_manager.load_theme(theme_name)

    def trigger_shake(self, frames, intensity):
        self.shake_timer = frames
        self.shake_intensity = intensity

    def play_sound(self, sound):
        if sound:
            sound.play()

    def handle_click(self, pos):
        if self.state == 'MENU':
            if self.renderer.btn_theme.collidepoint(pos):
                self.play_sound(self.click_sfx)
                self.theme_manager.next_theme()
                self.apply_theme()
            elif self.renderer.btn_1p.collidepoint(pos):
                self.play_sound(self.click_sfx)
                self.state = 'PLAYING'
                self.logic.reset(vs_ai=True)
                self.renderer.reset_animations()
            elif self.renderer.btn_2p.collidepoint(pos):
                self.play_sound(self.click_sfx)
                self.state = 'PLAYING'
                self.logic.reset(vs_ai=False)
                self.renderer.reset_animations()
        elif self.state == 'PLAYING':
            if not self.logic.game_over:
                if self.logic.vs_ai and self.logic.player == -1:
                    return
                cell_x, cell_y = pos[0] // 200, pos[1] // 200
                if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                    if self.logic.place_marker(cell_x, cell_y):
                        self.play_sound(self.click_sfx)
                        self.trigger_shake(5, 3)
                        if self.logic.update_winner():
                            self.play_sound(self.win_sfx)
                            self.trigger_shake(20 if self.logic.winner != 0 else 10, 10 if self.logic.winner != 0 else 5)
                        elif self.logic.vs_ai:
                            self.ai_timer = 20
            else:
                if self.renderer.btn_retry.collidepoint(pos):
                    self.play_sound(self.click_sfx)
                    self.logic.reset(vs_ai=self.logic.vs_ai)
                    self.renderer.reset_animations()
                elif self.renderer.btn_menu.collidepoint(pos):
                    self.play_sound(self.click_sfx)
                    self.state = 'MENU'

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            if self.state == 'MENU':
                self.renderer.draw_menu(self.display, self.theme_manager.get_current_theme_name(), self.theme_config)
            else:
                self.renderer.draw_grid(self.display, self.theme_config)
                self.renderer.draw_hover(self.display, self.logic, pygame.mouse.get_pos(), self.theme_config)
                self.renderer.draw_markers(self.display, self.logic, self.theme_config)
                if self.logic.game_over:
                    self.renderer.draw_game_over(self.display, self.logic, self.theme_config)
                    
                if self.state == 'PLAYING' and not self.logic.game_over and self.logic.vs_ai and self.logic.player == -1:
                    if self.ai_timer > 0:
                        self.ai_timer -= 1
                    else:
                        self.ai.play_best_move(self.logic.markers, self.logic.place_marker)
                        self.play_sound(self.click_sfx)
                        self.trigger_shake(5, 3)
                        if self.logic.update_winner():
                            self.play_sound(self.win_sfx)
                            self.trigger_shake(20 if self.logic.winner != 0 else 10, 10 if self.logic.winner != 0 else 5)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                elif event.type == pygame.MOUSEBUTTONUP and self.clicked:
                    self.clicked = False
                    self.handle_click(pygame.mouse.get_pos())
                
            dx, dy = 0, 0
            if self.shake_timer > 0:
                self.shake_timer -= 1
                dx = random.randint(-self.shake_intensity, self.shake_intensity)
                dy = random.randint(-self.shake_intensity, self.shake_intensity)
                
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.display, (dx, dy))
            pygame.display.update()
            clock.tick(60)
            
        pygame.quit()
        sys.exit()
