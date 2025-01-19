import pygame
from src.game import Game
from src.sound_manager import SoundManager

def main():
    pygame.init()
    # Démarrer en plein écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fight Club")
    
    # Créer une seule instance de SoundManager
    sound_manager = SoundManager()
    # Démarrer la musique une seule fois au lancement
    sound_manager.play_background_music()
    
    running = True
    while running:
        game = Game(screen, sound_manager)  
        action = game.run_menu()
        
        if action == "play":
            game.run()
        elif action == "quit":
            # Arrêter la musique avant de quitter
            sound_manager.stop_background_music()
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()