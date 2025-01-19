from src.game import main_menu, settings_menu, Game
import pygame

def main():
    while True:
        action = main_menu()

        if action == "play":
            game = Game()
            game.run()
            # Après la fin de la partie, retour automatique au menu principal
            pygame.time.wait(500)  # Petit délai pour éviter les clics accidentels
        elif action == "settings":
            settings_menu()
        elif action == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
