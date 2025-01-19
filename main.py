import pygame
from src.game import Game
from src.sound_manager import SoundManager
from src.settings import Settings
from src.sprite_manager import SpriteManager

class GameResources:
    def __init__(self):
        self.settings = Settings()
        
        self.sound_manager = SoundManager()
        
        self.sound_manager.set_master_volume(self.settings.master_volume)
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.set_sfx_volume(self.settings.sfx_volume)
        
        self.knight_sprites = SpriteManager()
        self.rogue_sprites = SpriteManager()
        try:
            self.knight_sprites.load_sprite_sheets("Assets/images/characters/Knight")
            self.rogue_sprites.load_sprite_sheets("Assets/images/characters/Rogue")
        except Exception as e:
            print(f"Erreur lors du chargement des sprites: {e}")

def main():
    pygame.init()
    
    # Obtenir la résolution native de l'écran
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    
    # Créer la fenêtre en plein écran avec la résolution native
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Fight Club")
    
    resources = GameResources()
    
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