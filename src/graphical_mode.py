import pygame
import sys
import os
import random
import time

from src.background_manager import BackgroundManager
from src.plot_manager import PlotManager
from src.stats_manager import StatsManager
from src.climate_manager import ClimateManager
from src.event_manager import EventManager
from src.puzzle_game import PuzzleGame
from src.shooting_game import ShootingGame
from config.plot import PLOT_SEQUENCES
from config.stats import CLIMATE_WEIGHTS, CLIMATE_CHANGE_INTERVAL

# Main graphical game module
class Game:
    def __init__(self, width=1536/1.5, height=1024/1.5, title="Eco Defender"):
        # Initialize Pygame and create resizable window
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        # Initialize mixer for music
        pygame.mixer.init()
        menu_music = os.path.join('assets', 'music', 'menu_theme.ogg')
        pygame.mixer.music.load(menu_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop indefinitely

        # Background manager for dynamic scene backgrounds
        self.bg_manager = BackgroundManager(self.screen, 'menu_bg.png')

        # Plot manager to handle narrative sequences and choices
        self.plot_manager = PlotManager(PLOT_SEQUENCES)

        # Event manager to handle environmental changes
        self.event_manager = EventManager()

        # Climate manager for weather changes
        self.climate_manager = ClimateManager()
        self.last_climate_change = time.time()

        # Puzzle game
        self.puzzle_game = PuzzleGame(self.screen, self.event_manager.stats)
        self.puzzle_triggered = False
        self.puzzle_active = False

        # Shooting game
        self.shooting_game = ShootingGame(self.screen, self.event_manager.stats)
        self.shooting_triggered = False
        self.shooting_active = False

        # Choice and history flags
        self.current_choices = None
        self.choice_rects = []  # clickable areas for choices
        self.reviewing_history = False

        # Text typing effect variables
        self.typing_text = []
        self.current_typing_index = 0
        self.last_typing_time = 0
        self.typing_speed = 50  # milliseconds between words
        self.typing_complete = False

        # Load fonts
        font_path = os.path.join('assets', 'fonts', 'Pixeboy-z8XGD.ttf')
        self.text_font = pygame.font.Font(font_path, 24)
        self.choice_font = pygame.font.Font(font_path, 20)
        self.stat_font = pygame.font.Font(font_path, 18)

    def start_typing_effect(self, lines):
        """Start a new typing effect with the given lines"""
        self.typing_text = []
        self.current_typing_index = 0
        self.typing_complete = False
        self.last_typing_time = pygame.time.get_ticks()
        
        # Split each line into words
        for line in lines:
            words = line.split()
            self.typing_text.append(words)

    def draw_text_box(self, lines):
        # Draw narrative text box at bottom with translucency
        w, h = self.screen.get_size()
        box_h = h // 3
        overlay = pygame.Surface((w, box_h), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 180))  # RGBA with alpha for translucency
        self.screen.blit(overlay, (0, h - box_h))

        # Initialize typing effect if needed
        if not self.typing_text:
            self.start_typing_effect(lines)

        # Update typing effect
        current_time = pygame.time.get_ticks()
        if not self.typing_complete and current_time - self.last_typing_time >= self.typing_speed:
            self.current_typing_index += 1
            self.last_typing_time = current_time

        # Calculate maximum lines that can fit in the box
        line_height = self.text_font.get_height() + 4
        max_lines = box_h // line_height - 1
        max_width = w - 20

        # Process and display typed text
        displayed_lines = []
        for line_words in self.typing_text:
            current_line = ""
            for i, word in enumerate(line_words):
                if i < self.current_typing_index:
                    current_line += word + " "
            
            # Word wrap the current line
            words = current_line.split()
            wrapped_lines = []
            current_wrapped_line = ""
            
            for word in words:
                test_line = current_wrapped_line + " " + word if current_wrapped_line else word
                if self.text_font.size(test_line)[0] <= max_width:
                    current_wrapped_line = test_line
                else:
                    if current_wrapped_line:
                        wrapped_lines.append(current_wrapped_line)
                    current_wrapped_line = word
            if current_wrapped_line:
                wrapped_lines.append(current_wrapped_line)
            
            displayed_lines.extend(wrapped_lines)

        # Check if typing is complete
        total_words = sum(len(line) for line in self.typing_text)
        if self.current_typing_index >= total_words:
            self.typing_complete = True

        # Display the last max_lines of wrapped text
        for i, line in enumerate(displayed_lines[-max_lines:]):
            surf = self.text_font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (10, h - box_h + 10 + i * line_height))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.VIDEORESIZE:
                    # Update screen and background manager on resize
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.bg_manager.screen = self.screen

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE) and not self.reviewing_history:
                        # If typing is not complete, complete it
                        if not self.typing_complete:
                            self.typing_complete = True
                            self.current_typing_index = sum(len(line) for line in self.typing_text)
                        # Otherwise advance narrative if no active choices
                        elif not self.current_choices:
                            choices = self.plot_manager.advance()
                            if choices:
                                self.current_choices = choices
                                self.typing_text = []  # Reset typing effect for next text
                            else:
                                # Clear current text and prepare for next line
                                self.typing_text = []
                                self.current_typing_index = 0
                                self.typing_complete = False
                                self.last_typing_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_r:
                        # Toggle review history view
                        self.reviewing_history = not self.reviewing_history
                    elif self.shooting_game.is_active():
                        # Handle bullet type switching
                        self.shooting_game.handle_key(event.key)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.current_choices:
                        # Handle choices (including ending choices)
                        for idx, rect in enumerate(self.choice_rects):
                            if rect.collidepoint(mx, my):
                                if self.current_choices[idx].get('action') == 'quit':
                                    running = False
                                elif self.current_choices[idx].get('action') == 'menu':
                                    self.__init__()  # Reset game state
                                    return
                                else:
                                    choice_id = self.current_choices[idx].get('id', f'choice_{idx}')
                                    self.event_manager.apply_choice_effect(choice_id)
                                    self.plot_manager.choose(idx)
                                    self.current_choices = None
                                    self.typing_text = []  # Reset typing effect for next text
                                    break
                    elif self.puzzle_game.is_active():
                        # Handle puzzle game clicks
                        if self.puzzle_game.handle_click((mx, my)):
                            self.puzzle_triggered = False
                            # Reset climate change timer to prevent immediate change
                            self.last_climate_change = time.time()
                            # Resume event manager updates
                            self.event_manager.resume_updates()
                            # Restore the last update time to prevent time accumulation
                            self.event_manager.last_update = time.time()
                    elif self.shooting_game.is_active():
                        # Handle shooting game clicks
                        if self.shooting_game.handle_click((mx, my)):
                            self.shooting_triggered = False
                            # Reset climate change timer to prevent immediate change
                            self.last_climate_change = time.time()
                            # Resume event manager updates
                            self.event_manager.resume_updates()
                            # Restore the last update time to prevent time accumulation
                            self.event_manager.last_update = time.time()
                    elif self.current_choices:
                        # Check which choice was clicked
                        for idx, rect in enumerate(self.choice_rects):
                            if rect.collidepoint(mx, my):
                                choice_id = self.current_choices[idx].get('id', f'choice_{idx}')
                                self.event_manager.apply_choice_effect(choice_id)
                                self.plot_manager.choose(idx)
                                self.current_choices = None
                                self.typing_text = []  # Reset typing effect for next text
                                break
                    elif not self.reviewing_history and not self.current_choices:
                        # If typing is not complete, complete it
                        if not self.typing_complete:
                            self.typing_complete = True
                            self.current_typing_index = sum(len(line) for line in self.typing_text)
                        # Otherwise advance narrative
                        else:
                            choices = self.plot_manager.advance()
                            if choices:
                                self.current_choices = choices
                                self.typing_text = []  # Reset typing effect for next text
                            else:
                                # Clear current text and prepare for next line
                                self.typing_text = []
                                self.current_typing_index = 0
                                self.typing_complete = False
                                self.last_typing_time = pygame.time.get_ticks()

            # Check for ending conditions
            current_values = self.event_manager.get_current_values()
            
            # Check for good ending
            if current_values['pollution'] <= 0.15 and current_values['deforestation'] <= 0.15 and self.plot_manager.current_seq != 'good_ending':
                self.plot_manager.current_seq = 'good_ending'
                self.plot_manager.current_index = 0
                self.typing_text = []
                self.current_typing_index = 0
                self.typing_complete = False
                self.last_typing_time = pygame.time.get_ticks()
                # Change background using the background manager
                self.bg_manager.load_background("Completely.png")
            
            # Check for bad ending
            elif current_values['pollution'] >= 1.0 and current_values['deforestation'] >= 1.0 and self.plot_manager.current_seq != 'bad_ending':
                self.plot_manager.current_seq = 'bad_ending'
                self.plot_manager.current_index = 0
                self.typing_text = []
                self.current_typing_index = 0
                self.typing_complete = False
                self.last_typing_time = pygame.time.get_ticks()

            # Update climate and stats only if no mini-game is active and not showing bad ending
            current_time = time.time()
            if not self.puzzle_game.is_active() and not self.shooting_game.is_active():
                if current_time - self.last_climate_change >= CLIMATE_CHANGE_INTERVAL:
                    self.climate_manager.update()
                    self.last_climate_change = current_time

                # Update dynamic stats each frame
                self.event_manager.update()  # Update values based on time
            else:
                # Pause event manager updates during mini-games
                self.event_manager.pause_updates()

            # Check if deforestation exceeds 85% and trigger puzzle
            current_values = self.event_manager.get_current_values()
            pollution_pct = current_values['pollution']
            deforest_pct = current_values['deforestation']
            climate = self.climate_manager.get()

            if deforest_pct > 0.85 and deforest_pct < 0.87 and not self.puzzle_triggered and not self.puzzle_game.is_active():
                self.puzzle_game.start_game()
                self.puzzle_triggered = True
                # Pause event manager updates when puzzle starts
                self.event_manager.pause_updates()
                # Store current climate to prevent changes during puzzle
                self.puzzle_climate = climate
                # Store the current values to prevent changes during puzzle
                self.puzzle_values = {
                    'pollution': pollution_pct,
                    'deforestation': deforest_pct
                }

            # Check if pollution exceeds 85% and trigger shooting game
            if pollution_pct > 0.85 and pollution_pct < 0.87 and not self.shooting_triggered and not self.shooting_game.is_active():
                self.shooting_game.start_game()
                self.shooting_triggered = True
                # Pause event manager updates when shooting game starts
                self.event_manager.pause_updates()
                # Store current climate to prevent changes during shooting game
                self.shooting_climate = climate
                # Store the current values to prevent changes during shooting game
                self.shooting_values = {
                    'pollution': pollution_pct,
                    'deforestation': deforest_pct
                }

            # Update background based on current conditions
            if self.puzzle_game.is_active():
                # Use stored values during puzzle game
                self.bg_manager.update_conditions(self.puzzle_climate, 
                                                self.puzzle_values['pollution'], 
                                                self.puzzle_values['deforestation'])
            elif self.shooting_game.is_active():
                # Use stored values during shooting game
                self.bg_manager.update_conditions(self.shooting_climate, 
                                                self.shooting_values['pollution'], 
                                                self.shooting_values['deforestation'])
            else:
                self.bg_manager.update_conditions(climate, pollution_pct, deforest_pct)

            # Render frame
            self.bg_manager.draw()
            
            # Draw stats using stored values during mini-games
            if self.puzzle_game.is_active():
                self.draw_stats(self.puzzle_values['pollution'], 
                              self.puzzle_values['deforestation'], 
                              self.puzzle_climate)
            elif self.shooting_game.is_active():
                self.draw_stats(self.shooting_values['pollution'], 
                              self.shooting_values['deforestation'], 
                              self.shooting_climate)
            else:
                self.draw_stats(current_values['pollution'], 
                              current_values['deforestation'], 
                              self.climate_manager.get())

            # Update and draw mini-games if active
            if self.puzzle_game.is_active():
                self.puzzle_game.update()
                self.puzzle_game.draw()
            elif self.shooting_game.is_active():
                self.shooting_game.update()
                self.shooting_game.draw()
            else:
                # Display appropriate screen: history, choices, or narrative
                if self.reviewing_history:
                    lines = self.plot_manager.review_history()
                    self.draw_text_box(lines)
                elif self.current_choices:
                    self.draw_choices(self.current_choices)
                else:
                    line = self.plot_manager.get_current_text()
                    self.draw_text_box([line])

            # Control prompts overlay
            self.draw_controls_help()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit(0)

    def draw_stats(self, pollution, deforest, climate):
        # Display dynamic Pollution, Deforestation as percentages, and Climate
        w, _ = self.screen.get_size()
        # Format as 'XX.X%' strings
        texts = [
            f"Pollution: {pollution * 100:.1f}%",
            f"Deforestation: {deforest * 100:.1f}%",
            f"Climate: {climate}"
        ]
        for i, text in enumerate(texts):
            surf = self.stat_font.render(text, True, (255, 255, 255))
            # right-align stats at top-right
            rect = surf.get_rect(topright=(w - 10, 10 + i * (surf.get_height() + 4)))
            self.screen.blit(surf, rect)

    def draw_choices(self, choices):
        # Clickable options with enhanced visual effects
        self.choice_rects.clear()
        w, h = self.screen.get_size()
        box_h = h // 4
        y_start = h - box_h - 40
        mx, my = pygame.mouse.get_pos()
        
        # Draw background for all choices
        choice_height = self.choice_font.get_height() + 20
        total_height = len(choices) * (choice_height + 10)
        choice_bg = pygame.Surface((w - 40, total_height), pygame.SRCALPHA)
        choice_bg.fill((0, 0, 0, 150))  # Semi-transparent black background
        self.screen.blit(choice_bg, (20, y_start - 10))
        
        for idx, choice in enumerate(choices):
            # Calculate position
            x, y = 30, y_start + idx * (choice_height + 10)
            
            # Check if mouse is hovering
            is_hovered = False
            rect = pygame.Rect(x, y, w - 60, choice_height)
            self.choice_rects.append(rect)
            
            if rect.collidepoint(mx, my):
                is_hovered = True
            
            # Draw choice text with hover effect
            text_color = (255, 255, 0) if is_hovered else (200, 200, 0)
            surf = self.choice_font.render(choice['text'], True, text_color)
            # Text position
            text_x = x + 40
            self.screen.blit(surf, (text_x, y + 10))
            
            # Draw arrow indicator
            if is_hovered:
                # Larger, animated arrow pointing right
                arrow_size = 15
                # Position arrow to the left of the text
                tip = (text_x - 25, y + choice_height // 2)  # Arrow pointing right
                base1 = (tip[0] - arrow_size, tip[1] - arrow_size // 2)
                base2 = (tip[0] - arrow_size, tip[1] + arrow_size // 2)
                pygame.draw.polygon(self.screen, (255, 255, 0), [tip, base1, base2])
                
                # Add glow effect
                glow_surface = pygame.Surface((arrow_size * 2, arrow_size * 2), pygame.SRCALPHA)
                pygame.draw.polygon(glow_surface, (255, 255, 0, 50), 
                                  [(arrow_size, arrow_size),  # Pointing right
                                   (0, arrow_size - arrow_size//2),
                                   (0, arrow_size + arrow_size//2)])
                self.screen.blit(glow_surface, (tip[0] - arrow_size, tip[1] - arrow_size))
    
    def draw_controls_help(self):
        # Show help prompts: how to advance and review
        w, h = self.screen.get_size()
        help_text = "Enter/Space/Click: Continue"
        surf = self.choice_font.render(help_text, True, (200, 200, 200))
        rect = surf.get_rect(bottomleft=(10, h - 5))
        self.screen.blit(surf, rect)


def run_graphical():
        game = Game()
        game.run()

