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
        
        # Bigger buttons with more padding
        self.btn_1p = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 - 50, 280, 60)
        self.btn_2p = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 + 30, 280, 60)
        
        self.btn_retry = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 - 20, 240, 50)
        self.btn_menu = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 + 45, 240, 50)
        
        self.shake_timer = 0
        self.shake_intensity = 0
        
        try:
            self.click_sfx = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
            self.win_sfx = pygame.mixer.Sound(os.path.join("assets", "win.wav"))
        except:
            self.click_sfx = None
            self.win_sfx = None

        self.state = 'MENU'
        self.vs_ai = False
        self.ai_timer = 0
        self.reset_game(vs_ai=False)

    def reset_game(self, vs_ai=False):
        self.markers = [[0, 0, 0] for _ in range(3)]
        self.animations = [[0.0 for _ in range(3)] for _ in range(3)]
        self.player = 1
        self.winner = 0
        self.game_over = False
        self.clicked = False
        self.vs_ai = vs_ai
        self.ai_timer = 0

    def trigger_shake(self, frames, intensity):
        self.shake_timer = frames
        self.shake_intensity = intensity

    def play_sound(self, sound):
        if sound:
            sound.play()

    def draw_menu(self):
        self.display.fill(self.bg_color)
        title = self.font.render("TIC TAC TOE", True, self.x_color)
        self.display.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 150))
        
        pygame.draw.rect(self.display, self.panel_color, self.btn_1p, border_radius=8)
        text_1p = self.font.render("1 Player (vs AI)", True, self.text_color)
        self.display.blit(text_1p, (self.btn_1p.centerx - text_1p.get_width() // 2, self.btn_1p.centery - text_1p.get_height() // 2))
        
        pygame.draw.rect(self.display, self.panel_color, self.btn_2p, border_radius=8)
        text_2p = self.font.render("2 Player", True, self.text_color)
        self.display.blit(text_2p, (self.btn_2p.centerx - text_2p.get_width() // 2, self.btn_2p.centery - text_2p.get_height() // 2))

    def draw_grid(self):
        self.display.fill(self.bg_color)
        for x in range(1, 3):
            pygame.draw.line(self.display, self.grid_color, (0, x * 200), (self.screen_width, x * 200), self.line_width)
            pygame.draw.line(self.display, self.grid_color, (x * 200, 0), (x * 200, self.screen_height), self.line_width)

    def draw_hover(self):
        if not self.game_over and not (self.vs_ai and self.player == -1):
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

    def check_win_state(self, board):
        lines = list(board)
        lines.extend([[board[j][i] for j in range(3)] for i in range(3)])
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2 - i] for i in range(3)])
        
        for line in lines:
            if sum(line) == 3:
                return 1
            elif sum(line) == -3:
                return -1
                
        if all(cell != 0 for row in board for cell in row):
            return 0
        return None

    def check_winner(self):
        res = self.check_win_state(self.markers)
        if res == 1:
            self.winner, self.game_over = 1, True
            self.trigger_shake(20, 10)
            self.play_sound(self.win_sfx)
        elif res == -1:
            self.winner, self.game_over = 2, True
            self.trigger_shake(20, 10)
            self.play_sound(self.win_sfx)
        elif res == 0:
            self.winner, self.game_over = 0, True
            self.trigger_shake(10, 5)

    def draw_game_over(self):
        text = f'Player {self.winner} wins!' if self.winner != 0 else "It's a Draw!"
        img = self.font.render(text, True, self.text_color)
        
        panel_rect = pygame.Rect(self.screen_width // 2 - 160, self.screen_height // 2 - 100, 320, 220)
        pygame.draw.rect(self.display, self.panel_color, panel_rect, border_radius=12)
        self.display.blit(img, (self.screen_width // 2 - img.get_width() // 2, self.screen_height // 2 - 80))
        
        pygame.draw.rect(self.display, self.hover_color, self.btn_retry, border_radius=8)
        retry_img = self.font.render('Retry', True, self.text_color)
        self.display.blit(retry_img, (self.btn_retry.centerx - retry_img.get_width() // 2, self.btn_retry.centery - retry_img.get_height() // 2))

        pygame.draw.rect(self.display, self.hover_color, self.btn_menu, border_radius=8)
        menu_img = self.font.render('Menu', True, self.text_color)
        self.display.blit(menu_img, (self.btn_menu.centerx - menu_img.get_width() // 2, self.btn_menu.centery - menu_img.get_height() // 2))

    def place_marker(self, x, y):
        self.markers[x][y] = self.player
        self.player *= -1
        self.trigger_shake(5, 3)
        self.play_sound(self.click_sfx)
        self.check_winner()
        if not self.game_over and self.vs_ai and self.player == -1:
            self.ai_timer = 20

    def minimax(self, board, depth, is_maximizing):
        res = self.check_win_state(board)
        if res == 1:
            return 10 - depth
        elif res == -1:
            return -10 + depth
        elif res == 0:
            return 0
            
        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = -1
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = 0
                        best_score = min(score, best_score)
            return best_score

    def play_ai_move(self):
        best_score = float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.markers[i][j] == 0:
                    self.markers[i][j] = -1
                    score = self.minimax(self.markers, 0, True)
                    self.markers[i][j] = 0
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            self.place_marker(best_move[0], best_move[1])

    def handle_click(self, pos):
        if self.state == 'MENU':
            if self.btn_1p.collidepoint(pos):
                self.play_sound(self.click_sfx)
                self.state = 'PLAYING'
                self.reset_game(vs_ai=True)
            elif self.btn_2p.collidepoint(pos):
                self.play_sound(self.click_sfx)
                self.state = 'PLAYING'
                self.reset_game(vs_ai=False)
        elif self.state == 'PLAYING':
            if not self.game_over:
                if self.vs_ai and self.player == -1:
                    return
                cell_x, cell_y = pos[0] // 200, pos[1] // 200
                if 0 <= cell_x < 3 and 0 <= cell_y < 3 and self.markers[cell_x][cell_y] == 0:
                    self.place_marker(cell_x, cell_y)
            else:
                if self.btn_retry.collidepoint(pos):
                    self.play_sound(self.click_sfx)
                    self.reset_game(vs_ai=self.vs_ai)
                elif self.btn_menu.collidepoint(pos):
                    self.play_sound(self.click_sfx)
                    self.state = 'MENU'

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            if self.state == 'MENU':
                self.draw_menu()
            else:
                self.draw_grid()
                self.draw_hover()
                self.draw_markers()
                if self.game_over:
                    self.draw_game_over()
                    
                if self.state == 'PLAYING' and not self.game_over and self.vs_ai and self.player == -1:
                    if self.ai_timer > 0:
                        self.ai_timer -= 1
                    else:
                        self.play_ai_move()
            
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

if __name__ == '__main__':
    game = TicTacToe()
    game.run()
