import pygame
import sys

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")
        
        self.line_width = 6
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.bg_color = (255, 255, 200)
        self.grid_color = (50, 50, 50)
        
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
                    pygame.draw.line(self.screen, self.green, (x * 200 + 15, y * 200 + 15), (x * 200 + 185, y * 200 + 185), self.line_width * 2)
                    pygame.draw.line(self.screen, self.green, (x * 200 + 15, y * 200 + 185), (x * 200 + 185, y * 200 + 15), self.line_width * 2)
                elif val == -1:
                    pygame.draw.circle(self.screen, self.red, (x * 200 + 100, y * 200 + 100), 85, self.line_width * 2)

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
        if self.winner != 0:
            text = f'Player {self.winner} wins!'
        else:
            text = "It's a Draw!"
            
        img = self.font.render(text, True, self.blue)
        pygame.draw.rect(self.screen, self.green, (self.screen_width // 2 - 100, self.screen_height // 2 - 60, 200, 50))
        self.screen.blit(img, (self.screen_width // 2 - 100, self.screen_height // 2 - 50))
        
        again_text = 'Play Again?'
        again_img = self.font.render(again_text, True, self.blue)
        pygame.draw.rect(self.screen, self.green, self.again_rect)
        self.screen.blit(again_img, (self.screen_width // 2 - 80, self.screen_height // 2 + 20))

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
