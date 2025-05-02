import pygame
import os

class BackgroundManager:
    """
    Handles loading, scaling, and switching background images for different game states.
    """
    def __init__(self, screen, default_bg_path, asset_folder="assets/images"):
        self.screen = screen
        self.asset_folder = asset_folder
        self.current_bg = None
        self.load_background(default_bg_path)
        self.current_climate = None
        self.current_pollution = 0
        self.current_deforestation = 0

    def load_background(self, filename):
        """
        Load a new background image by filename (relative to asset_folder).
        """
        path = os.path.join(self.asset_folder, filename)
        try:
            raw = pygame.image.load(path).convert()
            self.current_bg = raw
        except Exception as e:
            print(f"Error loading background: {e}")  # Debug print
            # Fallback to default background
            default_path = os.path.join(self.asset_folder, "menu_bg.png")
            self.current_bg = pygame.image.load(default_path).convert()

    def update_conditions(self, climate, pollution, deforestation):
        """
        Update environmental conditions and change background accordingly.
        """
        # Only update if conditions have changed
        if (climate == self.current_climate and 
            pollution == self.current_pollution and 
            deforestation == self.current_deforestation):
            return

        self.current_climate = climate
        self.current_pollution = pollution
        self.current_deforestation = deforestation

        # Determine which background to show based on conditions
        if climate == "Rainy":
            self.load_background("rainy.png")
        elif climate == "Stormy":
            self.load_background("stormy.png")
        elif climate == "Sunny":
            if pollution == 1 and deforestation == 1:
                self.load_background("sandstorm.png")
            elif pollution > 0.8:
                self.load_background("over_polluted.png")
            elif pollution > 0.5:
                self.load_background("slighter_polluted.png")
            elif deforestation > 0.8:
                self.load_background("Complete_deforestation.png")
            elif deforestation > 0.6:
                self.load_background("deforestation.png")
            elif deforestation > 0.3:
                self.load_background("slight_deforestation.png.")
            elif 0.16 < deforestation < 0.3 and 0.16 < pollution < 0.3:
                self.load_background("menu_bg.png")

            # else:
            #     self.load_background("menu_bg.png")  # Default sunny background
        # else:
        #     self.load_background("menu_bg.png")  # Default background

    def draw(self):
        """
        Scale the current background to fit the screen (letterboxing with black)
        and draw it.
        """
        if self.current_bg is None:
            return
        screen_w, screen_h = self.screen.get_size()
        orig_w, orig_h = self.current_bg.get_size()
        scale = min(screen_w / orig_w, screen_h / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        scaled = pygame.transform.scale(self.current_bg, (new_w, new_h))
        x = (screen_w - new_w) // 2
        y = (screen_h - new_h) // 2
        # Fill letterbox
        self.screen.fill((0, 0, 0))
        # Blit background
        self.screen.blit(scaled, (x, y))