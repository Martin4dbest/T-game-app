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

    def move(self, speed):
        self.x -= (speed / 30) * 1.4
        self.hitbox.x = self.x  # Update hitbox position

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.hitbox)  # Draw obstacle in red

    def collide(self, player_hitbox):
        return self.hitbox.colliderect(player_hitbox)
    

class Saw(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64)


class Spike(Obstacle):
    def __init__(self, x, y):
        height = 150 if y >= 200 else 280
        super().__init__(x, y, 48, height)

        self.behavior = random.choice(["static", "swinging", "rotating", "falling", "bouncing"])
        self.swing_offset = random.randint(0, 360)
        self.swing_speed = random.randint(3, 6)
        self.rotation_angle = 0
        self.bounce_direction = 1
        self.speed_y = random.randint(2, 5)  

        # Random Color
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0)])

        # Random Shape
        self.shape = random.choice(["triangle", "circle", "star", "hexagon", "blade"])

    def move(self, speed):
        super().move(speed)

        if self.behavior == "swinging":
            if self.y < 200:
                self.y = 80 + 100 * math.sin(math.radians(self.swing_offset))
            else:
                self.y = 150 + 50 * math.sin(math.radians(self.swing_offset))
            self.swing_offset += self.swing_speed

        elif self.behavior == "rotating":
            self.rotation_angle += 10  

        elif self.behavior == "falling":
            self.y += self.speed_y
            if self.y > 600:
                self.y = -50  # Reset above screen

        elif self.behavior == "bouncing":
            self.y += self.speed_y * self.bounce_direction
            if self.y <= 50 or self.y >= 400:
                self.bounce_direction *= -1  # Reverse direction

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        if self.shape == "triangle":
            self.draw_triangle(win)
        elif self.shape == "circle":
            self.draw_circle(win)
        elif self.shape == "star":
            self.draw_star(win)
        elif self.shape == "hexagon":
            self.draw_hexagon(win)
        elif self.shape == "blade":
            self.draw_blade(win)

    def draw_triangle(self, win):
        top_point = (self.x + self.width // 2, self.y)
        left_point = (self.x, self.y + self.height)
        right_point = (self.x + self.width, self.y + self.height)
        pygame.draw.polygon(win, self.color, [top_point, left_point, right_point])

    def draw_circle(self, win):
        pygame.draw.circle(win, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)

    def draw_star(self, win):
        points = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width * 0.35, self.y + self.height * 0.35),
            (self.x, self.y + self.height // 2),
            (self.x + self.width * 0.35, self.y + self.height * 0.65),
            (self.x + self.width // 2, self.y + self.height),
            (self.x + self.width * 0.65, self.y + self.height * 0.65),
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width * 0.65, self.y + self.height * 0.35),
        ]
        pygame.draw.polygon(win, self.color, points)

    def draw_hexagon(self, win):
        points = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width, self.y + self.height // 4),
            (self.x + self.width, self.y + (3 * self.height) // 4),
            (self.x + self.width // 2, self.y + self.height),
            (self.x, self.y + (3 * self.height) // 4),
            (self.x, self.y + self.height // 4),
        ]
        pygame.draw.polygon(win, self.color, points)

    def draw_blade(self, win):
        pygame.draw.ellipse(win, self.color, (self.x, self.y, self.width, self.height))


# Additional Obstacle: Fast-Moving Blades
class Blade(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 60, 20)
        self.speed_x = random.randint(8, 15)
        self.speed_y = random.choice([-5, 5])

    def move(self, speed):
        self.x -= self.speed_x
        self.y += self.speed_y

        if self.y < 50 or self.y > 500:
            self.speed_y *= -1  # Bounce off top and bottom

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.ellipse(win, (255, 255, 0), self.hitbox)


"""
class BladeObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 60, 60)
        self.speed_x = random.randint(8, 15)
        self.speed_y = random.choice([-5, 5])
        self.rotation_angle = 0

        try:
            self.original_image = pygame.image.load("images/blade.png")
            self.original_image = pygame.transform.scale(self.original_image, (self.width, self.height))
        except pygame.error:
            print("Warning: blade.png not found! Using placeholder.")
            self.original_image = pygame.Surface((self.width, self.height))
            self.original_image.fill((255, 0, 0))  

        self.image = self.original_image  

    def move(self, speed):
        self.x -= speed  
        print(f"Blade moved to {self.x}, {self.y}") 
        self.y += self.speed_y  # Move up/down
        if self.y <= 50 or self.y >= 500:
            self.speed_y *= -1  # Reverse direction

        # Update hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, speed):
        print(f"Before move: Blade at {self.x}, {self.y}")  # Debugging output
    
        self.x -= speed  # Use the provided speed for movement
        self.y += self.speed_y  # Move up/down

        # Bounce off top and bottom screen edges
        if self.y <= 50 or self.y >= 500:
            self.speed_y *= -1  # Reverse direction

        # Update hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        

    def move(self, speed):
    
        print(f"Before move: Blade at {self.x}, {self.y}")  # Debugging output

        self.x -= (self.speed_x + speed)  # Move left, factoring in extra speed
        self.y += self.speed_y  # Move up/down

        if self.y <= 50 or self.y >= 500:
            self.speed_y *= -1  # Reverse direction

        # Reset blade when it moves off-screen
        if self.x < -self.width:  # If blade fully exits left
            self.x = random.randint(800, 1200)  # Respawn on the right
            self.y = random.randint(50, 500)  # Random vertical position
            print(f"Blade respawned at {self.x}, {self.y}")  # Debugging output

        print(f"After move: Blade at {self.x}, {self.y}")  # Debugging output)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)



        

    def draw(self, win):
        self.rotation_angle += 10  
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        
        rotated_rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        win.blit(self.image, rotated_rect.topleft)

blades = [BladeObstacle(random.randint(600, 1200), random.randint(50, 500)) for _ in range(5)]

print(f"Spawned {len(blades)} blades")  # ✅ Check if blades exist



for blade in blades:
    blade.move(speed)  
    blade.draw(win)

    """
       



# Additional Obstacle: Rolling Ball
class RollingBall(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.speed_x = random.randint(4, 8)
        self.rotation_angle = 0

    def move(self, speed):
        self.x -= self.speed_x
        self.rotation_angle += self.speed_x * 2  

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.circle(win, (0, 255, 255), (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)






# Example Usage in Game
obstacles = []
for _ in range(5):
    obstacles.append(Spike(random.randint(600, 1200), random.choice([50, 250, 450])))
    obstacles.append(Blade(random.randint(600, 1200), random.randint(50, 550)))
    obstacles.append(RollingBall(random.randint(600, 1200), random.randint(300, 500)))

        
# ADD ROOF BARRIER
class RoofBarrier:
    def __init__(self):
        self.hitbox = pygame.Rect(0, 0, 800, 50)  # A ceiling across the screen

    def check_collision(self, player):
        if self.hitbox.colliderect(player.hitbox):
            player.y = 50  # Prevents player from going higher




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

        # Display "Game Over" message
        text1 = font.render("Game Over!", True, (255, 255, 255))
        win.blit(text1, (WIDTH // 2 - 100, HEIGHT // 2 - 80))

        # Display total score
        text2 = font.render(f"Your Score: {score}", True, (255, 255, 255))
        win.blit(text2, (WIDTH // 2 - 100, HEIGHT // 2 - 30))

        # Display restart and quit instructions
        text3 = font.render("Press ENTER to Restart or Q to Quit", True, (255, 255, 255))
        win.blit(text3, (WIDTH // 2 - 250, HEIGHT // 2 + 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to restart
                    score = 0  # Reset score
                    start_game()
                    return
                elif event.key == pygame.K_q:  # Press Q to quit
                    pygame.quit()
                    sys.exit()



def start_game():
    global speed, score, runner, obstacles, blades, pause, fallSpeed

    pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Increase speed every 0.5s
    pygame.time.set_timer(pygame.USEREVENT + 2, 3000)  # Spawn obstacle every 3s

    # Reset variables
    speed = 30
    score = 0
    runner = Player(200, 313, 64, 64)
    obstacles = []
    #blades = [BladeObstacle(random.randint(600, 1200), random.randint(50, 500)) for _ in range(3)]  # ✅ Blade Obstacles added
    pause = 0
    fallSpeed = 0

    # Restart background music on game restart
    if 'music_path' in globals() and os.path.exists(music_path):
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

        for obstacle in obstacles[:]:  # Use a copy to safely remove items
            obstacle.move(speed)
            if obstacle.collide(runner.hitbox):
                runner.falling = True
                if pause == 0:
                    pause = 1
                    fallSpeed = speed
                    pygame.mixer.music.stop()  # Stop background music
                    if 'failure_sound' in globals() and failure_sound:
                        failure_sound.play()  # Play failure sound

            if obstacle.x < -64:
                obstacles.remove(obstacle)

        # ✅ Move and draw blades so they persist across backgrounds
        """
        for blade in blades:
            blade.move(speed)
            blade.draw(win)
        """
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
if __name__ == "__main__":
    start_game()
    pygame.quit()