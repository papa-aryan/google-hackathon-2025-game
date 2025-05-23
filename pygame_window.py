import pygame
import ctypes
import sys # Import sys module
from apiTest import get_google_joke


try:
    # Try to set DPI awareness to match pixels to PC (Windows 8.1+)
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    print("used new version.")
except AttributeError:
    # Fallback for older Windows versions
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        print("used older version.")
    except AttributeError:
        print("Could not set DPI awareness. Display scaling issues might persist.")

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set screen dimensions
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Define map dimensions (larger than the screen)
map_width = 3000
map_height = 2000

# Set window title
pygame.display.set_caption('Pygame Window')

# Clock for controlling framerate
clock = pygame.time.Clock()

# Player Sprite Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5 # Increase speed for better visibility of camera movement

    def update_position(self, keys, map_width, map_height):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player within map boundaries
        self.rect.x = max(0, min(self.rect.x, map_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, map_height - self.rect.height))

# Character properties
char_color = (255, 0, 0)  # Red
char_width = 50
char_height = 100
# Initial player position (center of the map)
initial_player_x = map_width // 2 - char_width // 2
initial_player_y = map_height // 2 - char_height // 2

# Create Player instance
player = Player(initial_player_x, initial_player_y, char_width, char_height, char_color)

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Camera properties
camera_x = 0
camera_y = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                print("Space key pressed!")

    if not running: # Check if running is false to break loop before processing more
        break

    # Handle continuous key presses for movement
    keys = pygame.key.get_pressed()
    player.update_position(keys, map_width, map_height)

    # Update camera position to keep player centered
    camera_x = player.rect.x - screen_width // 2 + player.rect.width // 2
    camera_y = player.rect.y - screen_height // 2 + player.rect.height // 2

    # Clamp camera to map boundaries
    camera_x = max(0, min(camera_x, map_width - screen_width))
    camera_y = max(0, min(camera_y, map_height - screen_height))

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw background pattern (grid)
    grid_color = (200, 200, 200) # Light grey
    tile_size = 50
    # Calculate the visible range of tiles
    start_col = camera_x // tile_size
    end_col = (camera_x + screen_width) // tile_size + 1
    start_row = camera_y // tile_size
    end_row = (camera_y + screen_height) // tile_size + 1

    for x_offset in range(start_col * tile_size, end_col * tile_size, tile_size):
        pygame.draw.line(screen, grid_color, (x_offset - camera_x, 0), (x_offset - camera_x, screen_height))
    for y_offset in range(start_row * tile_size, end_row * tile_size, tile_size):
        pygame.draw.line(screen, grid_color, (0, y_offset - camera_y), (screen_width, y_offset - camera_y))

    # Draw all sprites (adjusting for camera)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

    # Update the display
    pygame.display.flip()

    # Cap the framerate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit() # Exit using sys.exit()
