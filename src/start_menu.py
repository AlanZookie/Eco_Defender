import pygame
import os
from src.background_manager import BackgroundManager


def show_start_menu(screen, clock):
    # Base resolution for reference
    BASE_WIDTH, BASE_HEIGHT = 1536, 1024

    # Initialize mixer for music
    pygame.mixer.init()
    menu_music = os.path.join('assets', 'music', 'menu_theme.ogg')
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop indefinitely

    # Load pixel-style background image
    bg_manager = BackgroundManager(screen, 'menu_bg.png')

    # Load 8-bit pixel fonts
    font_path = os.path.join('assets', 'fonts', 'Pixeboy-z8XGD.ttf')
    title_font = pygame.font.Font(font_path, 64)
    option_font = pygame.font.Font(font_path, 32)

    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return "quit"
                elif event.type == pygame.VIDEORESIZE:
                    # Adjust window size
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return "start"

            bg_manager.draw()

            # Dynamic font sizes
            w, h = screen.get_size()
            title_size = max(int(200 * (h / BASE_HEIGHT)), 16)
            option_size = max(int(32 * (h / BASE_HEIGHT)), 12)
            title_font = pygame.font.Font(font_path, title_size)
            option_font = pygame.font.Font(font_path, option_size)

            # Render title
            title_surf = title_font.render("Eco Defender", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(w // 2, int(h * 0.2)))
            screen.blit(title_surf, title_rect)

            # Render "Press Enter to Start"
            prompt = "Press Enter to Start"
            prompt_surf = option_font.render(prompt, True, (255, 255, 0))
            prompt_rect = prompt_surf.get_rect(center=(w // 2, int(h * 0.6)))
            screen.blit(prompt_surf, prompt_rect)

            # Update display
            pygame.display.flip()
            clock.tick(60)
