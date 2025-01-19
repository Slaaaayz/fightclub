import pygame
from src.settings import Settings

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.settings = Settings()
        
        # Couleurs
        self.COLOR_INACTIVE = (100, 100, 100)
        self.COLOR_ACTIVE = (255, 255, 255)
        self.COLOR_HOVER = (180, 180, 180)
        self.COLOR_BACKGROUND = (20, 20, 20)
        
        # Police
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 80)
        
        # États
        self.current_tab = "main"
        self.selected_option = 0
        self.hover_option = -1
        
        # Options des menus
        self.main_options = ["Play", "Settings", "Controls", "Quit"]
        self.settings_options = [
            "Music Volume: {}%",
            "SFX Volume: {}%",
            "Fullscreen: {}",
            "Back"
        ]
        self.controls_options = [
            "Player 1 Controls",
            "Player 2 Controls",
            "Back"
        ]
        
        # Rectangles des boutons
        self.button_rects = []
        self.create_buttons()
        
        # Valeurs des paramètres
        self.volume_step = 10

    def create_buttons(self):
        self.button_rects = []
        options = self.get_current_options()
        
        start_y = self.height * 0.4
        for i, option in enumerate(options):
            if self.current_tab == "settings":
                if "Volume" in option:
                    text = option.format(int(self.settings.music_volume * 100) if "Music" in option 
                                      else int(self.settings.sfx_volume * 100))
                elif "Fullscreen" in option:
                    text = option.format("On" if self.settings.fullscreen else "Off")
                else:
                    text = option
            else:
                text = option
                
            text_surface = self.font.render(text, True, self.COLOR_INACTIVE)
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
        if event.type == pygame.MOUSEMOTION:
            # Gestion du hover
            mouse_pos = pygame.mouse.get_pos()
            self.hover_option = -1
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.hover_option = i
                    break
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(event.pos):
                        return self.handle_click(i)
        
        return True

    def handle_click(self, option_index):
        options = self.get_current_options()
        selected_option = options[option_index]
        
        if self.current_tab == "main":
            if selected_option == "Play":
                return False  # Démarrer le jeu
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
            elif "SFX Volume" in selected_option:
                self.settings.sfx_volume = min(1.0, max(0.0, 
                    self.settings.sfx_volume + (0.1 if pygame.mouse.get_pos()[0] > self.width/2 else -0.1)))
            elif "Fullscreen" in selected_option:
                self.settings.fullscreen = not self.settings.fullscreen
                pygame.display.toggle_fullscreen()
            elif selected_option == "Back":
                self.current_tab = "main"
            self.settings.save_settings()
                
        elif self.current_tab == "controls":
            if selected_option == "Back":
                self.current_tab = "main"
                
        self.create_buttons()
        return True

    def draw_controls_info(self):
        info_font = pygame.font.Font(None, 36)
        y_pos = self.height * 0.6
        spacing = 30
        
        controls_p1 = [
            "Player 1 Controls:",
            "Q/D - Move Left/Right",
            "Z - Jump",
            "S - Light Attack",
            "A - Heavy Attack",
            "E - Special Attack"
        ]
        
        controls_p2 = [
            "Player 2 Controls:",
            "←/→ - Move Left/Right",
            "↑ - Jump",
            "Enter - Light Attack",
            "↓ - Heavy Attack",
            "Right Shift - Special Attack"
        ]
        
        # Afficher les contrôles du joueur 1
        x_pos = self.width * 0.25
        for text in controls_p1:
            surface = info_font.render(text, True, self.COLOR_ACTIVE)
            rect = surface.get_rect(center=(x_pos, y_pos))
            self.screen.blit(surface, rect)
            y_pos += spacing
            
        # Afficher les contrôles du joueur 2
        y_pos = self.height * 0.6
        x_pos = self.width * 0.75
        for text in controls_p2:
            surface = info_font.render(text, True, self.COLOR_ACTIVE)
            rect = surface.get_rect(center=(x_pos, y_pos))
            self.screen.blit(surface, rect)
            y_pos += spacing

    def draw(self):
        self.screen.fill(self.COLOR_BACKGROUND)
        
        # Titre
        title_text = "FIGHT CLUB"
        title_surface = self.title_font.render(title_text, True, self.COLOR_ACTIVE)
        title_rect = title_surface.get_rect(center=(self.width/2, self.height * 0.2))
        self.screen.blit(title_surface, title_rect)
        
        # Options
        options = self.get_current_options()
        for i, (option, rect) in enumerate(zip(options, self.button_rects)):
            if self.current_tab == "settings":
                if "Volume" in option:
                    text = option.format(int(self.settings.music_volume * 100) if "Music" in option 
                                      else int(self.settings.sfx_volume * 100))
                elif "Fullscreen" in option:
                    text = option.format("On" if self.settings.fullscreen else "Off")
                else:
                    text = option
            else:
                text = option
                
            color = self.COLOR_HOVER if i == self.hover_option else self.COLOR_INACTIVE
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, rect)
            
            if i == self.hover_option:
                pygame.draw.line(self.screen, color, 
                               (rect.left, rect.bottom + 2),
                               (rect.right, rect.bottom + 2), 2)
        
        # Afficher les informations des contrôles si on est dans l'onglet controls
        if self.current_tab == "controls":
            self.draw_controls_info()
        
        pygame.display.flip() 