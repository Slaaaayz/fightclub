import pygame
from src.settings import Settings
from src.sound_manager import SoundManager

class Menu:
    def __init__(self, screen, resources, is_temp_menu=False):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.settings = resources.settings
        self.sound_manager = resources.sound_manager
        
        self.clock = pygame.time.Clock()
        
        self.COLOR_INACTIVE = (40, 40, 60)
        self.COLOR_ACTIVE = (255, 255, 255)
        self.COLOR_HOVER = (60, 60, 80)
        self.COLOR_BACKGROUND = (20, 20, 30)
        
        self.COLOR_SLIDER_BG = (40, 40, 60)
        self.COLOR_SLIDER_FG = (0, 200, 255)
        self.COLOR_SLIDER_HOVER = (0, 220, 255)
        
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 90)
        
        self.current_tab = "main"
        self.selected_option = 0
        self.hover_option = -1
        
        self.last_hover = -1 
        
        self.main_options = ["Play", "Settings", "Controls", "Quit"]
        self.settings_options = [
            "Master Volume: {}%",  
            "Music Volume: {}%",   
            "SFX Volume: {}%",     
            "Show FPS: {}",
            "Back"
        ]
        self.controls_options = [
            "Player 1 Controls",
            "Player 2 Controls",
            "Back"
        ]
        
        self.button_rects = []
        self.sliders = {}
        self.create_buttons()
        
        self.volume_step = 10
        
        self.slider_width = 400
        self.slider_height = 8
        self.slider_button_size = 24
        
        self.dragging_slider = None 
        
    

    def create_buttons(self):
        self.button_rects = []
        self.sliders = {}
        options = self.get_current_options()
        
        start_y = self.height * 0.4
        for i, option in enumerate(options):
            if self.current_tab == "settings" and "Volume" in option:
                slider_rect = pygame.Rect(
                    self.width/2 - self.slider_width/2,
                    start_y + i * 70,
                    self.slider_width,
                    self.slider_height
                )
                self.sliders[option] = slider_rect
                self.button_rects.append(pygame.Rect(0, 0, 0, 0))
            else:
                text_surface = self.font.render(option, True, self.COLOR_INACTIVE)
                button_rect = text_surface.get_rect(center=(self.width/2, start_y + i * 70))
                self.button_rects.append(button_rect)

    def get_current_options(self):
        if self.current_tab == "main":
            return self.main_options
        elif self.current_tab == "settings":
            return self.settings_options
        elif self.current_tab == "controls":
            return self.controls_options
        return []

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = event.pos
                for option, slider_rect in self.sliders.items():
                    value = self.get_slider_value(option)
                    button_x = slider_rect.left + (slider_rect.width * value) - self.slider_button_size/2
                    button_rect = pygame.Rect(button_x, slider_rect.y - self.slider_button_size/2,
                                           self.slider_button_size, self.slider_button_size)
                    if button_rect.collidepoint(mouse_pos):
                        self.dragging_slider = option
                        return True
                
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(event.pos):
                        return self.handle_click(i)
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_slider = None
            
        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            slider_rect = self.sliders[self.dragging_slider]
            value = (event.pos[0] - slider_rect.left) / slider_rect.width
            value = max(0, min(1, value))
            if "Master" in self.dragging_slider:
                self.settings.master_volume = value
                self.sound_manager.set_master_volume(value)
            elif "Music" in self.dragging_slider:
                self.settings.music_volume = value
                self.sound_manager.set_music_volume(value)
            elif "SFX" in self.dragging_slider:
                self.settings.sfx_volume = value
                self.sound_manager.set_sfx_volume(value)
            self.settings.save_settings()
            
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            old_hover = self.hover_option
            self.hover_option = -1
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.hover_option = i
                    if old_hover != i:
                        self.sound_manager.play_sound('hover', volume=0.3)
                    break
        
        return True

    def handle_click(self, option_index):
        options = self.get_current_options()
        selected_option = options[option_index]
        
        if self.current_tab == "main":
            if selected_option == "Play":
                return False  
            elif selected_option == "Settings":
                self.current_tab = "settings"
            elif selected_option == "Controls":
                self.current_tab = "controls"
            elif selected_option == "Quit":
                pygame.quit()
                exit()
                
        elif self.current_tab == "settings":
            if "Music Volume" in selected_option:
                self.settings.music_volume = min(1.0, max(0.0, 
                    self.settings.music_volume + (0.1 if pygame.mouse.get_pos()[0] > self.width/2 else -0.1)))
                self.sound_manager.set_music_volume(self.settings.music_volume)
            elif "SFX Volume" in selected_option:
                self.settings.sfx_volume = min(1.0, max(0.0, 
                    self.settings.sfx_volume + (0.1 if pygame.mouse.get_pos()[0] > self.width/2 else -0.1)))
                self.sound_manager.set_sfx_volume(self.settings.sfx_volume)
            elif "Master Volume" in selected_option:
                self.settings.master_volume = min(1.0, max(0.0, 
                    self.settings.master_volume + (0.1 if pygame.mouse.get_pos()[0] > self.width/2 else -0.1)))
                self.sound_manager.set_master_volume(self.settings.master_volume)
            elif "Show FPS" in selected_option:
                self.settings.show_fps = not self.settings.show_fps
                self.settings.save_settings()
                if hasattr(self, 'game'):
                    self.game.settings = self.settings
            elif selected_option == "Back":
                if hasattr(self, 'is_temp_menu') and self.is_temp_menu:
                    return "back"
                else:
                    self.current_tab = "main"
                
        elif self.current_tab == "controls":
            if selected_option == "Back":
                self.current_tab = "main"
                
        self.create_buttons()
        return True

    def get_slider_value(self, option):
        if "Music" in option:
            return self.settings.music_volume
        elif "SFX" in option:
            return self.settings.sfx_volume
        elif "Master" in option:
            return self.settings.master_volume
        return 0

    def draw_controls_info(self):
        self.screen.fill(self.COLOR_BACKGROUND)
        
        title_text = "CONTROLS"
        shadow = self.title_font.render(title_text, True, (0, 0, 0))
        title = self.title_font.render(title_text, True, (0, 200, 255))
        
        shadow_rect = shadow.get_rect(center=(self.width/2 + 3, 80 + 3))
        title_rect = title.get_rect(center=(self.width/2, 80))
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        panel_width = self.width * 0.35
        panel_height = self.height * 0.6
        panel_padding = 30
        
        # Panel Joueur 1 (gauche)
        p1_panel = pygame.Rect(
            self.width * 0.1,
            self.height * 0.2,
            panel_width,
            panel_height
        )
        
        # Panel Joueur 2 (droite)
        p2_panel = pygame.Rect(
            self.width * 0.55,
            self.height * 0.2,
            panel_width,
            panel_height
        )
        
        def draw_control_panel(panel_rect, title, controls):
            pygame.draw.rect(self.screen, self.COLOR_INACTIVE, panel_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 200, 255), panel_rect, 2, border_radius=10)
            
            panel_title = pygame.font.Font(None, 48).render(title, True, (0, 200, 255))
            title_rect = panel_title.get_rect(
                centerx=panel_rect.centerx,
                top=panel_rect.top + 20
            )
            self.screen.blit(panel_title, title_rect)
            
            pygame.draw.line(
                self.screen,
                (0, 200, 255),
                (panel_rect.left + 20, title_rect.bottom + 10),
                (panel_rect.right - 20, title_rect.bottom + 10),
                2
            )
            
            y = title_rect.bottom + 40
            control_font = pygame.font.Font(None, 36)
            
            for action, key in controls:
                action_text = control_font.render(action, True, (255, 255, 255))
                action_rect = action_text.get_rect(
                    left=panel_rect.left + panel_padding,
                    centery=y
                )
                self.screen.blit(action_text, action_rect)
                
                key_bg = pygame.Rect(
                    panel_rect.right - 120 - panel_padding,  
                    y - 15,
                    100,  
                    30
                )
                pygame.draw.rect(self.screen, (40, 40, 60), key_bg, border_radius=5)
                pygame.draw.rect(self.screen, (0, 200, 255), key_bg, 2, border_radius=5)
                
                key_text = control_font.render(key, True, (200, 200, 200))
                key_rect = key_text.get_rect(center=key_bg.center)
                self.screen.blit(key_text, key_rect)
                
                y += 60
        
        controls_p1 = [
            ("Move Left", "Q"),
            ("Move Right", "D"),
            ("Jump", "Z"),
            ("Light Attack", "S"),
            ("Heavy Attack", "A"),
            ("Special Attack", "E")
        ]
        
        controls_p2 = [
            ("Move Left", "LEFT"),
            ("Move Right", "RIGHT"),
            ("Jump", "UP"),
            ("Light Attack", "Enter"),
            ("Heavy Attack", "DOWN"),
            ("Special Attack", "R-Shift")
        ]
        
        draw_control_panel(p1_panel, "PLAYER 1", controls_p1)
        draw_control_panel(p2_panel, "PLAYER 2", controls_p2)

    def draw(self):
        self.screen.fill(self.COLOR_BACKGROUND)
        
        title_text = "FIGHT CLUB"
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        title_surface = self.title_font.render(title_text, True, (0, 200, 255))
        shadow_rect = shadow_surface.get_rect(center=(self.width/2 + 4, self.height * 0.2 + 4))
        title_rect = title_surface.get_rect(center=(self.width/2, self.height * 0.2))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        options = self.get_current_options()
        button_count = len([opt for opt in options if opt != "Back"])  
        start_y = self.height * 0.4
        
        total_height = button_count * 70 
        if total_height > (self.height * 0.8 - start_y):  
            spacing = (self.height * 0.8 - start_y) / button_count
        else:
            spacing = 70
        
        current_y = start_y
        for i, option in enumerate(options):
            if option == "Back": 
                continue
            
            if self.current_tab == "settings" and "Volume" in option:
                slider_rect = pygame.Rect(
                    self.width/2 - self.slider_width/2,
                    current_y,
                    self.slider_width,
                    self.slider_height
                )
                self.sliders[option] = slider_rect
                
                value = self.get_slider_value(option)
                text = f"{option.split(':')[0]}: {int(value * 100)}%"
                text_surface = self.font.render(text, True, self.COLOR_ACTIVE)
                text_rect = text_surface.get_rect(midtop=(self.width/2, current_y - 40))
                self.screen.blit(text_surface, text_rect)
                
                pygame.draw.rect(self.screen, self.COLOR_SLIDER_BG, slider_rect)
                
                filled_rect = pygame.Rect(
                    slider_rect.left,
                    slider_rect.top,
                    slider_rect.width * value,
                    slider_rect.height
                )
                pygame.draw.rect(self.screen, self.COLOR_SLIDER_FG, filled_rect)
                
                button_x = slider_rect.left + (slider_rect.width * value)
                button_center = (button_x, slider_rect.centery)
                pygame.draw.circle(self.screen, self.COLOR_SLIDER_FG, button_center, 
                                 self.slider_button_size/2)
            elif self.current_tab == "settings" and "Show FPS" in option:
                rect = pygame.Rect(
                    self.width/2 - 100,
                    current_y,
                    200,
                    50
                )
                self.button_rects[i] = rect
                
                text = f"Show FPS: {'On' if self.settings.show_fps else 'Off'}"
                
                color = self.COLOR_HOVER if i == self.hover_option else self.COLOR_INACTIVE
                pygame.draw.rect(self.screen, color, rect)
                
                text_surface = self.font.render(text, True, self.COLOR_ACTIVE)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)
            else:
                rect = pygame.Rect(
                    self.width/2 - 100,
                    current_y,
                    200,
                    50
                )
                self.button_rects[i] = rect
                
                color = self.COLOR_HOVER if i == self.hover_option else self.COLOR_INACTIVE
                pygame.draw.rect(self.screen, color, rect)
                
                text_surface = self.font.render(option, True, self.COLOR_ACTIVE)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)
            
            current_y += spacing
        
        if self.current_tab == "controls":
            self.draw_controls_info()
        
        if self.current_tab != "main":
            back_index = next(i for i, opt in enumerate(options) if opt == "Back")
            back_rect = pygame.Rect(
                self.width/2 - 100,
                self.height * 0.85,
                200,
                50
            )
            self.button_rects[back_index] = back_rect
            
            color = self.COLOR_HOVER if back_index == self.hover_option else self.COLOR_INACTIVE
            pygame.draw.rect(self.screen, color, back_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 200, 255), back_rect, 2, border_radius=10)
            
            back_text = self.font.render("Back", True, self.COLOR_ACTIVE)
            back_rect_text = back_text.get_rect(center=back_rect.center)
            self.screen.blit(back_text, back_rect_text) 