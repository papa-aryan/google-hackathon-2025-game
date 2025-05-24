import pygame
import ctypes
import sys
import importlib # Added for reloading modules
from apiTest import get_google_joke # Assuming this is still needed
from player import Player # Import Player from player.py
from camera import Camera # Import Camera from camera.py
import tilemap # Import the new tilemap module
from wizard import Wizard # Import the Wizard class
from interaction_manager import InteractionManager # Import InteractionManager


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

# Font for interaction popup
interaction_font = pygame.font.Font(None, 36) # Added font

# Game state for wizard interaction (These will be managed by InteractionManager or influenced by it)
show_interaction_popup = False
player_can_move = True
# player_has_interacted_this_visit = False # This will be handled by InteractionManager per interactable

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

# Create Wizard instance near the top-left of the map
wizard_x = 439
wizard_y = 388
# Wizard now takes interaction_radius and interaction_offset_y
wizard = Wizard(wizard_x, wizard_y, interaction_radius=30, interaction_offset_y=28)

# Initialize Interaction Manager
interaction_manager = InteractionManager()
interaction_manager.add_interactable(wizard)
# Add other NPCs to interaction_manager here as they are created

# These definitions are now part of the Wizard's get_interaction_properties
# interaction_circle_radius = 30
# interaction_circle_center_x = wizard.rect.centerx
# interaction_circle_center_y = wizard.rect.bottom + 28
# static_interaction_circle_center = pygame.math.Vector2(interaction_circle_center_x, interaction_circle_center_y)
# interaction_circle_color = (135, 206, 250)  # LightSkyBlue
# interaction_circle_thickness = 3


# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(wizard) # Add wizard to the sprite group
# Add other NPCs to all_sprites here


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
                    print("Map reloaded successfully!")
                except Exception as e:
                    print(f"Error reloading map: {e}")
            
            # Interaction key presses (E and Q)
            current_interactable = interaction_manager.get_eligible_interactable()
            if current_interactable and show_interaction_popup:
                if event.key == pygame.K_e:
                    print(f"E pressed - interacting with {current_interactable.id}")
                    interaction_manager.set_interacted_flag(current_interactable.id, True)
                    show_interaction_popup = False
                    player_can_move = True
                    # Potentially trigger specific action for current_interactable
                elif event.key == pygame.K_q:
                    print(f"Q pressed - moving on from {current_interactable.id}")
                    interaction_manager.set_interacted_flag(current_interactable.id, True) # Mark as interacted to hide circle
                    show_interaction_popup = False
                    player_can_move = True


    if not running: # Check if running is false to break loop before processing more
        break

    # Handle continuous key presses for movement
    keys = pygame.key.get_pressed()
    if player_can_move:
        player.update_position(keys, map_width, map_height, last_direction_keydown_event, tilemap.can_move)

    # Update Interaction Manager
    interaction_manager.update(player.rect.center)
    
    # Determine if popup should be shown based on InteractionManager
    eligible_interactable = interaction_manager.get_eligible_interactable()
    if eligible_interactable:
        if not show_interaction_popup: # Only trigger if popup isn't already shown
            show_interaction_popup = True
            player_can_move = False
            print(f"Player entered {eligible_interactable.id}\'s interaction circle. Popup shown.")
    elif show_interaction_popup: # No eligible interactable, but popup is shown (player moved away or interacted)
        show_interaction_popup = False
        player_can_move = True
        # print("Popup hidden because no eligible interactable or player moved away.")


    # Update camera position to keep player centered
    game_camera.update(player, map_width, map_height)

    # Update all sprites (including the wizard's own update logic)
    all_sprites.update() # This will call wizard.update()

    # Fill the screen with white
    screen.fill((173, 216, 230))

    # Draw the tilemap
    tilemap.draw_map(screen, game_camera)

    # Draw all sprites (adjusting for camera)
    for sprite in all_sprites:
        screen.blit(sprite.image, game_camera.apply(sprite))

    # Draw interaction circles for all interactables that haven't been interacted with
    for interactable_obj in interaction_manager.get_all_interactables():
        if not interaction_manager.get_interacted_flag(interactable_obj.id):
            props = interactable_obj.get_interaction_properties()
            circle_center_vec = pygame.math.Vector2(props['center'])
            # Apply camera offset to the circle's static world position for drawing
            circle_draw_center_x_on_screen = circle_center_vec.x + game_camera.camera.x
            circle_draw_center_y_on_screen = circle_center_vec.y + game_camera.camera.y
            pygame.draw.circle(screen, props['color'],
                               (int(circle_draw_center_x_on_screen), int(circle_draw_center_y_on_screen)),
                               props['radius'], props['thickness'])

    # Draw interaction popup if active
    if show_interaction_popup and eligible_interactable:
        props = eligible_interactable.get_interaction_properties()
        popup_text = props['message']
        text_surface = interaction_font.render(popup_text, True, (0, 0, 0)) # Black text
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 50)) # Position at bottom-center
        
        # Optional: Add a background to the popup text for better visibility
        popup_bg_rect = text_rect.inflate(20, 10) # Add some padding
        pygame.draw.rect(screen, (200, 200, 200), popup_bg_rect) # Light grey background
        pygame.draw.rect(screen, (0, 0, 0), popup_bg_rect, 2) # Black border

        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the framerate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit() # Exit using sys.exit()
