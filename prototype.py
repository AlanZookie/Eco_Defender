import pygame, sys, random, math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
# Colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY   = (200, 200, 200)

# Setup the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eco Defender Prototype")
clock = pygame.time.Clock()

# Resources and City Health
money = 100.0
power = 300.0
city_health = 10

# Tower costs
COST_TREE = 5
COST_SOLAR = 10
COST_RECYCLE = 50

# Global variable to track the currently selected tower type.
selected_tower_type = "Tree"  # Default selection

# --- Tower Class ---
class Tower:
    def __init__(self, pos, tower_type):
        self.pos = pos
        self.type = tower_type
        # Common properties for drawing and collision
        self.radius = 20
        # Define specific properties based on tower type
        if self.type == "Tree":
            self.range = 100
            self.damage = 2
            self.color = GREEN
            self.cooldown = 0  # milliseconds
        elif self.type == "Solar":
            self.color = YELLOW
        elif self.type == "Recycle":
            self.color = BLUE

    def update(self, dt):
        # Only tree towers have a shooting cooldown
        if self.type == "Tree" and self.cooldown > 0:
            self.cooldown -= dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
        font = pygame.font.SysFont(None, 24)
        # Display first letter as identifier
        label = self.type[0]
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=self.pos)
        surface.blit(text, text_rect)

    def can_shoot(self):
        return self.type == "Tree" and self.cooldown <= 0

    def shoot(self):
        self.cooldown = 1000  # Tree tower: 1-sec cooldown

# --- Enemy Class ---
class Enemy:
    def __init__(self):
        self.x = 0
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 50  # pixels per second
        self.health = 5

    def update(self, dt):
        self.x += self.speed * (dt / 1000)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x - 10, self.y - 10, 20, 20))
        font = pygame.font.SysFont(None, 20)
        health_text = font.render(str(self.health), True, BLACK)
        surface.blit(health_text, (self.x - 10, self.y - 30))

    def is_dead(self):
        return self.health <= 0

# Lists to hold towers and enemies
towers = []
enemies = []
enemy_spawn_timer = 0  # milliseconds

# Main game loop
running = True
while running:
    dt = clock.tick(FPS)  # dt in milliseconds

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Key press to change tower selection
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_tower_type = "Tree"
            elif event.key == pygame.K_2:
                selected_tower_type = "Solar"
            elif event.key == pygame.K_3:
                selected_tower_type = "Recycle"
        # On mouse click, attempt to build the selected tower if enough money
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if selected_tower_type == "Tree" and money >= COST_TREE:
                towers.append(Tower(pos, "Tree"))
                money -= COST_TREE
            elif selected_tower_type == "Solar" and money >= COST_SOLAR:
                towers.append(Tower(pos, "Solar"))
                money -= COST_SOLAR
            elif selected_tower_type == "Recycle" and money >= COST_RECYCLE:
                towers.append(Tower(pos, "Recycle"))
                money -= COST_RECYCLE

    # Update towers
    for tower in towers:
        tower.update(dt)

    # Spawn enemy every 2 seconds
    enemy_spawn_timer += dt
    if enemy_spawn_timer > 2000:
        enemies.append(Enemy())
        enemy_spawn_timer = 0

    # Update enemies
    for enemy in enemies:
        enemy.update(dt)

    # Towers (only Tree) shoot at first enemy in range
    for tower in towers:
        if tower.can_shoot():
            for enemy in enemies:
                dist = math.hypot(tower.pos[0] - enemy.x, tower.pos[1] - enemy.y)
                if dist <= tower.range:
                    enemy.health -= tower.damage
                    tower.shoot()
                    break  # one shot per cooldown

    # Check collisions: If enemy touches a Solar or Recycle tower, destroy the tower.
    for enemy in enemies:
        for tower in towers[:]:
            if tower.type in ["Solar", "Recycle"]:
                # Approximate collision: distance less than sum of radii (20 + 10)
                if math.hypot(tower.pos[0] - enemy.x, tower.pos[1] - enemy.y) < (tower.radius + 10):
                    towers.remove(tower)

    # Remove dead enemies and check if enemy passed the right edge
    for enemy in enemies[:]:
        if enemy.is_dead():
            enemies.remove(enemy)
            money += 5  # Reward for killing enemy
        elif enemy.x > WIDTH:
            enemies.remove(enemy)
            city_health -= 1

    # Resource production and consumption update (per frame)
    # Count solar and recycle towers:
    num_solar = sum(1 for t in towers if t.type == "Solar")
    num_recycle = sum(1 for t in towers if t.type == "Recycle")
    # Solar towers produce 1 power per sec
    power += num_solar * (1 * dt / 1000)
    # Recycle towers: each costs 3 power per sec and produces $1 per sec
    power -= num_recycle * (3 * dt / 1000)
    money += num_recycle * (1 * dt / 1000)
    # Clamp resources to a minimum of 0
    money = max(money, 0)
    power = max(power, 0)

    # Draw everything
    screen.fill(WHITE)
    for tower in towers:
        tower.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    # Draw instructions and resource info overlay
    overlay_font = pygame.font.SysFont(None, 24)
    instructions = [
        "Press 1: Tree ($5) [Attacks enemies]",
        "Press 2: Solar ($10, +1 power/sec) [Fragile: destroyed on enemy contact]",
        "Press 3: Recycle ($50, -3 power/sec, +$1/sec) [Fragile: destroyed on enemy contact]",
        f"Selected Tower: {selected_tower_type}",
        f"Money: ${money:.1f}   Power: {power:.1f}   City Health: {city_health}"
    ]
    for i, line in enumerate(instructions):
        text_surface = overlay_font.render(line, True, BLACK)
        screen.blit(text_surface, (10, 10 + i * 20))

    pygame.display.flip()

    # Check game over condition
    if city_health <= 0:
        print("Game Over!")
        running = False

pygame.quit()
sys.exit()

