import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Couleurs
        self.COLOR_INACTIVE = (100, 100, 100)
        self.COLOR_ACTIVE = (255, 255, 255)
        self.COLOR_HOVER = (180, 180, 180)
        
        # Police
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 80)
        
        # États
        self.current_tab = "main"  # main, settings, controls
        self.selected_option = 0
        self.hover_option = -1
        
        # Options du menu principal
        self.main_options = ["Play", "Settings", "Controls", "Quit"]
        self.settings_options = ["Volume", "Fullscreen", "Back"]
        self.controls_options = ["Player 1", "Player 2", "Back"]
        
        # Rectangles des boutons (seront initialisés dans create_buttons)
        self.button_rects = []
        self.create_buttons()

    def create_buttons(self):
        self.button_rects = []
        options = self.get_current_options()
        
        start_y = self.height * 0.4
        for i, option in enumerate(options):
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
                return False  # Quitter le menu et commencer le jeu
            elif selected_option == "Settings":
                self.current_tab = "settings"
            elif selected_option == "Controls":
                self.current_tab = "controls"
            elif selected_option == "Quit":
                pygame.quit()
                exit()
        
        elif self.current_tab in ["settings", "controls"]:
            if selected_option == "Back":
                self.current_tab = "main"
                
        self.create_buttons()
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fond noir
        
        # Titre
        title_text = "FIGHT CLUB"
        title_surface = self.title_font.render(title_text, True, self.COLOR_ACTIVE)
        title_rect = title_surface.get_rect(center=(self.width/2, self.height * 0.2))
        self.screen.blit(title_surface, title_rect)
        
        # Options
        options = self.get_current_options()
        for i, (option, rect) in enumerate(zip(options, self.button_rects)):
            color = self.COLOR_HOVER if i == self.hover_option else self.COLOR_INACTIVE
            text_surface = self.font.render(option, True, color)
            self.screen.blit(text_surface, rect)
            
            # Effet de soulignement au hover
            if i == self.hover_option:
                pygame.draw.line(self.screen, color, 
                               (rect.left, rect.bottom + 2),
                               (rect.right, rect.bottom + 2), 2)
        
        pygame.display.flip() 