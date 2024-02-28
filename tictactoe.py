import pygame
import sys
import random
import os

class TicTacToe:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display = pygame.Surface((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")
        
        self.line_width = 8
        self.x_color = (80, 250, 123)
        self.o_color = (255, 85, 85)
        self.text_color = (248, 248, 242)
        self.bg_color = (28, 30, 38)
        self.hover_color = (38, 40, 50)
        self.grid_color = (68, 71, 90)
        self.panel_color = (40, 42, 54)
        
        self.font = pygame.font.SysFont(None, 40)
        self.again_rect = pygame.Rect(self.screen_width // 2 - 80, self.screen_height // 2 + 10, 160, 50)
        
        self.shake_timer = 0
        self.shake_intensity = 0
        
        try:
            self.click_sfx = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
            self.win_sfx = pygame.mixer.Sound(os.path.join("assets", "win.wav"))
        except:
            self.click_sfx = None
            self.win_sfx = None

        self.reset_game()

    def reset_game(self):
        self.markers = [[0, 0, 0] for _ in range(3)]
        self.animations = [[0.0 for _ in range(3)] for _ in range(3)]
        self.player = 1
        self.winner = 0
        self.game_over = False
        self.clicked = False

    def trigger_shake(self, frames, intensity):
        self.shake_timer = frames
        self.shake_intensity = intensity

    def play_sound(self, sound):
        if sound:
            sound.play()

    def draw_grid(self):
        self.display.fill(self.bg_color)
        for x in range(1, 3):
            pygame.draw.line(self.display, self.grid_color, (0, x * 200), (self.screen_width, x * 200), self.line_width)
            pygame.draw.line(self.display, self.grid_color, (x * 200, 0), (x * 200, self.screen_height), self.line_width)

    def draw_hover(self):
        if not self.game_over:
            pos = pygame.mouse.get_pos()
            cell_x, cell_y = pos[0] // 200, pos[1] // 200
            if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                if self.markers[cell_x][cell_y] == 0:
                    pygame.draw.rect(self.display, self.hover_color, (cell_x * 200, cell_y * 200, 200, 200))

    def draw_markers(self):
        for x, row in enumerate(self.markers):
            for y, val in enumerate(row):
                if val != 0:
                    prog = self.animations[x][y]
                    if prog < 1.0:
                        self.animations[x][y] = min(1.0, prog + 0.1)
                        prog = self.animations[x][y]
                    
                    cx, cy = x * 200 + 100, y * 200 + 100
                    
                    if val == 1:
                        l = 60 * prog
                        pygame.draw.line(self.display, self.x_color, (cx - l, cy - l), (cx + l, cy + l), self.line_width)
                        pygame.draw.line(self.display, self.x_color, (cx - l, cy + l), (cx + l, cy - l), self.line_width)
                    elif val == -1:
                        r = max(self.line_width, int(60 * prog))
                        pygame.draw.circle(self.display, self.o_color, (cx, cy), r, self.line_width)

    def check_winner(self):
        lines = list(self.markers)
        lines.extend([[self.markers[j][i] for j in range(3)] for i in range(3)])
        lines.append([self.markers[i][i] for i in range(3)])
        lines.append([self.markers[i][2 - i] for i in range(3)])
        
        for line in lines:
            if sum(line) == 3:
                self.winner, self.game_over = 1, True
                self.trigger_shake(20, 10)
                self.play_sound(self.win_sfx)
                return
            elif sum(line) == -3:
                self.winner, self.game_over = 2, True
                self.trigger_shake(20, 10)
                self.play_sound(self.win_sfx)
                return

        if all(cell != 0 for row in self.markers for cell in row):
            self.game_over = True
            self.winner = 0
            self.trigger_shake(10, 5)

    def draw_game_over(self):
        text = f'Player {self.winner} wins!' if self.winner != 0 else "It's a Draw!"
        img = self.font.render(text, True, self.text_color)
        pygame.draw.rect(self.display, self.panel_color, (self.screen_width // 2 - 100, self.screen_height // 2 - 60, 200, 50), border_radius=8)
        self.display.blit(img, (self.screen_width // 2 - 90, self.screen_height // 2 - 50))
        
        again_img = self.font.render('Play Again?', True, self.text_color)
        pygame.draw.rect(self.display, self.panel_color, self.again_rect, border_radius=8)
        self.display.blit(again_img, (self.screen_width // 2 - 75, self.screen_height // 2 + 20))

    def handle_click(self, pos):
        if not self.game_over:
            cell_x, cell_y = pos[0] // 200, pos[1] // 200
            if self.markers[cell_x][cell_y] == 0:
                self.markers[cell_x][cell_y] = self.player
                self.player *= -1
                self.trigger_shake(5, 3)
                self.play_sound(self.click_sfx)
                self.check_winner()
        else:
            if self.again_rect.collidepoint(pos):
                self.reset_game()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.draw_grid()
            self.draw_hover()
            self.draw_markers()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                elif event.type == pygame.MOUSEBUTTONUP and self.clicked:
                    self.clicked = False
                    self.handle_click(pygame.mouse.get_pos())
            
            if self.game_over:
                self.draw_game_over()
                
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

if __name__ == '__main__':
    game = TicTacToe()
    game.run()
