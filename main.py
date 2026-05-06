import sys

from logic.controller import Controller

def main():
    
    controller = Controller()
    controller.initialize_game_from_menu()
    controller.start_game()

    sys.exit()


if __name__ == "__main__":
    main()
