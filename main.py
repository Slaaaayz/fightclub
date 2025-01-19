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
    sound_manager.play_background_music()
    
    running = True
    while running:
        game = Game(screen, sound_manager)  
        action = game.run_menu()
        
        if action == "play":
            game.run()
        elif action == "quit":
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()