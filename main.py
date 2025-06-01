import pygame
import ctypes
import sys
import importlib
from player import Player
from camera import Camera
import tilemap 
from wizard import Wizard
from naval_npc import NavalNPC
from interaction_manager import InteractionManager
from mapManager import MapManager 
from wizardChatManager import WizardChatManager 
from settings_manager import SettingsManager 
import wizardHouse # Ensure wizardHouse is imported to be available for MapManager
import random
from minigameManager import MinigameManager
from quizManager import QuizManager
from mysterious_rect import MysteriousRect


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
interaction_font = pygame.font.Font(None, 72) # Added font

# Point tracker
player_points = 0
points_font = pygame.font.Font(None, 36)

# Typewriter effect state
typing_active = False
text_to_type_full = ""
typed_text_display = ""
typing_char_index = 0
typing_last_char_time = 0
TYPING_DELAY_MS = 40  # Milliseconds per character, adjust for speed

# Game state for wizard interaction (These will be managed by InteractionManager or influenced by it)
show_interaction_popup = False
player_can_move = True
# player_has_interacted_this_visit = False # This will be handled by InteractionManager per interactable

# Set screen dimensions
screen_width = 1700
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialize ChatManager
wizard_chat_manager = WizardChatManager(screen_width, screen_height)

# Initialize SettingsManager
settings_manager = SettingsManager(screen_width, screen_height)

# Initialize MinigameManager
minigame_manager = MinigameManager()

# Initialize QuizManager
quiz_manager = QuizManager(screen_width, screen_height)

def on_quiz_completion(points):
    """Callback when player completes quiz correctly"""
    global player_points
    old_points = player_points
    player_points += points
    print(f"DEBUG: Quiz completion callback - gained {points} points. {old_points} -> {player_points}")

def on_quiz_failure():
    """Callback when player fails quiz or cancels"""
    print("DEBUG: Quiz failure callback - no points awarded")

# Set quiz callbacks
quiz_manager.set_callbacks(on_quiz_completion, on_quiz_failure)

# Set up points callback for settings manager
def update_player_points(new_points):
    global player_points
    player_points = new_points
    print(f"Player points updated to: {player_points}")

settings_manager.set_points_callback(update_player_points)

def on_minigame_completion(points):
    """Callback when player completes minigame"""
    global player_points
    player_points += points
    print(f"Minigame completed! Gained {points} points. Total: {player_points}")
    # Return to main map
    map_manager.return_from_minigame(player, wizard, all_sprites, interaction_manager, update_map_dimensions_from_manager)

def on_minigame_death():
    """Callback when player dies in minigame"""
    global player_points
    player_points = max(0, player_points - 1)  # Don't go below 0
    print(f"Died in minigame! Lost 1 point. Total: {player_points}")
    # Return to main map
    map_manager.return_from_minigame(player, wizard, all_sprites, interaction_manager, update_map_dimensions_from_manager)

# Set minigame callbacks
minigame_manager.set_callbacks(on_minigame_completion, on_minigame_death)

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

def draw_point_tracker(screen):
    """Draw the point tracker at the top left of the screen"""
    points_text = f"Wisdom Points: {player_points}"
    points_surface = points_font.render(points_text, True, (255, 255, 255))  # White text
    # Add a semi-transparent background for better visibility
    bg_rect = pygame.Rect(5, 5, points_surface.get_width() + 10, points_surface.get_height() + 10)
    pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)  # Semi-transparent black background
    screen.blit(points_surface, (10, 10))


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

# Create Naval NPC instance at a different location
naval_npc_x = random.randint(600, 1000)
naval_npc_y = random.randint(500, 850)
naval_npc = NavalNPC(naval_npc_x, naval_npc_y, interaction_radius=40)

# Create Mysterious Rectangle in top-right corner of map
mysterious_rect_x = map_width - 250  # 100 pixels from right edge
mysterious_rect_y = 200  # 50 pixels from top edge
mysterious_rect = MysteriousRect(mysterious_rect_x, mysterious_rect_y, width=60, height=60, interaction_radius=50)

# Initialize Interaction Manager
interaction_manager = InteractionManager()
interaction_manager.add_interactable(wizard)
interaction_manager.add_interactable(naval_npc)
interaction_manager.add_interactable(mysterious_rect)
# Add other NPCs to interaction_manager here as they are created

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(wizard) # Add wizard to the sprite group
all_sprites.add(naval_npc) # Add naval NPC to the sprite group
# Add other NPCs to all_sprites here


# Camera properties
game_camera = Camera(screen_width, screen_height) # Create Camera instance

# Game loop
running = True
last_direction_keydown_event = None # Added to track the last directional key event
while running:
    current_time_ticks = pygame.time.get_ticks() # Get current time once per frame for typing
    
    for event in pygame.event.get():        # Handle chat events first - if chat is active, it should have priority
        if not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
            if wizard_chat_manager.handle_event(event):
                continue  # Skip other event processing if chat handled the event
        
        # Handle quiz events
        if not minigame_manager.should_disable_main_game_elements():
            if quiz_manager.handle_event(event):
                continue  # Skip other event processing if quiz handled the event
        
        # Handle settings manager events
        if not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if settings_manager.handle_click(event.pos):
                        continue  # Skip other event processing if settings handled the event
                  # Handle settings manager keyboard input
            if settings_manager.handle_key_input(event):
                continue  # Skip other event processing if settings handled the event
        
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.USEREVENT + 1:  # Completion callback
            if minigame_manager.completion_callback:
                minigame_manager.completion_callback(minigame_manager.pending_collectible_points)
            # Now actually end the minigame
            minigame_manager.is_active = False
            minigame_manager.minigame_completed = False
            player_can_move = True
            show_interaction_popup = False
            typing_active = False
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        elif event.type == pygame.USEREVENT + 2:  # Death callback
            if minigame_manager.player_death_callback:
                minigame_manager.player_death_callback()
            # Now actually end the minigame
            minigame_manager.is_active = False
            minigame_manager.minigame_completed = False
            player_can_move = True
            show_interaction_popup = False
            typing_active = False
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements(): 
                # ESC now opens settings instead of exiting
                if not settings_manager.is_popup_active:
                    settings_manager.is_popup_active = True
                    settings_manager._close_input_fields()
                else:
                    settings_manager.is_popup_active = False
                    settings_manager._close_input_fields()

            elif event.key == pygame.K_F1:  # F1 to toggle debug
                if minigame_manager.is_active:
                    minigame_manager.toggle_debug_mode()
                player_points += 1  

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
            
            last_direction_keydown_event = event.key 

            if show_interaction_popup and eligible_interactable:
                if event.key == pygame.K_e: 
                    if eligible_interactable.id == "wizard":
                        # Use the wizard instance directly
                        current_wizard_message = wizard.interaction_message
                        if wizard.is_fetching_joke:
                            print("Wizard is still thinking...")
                            # Typing for "thinking..." is handled by the main typing logic
                        elif wizard.interaction_message == wizard.prompt_talk:
                            # Initial E press, message is the "talk" prompt
                            print(f"E pressed. Requesting joke from Wizard.")
                            wizard.request_new_joke()
                            # Popup remains, player cannot move. Typing will be triggered by wizard.new_message_to_type.
                        else: # Implies joke/result is displayed (not fetching, not initial prompt_talk)
                            # Joke/result displayed, E means "Visit The Wizard"
                            print(f"E pressed. Visiting Wizard's House.")
                            interaction_manager.set_interacted_flag(wizard.id, True)
                            show_interaction_popup = False
                            player_can_move = True
                            typing_active = False # Stop any typing
                            map_manager.switch_map(
                                "wizard_house", 
                                player, 
                                wizard,                 
                                all_sprites,            
                                interaction_manager,    
                                update_map_dimensions_from_manager                            )
                            wizard.reset_interaction_state() # Reset for next time on main map
                            print("Teleported to Wizard's House.")
                    
                    elif eligible_interactable.id == "wizard_house_stay_query_circle":
                        print(f"E pressed. Starting conversation with Wizard.")
                        # Start conversation with the wizard
                        interaction_manager.set_interacted_flag(eligible_interactable.id, True)
                        show_interaction_popup = False
                        player_can_move = False  # Disable player movement during chat
                        typing_active = False
                        wizard_chat_manager.start_conversation()
                    
                    elif eligible_interactable.id.startswith("naval_npc"):
                        print(f"E pressed. Talking to Naval.")
                        if naval_npc.check_points_and_interact(player_points):
                            # Player has enough points - normal interaction will proceed
                            pass
                        else:
                            # Player doesn't have enough points - show popup
                            naval_npc.show_insufficient_points_message()
                    
                    elif eligible_interactable.id.startswith("mysterious_rect"):
                        print(f"E pressed. Interacting with Mysterious Rectangle.")
                        # Request new AI response from the Mysterious Rectangle
                        mysterious_rect.request_new_response()
                        # Popup remains active, typing will be triggered by mysterious_rect.new_message_to_type
                elif event.key == pygame.K_q: 
                    print(f"Q pressed with eligible interactable: {eligible_interactable.id if eligible_interactable else 'None'}.")
                    if eligible_interactable:
                        if eligible_interactable.id == "wizard":
                            print(f"Q pressed. Moving on from Wizard.")
                            interaction_manager.set_interacted_flag(wizard.id, True)
                            show_interaction_popup = False
                            player_can_move = True
                            typing_active = False # Stop typing
                            wizard.reset_interaction_state() # Reset wizard's state
                        elif eligible_interactable.id == "wizard_house_stay_query_circle":
                            print(f"Q pressed. Returning to Main Map from Wizard's House.")
                            interaction_manager.set_interacted_flag(eligible_interactable.id, True) # Mark as interacted
                            show_interaction_popup = False
                            player_can_move = True
                            typing_active = False # Stop typing
                            map_manager.switch_map(
                                "main_map", 
                                player, 
                                wizard, 
                                all_sprites, 
                                interaction_manager, 
                                update_map_dimensions_from_manager
                            )
                            player_target_x_center = wizard.static_interaction_center[0]
                            player_target_y_bottom = wizard.static_interaction_center[1] + wizard.interaction_radius + 100 # 10px buffer below circle
                            
                            player.rect.centerx = player_target_x_center
                            player.rect.bottom = player_target_y_bottom

                            wizard.reset_interaction_state() # Also reset main map wizard if returning
                            print("Returning to Main Map from Wizard's House via Q key.")
                        elif eligible_interactable.id == "wizard_in_house":
                            print(f"Q pressed. Leaving conversation with Wizard in House.")
                            show_interaction_popup = False
                            player_can_move = True
                            typing_active = False # Stop typing
                            # Potentially reset wizard_in_house state if it has one
                            # wizard_in_house.reset_interaction_state() # If applicable
                        elif eligible_interactable.id.startswith("naval_npc"):
                            print(f"Q pressed. Moving on from Naval Officer.")
                            interaction_manager.set_interacted_flag(eligible_interactable.id, True)
                            show_interaction_popup = False
                            player_can_move = True
                            typing_active = False # Stop typing
                            naval_npc.reset_interaction_state() # Reset naval NPC's state
                        
                        elif eligible_interactable.id.startswith("mysterious_rect"):
                            print(f"Q pressed. Moving on from Mysterious Rectangle.")
                            interaction_manager.set_interacted_flag(eligible_interactable.id, True)
                            show_interaction_popup = False
                            player_can_move = True
                            typing_active = False # Stop typing
                            mysterious_rect.reset_interaction_state() # Reset mysterious rectangle's state
    
    # Handle chat state changes - restore player movement when chat ends
    if not wizard_chat_manager.is_active and not player_can_move and not show_interaction_popup:
        player_can_move = True
        print("Chat ended, restoring player movement")
        
    keys = pygame.key.get_pressed()
    
    # Update settings manager with current mouse state
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    settings_manager.update_mouse_state(mouse_pos, mouse_clicked)

    # Update settings manager with current points
    settings_manager.set_current_points(player_points)
    
    if player_can_move and not wizard_chat_manager.is_active and not settings_manager.show_input_fields and not quiz_manager.is_active:
        player.update_position(keys, map_width, map_height, last_direction_keydown_event, map_manager.can_move)        # Check for item collection after player movement
        if map_manager.current_map_data["name"] == "main_map":  # Only on main map
            if tilemap.collect_item(player.rect.centerx, player.rect.centery+10, map_manager.get_current_tile_size()):
                # Random chance to trigger minigame or quiz
                rand_chance = random.random()
                if rand_chance < 0.8:  # 80% chance for quiz
                    print("Quiz triggered!")
                    quiz_manager.start_quiz(1)  # 1 point for this collectible
                elif rand_chance < 0.9:  # 10% chance for minigame (0.3 to 0.6)
                    print("Minigame triggered!")
                    minigame_manager.start_minigame(1, player.rect)  # 1 point for this collectible
                    map_manager.switch_to_minigame(player, all_sprites, interaction_manager, update_map_dimensions_from_manager)
                else:                    # Normal collectible collection (40% chance)
                    player_points += 1
                    print(f"Item collected! Points: {player_points}")
    
    # Update collectibles system (respawn timers) - only if not in minigame or quiz
    if map_manager.current_map_data["name"] == "main_map" and not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
        tilemap.update_collectibles()

    # Update interaction manager - only if not in minigame or quiz
    if not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
        interaction_manager.update(player.rect.center)

    if minigame_manager.is_active:
        minigame_manager.update(player.rect, map_width, map_height)
    
    # Update quiz manager
    quiz_manager.update()
    
    # Handle interactions - only if not in minigame or quiz
    if not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
        eligible_interactable = interaction_manager.get_eligible_interactable()
        if eligible_interactable:
            if not show_interaction_popup: 
                show_interaction_popup = True
                player_can_move = False 
                print(f"Player entered {eligible_interactable.id}'s interaction circle. Popup shown.")            # Check if we need to start typing a new message immediately
            if eligible_interactable.id == "wizard" and wizard.new_message_to_type:
                props = wizard.get_interaction_properties() # Get current message
                text_to_type_full = props['message']
                typed_text_display = "" # Start with one char to avoid empty split issues if first char is newline
                typing_char_index = 0
                typing_last_char_time = current_time_ticks 
                typing_active = True
                wizard.new_message_to_type = False # Consume the flag
            elif eligible_interactable.id.startswith("naval_npc") and naval_npc.new_message_to_type:
                props = naval_npc.get_interaction_properties() # Get current message
                text_to_type_full = props['message']
                typed_text_display = ""
                typing_char_index = 0
                typing_last_char_time = current_time_ticks 
                typing_active = True
                naval_npc.new_message_to_type = False # Consume the flag
            elif eligible_interactable.id.startswith("mysterious_rect") and mysterious_rect.new_message_to_type:
                props = mysterious_rect.get_interaction_properties() # Get current message
                text_to_type_full = props['message']
                typed_text_display = ""
                typing_char_index = 0
                typing_last_char_time = current_time_ticks 
                typing_active = True
                mysterious_rect.new_message_to_type = False # Consume the flag

    elif show_interaction_popup: # No eligible interactable, but popup is shown
        show_interaction_popup = False
        player_can_move = True
        typing_active = False # Stop typing if popup is hidden
        # print("Popup hidden because no eligible interactable or player moved away.")

    # Handle typewriter effect for active popup
    if typing_active and show_interaction_popup:
        if current_time_ticks - typing_last_char_time > TYPING_DELAY_MS:
            if typing_char_index < len(text_to_type_full):
                typed_text_display += text_to_type_full[typing_char_index]
                typing_char_index += 1
                typing_last_char_time = current_time_ticks
            else:
                typing_active = False # Typing finished    # Check if wizard has a new message to type (e.g., after thinking) - only if not in minigame or quiz
    if show_interaction_popup and eligible_interactable and eligible_interactable.id == "wizard" and not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
        if wizard.new_message_to_type and not typing_active: # Start typing if new message and not already typing
            props = wizard.get_interaction_properties()
            text_to_type_full = props['message']
            typed_text_display = ""
            typing_char_index = 0
            typing_last_char_time = current_time_ticks
            typing_active = True
            wizard.new_message_to_type = False      # Check if naval_npc has a new message to type (e.g., after thinking) - only if not in minigame or quiz
    if show_interaction_popup and eligible_interactable and eligible_interactable.id.startswith("naval_npc") and not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
        if naval_npc.new_message_to_type and not typing_active: # Start typing if new message and not already typing
            props = naval_npc.get_interaction_properties()
            text_to_type_full = props['message']
            typed_text_display = ""
            typing_char_index = 0
            typing_last_char_time = current_time_ticks
            typing_active = True
            naval_npc.new_message_to_type = False
      # Check if mysterious_rect has a new message to type (e.g., after thinking) - only if not in minigame or quiz
    if show_interaction_popup and eligible_interactable and eligible_interactable.id.startswith("mysterious_rect") and not minigame_manager.should_disable_main_game_elements() and not quiz_manager.should_disable_main_game_elements():
        if mysterious_rect.new_message_to_type and not typing_active: # Start typing if new message and not already typing
            props = mysterious_rect.get_interaction_properties()
            text_to_type_full = props['message']
            typed_text_display = ""
            typing_char_index = 0
            typing_last_char_time = current_time_ticks
            typing_active = True
            mysterious_rect.new_message_to_type = False

    game_camera.update(player, map_width, map_height)
      # Update sprites - only update NPCs if not in minigame
    if not minigame_manager.should_disable_main_game_elements():
        if map_manager.current_map_name == "main_map":
            # Main map: update both player and NPCs
            naval_npc.set_update_parameters(map_width, map_height, map_manager.can_move, player)
            all_sprites.update()
        else:
            # Other maps (wizard house): only update player and map-specific entities
            player.update()
            # Update any map-specific NPCs here if they exist
    else:
        # During minigame, only update the player
        player.update()

    # Fill the screen with white
    screen.fill((173, 216, 230))

    # Draw the tilemap using the MapManager's current map data
    # tilemap.draw_map(screen, game_camera) # OLD WAY
    # NEW WAY: Pass necessary data from map_manager to tilemap.draw_map
    current_map_layout = map_manager.get_current_map_layout()
    current_building_layout = map_manager.get_current_building_layout()
    current_decoration_layout = map_manager.get_current_decoration_layout() # ADDED
    current_tile_size = map_manager.get_current_tile_size()
    tilemap.draw_map(screen, game_camera, current_map_layout, current_building_layout, current_decoration_layout, current_tile_size) # Draw all sprites (adjusting for camera)
    
    # Draw minigame elements if active
    if minigame_manager.is_active and map_manager.current_map_name == "minigame_arena":
        # Draw countdown timer
        remaining_time = minigame_manager.get_remaining_time()
        timer_text = f"Survive: {remaining_time}s"
        timer_surface = pygame.font.Font(None, 60).render(timer_text, True, (255, 0, 0))
        screen.blit(timer_surface, (screen_width // 2 - timer_surface.get_width() // 2, 70))
        
        # Draw hazards
        for hazard in minigame_manager.hazards:
            hazard_screen_pos = game_camera.apply_point((hazard.x, hazard.y))
            pygame.draw.circle(screen, (255, 0, 0), hazard_screen_pos, 20)
            
        # Draw debug collision areas
        minigame_manager.draw_debug_info(screen, player.rect, game_camera)
        
        # Draw speed popup
        minigame_manager.draw_speed_popup(screen)

    minigame_manager.draw_result_popup(screen)
    
    # Draw sprites - conditionally disable NPCs during minigame
    for sprite in all_sprites:        # Skip NPCs during minigame, but always draw the player
        if minigame_manager.should_disable_main_game_elements() and hasattr(sprite, 'id') and sprite.id != "player":
            continue
            
        if (hasattr(sprite, 'id') and sprite.id.startswith("naval_npc") and 
            map_manager.current_map_name == "wizard_house"):
            continue

        screen.blit(sprite.image, game_camera.apply(sprite))      # Draw NavalNPC speech bubbles - only if not in minigame

    # Draw NavalNPC speech bubbles - only if not in minigame
    if map_manager.current_map_name != "wizard_house" and not minigame_manager.should_disable_main_game_elements():
        naval_npc.draw_speech_bubble(screen, game_camera)

    # Draw Mysterious Rectangle - only if not in minigame and on main map
    if map_manager.current_map_name == "main_map" and not minigame_manager.should_disable_main_game_elements():
        mysterious_rect.draw(screen, game_camera, player.rect.center)

    # Draw interaction circles - only if not in minigame
    if not minigame_manager.should_disable_main_game_elements():
        
        # Draw naval NPC insufficient points popup - only if not in minigame
        naval_npc.draw_insufficient_points_popup(screen)
        
        for interactable_obj in interaction_manager.get_all_interactables():
            if not interaction_manager.get_interacted_flag(interactable_obj.id):
                props = interactable_obj.get_interaction_properties()

            # Skip both naval_npc AND mysterious_rect
            if props['id'].startswith("naval_npc") or props['id'].startswith("mysterious_rect"):
                continue

            # Draw circles only for other interactables (like wizard)
            circle_center_vec = pygame.math.Vector2(props['center'])
            circle_draw_center_x_on_screen = circle_center_vec.x + game_camera.camera.x
            circle_draw_center_y_on_screen = circle_center_vec.y + game_camera.camera.y
            pygame.draw.circle(screen, props['color'],
                            (int(circle_draw_center_x_on_screen), int(circle_draw_center_y_on_screen)),
                            props['radius'], props['thickness'])   
             
    if show_interaction_popup and eligible_interactable and not minigame_manager.should_disable_main_game_elements():
        current_message_for_popup = ""
        if typing_active:
            # Check if interactable needs custom typing
            props = eligible_interactable.get_interaction_properties()
            if props.get("needs_custom_typing") and hasattr(eligible_interactable, 'get_typing_message'):
                current_message_for_popup = eligible_interactable.get_typing_message(len(typed_text_display), screen_width)
            else:
                current_message_for_popup = typed_text_display
        else:
            # For non-typing display
            props = eligible_interactable.get_interaction_properties()
            if props.get("needs_custom_display") and hasattr(eligible_interactable, 'get_display_message'):
                current_message_for_popup = eligible_interactable.get_display_message(screen_width)
            else:
                current_message_for_popup = props['message']
        
        popup_text_lines = current_message_for_popup.split('\n')
        
        # Calculate total height and max width for the background
        line_height = interaction_font.get_linesize()
        total_text_height = len(popup_text_lines) * line_height
        
        rendered_lines = []
        max_line_width = 0
        for line in popup_text_lines:
            text_surface = interaction_font.render(line, True, (0, 0, 0)) # Black text
            rendered_lines.append(text_surface)
            if text_surface.get_width() > max_line_width:
                max_line_width = text_surface.get_width()

        # Optional: Add a background to the popup text for better visibility
        # Position the background box
        popup_bg_rect_width = max_line_width + 20 # Add padding
        popup_bg_rect_height = total_text_height + 10 # Add padding
        popup_bg_rect_x = (screen_width - popup_bg_rect_width) // 2
        popup_bg_rect_y = screen_height - popup_bg_rect_height - 40 # Position near bottom, adjust 40 as needed
        
        main_popup_bg_rect = pygame.Rect(popup_bg_rect_x, popup_bg_rect_y, popup_bg_rect_width, popup_bg_rect_height)
        pygame.draw.rect(screen, (200, 200, 200), main_popup_bg_rect) # Light grey background
        pygame.draw.rect(screen, (0, 0, 0), main_popup_bg_rect, 2) # Black border

        # Blit each line
        current_y = main_popup_bg_rect.top + 5 # Start y for the first line (inside the padding)
        for text_surface in rendered_lines:
            text_rect = text_surface.get_rect(centerx=main_popup_bg_rect.centerx, top=current_y)
            screen.blit(text_surface, text_rect)
            current_y += line_height

        # --- BEGIN: Draw second, non-typewritten popup for wizard's E/Q options ---
        if eligible_interactable.id == "wizard" and \
           not wizard.is_fetching_joke and \
           wizard.interaction_message != wizard.prompt_talk:

            second_popup_text_content = wizard.prompt_visit_or_leave
            second_popup_lines = second_popup_text_content.split('\n')
            
            second_total_text_height = len(second_popup_lines) * line_height
            
            second_rendered_lines = []
            second_max_line_width = 0
            for line in second_popup_lines:
                text_surface = interaction_font.render(line, True, (0, 0, 0)) # Black text
                second_rendered_lines.append(text_surface)
                if text_surface.get_width() > second_max_line_width:
                    second_max_line_width = text_surface.get_width()

            second_popup_bg_rect_width = second_max_line_width + 20 # Padding
            second_popup_bg_rect_height = second_total_text_height + 10 # Padding
            
            second_popup_bg_rect_x = (screen_width - second_popup_bg_rect_width) // 2
            # Position second popup above the main one
            second_popup_bg_rect_y = main_popup_bg_rect.top - second_popup_bg_rect_height - 10 # 10px spacing above main popup

            second_popup_bg_rect = pygame.Rect(second_popup_bg_rect_x, second_popup_bg_rect_y, second_popup_bg_rect_width, second_popup_bg_rect_height)
            pygame.draw.rect(screen, (220, 220, 200), second_popup_bg_rect) # Slightly different background
            pygame.draw.rect(screen, (0, 0, 0), second_popup_bg_rect, 2) # Black border

            current_y_second = second_popup_bg_rect.top + 5 # Start y for the first line
            for text_surface in second_rendered_lines:
                text_rect = text_surface.get_rect(centerx=second_popup_bg_rect.centerx, top=current_y_second)
                screen.blit(text_surface, text_rect)
                current_y_second += line_height        # --- END: Draw second popup ---    # Draw chat interface if active - only if not in minigame
    
    if not minigame_manager.should_disable_main_game_elements():
        wizard_chat_manager.draw(screen)
    
    # Draw settings interface - only if not in minigame
    if not minigame_manager.should_disable_main_game_elements():
        settings_manager.draw(screen)
    
    # Draw quiz interface - only if not in minigame
    if not minigame_manager.should_disable_main_game_elements():
        quiz_manager.draw(screen)
    
    # Draw point tracker
    draw_point_tracker(screen)
    


    # Update the display
    pygame.display.flip()

    # Cap the framerate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit() # Exit using sys.exit()
