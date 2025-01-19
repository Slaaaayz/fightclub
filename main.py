import pygame
from src.game import Game
from src.sound_manager import SoundManager
from src.settings import Settings

def main():
    pygame.init()
    
    # Charger les paramètres avant de créer la fenêtre
    settings = Settings()
    
    # Créer la fenêtre avec le bon mode
    if settings.fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1280, 720))  # Taille par défaut si pas en plein écran
        
    pygame.display.set_caption("Fight Club")
    
    # Créer une seule instance de SoundManager
    sound_manager = SoundManager()
    
    # Appliquer les volumes initiaux
    sound_manager.set_master_volume(settings.master_volume)
    sound_manager.set_music_volume(settings.music_volume)
    sound_manager.set_sfx_volume(settings.sfx_volume)
    
    # Démarrer la musique une seule fois au lancement
    sound_manager.play_background_music()
    
    running = True
    while running:
        game = Game(screen, sound_manager)  
        action = game.run_menu()
        
        if action == "play":
            game.run()
        elif action == "quit":
            # Arrêter la musique seulement quand on quitte complètement le jeu
            sound_manager.stop_background_music()
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()