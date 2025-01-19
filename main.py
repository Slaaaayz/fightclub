from src.game import Game
import pygame

def main():
    pygame.init()
    # Créer une seule fenêtre qui sera partagée
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    game = Game(screen)  # Passer l'écran au jeu
    
    while True:
        # Afficher le menu et obtenir l'action
        action = game.run_menu()
        
        if action == "quit":
            break
        elif action == "play":
            game.run()  # Lancer le jeu
            pygame.time.wait(500)  # Petit délai avant de revenir au menu

    pygame.quit()

if __name__ == "__main__":
    main()
