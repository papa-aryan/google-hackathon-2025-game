import pygame
import ctypes
import sys
import importlib # Added for reloading modules
from apiTest import get_google_joke # Assuming this is still needed
from player import Player # Import Player from player.py
from camera import Camera # Import Camera from camera.py
import tilemap # Import the new tilemap module


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
screen_width = 1700
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialize the tilemap system
tilemap.init_tilemap('cloud_tileset.png')

# Define map dimensions (larger than the screen)
# Use tilemap dimensions
# Make map_width and map_height global so they can be updated
map_width = 0
map_height = 0

def update_map_dimensions():
    global map_width, map_height
    map_width = len(tilemap.MAP[0]) * tilemap.TILE_GAME_SIZE
    map_height = len(tilemap.MAP) * tilemap.TILE_GAME_SIZE

update_map_dimensions() # Initial calculation

# Set window title
pygame.display.set_caption('Pygame Window')

# Clock for controlling framerate
clock = pygame.time.Clock()

# Character properties
# char_color is no longer used by Player
# char_width = 50 # Used for initial centering calculation - No longer needed for this method
# char_height = 100 # Used for initial centering calculation - No longer needed for this method
# Initial player position (center of the map)
# initial_player_x = map_width // 2 - char_width // 2 # Old method
# initial_player_y = map_height // 2 - char_height // 2 # Old method

# Create Player instance
player = Player(0, 0) # Create player at a temporary position
# Center the player on the map using its actual rect center
player.rect.center = (map_width // 2, map_height // 2)

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Camera properties
game_camera = Camera(screen_width, screen_height) # Create Camera instance

# Game loop
running = True
last_direction_keydown_event = None # Added to track the last directional key event
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                print("Space key pressed!")
            # Store the last directional key pressed
            elif event.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s, \
                               pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                last_direction_keydown_event = event.key
            elif event.key == pygame.K_u: # Added for map refresh
                try:
                    importlib.reload(tilemap)
                    tilemap.init_tilemap('cloud_tileset.png') # Re-initialize tileset
                    update_map_dimensions() # Recalculate map dimensions
                    # Recenter player if map dimensions change significantly (optional, could be complex)
                    # For now, just reload data. Player might be off-center if map size changes.
                    print("Map reloaded successfully!")
                except Exception as e:
                    print(f"Error reloading map: {e}")


    if not running: # Check if running is false to break loop before processing more
        break

    # Handle continuous key presses for movement
    keys = pygame.key.get_pressed()
    player.update_position(keys, map_width, map_height, last_direction_keydown_event, tilemap.can_move)

    # Update camera position to keep player centered
    game_camera.update(player, map_width, map_height)


    # Fill the screen with white
    screen.fill((173, 216, 230))

    # Draw the tilemap
    tilemap.draw_map(screen, game_camera)

    # Draw all sprites (adjusting for camera)
    for sprite in all_sprites:
        # screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y)) <--- REPLACE
        screen.blit(sprite.image, game_camera.apply(sprite))


    # Update the display
    pygame.display.flip()

    # Cap the framerate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit() # Exit using sys.exit()
