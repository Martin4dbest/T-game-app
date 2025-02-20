import pygame
import random
import sys
import os
import math

pygame.init()
pygame.mixer.init()


# Get the path of the current script (inside minigame_bonus)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
IMAGES_DIR = os.path.join(BASE_DIR, "images")  # Now correctly points to minigame_bonus/images

# Screen settings
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terry G's Ultimate Runner 🏃🏳‍⚡")  

# Load and play background music
music_path = os.path.join(BASE_DIR, "music.mp3")
failure_sound_path = os.path.join(BASE_DIR, "cartoon-fail-trumpet.mp3")

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

# Load multiple backgrounds from the "images" folder
backgrounds = []
for i in range(1, 7):
    path = os.path.join(IMAGES_DIR, f"background{i}.png")  # Ensure correct path
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

        # Load and scale the player image using absolute path
        player_image_path = os.path.join(IMAGES_DIR, "myrunner.png")
        if os.path.exists(player_image_path):
            self.image = pygame.image.load(player_image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            print(f"Warning: '{player_image_path}' not found! Using a placeholder color.")
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 0, 0))  # Red color for missing player image

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
        win.blit(self.image, (self.x, self.y))  # Draw the player image

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


class Ball(Obstacle):
    def __init__(self, x, y, radius, color):
        # Call the constructor of the parent class (Obstacle)
        super().__init__(x, y, radius * 2, radius * 2)  # Use diameter for width and height
        self.radius = radius
        self.color = color

    def move(self):
        self.y += 5  # Make the ball fall down (you can adjust speed)
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def collide(self, player_hitbox):
        return self.hitbox.colliderect(player_hitbox)


# Create falling balls
balls = [
    Ball(400, 100, 30, (0, 255, 0)),  # Green ball
    Ball(600, 150, 40, (255, 255, 0)),  # Yellow ball
]
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

    # Draw balls
    for ball in balls:
        ball.move()  # Update ball position (falling down)
        ball.draw(win)  # Draw ball

    # Draw player
    runner.draw(win)

    # Display Score
    font = pygame.font.SysFont("Arial", 30)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(text, (10, 10))

    pygame.display.update()
    

def end_screen(question_number, score):
    global obstacles, speed
    pygame.mixer.music.stop()  # Stop background music
    
    if failure_sound:
        failure_sound.play()
        pygame.time.delay(int(failure_sound.get_length() * 1000))  # Wait for sound to complete
    
    pygame.quit()  # Close pygame properly
    return score  # Return score back to quiz logic
def start_game(question_number):
    if not pygame.get_init():
        pygame.init()
    pygame.mixer.init()  # Ensure mixer is reinitialized to avoid errors

    # Only start the minigame when question_number is a multiple of 3
    if question_number % 3 != 0:
        return 0  

    pygame.time.set_timer(pygame.USEREVENT + 1, 500)
    pygame.time.set_timer(pygame.USEREVENT + 2, 3000)
    pygame.time.set_timer(pygame.USEREVENT + 3, 2000)

    global speed, score, runner, obstacles, pause, fallSpeed, bgX, bgX2, balls, lives
    
    speed = 30
    score = 0
    runner = Player(200, 313, 64, 64)
    obstacles = []
    balls = []
    pause = 0
    fallSpeed = 0

    # Ensure music is loaded before playing
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)  # Reload music
        pygame.mixer.music.play(-1)

    run = True
    while run:
        clock.tick(speed)

        score = speed // 10 - 3  # Score calculation

        # Handle obstacles
        for obstacle in obstacles:
            obstacle.move()
            if obstacle.collide(runner.hitbox):
                pygame.mixer.music.stop()
                run = False  # Exit game loop
                break  # Ensure immediate exit

        # Handle falling balls
        for ball in balls:
            if ball.y > runner.y - 100:
                ball.move()
            if ball.collide(runner.hitbox):
                pygame.mixer.music.stop()
                run = False  # Exit game loop
                break  # Ensure immediate exit

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                speed += 1
            if event.type == pygame.USEREVENT + 2:
                obstacles.append(Saw(810, 310) if random.choice([True, False]) else Spike(810, 0))
            if event.type == pygame.USEREVENT + 3:
                balls.append(Ball(810, -100, random.randint(20, 40), (0, 255, 0) if random.choice([True, False]) else (255, 255, 0)))

        keys = pygame.key.get_pressed()
        if not runner.falling:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not runner.jumping:
                    runner.jumping = True
            if keys[pygame.K_DOWN]:
                runner.sliding = True

        runner.move()
        redraw_window()  # Update screen

    return end_screen(question_number, score)  # Play failure sound before returning to quiz


