import pygame

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Création des boutons
        button_width = 200
        button_height = 50
        button_x = width // 2 - button_width // 2
        
        self.play_button = pygame.Rect(
            button_x,
            height // 2 - button_height - 10,
            button_width,
            button_height
        )
        
        self.quit_button = pygame.Rect(
            button_x,
            height // 2 + 10,
            button_width,
            button_height
        )
        
        # Police pour le texte
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        # Fond noir
        screen.fill((0, 0, 0))
        
        # Dessin des boutons
        pygame.draw.rect(screen, (100, 100, 100), self.play_button)
        pygame.draw.rect(screen, (100, 100, 100), self.quit_button)
        
        # Texte des boutons
        play_text = self.font.render("JOUER", True, (255, 255, 255))
        quit_text = self.font.render("QUITTER", True, (255, 255, 255))
        
        # Centrage du texte sur les boutons
        play_rect = play_text.get_rect(center=self.play_button.center)
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        
        # Affichage du texte
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        
        # Titre du jeu
        title_text = self.font.render("BRAWLHALLA CLONE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width//2, self.height//3))
        screen.blit(title_text, title_rect) 