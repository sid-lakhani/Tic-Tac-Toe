import pygame

class Renderer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 40)
        self.line_width = 8
        
        self.btn_1p = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 - 50, 280, 60)
        self.btn_2p = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 + 30, 280, 60)
        self.btn_retry = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 - 20, 240, 50)
        self.btn_menu = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 + 45, 240, 50)
        self.btn_theme = pygame.Rect(self.screen_width - 220, 20, 200, 40)
        
        self.animations = [[0.0 for _ in range(3)] for _ in range(3)]

    def reset_animations(self):
        self.animations = [[0.0 for _ in range(3)] for _ in range(3)]

    def draw_menu(self, display, theme, config):
        if config.get('use_assets'):
            display.blit(config['bg_img'], (0, 0))
        else:
            display.fill(config['bg_color'])
            
        title = self.font.render("TIC TAC TOE", True, config['text_color'])
        display.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 150))
        
        pygame.draw.rect(display, config['panel_color'], self.btn_theme, border_radius=8)
        theme_font = pygame.font.SysFont(None, 24)
        theme_text = theme_font.render(f"Theme: {theme}", True, config['text_color'])
        display.blit(theme_text, (self.btn_theme.centerx - theme_text.get_width() // 2, self.btn_theme.centery - theme_text.get_height() // 2))
        
        pygame.draw.rect(display, config['panel_color'], self.btn_1p, border_radius=8)
        text_1p = self.font.render("1 Player (vs AI)", True, config['text_color'])
        display.blit(text_1p, (self.btn_1p.centerx - text_1p.get_width() // 2, self.btn_1p.centery - text_1p.get_height() // 2))
        
        pygame.draw.rect(display, config['panel_color'], self.btn_2p, border_radius=8)
        text_2p = self.font.render("2 Player", True, config['text_color'])
        display.blit(text_2p, (self.btn_2p.centerx - text_2p.get_width() // 2, self.btn_2p.centery - text_2p.get_height() // 2))

    def draw_grid(self, display, config):
        if config.get('use_assets'):
            display.blit(config['bg_img'], (0, 0))
            grid_img = config.get('grid_img')
            if grid_img:
                display.blit(grid_img, (0, 0))
            else:
                for x in range(1, 3):
                    pygame.draw.line(display, config['grid_color'], (0, x * 200), (self.screen_width, x * 200), self.line_width)
                    pygame.draw.line(display, config['grid_color'], (x * 200, 0), (x * 200, self.screen_height), self.line_width)
        else:
            display.fill(config['bg_color'])
            for x in range(1, 3):
                pygame.draw.line(display, config['grid_color'], (0, x * 200), (self.screen_width, x * 200), self.line_width)
                pygame.draw.line(display, config['grid_color'], (x * 200, 0), (x * 200, self.screen_height), self.line_width)

    def draw_hover(self, display, logic, pos, config):
        if not logic.game_over and not (logic.vs_ai and logic.player == -1):
            cell_x, cell_y = pos[0] // 200, pos[1] // 200
            if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                if logic.markers[cell_x][cell_y] == 0:
                    cx, cy = cell_x * 200 + 100, cell_y * 200 + 100
                    if config.get('use_assets'):
                        ghost = config['x_img'].copy() if logic.player == 1 else config['o_img'].copy()
                        ghost.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_MULT)
                        display.blit(ghost, (cx - 100, cy - 100))
                    else:
                        s = pygame.Surface((200, 200), pygame.SRCALPHA)
                        if logic.player == 1:
                            pygame.draw.line(s, (*config['x_color'], 80), (40, 40), (160, 160), self.line_width)
                            pygame.draw.line(s, (*config['x_color'], 80), (40, 160), (160, 40), self.line_width)
                        else:
                            pygame.draw.circle(s, (*config['o_color'], 80), (100, 100), 60, self.line_width)
                        display.blit(s, (cell_x * 200, cell_y * 200))

    def draw_markers(self, display, logic, config):
        for x, row in enumerate(logic.markers):
            for y, val in enumerate(row):
                if val != 0:
                    prog = self.animations[x][y]
                    if prog < 1.0:
                        self.animations[x][y] = min(1.0, prog + 0.1)
                        prog = self.animations[x][y]
                    
                    cx, cy = x * 200 + 100, y * 200 + 100
                    
                    if config.get('use_assets'):
                        size = int(200 * prog)
                        if size > 0:
                            img = config['x_img'] if val == 1 else config['o_img']
                            scaled = pygame.transform.scale(img, (size, size))
                            display.blit(scaled, (cx - size // 2, cy - size // 2))
                    else:
                        if val == 1:
                            l = 60 * prog
                            pygame.draw.line(display, config['x_color'], (cx - l, cy - l), (cx + l, cy + l), self.line_width)
                            pygame.draw.line(display, config['x_color'], (cx - l, cy + l), (cx + l, cy - l), self.line_width)
                        elif val == -1:
                            r = max(self.line_width, int(60 * prog))
                            pygame.draw.circle(display, config['o_color'], (cx, cy), r, self.line_width)

    def draw_game_over(self, display, logic, config):
        text = f'Player {logic.winner} wins!' if logic.winner != 0 else "It's a Draw!"
        img = self.font.render(text, True, config['text_color'])
        
        panel_rect = pygame.Rect(self.screen_width // 2 - 160, self.screen_height // 2 - 100, 320, 220)
        pygame.draw.rect(display, config['panel_color'], panel_rect, border_radius=12)
        display.blit(img, (self.screen_width // 2 - img.get_width() // 2, self.screen_height // 2 - 80))
        
        pygame.draw.rect(display, config['hover_color'], self.btn_retry, border_radius=8)
        retry_img = self.font.render('Retry', True, config['text_color'])
        display.blit(retry_img, (self.btn_retry.centerx - retry_img.get_width() // 2, self.btn_retry.centery - retry_img.get_height() // 2))

        pygame.draw.rect(display, config['hover_color'], self.btn_menu, border_radius=8)
        menu_img = self.font.render('Menu', True, config['text_color'])
        display.blit(menu_img, (self.btn_menu.centerx - menu_img.get_width() // 2, self.btn_menu.centery - menu_img.get_height() // 2))
