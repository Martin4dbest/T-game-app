import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
GROUND_LEVEL = HEIGHT - 70
SLIDE_DURATION = 20  # Frames for slide effect

# Load assets
human_runner = pygame.image.load("images/runner.png")
zombie_obstacle = pygame.image.load("images/zombie.png")
fire_pit_obstacle = pygame.image.load("images/fire_pit.png")
flying_bat_obstacle = pygame.image.load("images/bat.png")

# Scale assets
human_runner = pygame.transform.scale(human_runner, (50, 70))
zombie_obstacle = pygame.transform.scale(zombie_obstacle, (50, 70))
fire_pit_obstacle = pygame.transform.scale(fire_pit_obstacle, (60, 30))
flying_bat_obstacle = pygame.transform.scale(flying_bat_obstacle, (50, 40))

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game")

# Runner class
class Runner:
    def __init__(self):
        self.image = human_runner
        self.rect = self.image.get_rect(midbottom=(80, GROUND_LEVEL))
        self.gravity = 0
        self.is_sliding = False
        self.slide_timer = 0

    def jump(self):
        if self.rect.bottom >= GROUND_LEVEL and not self.is_sliding:
            self.gravity = -15

    def slide(self):
        if not self.is_sliding and self.rect.bottom == GROUND_LEVEL:
            self.is_sliding = True
            self.slide_timer = SLIDE_DURATION
            self.rect.height = 40  # Reduce height for sliding

    def apply_gravity(self):
        if not self.is_sliding:
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= GROUND_LEVEL:
                self.rect.bottom = GROUND_LEVEL

    def update(self):
        self.apply_gravity()
        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False
                self.rect.height = 70  # Restore height after sliding

    def draw(self):
        screen.blit(self.image, self.rect)

# Obstacle class
class Obstacle:
    def __init__(self, obstacle_type):
        if obstacle_type == "zombie":
            self.image = zombie_obstacle
            self.rect = self.image.get_rect(midbottom=(random.randint(850, 1100), GROUND_LEVEL))
        elif obstacle_type == "fire_pit":
            self.image = fire_pit_obstacle
            self.rect = self.image.get_rect(midbottom=(random.randint(850, 1100), GROUND_LEVEL + 20))
        elif obstacle_type == "flying_bat":
            self.image = flying_bat_obstacle
            self.rect = self.image.get_rect(midbottom=(random.randint(850, 1100), GROUND_LEVEL - 100))
        self.speed = 7

    def move(self):
        self.rect.x -= self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Game loop
runner = Runner()
obstacles = []
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                runner.jump()
            elif event.key == pygame.K_DOWN:
                runner.slide()

    runner.update()
    runner.draw()

    # Spawn obstacles
    if random.randint(1, 100) < 2:
        obstacle_type = random.choice(["zombie", "fire_pit", "flying_bat"])
        obstacles.append(Obstacle(obstacle_type))

    for obstacle in obstacles[:]:
        obstacle.move()
        obstacle.draw()
        if obstacle.rect.right < 0:
            obstacles.remove(obstacle)
        if runner.rect.colliderect(obstacle.rect):
            running = False
            print("Game Over!")

    pygame.display.update()
    clock.tick(30)

pygame.quit()
