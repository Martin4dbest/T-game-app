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
WIDTH, HEIGHT = 1000, 800
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




# (Previous code remains unchanged until the Player class)# (Previous code remains unchanged until the Player class)
# (Previous code remains unchanged until the Player class)

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jump_speed = 15  # Speed of jumping
        self.fall_speed = 15  # Speed of falling
        self.slide_speed = 10  # Speed of sliding
        self.ground_level = 313  # Ground level for the player
        self.max_jump_height = 100  # Maximum height the player can jump (increased for tall obstacles)
        self.is_on_ground = True  # Track if the player is on the ground
        self.is_sliding = False  # Track if the player is sliding
        self.falling = False  # Track if the player is falling
        self.jumping = False  # Track if the player is jumping

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
        keys = pygame.key.get_pressed()
        
        #ground_level = HEIGHT - self.height - 50  # Prevents player from sinking below
        ground_level = HEIGHT - self.height  # Strict ground limit

        # Jumping with up arrow
        if keys[pygame.K_UP] and self.y > self.max_jump_height:  # Only jump if not already at max height
            self.y -= self.jump_speed
            self.jumping = True
            self.falling = False  # Reset falling state

        # Falling with down arrow
        if keys[pygame.K_DOWN] and self.y < ground_level:  # Only fall if above ground
            self.y += self.fall_speed
            self.falling = True
            self.jumping = False  # Reset jumping state

        # Sliding with forward arrow (right arrow key)
        if keys[pygame.K_RIGHT] and self.is_on_ground:  
            self.is_sliding = True
        else:
            self.is_sliding = False

        # Ensure the player doesn't go above the max jump height
        if self.y < self.max_jump_height:
            self.y = self.max_jump_height
            self.jumping = False  # Stop jumping when reaching max height

        # Ensure the player doesn't go below the ground level
        if self.y > ground_level:
            self.y = ground_level
            self.falling = False  # Stop falling when hitting the ground

        # Update hitbox position
        if self.is_sliding:
            self.hitbox = pygame.Rect(self.x, self.y + self.height // 2, self.width, self.height // 2)
        else:
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        if self.is_sliding:
            win.blit(pygame.transform.scale(self.image, (self.width, self.height // 2)), (self.x, self.y + self.height // 2))
        else:
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
        self.color = (255, 0, 0)  # Red color for saw

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)

class Spike(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 310)
        self.color = (0, 0, 0)  # Black color for spike

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)

class HotWater(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 20)
        self.color = (0, 0, 255)  # Blue color for hot water

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)

class Block(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 20)
        self.color = (255, 165, 0)  # Orange color for block

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)

class Triangle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.color = (255, 0, 255)  # Purple color for triangle

    def draw(self, win):
        pygame.draw.polygon(win, self.color, [(self.x, self.y + self.height), (self.x + self.width / 2, self.y), (self.x + self.width, self.y + self.height)])

class Star(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.color = (255, 255, 0)  # Yellow color for star

    def draw(self, win):
        pygame.draw.polygon(win, self.color, [
            (self.x + 25, self.y),
            (self.x + 30, self.y + 20),
            (self.x + 50, self.y + 20),
            (self.x + 35, self.y + 35),
            (self.x + 40, self.y + 50),
            (self.x + 25, self.y + 40),
            (self.x + 10, self.y + 50),
            (self.x + 15, self.y + 35),
            (self.x, self.y + 20),
            (self.x + 20, self.y + 20)
        ])

class MovingBlock(Obstacle):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 100, 20)
        self.color = (0, 255, 0)  # Green color for moving block
        self.direction = direction  # "up" or "down"

    def move(self):
        self.x -= (speed / 30) * 1.4  # Move left
        if self.direction == "up":
            self.y -= 5  # Move up
        elif self.direction == "down":
            self.y += 5  # Move down
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)


class Ball(Obstacle):
    def __init__(self, x, y, radius, color):
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

# (Previous code remains unchanged until the Obstacle class)

# (Previous code remains unchanged until the Obstacle class)

class RectangularSpike(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 20)  # Width = 50, Height = 20
        self.color = (255, 0, 0)  # Red color for rectangular spike
        self.speed = 5  # Speed at which the spike moves upward

    def move(self):
        self.y -= self.speed  # Move upward
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)

# Add rectangular spikes moving upward from below
obstacles = [
    Saw(800, 313),
    Spike(1000, 313),
    HotWater(1200, 500),  # Hot water obstacle
    Block(1400, 200),  # Block obstacle
    Triangle(1600, 313),  # Triangle obstacle
    Star(1800, 313),  # Star obstacle
    MovingBlock(2000, 500, "up"),  # Moving block going up
    MovingBlock(2200, 200, "down"),  # Moving block going down
    Saw(2400, 313),  # Another saw
    Spike(2600, 313),  # Another spike
    HotWater(2800, 500),  # Another hot water
    Block(3000, 200),  # Another block
    Triangle(3200, 313),  # Another triangle
    Star(3400, 313),  # Another star
    MovingBlock(3600, 500, "up"),  # Another moving block going up
    MovingBlock(3800, 200, "down"),  # Another moving block going down
    Block(4000, HEIGHT - 50),  # Scattered box very low
    Block(4200, HEIGHT - 100),  # Scattered box very low
    Block(4400, HEIGHT - 150),  # Scattered box very low
    RectangularSpike(4600, HEIGHT - 20),  # Rectangular spike moving upward from below
    RectangularSpike(5000, HEIGHT - 20),  # Another rectangular spike
    RectangularSpike(5400, HEIGHT - 20),  # Another rectangular spike
]


import pygame
import sys
import os
import random

def redraw_window(question_number):
    global bgX, bgX2, current_bg_index, win, timer, start_ticks
    
    if pygame.display.get_surface() is None:
        return
    
    current_bg_index = (score // 3) % len(backgrounds)
    win.blit(backgrounds[current_bg_index], (bgX, 0))
    win.blit(backgrounds[current_bg_index], (bgX2, 0))
    
    bgX -= (speed / 30) * 1.4
    bgX2 -= (speed / 30) * 1.4
    if bgX < -WIDTH:
        bgX = WIDTH
    if bgX2 < -WIDTH:
        bgX2 = WIDTH
    
    for obstacle in obstacles:
        obstacle.draw(win)
    
    for ball in balls:
        ball.move()
        ball.draw(win)
    
    runner.draw(win)
    
    font = pygame.font.SysFont("Arial", 30)
    
    # Set colors for different texts
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White
    timer_text = font.render(f"Time: {max(0, (120 if question_number == 15 else 40) - (pygame.time.get_ticks() - start_ticks) // 1000)}s", True, (255, 255, 255))  # White
    lives_text = font.render("Lives: 3" if question_number == 15 else "Lives: 1", True, (255, 0, 0))  # Red
    target_text = font.render(f"Target Score: {10 if question_number == 15 else 8}", True, (0, 0, 255))  # Blue
    
    # Display text on the screen
    win.blit(score_text, (10, 10))  
    win.blit(timer_text, (650, 10))  
    win.blit(lives_text, (650, 50))  
    win.blit(target_text, (10, 50))  
    
    pygame.display.update()



def end_screen(question_number, score, success=False):
    global win
    pygame.mixer.music.pause()
    
    target_score = 10 if question_number == 15 else 8
    
    if not success:
        failure_sound.play()
        pygame.time.delay(int(failure_sound.get_length() * 1000))
    else:
        if question_number in [3, 6, 9, 12]:  # Only show message for these numbers
            win.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 40)
            message = font.render("Well Done!", True, (0, 255, 0))
            score_text = font.render(f"Score: {score}", True, (0, 255, 0))
            target_text = font.render(f"Target: {target_score}", True, (0, 255, 0))
            question_text = font.render(f"Questions Attempted: {question_number}", True, (0, 255, 0))
            win.blit(message, (300, 200))
            win.blit(score_text, (300, 250))
            win.blit(target_text, (300, 300))
            win.blit(question_text, (300, 350))
            pygame.display.update()
            pygame.time.delay(8000)
    
    pygame.display.quit()
    return score



def start_game(question_number):
    global win, speed, score, runner, obstacles, pause, fallSpeed, bgX, bgX2, balls, lives, start_ticks
    
    if question_number % 3 != 0:
        return 0  

    pygame.init()
    pygame.mixer.init()
    
    # Set screen size dynamically to ensure consistency across minigame stages
    if question_number < 6:
        win = pygame.display.set_mode((1200, 800))  # Use this for first minigame
    else:
        win = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)  # Maintain same size but allow resizing

    pygame.display.set_caption(f"Minigame - Question {question_number}")
    
    pygame.time.set_timer(pygame.USEREVENT + 1, 500)
    pygame.time.set_timer(pygame.USEREVENT + 2, 2500)  # Obstacle spawn rate
    pygame.time.set_timer(pygame.USEREVENT + 3, 1800)  # Ball spawn rate
    
    speed = 30
    score = 0
    lives = 1  
    runner = Player(200, 313, 64, 64)
    obstacles = []
    balls = []
    pause = 0
    fallSpeed = 0
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    
    run = True
    target_score = 10 if question_number == 15 else 8
    allow_continuation = question_number in [3, 6, 9, 12]
    
    if question_number == 15:
        remaining_time = 120
    elif question_number in [3, 6, 9, 12]:  
        remaining_time = 40
    else:
        remaining_time = 20

    while run:
        clock.tick(speed)
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  

        if elapsed_time >= remaining_time:
            if question_number == 15 and score < target_score and lives == 0:
                show_compensation_message()
                return  # Ensure game exits instead of lingering
            return end_screen(question_number, score, success=True)

        if not allow_continuation and score >= target_score and question_number != 15:  
            return end_screen(question_number, score, success=True)


        score = (speed // 8) - 2  # Score increases slightly faster than before

        for obstacle in obstacles[:]:
            obstacle.move()
            if obstacle.collide(runner.hitbox):
                lives -= 1
                # If the target score is already reached, go to end screen instead of quitting
                if score >= target_score and question_number in [3, 6, 9, 12]:
                    return end_screen(question_number, score, success=True)
                elif lives == 0 and question_number == 15 and score < target_score:
                    return show_compensation_message()
                return end_screen(question_number, score)

        for ball in balls[:]:
            if ball.y > runner.y - 100:
                ball.move()
            if ball.collide(runner.hitbox):
                lives -= 1
                # Ensure end screen appears if target score is reached
                if score >= target_score and question_number in [3, 6, 9, 12]:
                    return end_screen(question_number, score, success=True)
                elif lives == 0 and question_number == 15 and score < target_score:
                    return show_compensation_message()
                return end_screen(question_number, score)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT + 1:
                speed += 1
            if event.type == pygame.USEREVENT + 2:
                obstacle_y = random.choice([0, 310, random.randint(50, 250), random.randint(350, 550)])
                obstacle_x = random.choice([810, random.randint(50, 750)])
                obstacle_type = random.choice([Saw, Spike, HotWater, Triangle, Star])
                size_multiplier = random.choice([1, 1.5, 2])  

                new_obstacle = obstacle_type(obstacle_x, obstacle_y)
                
                if isinstance(new_obstacle, Spike):
                    new_obstacle.height = min(new_obstacle.height * size_multiplier, 120)  # Max height limit
                
                new_obstacle.width *= size_multiplier
                obstacles.append(new_obstacle)
                
                if random.random() < 0.15:  
                    surprise_x = runner.x + random.randint(200, 300)
                    surprise_obstacle = obstacle_type(surprise_x, runner.y)
                    surprise_obstacle.active = False  
                    surprise_obstacle.activation_time = pygame.time.get_ticks() + 6000 
                    obstacles.append(surprise_obstacle)

            if event.type == pygame.USEREVENT + 3:
                ball_x = random.randint(200, 600)  
                ball_y = -50  
                balls.append(Ball(ball_x, ball_y, random.randint(20, 40), (0, 255, 0) if random.choice([True, False]) else (255, 255, 0)))
        
        current_time = pygame.time.get_ticks()
        for obs in obstacles:
            if hasattr(obs, 'activation_time') and not obs.active:
                if current_time >= obs.activation_time:
                    obs.active = True  

        # **✅ Fixed Movement Logic (Continuous Backward Movement)**
        keys = pygame.key.get_pressed()
        if not runner.falling:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:  
                if not runner.jumping:
                    runner.jumping = True
            if keys[pygame.K_DOWN]:  
                runner.sliding = True
            if keys[pygame.K_RIGHT]:  
                runner.x += 5  # Move forward
            if keys[pygame.K_LEFT]:  
                runner.x -= 5  # Move backward continuously

        # **✅ Prevent Player from Moving Out of Screen**
        runner.x = max(0, min(runner.x, 800 - runner.width))

        runner.move()
        redraw_window(question_number)
    
    pygame.quit()
    return 0




# Global counter to track how many times the player has lost
loss_count = 0  

def show_compensation_message():
    """Displays a different message based on how many times the player has lost."""
    global loss_count  

    win.fill((0, 0, 0))  
    font = pygame.font.Font(None, 36)

    messages = [
        "Sorry, you lost, but you still have 2 lives left. Try again!",
        "Oops, you lost another life. You have one life left after this, so try!",
        "Great job getting this far! You can cash out, but you didn't make the leaderboard."
    ]

    # Ensure we don't go beyond the message list
    message = messages[min(loss_count, len(messages) - 1)]

    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() // 2))
    win.blit(text, text_rect)
    pygame.display.update()
    
    pygame.time.delay(5000)  # Show message for 5 seconds

    win.fill((255, 255, 255))  # Clear screen
    pygame.display.update()

    # Increase loss count for the next time this function is called
    loss_count += 1  

    # Quit pygame if it's the last message
    if loss_count >= len(messages):
        pygame.quit()

    return 0  # Return 0 after displaying the message




