import pygame
import sys

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")
        
        self.line_width = 8
        self.x_color = (80, 250, 123)
        self.o_color = (255, 85, 85)
        self.text_color = (248, 248, 242)
        self.bg_color = (28, 30, 38)
        self.grid_color = (68, 71, 90)
        self.panel_color = (40, 42, 54)
        
        self.font = pygame.font.SysFont(None, 40)
        self.again_rect = pygame.Rect(self.screen_width // 2 - 80, self.screen_height // 2 + 10, 160, 50)
        
        self.reset_game()

    def reset_game(self):
        self.markers = [[0, 0, 0] for _ in range(3)]
        self.player = 1
        self.winner = 0
        self.game_over = False
        self.clicked = False

    def draw_grid(self):
        self.screen.fill(self.bg_color)
        for x in range(1, 3):
            pygame.draw.line(self.screen, self.grid_color, (0, x * 200), (self.screen_width, x * 200), self.line_width)
            pygame.draw.line(self.screen, self.grid_color, (x * 200, 0), (x * 200, self.screen_height), self.line_width)

    def draw_markers(self):
        for x, row in enumerate(self.markers):
            for y, val in enumerate(row):
                if val == 1:
                    pygame.draw.line(self.screen, self.x_color, (x * 200 + 40, y * 200 + 40), (x * 200 + 160, y * 200 + 160), self.line_width)
                    pygame.draw.line(self.screen, self.x_color, (x * 200 + 40, y * 200 + 160), (x * 200 + 160, y * 200 + 40), self.line_width)
                elif val == -1:
                    pygame.draw.circle(self.screen, self.o_color, (x * 200 + 100, y * 200 + 100), 60, self.line_width)

    def check_winner(self):
        lines = list(self.markers)
        lines.extend([[self.markers[j][i] for j in range(3)] for i in range(3)])
        lines.append([self.markers[i][i] for i in range(3)])
        lines.append([self.markers[i][2 - i] for i in range(3)])
        
        for line in lines:
            if sum(line) == 3:
                self.winner, self.game_over = 1, True
                return
            elif sum(line) == -3:
                self.winner, self.game_over = 2, True
                return

        if all(cell != 0 for row in self.markers for cell in row):
            self.game_over = True
            self.winner = 0

    def draw_game_over(self):
        text = f'Player {self.winner} wins!' if self.winner != 0 else "It's a Draw!"
        img = self.font.render(text, True, self.text_color)
        pygame.draw.rect(self.screen, self.panel_color, (self.screen_width // 2 - 100, self.screen_height // 2 - 60, 200, 50), border_radius=8)
        self.screen.blit(img, (self.screen_width // 2 - 90, self.screen_height // 2 - 50))
        
        again_img = self.font.render('Play Again?', True, self.text_color)
        pygame.draw.rect(self.screen, self.panel_color, self.again_rect, border_radius=8)
        self.screen.blit(again_img, (self.screen_width // 2 - 75, self.screen_height // 2 + 20))

    def handle_click(self, pos):
        if not self.game_over:
            cell_x, cell_y = pos[0] // 200, pos[1] // 200
            if self.markers[cell_x][cell_y] == 0:
                self.markers[cell_x][cell_y] = self.player
                self.player *= -1
                self.check_winner()
        else:
            if self.again_rect.collidepoint(pos):
                self.reset_game()

    def run(self):
        running = True
        while running:
            self.draw_grid()
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
                
            pygame.display.update()
            
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = TicTacToe()
    game.run()
