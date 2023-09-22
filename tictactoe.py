import pygame
from pygame.locals import *

pygame.init()


screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac Toe")

line_width = 6
markers = []
clicked = False
pos = []
player = 1
winner = 0
game_over = False

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0 , 255)

font = pygame.font.SysFont(None, 40)

again_rect = Rect(screen_width // 2 - 80, screen_height // 2 + 10 , 160, 50)

def draw_grid():
    bg = (255, 255, 200)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, x * 200), (screen_width, x * 200), line_width)
        pygame.draw.line(screen, grid, ( x * 200, 0), (x * 200, screen_width), line_width)
        
for x in range(3):
    row = [0] * 3
    markers.append(row)
            
            
def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
              pygame.draw.line(screen, green, (x_pos * 200 + 15, y_pos * 200 + 15), (x_pos * 200 + 185, y_pos * 200 + 185), line_width*2)
              pygame.draw.line(screen, green, (x_pos * 200 + 15, y_pos * 200 + 185), (x_pos * 200 + 185, y_pos * 200 + 15), line_width*2)
            if y == -1:
                pygame.draw.circle(screen, red, (x_pos * 200 + 100, y_pos * 200 + 100), 85, line_width*2)
            y_pos += 1
        x_pos += 1
        
def check_winner():
    
    global winner
    global game_over
    
    y_pos = 0
    for x in markers:
        if sum(x) == 3:
            winner = 1
            game_over = True
        if sum(x) == -3:
            winner = 2
            game_over = True
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True
        y_pos =+ 1
    
    if markers[0][0] + markers [1][1] + markers [2][2] == 3 or markers[2][0] + markers [1][1] + markers [0][2] == 3:
        winner = 1
        game_over = True
    if markers[0][0] + markers [1][1] + markers [2][2] == -3 or markers[2][0] + markers [1][1] + markers [0][2] == -3:
        winner = 2
        game_over = True

def draw_winner(winner):
    win_text = 'Player ' + str(winner) + ' wins!'
    win_img = font.render(win_text, True, blue)
    pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
    screen.blit(win_img, (screen_width // 2 - 100, screen_height // 2 - 50))
    
    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 20))
    
def check_draw():
    global game_over
    if all(markers[i][j] != 0 for i in range(3) for j in range(3)):
        game_over = True

def draw_draw():
    draw_text = 'It\'s a Draw!'
    draw_img = font.render(draw_text, True, blue)
    draw_rect = draw_img.get_rect(center=(screen_width // 2, screen_height // 2 - 25))
    pygame.draw.rect(screen, green, draw_rect)
    screen.blit(draw_img, draw_rect)
    
    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    again_rect = again_img.get_rect(center=(screen_width // 2, screen_height // 2 + 25))
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, again_rect)


running = True
while running:
    
    draw_grid()
    draw_markers()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over == 0:
            if event.type == MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked == False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0]
                cell_y = pos[1]
                if markers [cell_x // 200][cell_y // 200] == 0:
                    markers [cell_x // 200][cell_y // 200] = player
                    player *= -1
                    check_winner()
                    check_draw()
    
    if game_over == True:
        if winner != 0:
            draw_winner(winner)
        else:
            draw_draw()
            
            pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN and clicked == False:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked == False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                markers = []
                pos = []
                player = 1
                winner = 0
                game_over = False
                for x in range(3):
                    row = [0] * 3
                    markers.append(row)
                    
            
    pygame.display.update()

pygame.quit()