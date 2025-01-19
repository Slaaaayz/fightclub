import pygame
from src.game import Game
from src.sound_manager import SoundManager
from src.settings import Settings
from src.sprite_manager import SpriteManager

class GameResources:
    def __init__(self):
        # Charger les paramètres avant de créer la fenêtre
        self.settings = Settings()
        
        # Créer une seule instance de SoundManager
        self.sound_manager = SoundManager()
        
        # Appliquer les volumes initiaux
        self.sound_manager.set_master_volume(self.settings.master_volume)
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.set_sfx_volume(self.settings.sfx_volume)
        
        # Charger les sprites une seule fois
        self.knight_sprites = SpriteManager()
        self.rogue_sprites = SpriteManager()
        try:
            self.knight_sprites.load_sprite_sheets("Assets/images/characters/Knight")
            self.rogue_sprites.load_sprite_sheets("Assets/images/characters/Rogue")
        except Exception as e:
            print(f"Erreur lors du chargement des sprites: {e}")

def main():
    pygame.init()
    
    # Créer la fenêtre AVANT de créer les ressources
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fight Club")
    
    # Créer une seule instance des ressources APRÈS avoir créé la fenêtre
    resources = GameResources()
    
    # Appliquer le mode plein écran si nécessaire
    if resources.settings.fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # Démarrer la musique une seule fois au lancement
    resources.sound_manager.play_background_music()
    
    running = True
    while running:
        game = Game(screen, resources)
        action = game.run_menu()
        
        if action == "play":
            game.run()
        elif action == "quit":
            resources.sound_manager.stop_background_music()
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()