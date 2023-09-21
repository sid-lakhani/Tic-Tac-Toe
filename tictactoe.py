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

green = (0, 255, 0)
red = (255, 0, 0)

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

running = True
while running:
    
    draw_grid()
    draw_markers()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            
    pygame.display.update()

pygame.quit()

    
