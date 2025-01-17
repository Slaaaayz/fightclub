from src.game import main_menu, settings_menu, Game

def main():
    while True:
        action = main_menu()

        if action == "play":
            game = Game()
            game.run()
        elif action == "settings":
            settings_menu()

if __name__ == "__main__":
    main()
