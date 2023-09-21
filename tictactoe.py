import pygame
from pygame.locals import *

pygame.init()


screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac Toe")

line_width = 6
markers = []

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
            
print(markers)

running = True
while running:
    
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()

    
