import pygame
import random
import time
import math

class ShootingGame:
    def __init__(self, screen, stats_manager):
        self.screen = screen
        self.stats_manager = stats_manager
        self.active = False
        self.show_continue = False
        self.continue_button = None
        self.time_limit = 30  # 30 seconds to survive
        self.start_time = 0
        self.lives = 3
        self.score = 0
        self.show_instructions = True  # New flag for instructions
        self.instructions_time = 0  # Track how long instructions have been shown
        
        # Airplane properties
        self.airplane_pos = [0, 0]
        self.airplane_speed = 15  # Reduced from 25 to 15 for smoother movement
        self.airplane_size = 80  # Increased from 40 to 80
        self.airplane_angle = 0
        self.current_bullet_type = 1  # 1-4 for different bullet types
        
        # Bullet properties
        self.bullets = []
        self.bullet_speed = 15  # Reduced from 20 to 15
        self.bullet_size = 10  # Increased from 5 to 10
        self.last_shot = 0
        self.shot_cooldown = 100  # Reduced from 200 to 100 for faster shooting
        self.bullet_colors = {
            1: (255, 0, 0),    # Red for waste water
            2: (0, 255, 0),    # Green for gas
            3: (255, 255, 0),  # Yellow for mouse
            4: (0, 0, 255)     # Blue for garbage
        }
        
        # Enemy properties
        self.enemies = []
        self.enemy_spawn_rate = 1000  # Increased from 800 to 1000 for fewer enemies
        self.last_enemy_spawn = 0
        self.enemy_speed = 3  # Reduced from 7 to 3
        self.enemy_size = 60  # Increased from 30 to 60
        self.enemy_types = {
            1: {'color': (255, 0, 0), 'name': 'Waste Water'},    # Red
            2: {'color': (0, 255, 0), 'name': 'Gas'},            # Green
            3: {'color': (255, 255, 0), 'name': 'Mouse'},        # Yellow
            4: {'color': (0, 0, 255), 'name': 'Garbage'}         # Blue
        }
        
        # Load images
        self.load_images()
        
    def load_images(self):
        """Load and scale game images"""
        # Load airplane image
        airplane_img = pygame.image.load('assets/shooting/plane.png').convert_alpha()
        self.airplane_img = pygame.transform.scale(airplane_img, (self.airplane_size, self.airplane_size))
        
        # Load enemy images
        self.enemy_imgs = {}
        enemy_types = {
            1: 'waste_water.png',
            2: 'gas.png',
            3: 'mouse.png',
            4: 'garbage.png'
        }
        
        for enemy_type, filename in enemy_types.items():
            enemy_img = pygame.image.load(f'assets/shooting/{filename}').convert_alpha()
            self.enemy_imgs[enemy_type] = pygame.transform.scale(enemy_img, (self.enemy_size, self.enemy_size))
        
        # Create bullet images for each type
        self.bullet_imgs = {}
        for bullet_type, color in self.bullet_colors.items():
            bullet_img = pygame.Surface((self.bullet_size, self.bullet_size), pygame.SRCALPHA)
            pygame.draw.circle(bullet_img, color, 
                             (self.bullet_size//2, self.bullet_size//2), 
                             self.bullet_size//2)
            self.bullet_imgs[bullet_type] = bullet_img
    
    def start_game(self):
        """Start the shooting game"""
        self.active = True
        self.show_continue = False
        self.show_instructions = True
        self.instructions_time = time.time()
        self.start_time = time.time()
        self.lives = 3
        self.score = 0
        self.bullets = []
        self.enemies = []
        self.current_bullet_type = 1
        
        # Initialize airplane position at the bottom center
        screen_width, screen_height = self.screen.get_size()
        self.airplane_pos = [screen_width // 2, screen_height - 100]
        self.airplane_angle = 0
    
    def is_active(self):
        """Check if the game is currently active"""
        return self.active
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if not self.active:
            return False
            
        if self.show_instructions:
            self.show_instructions = False
            return False
            
        if self.show_continue:
            # Check if continue button was clicked
            if self.continue_button and self.continue_button.collidepoint(pos):
                self.active = False
                return True
            return False
            
        return False
    
    def handle_key(self, key):
        """Handle keyboard input"""
        if not self.active:
            return
            
        # Switch bullet type with number keys 1-4
        if pygame.K_1 <= key <= pygame.K_4:
            self.current_bullet_type = key - pygame.K_1 + 1
    
    def shoot_bullet(self):
        """Create a new bullet"""
        bullet_pos = [self.airplane_pos[0], self.airplane_pos[1]]
        # Bullets always shoot upward
        bullet_angle = -math.pi/2  # -90 degrees (upward)
        self.bullets.append({
            'pos': bullet_pos,
            'angle': bullet_angle,
            'type': self.current_bullet_type
        })
    
    def spawn_enemy(self):
        """Spawn a new enemy"""
        screen_width = self.screen.get_size()[0]
        x = random.randint(0, screen_width - self.enemy_size)
        y = -self.enemy_size
        enemy_type = random.randint(1, 4)  # Random enemy type
        self.enemies.append({
            'pos': [x, y],
            'speed': self.enemy_speed,
            'type': enemy_type
        })
    
    def update(self):
        """Update game state"""
        if not self.active:
            return
            
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Check if time is up
        if elapsed_time >= self.time_limit:
            self.show_continue = True
            # Check if score reached 100
            if self.score >= 100:
                self.stats_manager.set('pollution', 0.35)  # Success: reduce pollution to 35%
            else:
                self.stats_manager.set('pollution', 0.88)  # Failure: set pollution to 88%
            return
            
        # Spawn enemies
        current_ticks = pygame.time.get_ticks()
        if current_ticks - self.last_enemy_spawn >= self.enemy_spawn_rate:
            self.spawn_enemy()
            self.last_enemy_spawn = current_ticks
        
        # Auto-shoot bullets
        if current_ticks - self.last_shot >= self.shot_cooldown:
            self.shoot_bullet()
            self.last_shot = current_ticks
        
        # Update airplane position based on mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Set airplane position directly to mouse position, offset by half the size
        self.airplane_pos[0] = mouse_x - self.airplane_size // 2
        self.airplane_pos[1] = mouse_y - self.airplane_size // 2
        
        # Keep airplane on screen
        screen_width, screen_height = self.screen.get_size()
        self.airplane_pos[0] = max(0, min(screen_width - self.airplane_size, self.airplane_pos[0]))
        self.airplane_pos[1] = max(0, min(screen_height - self.airplane_size, self.airplane_pos[1]))
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet['pos'][0] += math.cos(bullet['angle']) * self.bullet_speed
            bullet['pos'][1] += math.sin(bullet['angle']) * self.bullet_speed
            
            # Remove bullets that are off screen
            if (bullet['pos'][0] < 0 or bullet['pos'][0] > screen_width or
                bullet['pos'][1] < 0 or bullet['pos'][1] > screen_height):
                self.bullets.remove(bullet)
        
        # Update enemies
        enemies_to_remove = []
        bullets_to_remove = []
        
        for enemy in self.enemies[:]:
            enemy['pos'][1] += enemy['speed']
            
            # Check collision with airplane
            airplane_rect = pygame.Rect(self.airplane_pos[0], self.airplane_pos[1],
                                      self.airplane_size, self.airplane_size)
            enemy_rect = pygame.Rect(enemy['pos'][0], enemy['pos'][1],
                                   self.enemy_size, self.enemy_size)
            
            if airplane_rect.colliderect(enemy_rect):
                self.lives -= 1
                enemies_to_remove.append(enemy)
                if self.lives <= 0:
                    self.show_continue = True
                    self.stats_manager.set('pollution', 0.88)  # Failure: set pollution to 88%
                    return
            
            # Check collision with bullets
            for bullet in self.bullets[:]:
                if bullet in bullets_to_remove:
                    continue
                    
                bullet_rect = pygame.Rect(bullet['pos'][0], bullet['pos'][1],
                                        self.bullet_size, self.bullet_size)
                if bullet_rect.colliderect(enemy_rect):
                    # Only destroy if bullet type matches enemy type
                    if bullet['type'] == enemy['type']:
                        bullets_to_remove.append(bullet)
                        enemies_to_remove.append(enemy)
                        self.score += 10
                    break
            
            # Remove enemies that are off screen
            if enemy['pos'][1] > screen_height:
                enemies_to_remove.append(enemy)
        
        # Remove enemies and bullets that were marked for removal
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
                
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
    
    def draw(self):
        """Draw the game"""
        if not self.active:
            return
            
        # Draw background
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        if self.show_instructions:
            # Draw instructions background
            instructions_bg = pygame.Surface((600, 400), pygame.SRCALPHA)
            instructions_bg.fill((0, 0, 0, 200))
            screen_width, screen_height = self.screen.get_size()
            instructions_bg_rect = instructions_bg.get_rect(center=(screen_width//2, screen_height//2))
            self.screen.blit(instructions_bg, instructions_bg_rect)
            
            # Draw instructions title
            font = pygame.font.Font(None, 48)
            title = font.render("How to Play", True, (255, 255, 255))
            title_rect = title.get_rect(centerx=instructions_bg_rect.centerx, 
                                      top=instructions_bg_rect.top + 20)
            self.screen.blit(title, title_rect)
            
            # Draw bullet type instructions
            font = pygame.font.Font(None, 36)
            y_offset = title_rect.bottom + 20
            
            # Draw bullet type headers
            bullet_header = font.render("Bullet Types (Press 1-4 to switch):", True, (255, 255, 255))
            self.screen.blit(bullet_header, (instructions_bg_rect.left + 20, y_offset))
            y_offset += 40
            
            # Draw each bullet type instruction with preview
            for bullet_type, color in self.bullet_colors.items():
                # Draw bullet preview
                bullet_preview = self.bullet_imgs[bullet_type]
                self.screen.blit(bullet_preview, (instructions_bg_rect.left + 20, y_offset))
                
                # Draw bullet text
                bullet_text = font.render(f"{bullet_type}. {self.enemy_types[bullet_type]['name']}", 
                                        True, color)
                self.screen.blit(bullet_text, (instructions_bg_rect.left + 50, y_offset))
                y_offset += 30
            
            # Draw enemy type instructions
            y_offset += 20
            enemy_header = font.render("Enemy Types:", True, (255, 255, 255))
            self.screen.blit(enemy_header, (instructions_bg_rect.left + 20, y_offset))
            y_offset += 40
            
            # Draw each enemy type instruction with preview
            for enemy_type, data in self.enemy_types.items():
                # Draw enemy preview
                enemy_preview = self.enemy_imgs[enemy_type]
                self.screen.blit(enemy_preview, (instructions_bg_rect.left + 20, y_offset))
                
                # Draw enemy text
                enemy_text = font.render(f"{enemy_type}. {data['name']} - Match with same number bullet", 
                                       True, data['color'])
                self.screen.blit(enemy_text, (instructions_bg_rect.left + 50, y_offset))
                y_offset += 30
            
            # Draw continue prompt
            y_offset += 40
            continue_text = font.render("Click to start the game", True, (255, 255, 255))
            continue_rect = continue_text.get_rect(centerx=instructions_bg_rect.centerx, 
                                                top=y_offset)
            self.screen.blit(continue_text, continue_rect)
            
            return
        
        # Draw game title
        font = pygame.font.Font(None, 36)
        title = font.render("Airplane Defense", True, (255, 255, 255))
        self.screen.blit(title, (10, 10))
        
        # Draw timer
        current_time = time.time()
        remaining_time = max(0, self.time_limit - (current_time - self.start_time))
        timer_text = font.render(f"Time: {int(remaining_time)}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 50))
        
        # Draw lives
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 90))
        
        # Draw score
        score_text = font.render(f"Score: {self.score}/100", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 130))
        
        # Draw current bullet type
        bullet_type_text = font.render(f"Bullet Type: {self.current_bullet_type} ({self.enemy_types[self.current_bullet_type]['name']})", 
                                     True, self.bullet_colors[self.current_bullet_type])
        self.screen.blit(bullet_type_text, (10, 170))
        
        # Draw airplane (always pointing upward)
        self.screen.blit(self.airplane_img, self.airplane_pos)
        
        # Draw bullets
        for bullet in self.bullets:
            self.screen.blit(self.bullet_imgs[bullet['type']], bullet['pos'])
        
        # Draw enemies
        for enemy in self.enemies:
            self.screen.blit(self.enemy_imgs[enemy['type']], enemy['pos'])
        
        # Draw continue button if game is over
        if self.show_continue:
            screen_width, screen_height = self.screen.get_size()
            button_width, button_height = 200, 50
            button_x = (screen_width - button_width) // 2
            button_y = screen_height - 100
            
            # Draw button background
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (50, 50, 50), button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
            
            # Draw button text
            button_font = pygame.font.Font(None, 32)
            button_text = button_font.render("Continue", True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
            
            self.continue_button = button_rect
            
            # Draw game over message
            if self.lives <= 0:
                message = "Game Over! Pollution increased to 88%"
            elif self.score >= 100:
                message = "You survived! Pollution reduced to 35%"
            else:
                message = "Time's up! Pollution increased to 88%"
            message_text = font.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(screen_width//2, screen_height//2))
            self.screen.blit(message_text, message_rect) 