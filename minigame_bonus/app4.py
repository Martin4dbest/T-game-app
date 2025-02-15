import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 1000, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terry G's Ultimate Runner 🏃🏳‍⚡")  

# Load and play background music
music_path = "music.mp3"
failure_sound_path = "cartoon-fail-trumpet.mp3"

if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Loop indefinitely
else:
    print("Warning: 'music.mp3' not found! No background music will play.")

# Load failure sound effect
if os.path.exists(failure_sound_path):
    failure_sound = pygame.mixer.Sound(failure_sound_path)
else:
    print("Warning: 'cartoon-fail-trumpet.mp3' not found! No failure sound will play.")
    failure_sound = None

# Ensure the images folder exists
if not os.path.exists("images"):
    os.makedirs("images")

# Load multiple backgrounds from the "images" folder
backgrounds = []
for i in range(1, 7):
    path = os.path.join("images", f"background{i}.png")  # Ensure correct path
    if os.path.exists(path):
        backgrounds.append(pygame.image.load(path))
    else:
        print(f"Warning: '{path}' not found! Using a placeholder color.")
        temp_bg = pygame.Surface((WIDTH, HEIGHT))
        temp_bg.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  # Random colors
        backgrounds.append(temp_bg)

current_bg_index = 0
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

# Initialize background positions
bgX = 0
bgX2 = WIDTH

# Global variables
speed = 30
score = 0
pause = 0
fallSpeed = 0
obstacles = []

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        if self.jumping:
            self.y -= 10
            if self.y <= 200:
                self.jumping = False
        elif self.y < 313:
            self.y += 10
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), self.hitbox)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x -= (speed / 30) * 1.4
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def collide(self, player_hitbox):
        return self.hitbox.colliderect(player_hitbox)

class Saw(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64)

class Spike(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 310)

def redraw_window():
    global bgX, bgX2, current_bg_index

    # Change background every 3-score interval
    current_bg_index = (score // 3) % len(backgrounds)

    # Draw backgrounds
    win.blit(backgrounds[current_bg_index], (bgX, 0))
    win.blit(backgrounds[current_bg_index], (bgX2, 0))

    # Move background
    bgX -= (speed / 30) * 1.4
    bgX2 -= (speed / 30) * 1.4

    # Reset background position
    if bgX < -WIDTH:
        bgX = WIDTH
    if bgX2 < -WIDTH:
        bgX2 = WIDTH

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(win)

    # Draw player
    runner.draw(win)

    # Display Score
    font = pygame.font.SysFont("Arial", 30)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(text, (10, 10))

    pygame.display.update()

def end_screen():
    global obstacles, speed, score
    run = True
    while run:
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 40)
        text = font.render("Game Over! Press R to Restart or Q to Quit", True, (255, 255, 255))
        win.blit(text, (WIDTH // 2 - 250, HEIGHT // 2 - 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_game()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def start_game():
    global speed, score, runner, obstacles, pause, fallSpeed, bgX, bgX2

    pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Increase speed every 0.5s
    pygame.time.set_timer(pygame.USEREVENT + 2, 3000)  # Spawn obstacle every 3s

    # Reset variables
    speed = 30
    score = 0
    runner = Player(200, 313, 64, 64)
    obstacles = []
    pause = 0
    fallSpeed = 0

    # Restart background music on game restart
    if os.path.exists(music_path):
        pygame.mixer.music.play(-1)  # Loop indefinitely

    run = True
    while run:
        clock.tick(speed)

        if pause > 0:
            pause += 1
            if pause > fallSpeed * 2:
                end_screen()
                return

        # Score updates with speed increase
        score = speed // 10 - 3

        for obstacle in obstacles:
            obstacle.move()
            if obstacle.collide(runner.hitbox):
                runner.falling = True
                if pause == 0:
                    pause = 1
                    fallSpeed = speed
                    pygame.mixer.music.stop()  # Stop background music
                    if failure_sound:
                        failure_sound.play()  # Play failure sound

            if obstacle.x < -64:
                obstacles.remove(obstacle)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT + 1:
                speed += 1

            if event.type == pygame.USEREVENT + 2:
                if random.choice([True, False]):
                    obstacles.append(Saw(810, 310))
                else:
                    obstacles.append(Spike(810, 0))

        # Player controls
        keys = pygame.key.get_pressed()
        if not runner.falling:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not runner.jumping:
                    runner.jumping = True
            if keys[pygame.K_DOWN]:
                runner.sliding = True

        runner.move()
        redraw_window()

# Start game
start_game()
