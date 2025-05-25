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
from mapManager import MapManager # Import MapManager
import wizardHouse # Ensure wizardHouse is imported to be available for MapManager


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

# Define map dimensions (larger than the screen)
# Use tilemap dimensions
# Make map_width and map_height global so they can be updated
map_width = 0
map_height = 0

# Instantiate MapManager FIRST, as other modules might need it during their setup if they call get_current_map_data
map_manager = MapManager()

# Now initialize tilemap, which might use map_manager if refactored to do so,
# or main.py will pass map_manager.get_current_tile_size() etc.
# Pass the tileset_width from the current map data
tilemap.init_tilemap(
    map_manager.current_map_data["tileset_path"],
    map_manager.current_map_data["tileset_width"],
    map_manager.current_map_data["tile_orig_size"] # Pass the specific original tile size for the initial map
)


def update_map_dimensions_from_manager(new_width, new_height):
    global map_width, map_height
    map_width = new_width
    map_height = new_height
    print(f"Global map dimensions updated by MapManager: {map_width}x{map_height}")


# Initial map dimensions are set by MapManager based on the starting map ("main_map")
map_width = len(map_manager.get_current_map_layout()[0]) * map_manager.get_current_tile_size()
map_height = len(map_manager.get_current_map_layout()) * map_manager.get_current_tile_size()
print(f"Initial map dimensions: {map_width}x{map_height}")


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
# Center the player on the initial map
player.rect.center = (map_width // 2, map_height // 2)

# Create Wizard instance near the top-left of the map
wizard_x = 439 
wizard_y = 388
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
            if event.key == pygame.K_ESCAPE: # Check for ESC key press
                running = False
            elif event.key == pygame.K_u: # Check for 'U' key press
                print("'U' key pressed. Attempting to reload and refresh map data...")
                try:
                    # Reload the map modules
                    importlib.reload(tilemap)
                    importlib.reload(wizardHouse) # Reload other map modules if you have them
                    print("Map modules reloaded.")

                    # Refresh the map data in MapManager using the reloaded modules
                    # The player object might not be strictly needed if refresh doesn't move it,
                    # but pass relevant objects if your refresh logic expands.
                    map_manager.refresh_active_map_after_reload(update_map_dimensions_from_manager)
                    print("Map data refreshed in MapManager.")

                except Exception as e:
                    print(f"Error during map reload/refresh: {e}")
            
            last_direction_keydown_event = event.key # Update last direction key

            if show_interaction_popup and eligible_interactable:
                if event.key == pygame.K_e: # Player presses E to interact
                    print(f"E pressed. Interacting with: {eligible_interactable.id}")
                    if eligible_interactable.id == "wizard":
                        # Player is interacting with the wizard
                        interaction_manager.set_interacted_flag(wizard.id, True) # Mark as interacted for this visit
                        show_interaction_popup = False # Hide popup
                        player_can_move = True # Allow player to move again
                        
                        # Switch to wizard's house map
                        map_manager.switch_map(
                            "wizard_house", 
                            player, 
                            wizard,                 # Pass wizard instance
                            all_sprites,            # Pass all_sprites group
                            interaction_manager,    # Pass interaction_manager instance
                            update_map_dimensions_from_manager # Pass callback function
                        ) # MODIFIED CALL
                        # Player position is handled by switch_map
                        # NPCs are handled by switch_map
                        print("Teleported to Wizard's House.")
                        # No need to break here, let the loop continue to redraw with new map
                    
                    # Add other interactable actions here if needed
                    # elif eligible_interactable.id == "some_other_npc":
                    #     pass

                elif event.key == pygame.K_q: # Player presses Q to move on
                    print("Q pressed. Moving on from interaction.")
                    if eligible_interactable: # Ensure there's something to move on from
                         # Mark as interacted to prevent immediate re-trigger if player stays in circle
                        interaction_manager.set_interacted_flag(eligible_interactable.id, True)
                    show_interaction_popup = False
                    player_can_move = True
    
    if not running: # Check if running is false to break loop before processing more
        break

    # Handle continuous key presses for movement
    keys = pygame.key.get_pressed()
    if player_can_move:
        # Pass the MapManager's can_move method for collision detection
        player.update_position(keys, map_width, map_height, last_direction_keydown_event, map_manager.can_move)

    # Update Interaction Manager
    interaction_manager.update(player.rect.center)
    
    # Determine if popup should be shown based on InteractionManager
    eligible_interactable = interaction_manager.get_eligible_interactable()
    if eligible_interactable:
        if not show_interaction_popup: # Only set to true if it wasn't already
            show_interaction_popup = True
            player_can_move = False # Stop player movement when popup appears
            print(f"Player entered {eligible_interactable.id}\'s interaction circle. Popup shown.")
    elif show_interaction_popup: # No eligible interactable, but popup is shown
        show_interaction_popup = False
        player_can_move = True
        # print("Popup hidden because no eligible interactable or player moved away.")


    # Update camera position to keep player centered
    game_camera.update(player, map_width, map_height) # map_width and map_height are now dynamic

    # Update all sprites (including the wizard's own update logic)
    # Sprites list is managed by map_manager for map-specific NPCs
    all_sprites.update() 

    # Fill the screen with white
    screen.fill((173, 216, 230))

    # Draw the tilemap using the MapManager's current map data
    # tilemap.draw_map(screen, game_camera) # OLD WAY
    # NEW WAY: Pass necessary data from map_manager to tilemap.draw_map
    current_map_layout = map_manager.get_current_map_layout()
    current_building_layout = map_manager.get_current_building_layout()
    current_decoration_layout = map_manager.get_current_decoration_layout() # ADDED
    current_tile_size = map_manager.get_current_tile_size()
    tilemap.draw_map(screen, game_camera, current_map_layout, current_building_layout, current_decoration_layout, current_tile_size) # MODIFIED

    # Draw all sprites (adjusting for camera)
    # Ensure all_sprites only contains sprites relevant to the current map
    for sprite in all_sprites:
        screen.blit(sprite.image, game_camera.apply(sprite))

    # Draw interaction circles for all interactables that haven't been interacted with
    # and are on the current map (implicitly handled if interaction_manager only has current map's interactables)
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
