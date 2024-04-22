import pygame
import os

class ThemeManager:
    def __init__(self):
        self.themes = ['Whiteboard', 'Blackboard', 'Paper']
        self.current_idx = 0
        self.assets = {}

    def get_current_theme_name(self):
        return self.themes[self.current_idx]

    def next_theme(self):
        self.current_idx = (self.current_idx + 1) % len(self.themes)
        return self.get_current_theme_name()

    def load_theme(self, name):
        config = {}
        config['use_assets'] = True
        
        folder_name = name.lower()
        
        # UI Colors
        if name == 'Blackboard':
            config['font_path'] = os.path.join('assets', 'fonts', 'patrickhand.ttf')
            config['text_color'] = (248, 248, 242)
            config['bg_color'] = (30, 45, 35)
            config['overlay_color'] = (0, 0, 0, 150)
            config['hover_color'] = (45, 65, 50)
            config['grid_color'] = (100, 120, 110)
            config['panel_color'] = (40, 60, 45)
        elif name == 'Whiteboard':
            config['font_path'] = os.path.join('assets', 'fonts', 'kalam.ttf')
            config['text_color'] = (40, 42, 54)
            config['bg_color'] = (250, 250, 250)
            config['overlay_color'] = (255, 255, 255, 180)
            config['hover_color'] = (230, 230, 240)
            config['grid_color'] = (200, 200, 210)
            config['panel_color'] = (240, 240, 245)
        elif name == 'Paper':
            config['font_path'] = os.path.join('assets', 'fonts', 'indieflower.ttf')
            config['text_color'] = (40, 40, 40)
            config['bg_color'] = (245, 235, 220)
            config['overlay_color'] = (255, 255, 255, 180)
            config['hover_color'] = (235, 220, 200)
            config['grid_color'] = (160, 180, 210)
            config['panel_color'] = (255, 250, 240)
            
        if folder_name not in self.assets:
            self.assets[folder_name] = {}
            try:
                self.assets[folder_name]['bg'] = pygame.image.load(os.path.join('assets', 'themes', folder_name, 'bg.png')).convert()
                self.assets[folder_name]['x'] = pygame.image.load(os.path.join('assets', 'themes', folder_name, 'x.png')).convert_alpha()
                self.assets[folder_name]['o'] = pygame.image.load(os.path.join('assets', 'themes', folder_name, 'o.png')).convert_alpha()
                self.assets[folder_name]['grid'] = pygame.image.load(os.path.join('assets', 'themes', folder_name, 'grid.png')).convert_alpha()
            except Exception as e:
                print(f"Could not load {name} assets:", e)
                config['use_assets'] = False
                
        if config['use_assets']:
            bg_img = self.assets[folder_name]['bg']
            if bg_img.get_width() != 600 or bg_img.get_height() != 600:
                bg_img = pygame.transform.scale(bg_img, (600, 600))
            config['bg_img'] = bg_img
            config['x_img'] = self.assets[folder_name]['x']
            config['o_img'] = self.assets[folder_name]['o']
            config['grid_img'] = self.assets[folder_name]['grid']
            
        try:
            config['title_font'] = pygame.font.Font(config['font_path'], 70)
            config['btn_font'] = pygame.font.Font(config['font_path'], 35)
            config['small_font'] = pygame.font.Font(config['font_path'], 24)
        except Exception as e:
            print("Font error:", e)
            config['title_font'] = pygame.font.SysFont(None, 70)
            config['btn_font'] = pygame.font.SysFont(None, 35)
            config['small_font'] = pygame.font.SysFont(None, 24)

        return config
