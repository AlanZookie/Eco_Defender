import pygame
import sys

from src.start_menu import show_start_menu
from src.graphical_mode import run_graphical
# from text_mode import run_text


def main():
    # Initialize Pygame for menu display
    pygame.init()
    screen = pygame.display.set_mode((1536/1.5, 1024/1.5))
    pygame.display.set_caption("Eco Defender Launcher")
    clock = pygame.time.Clock()

    # Show start menu and get user choice
    choice = show_start_menu(screen, clock)
    pygame.quit()

    if choice == "start":
        run_graphical()
    else:
        sys.exit(0)



if __name__ == "__main__":
    main()