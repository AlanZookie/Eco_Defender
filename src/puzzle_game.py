import pygame
import random
import time
import os
from src.stats_manager import StatsManager

class PuzzleGame:
    def __init__(self, screen, stats_manager):
        self.screen = screen
        self.stats_manager = stats_manager
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.active = False
        self.puzzle_solved = False
        self.time_limit = 1  # seconds
        self.start_time = 0
        self.remaining_time = self.time_limit
        self.show_continue = False
        self.continue_button = None
        
        # Puzzle elements
        self.grid_size = 3  # 3x3 grid
        self.tile_size = min(self.width, self.height) // (self.grid_size + 2)
        self.grid_offset_x = (self.width - self.grid_size * self.tile_size) // 2
        self.grid_offset_y = (self.height - self.grid_size * self.tile_size) // 2
        
        # Load and prepare tree image
        tree_img_path = os.path.join('assets', 'images', 'tree_puzzle.png')
        if os.path.exists(tree_img_path):
            self.original_image = pygame.image.load(tree_img_path)
            self.original_image = pygame.transform.scale(self.original_image, 
                                                      (self.tile_size * self.grid_size, 
                                                       self.tile_size * self.grid_size))
        else:
            # Create a more vivid and detailed tree image
            self.original_image = pygame.Surface((self.tile_size * self.grid_size, 
                                                self.tile_size * self.grid_size))
            self.original_image.fill((135, 206, 235))  # Sky blue background
            
            # Draw detailed tree trunk
            trunk_width = self.tile_size * self.grid_size // 4
            trunk_height = self.tile_size * self.grid_size // 2
            trunk_x = self.tile_size * self.grid_size // 2 - trunk_width // 2
            trunk_y = self.tile_size * self.grid_size - trunk_height
            
            # Draw main trunk
            pygame.draw.rect(self.original_image, (101, 67, 33),  # Dark brown
                           (trunk_x, trunk_y, trunk_width, trunk_height))
            
            # Draw tree bark texture
            for i in range(5):
                bark_x = trunk_x + i * trunk_width // 4
                pygame.draw.line(self.original_image, (139, 69, 19),  # Lighter brown
                               (bark_x, trunk_y),
                               (bark_x, trunk_y + trunk_height), 2)
            
            # Draw detailed leaves
            leaf_colors = [(34, 139, 34), (0, 100, 0), (0, 128, 0)]  # Different shades of green
            
            # Draw three layers of leaves
            for layer in range(3):
                leaf_size = self.tile_size * self.grid_size // (2 + layer)
                leaf_y = trunk_y - (layer * leaf_size // 2)
                
                # Draw left side leaves
                for i in range(3):
                    leaf_x = trunk_x - leaf_size // 2 + i * leaf_size // 3
                    pygame.draw.circle(self.original_image, leaf_colors[layer],
                                     (leaf_x, leaf_y), leaf_size // 3)
                
                # Draw right side leaves
                for i in range(3):
                    leaf_x = trunk_x + trunk_width + leaf_size // 2 - i * leaf_size // 3
                    pygame.draw.circle(self.original_image, leaf_colors[layer],
                                     (leaf_x, leaf_y), leaf_size // 3)
                
                # Draw center leaves
                for i in range(2):
                    leaf_x = trunk_x + trunk_width // 2 + (i * 2 - 1) * leaf_size // 4
                    pygame.draw.circle(self.original_image, leaf_colors[layer],
                                     (leaf_x, leaf_y), leaf_size // 3)
            
            # Draw some apples
            apple_positions = [
                (trunk_x + trunk_width // 4, trunk_y + trunk_height // 4),
                (trunk_x + trunk_width * 3 // 4, trunk_y + trunk_height // 3),
                (trunk_x + trunk_width // 2, trunk_y + trunk_height // 2)
            ]
            for pos in apple_positions:
                pygame.draw.circle(self.original_image, (255, 0, 0), pos, 8)  # Red apple
                pygame.draw.circle(self.original_image, (0, 0, 0), pos, 8, 1)  # Apple outline
        
        # Initialize puzzle
        self.tiles = []
        self.empty_pos = None
        self.moves = 0
        
        # Instructions
        self.instructions = [
            "Deforestation has reached critical levels!",
            "Slide the tiles to restore the tree image.",
            "Click on adjacent tiles to move them.",
            "Complete the puzzle within the time limit.",
            "Success will reduce deforestation to 35%."
        ]

    def start_game(self):
        """Start the puzzle game"""
        self.active = True
        self.puzzle_solved = False
        self.show_continue = False
        self.start_time = time.time()
        self.remaining_time = self.time_limit
        self.moves = 0
        self.generate_puzzle()

    def end_game(self):
        """End the puzzle game"""
        self.active = False
        self.puzzle_solved = False
        self.show_continue = False
        self.remaining_time = 0

    def generate_puzzle(self):
        """Generate a new sliding puzzle"""
        # Create tiles from the original image
        self.tiles = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                tile = self.original_image.subsurface(
                    x * self.tile_size, y * self.tile_size,
                    self.tile_size, self.tile_size
                )
                self.tiles.append(tile)
        
        # Set empty position (bottom right)
        self.empty_pos = (self.grid_size - 1, self.grid_size - 1)
        
        # Shuffle the puzzle
        for _ in range(100):  # Perform 100 random moves
            possible_moves = self.get_possible_moves()
            if possible_moves:
                self.swap_tiles(random.choice(possible_moves))

    def get_possible_moves(self):
        """Get list of possible moves from current position"""
        moves = []
        x, y = self.empty_pos
        
        # Check adjacent positions
        if x > 0:
            moves.append((x - 1, y))  # Left
        if x < self.grid_size - 1:
            moves.append((x + 1, y))  # Right
        if y > 0:
            moves.append((x, y - 1))  # Up
        if y < self.grid_size - 1:
            moves.append((x, y + 1))  # Down
            
        return moves

    def swap_tiles(self, pos):
        """Swap a tile with the empty position"""
        x, y = pos
        empty_x, empty_y = self.empty_pos
        
        # Calculate indices
        tile_idx = y * self.grid_size + x
        empty_idx = empty_y * self.grid_size + empty_x
        
        # Swap tiles
        self.tiles[tile_idx], self.tiles[empty_idx] = self.tiles[empty_idx], self.tiles[tile_idx]
        self.empty_pos = pos
        self.moves += 1

    def check_solution(self):
        """Check if the puzzle is solved"""
        for i, tile in enumerate(self.tiles):
            x = i % self.grid_size
            y = i // self.grid_size
            original_tile = self.original_image.subsurface(
                x * self.tile_size, y * self.tile_size,
                self.tile_size, self.tile_size
            )
            if tile != original_tile:
                return False
        return True

    def handle_click(self, pos):
        """Handle mouse click events"""
        if not self.active:
            return False
            
        x, y = pos
        
        # Check if clicking continue button
        if self.show_continue and self.continue_button and self.continue_button.collidepoint(x, y):
            self.end_game()
            return True
            
        if self.puzzle_solved or self.remaining_time <= 0:
            return False
            
        # Convert screen coordinates to grid coordinates
        grid_x = (x - self.grid_offset_x) // self.tile_size
        grid_y = (y - self.grid_offset_y) // self.tile_size
        
        # Check if click is within grid
        if (0 <= grid_x < self.grid_size and 
            0 <= grid_y < self.grid_size):
            clicked_pos = (grid_x, grid_y)
            
            # Check if clicked position is adjacent to empty position
            if clicked_pos in self.get_possible_moves():
                self.swap_tiles(clicked_pos)
                
                # Check if puzzle is solved
                if self.check_solution():
                    self.puzzle_solved = True
                    self.stats_manager.set('deforestation', 0.35)  # Set deforestation to 35%
                    self.show_continue = True
                    return True
                
        return False

    def update(self):
        """Update game state"""
        if not self.active:
            return
            
        # Update remaining time
        self.remaining_time = max(0, self.time_limit - (time.time() - self.start_time))
        
        # Check if time ran out
        if self.remaining_time <= 0 and not self.puzzle_solved:
            self.show_continue = True
            # Increase deforestation by 0.05 when time runs out
            # current_deforestation = self.stats_manager.get('deforestation')
            self.stats_manager.set('deforestation', 0.88)

    def draw(self):
        """Draw the puzzle game"""
        if not self.active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw instructions
        for i, text in enumerate(self.instructions):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i * 40))
        
        # Draw timer and moves
        timer_text = f"Time: {int(self.remaining_time)}s  Moves: {self.moves}"
        timer_surface = self.font.render(timer_text, True, (255, 255, 255))
        self.screen.blit(timer_surface, (self.width - 300, 20))
        
        # Draw grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(
                    self.grid_offset_x + x * self.tile_size,
                    self.grid_offset_y + y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                
                # Draw tile or empty space
                if (x, y) != self.empty_pos:
                    tile_idx = y * self.grid_size + x
                    self.screen.blit(self.tiles[tile_idx], rect)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
        
        # Draw success/failure message
        if self.puzzle_solved:
            success_text = f"Success! Deforestation reduced to 35% (Moves: {self.moves})"
            text_surface = self.font.render(success_text, True, (0, 255, 0))
            self.screen.blit(text_surface, 
                           (self.width // 2 - text_surface.get_width() // 2,
                            self.height - 100))
        elif self.remaining_time <= 0:
            failure_text = "Time's up!"
            text_surface = self.font.render(failure_text, True, (255, 0, 0))
            self.screen.blit(text_surface,
                           (self.width // 2 - text_surface.get_width() // 2,
                            self.height - 100))
        
        # Draw continue button if game is over
        if self.show_continue:
            button_text = "Continue"
            text_surface = self.font.render(button_text, True, (255, 255, 255))
            button_width = text_surface.get_width() + 40
            button_height = text_surface.get_height() + 20
            button_x = self.width // 2 - button_width // 2
            button_y = self.height - 50
            
            # Create button rectangle
            self.continue_button = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Draw button background
            pygame.draw.rect(self.screen, (50, 50, 50), self.continue_button)
            pygame.draw.rect(self.screen, (100, 100, 100), self.continue_button, 2)
            
            # Draw button text
            text_rect = text_surface.get_rect(center=self.continue_button.center)
            self.screen.blit(text_surface, text_rect)

    def is_active(self):
        """Check if the puzzle game is active"""
        return self.active

    def is_solved(self):
        """Check if the puzzle was solved"""
        return self.puzzle_solved 