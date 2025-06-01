import pygame
import random
import textwrap
from entity import Entity
from databaseHandler import DatabaseHandler


class NavalNPC(Entity):
    def __init__(self, x, y, interaction_radius=50):
        # Entity's __init__ loads the image and sets self.image and self.rect
        super().__init__(x, y, "images/npcs/navalSprite.png")
        self.id = f"naval_npc_{x}_{y}"  # Unique ID for this interactable
        
        # Scale the loaded image to appropriate dimensions
        npc_size = (84, 128)  # Similar to wizard size
        self.image_right = pygame.transform.scale(self.image, npc_size)
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        
        self.facing_right = True
        self.image = self.image_right
        
        # Update rect with the new scaled image and position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement properties
        self.speed = 2  # Slower than player
        self.movement_direction = random.choice(['up', 'down', 'left', 'right', 'idle'])
        self.movement_timer = 0
        self.movement_duration = random.randint(60, 600)  # Frames to move in current direction
        self.idle_timer = 0
        self.idle_duration = random.randint(60, 300)  # Frames to stay idle
        
        # Speaking properties
        self.speaking_timer = 0
        self.speaking_interval = random.randint(300,480) 
        self.is_speaking = False
        self.speech_duration = 300 
        self.current_speech = "Exchange 5 points for some timeless wisdom?"
        self.speech_bubble_offset_y = -40  # Above the NPC
        
        # Interaction properties
        self.interaction_radius = interaction_radius
        self.interaction_center_x = self.rect.centerx
        self.interaction_center_y = self.rect.bottom
        self.static_interaction_center = (self.interaction_center_x, self.interaction_center_y)
        
        self.interaction_message = "Press E to Interact with Naval. Press Q to Walk Away."  # Simple static message
        self.new_message_to_type = False  # For consistency with interaction system

        # Point check popup system
        self.show_insufficient_points_popup = False
        self.popup_start_time = 0
        self.popup_duration = 4000  # 4 seconds in milliseconds
        self.popup_message = "Come back when you have at least 5 points bro..."

        # Quote popup system
        self.show_quote_popup = False
        self.quote_popup_start_time = 0
        self.quote_popup_duration = 6000  # 6 seconds in milliseconds
        self.current_quote = ""

        # Quote tracking
        self.settings_manager = None  # Will be set from main
        self.available_quote_ids = list(range(1, 6))  # [1, 2, 3, 4, 5]
    
        # Initialize database handler
        try:
            self.db_handler = DatabaseHandler()
        except Exception as e:
            print(f"Failed to initialize database handler for naval NPC: {e}")
            self.db_handler = None
        
        # Point deduction callback
        self.point_deduction_callback = None
    
    def update(self):
        """Basic update method for pygame sprite system"""
        # This method is called by all_sprites.update() and should not require parameters
        # Check if we have the necessary parameters stored
        if hasattr(self, '_stored_map_width') and hasattr(self, '_stored_map_height') and hasattr(self, '_stored_collision_func'):
            self.update_ai_behavior(self._stored_map_width, self._stored_map_height, self._stored_collision_func)
    
    def set_update_parameters(self, map_width, map_height, collision_check_func, player_sprite=None):
        """Store parameters for the basic update method"""
        self._stored_map_width = map_width
        self._stored_map_height = map_height
        self._stored_collision_func = collision_check_func
        self._stored_player_sprite = player_sprite 

    def update_ai_behavior(self, map_width, map_height, collision_check_func):
        """Update NPC movement, speaking, and other behaviors"""
        current_time = pygame.time.get_ticks()
        
        # Update movement
        self._update_movement(map_width, map_height, collision_check_func,
                              getattr(self, '_stored_player_sprite', None))
        
        # Update speaking behavior
        self._update_speaking()
        
        # Update popup timer
        self.update_popup()
        
        # Update interaction center when NPC moves
        self.interaction_center_x = self.rect.centerx
        self.interaction_center_y = self.rect.bottom - 40
        self.static_interaction_center = (self.interaction_center_x, self.interaction_center_y)

    def _update_movement(self, map_width, map_height, collision_check_func, player_sprite=None):
        """Handle AI movement logic"""
        if self.movement_direction == 'idle':
            self.idle_timer += 1
            if self.idle_timer >= self.idle_duration:
                # Choose new movement direction
                self.movement_direction = random.choice(['up', 'down', 'left', 'right', 'idle'])
                self.movement_timer = 0
                self.movement_duration = random.randint(60, 180)
                self.idle_timer = 0
                self.idle_duration = random.randint(30, 120)
        else:
            self.movement_timer += 1
            
            # Calculate movement delta
            dx, dy = 0, 0
            if self.movement_direction == 'up':
                dy = -self.speed
            elif self.movement_direction == 'down':
                dy = self.speed
            elif self.movement_direction == 'left':
                dx = -self.speed
                if self.facing_right:
                    self.facing_right = False
                    self.image = self.image_left
            elif self.movement_direction == 'right':
                dx = self.speed
                if not self.facing_right:
                    self.facing_right = True
                    self.image = self.image_right
            
            # Check collision before moving
            future_x = self.rect.x + dx
            future_y = self.rect.y + dy
            
            can_move = True

            if player_sprite:
                temp_rect = self.rect.copy()
                temp_rect.x = future_x
                temp_rect.y = future_y
                if temp_rect.colliderect(player_sprite.rect):
                    can_move = False

            if collision_check_func:
                # Check collision at key points (similar to player collision detection)
                npc_w = self.rect.width
                npc_h = self.rect.height
                
                # Check lower half collision points
                y_lower_half_top = future_y + npc_h // 2
                y_lower_half_bottom = future_y + npc_h - 1
                horizontal_offset = npc_w // 3
                x_collision_left = future_x + horizontal_offset
                x_collision_right = future_x + npc_w - 1 - horizontal_offset
                x_center = future_x + npc_w // 2
                
                # Check collision points
                if not collision_check_func(x_collision_left, y_lower_half_bottom):
                    can_move = False
                elif not collision_check_func(x_collision_right, y_lower_half_bottom):
                    can_move = False
                elif not collision_check_func(x_center, y_lower_half_bottom):
                    can_move = False
                elif not collision_check_func(x_collision_left, y_lower_half_top):
                    can_move = False
                elif not collision_check_func(x_collision_right, y_lower_half_top):
                    can_move = False
            
            # Apply movement if no collision
            if can_move:
                self.rect.x = future_x
                self.rect.y = future_y
                
                # Boundary checks
                self.rect.x = max(0, min(self.rect.x, map_width - self.rect.width))
                self.rect.y = max(0, min(self.rect.y, map_height - self.rect.height))
            else:
                # Change direction if blocked
                self.movement_direction = random.choice(['up', 'down', 'left', 'right', 'idle'])
                self.movement_timer = 0
                self.movement_duration = random.randint(60, 180)
            
            # Change direction after duration
            if self.movement_timer >= self.movement_duration:
                self.movement_direction = random.choice(['up', 'down', 'left', 'right', 'idle'])
                self.movement_timer = 0
                self.movement_duration = random.randint(60, 180)

    def _update_speaking(self):
        """Handle simple speech bubble display"""
        # Update speech timer
        self.speaking_timer += 1
        
        # Check if it's time to show speech bubble
        if not self.is_speaking and self.speaking_timer >= self.speaking_interval:
            self.is_speaking = True
            self.speech_duration = 300  # 5 seconds at 60 FPS
            self.speaking_timer = 0
            self.speaking_interval = random.randint(240, 480)  # 4-8 seconds at 60 FPS
          # Handle speech duration
        if self.is_speaking:
            self.speech_duration -= 1
            if self.speech_duration <= 0:
                self.is_speaking = False

    def reset_interaction_state(self):
        """Reset the NPC's interaction state"""
        self.interaction_message = "Press E to Interact with Naval. Press Q to Walk Away."
        self.new_message_to_type = False

    def check_points_and_interact(self, player_points):
        """Check if player has enough points and set appropriate interaction state"""
        if player_points >= 5:
            # Player has enough points - fetch and show quote
            self._fetch_and_show_quote()
            return True  # Sufficient points
        else:
            # Player doesn't have enough points - trigger error popup
            return False  # Insufficient points

    def set_settings_manager(self, settings_manager):
        """Set reference to settings manager for user tracking."""
        self.settings_manager = settings_manager

    def _get_available_quotes(self):
        """Get list of quote IDs that haven't been unlocked yet."""
        if not self.settings_manager:
            return self.available_quote_ids  # Return all if no user tracking
        
        unlocked_quotes = self.settings_manager.get_unlocked_quotes()
        available = [qid for qid in self.available_quote_ids if qid not in unlocked_quotes]
        return available

    def _fetch_and_show_quote(self):
        """Fetch a random quote from database and show quote popup"""
        if not self.db_handler:
            print("Error: No database connection for naval NPC")
            return
        
        # Get available quotes (not yet unlocked)
        available_quotes = self._get_available_quotes()
        
        if not available_quotes:
            # All quotes unlocked - show special message
            self.current_quote = "You have unlocked all of my wisdom, young seeker. Return when new knowledge arrives."
            self.show_quote_popup = True
            self.quote_popup_start_time = pygame.time.get_ticks()
            print("All naval quotes already unlocked!")
            return
            
        try:
            # Get random quote from available ones
            quote_id = random.choice(available_quotes)
            
            # Fetch quote from naval_quotes collection
            quote_doc = self.db_handler.read_document("naval_quotes", str(quote_id))
            
            if quote_doc and "quote" in quote_doc:
                self.current_quote = quote_doc["quote"]
                self.show_quote_popup = True
                self.quote_popup_start_time = pygame.time.get_ticks()
                
                # Mark quote as unlocked
                if self.settings_manager:
                    self.settings_manager.add_unlocked_quote(quote_id)
                
                # Deduct points through callback
                if self.point_deduction_callback:
                    self.point_deduction_callback(5)
                    
                print(f"Naval quote {quote_id} fetched and unlocked: {self.current_quote[:50]}...")
            else:
                print(f"Error: Could not fetch quote {quote_id} from naval_quotes collection")
                
        except Exception as e:
            print(f"Error fetching naval quote: {e}")

    def set_point_deduction_callback(self, callback):
        """Set callback function to deduct points from main game"""
        self.point_deduction_callback = callback

    def get_interaction_properties(self):
        """Returns interaction properties for the interaction manager"""
        return {
            "id": self.id,
            "center": self.static_interaction_center,
            "radius": self.interaction_radius,
            "message": self.interaction_message,
            "color": (255, 140, 0),  # Dark orange color
            "thickness": 3
        }

    def draw_speech_bubble(self, screen, camera):
        """Draw speech bubble with fixed message"""
        if self.is_speaking and self.current_speech:
            # Calculate speech bubble position relative to camera
            bubble_center_x = self.rect.centerx + camera.camera.x
            bubble_center_y = self.rect.top + self.speech_bubble_offset_y + camera.camera.y
            
            # Render speech text with wrapping
            font = pygame.font.Font(None, 30)
            wrapped_text = textwrap.fill(self.current_speech, width=30)
            speech_lines = wrapped_text.split('\n')
            
            # Calculate bubble dimensions
            line_height = font.get_linesize()
            max_line_width = 0
            rendered_lines = []
            
            for line in speech_lines:
                text_surface = font.render(line, True, (0, 0, 0))
                rendered_lines.append(text_surface)
                if text_surface.get_width() > max_line_width:
                    max_line_width = text_surface.get_width()
            
            bubble_width = max_line_width + 20
            bubble_height = len(speech_lines) * line_height + 10
            
            # Draw bubble background with slight transparency
            bubble_rect = pygame.Rect(
                bubble_center_x - bubble_width // 2,
                bubble_center_y - bubble_height // 2,
                bubble_width,
                bubble_height
            )
            
            # Create a surface for the bubble with alpha
            bubble_surface = pygame.Surface((bubble_width, bubble_height))
            bubble_surface.set_alpha(240)  # Slight transparency
            bubble_surface.fill((255, 255, 200))  # Light yellow background
            screen.blit(bubble_surface, bubble_rect.topleft)
            
            pygame.draw.rect(screen, (100, 100, 100), bubble_rect, 2)  # Gray border
            
            # Draw speech text
            current_y = bubble_rect.top + 5
            for text_surface in rendered_lines:
                text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
                screen.blit(text_surface, text_rect)
                current_y += line_height

    def update_popup(self):
        """Update popup timer and visibility"""
        current_time = pygame.time.get_ticks()
        
        # Update insufficient points popup
        if self.show_insufficient_points_popup:
            if current_time - self.popup_start_time >= self.popup_duration:
                self.show_insufficient_points_popup = False
        
        # Update quote popup
        if self.show_quote_popup:
            if current_time - self.quote_popup_start_time >= self.quote_popup_duration:
                self.show_quote_popup = False
                self.current_quote = ""
                
    def show_insufficient_points_message(self):
        """Show the insufficient points popup"""
        self.show_insufficient_points_popup = True
        self.popup_start_time = pygame.time.get_ticks()

    def draw_insufficient_points_popup(self, screen):
        """Draw insufficient points popup"""
        if not self.show_insufficient_points_popup:
            return
            
        # Create popup similar to minigame result popup
        font = pygame.font.Font(None, 48)
        text_surface = font.render(self.popup_message, True, (255, 255, 255))
        
        # Background dimensions
        padding = 30
        bg_width = text_surface.get_width() + padding * 2
        bg_height = text_surface.get_height() + padding * 2
        
        # Center on screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        bg_x = (screen_width - bg_width) // 2
        bg_y = (screen_height - bg_height) // 3  # Upper third of screen
        
        # Draw background
        bg_surface = pygame.Surface((bg_width, bg_height))
        bg_surface.fill((50, 50, 50))  # Dark background
        screen.blit(bg_surface, (bg_x, bg_y))
        
        # Draw border
        border_rect = pygame.Rect(bg_x - 2, bg_y - 2, bg_width + 4, bg_height + 4)
        pygame.draw.rect(screen, (255, 100, 100), border_rect, 4)  # Red border
        
        # Draw text
        text_x = bg_x + padding
        text_y = bg_y + padding
        screen.blit(text_surface, (text_x, text_y))

    def draw_quote_popup(self, screen):
        """Draw quote popup with fetched wisdom"""
        if not self.show_quote_popup or not self.current_quote:
            return
            
        # Create sleek popup for quote display
        font = pygame.font.Font(None, 64)
        
        # Wrap text for better display
        wrapped_text = textwrap.fill(self.current_quote, width=50)
        quote_lines = wrapped_text.split('\n')
        
        # Calculate dimensions
        line_height = font.get_linesize()
        max_line_width = 0
        rendered_lines = []
        
        for line in quote_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            rendered_lines.append(text_surface)
            if text_surface.get_width() > max_line_width:
                max_line_width = text_surface.get_width()
        
        # Background dimensions with padding
        padding = 80
        bg_width = max_line_width + padding * 2
        bg_height = len(quote_lines) * line_height + padding * 2
        
        # Center on screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        bg_x = (screen_width - bg_width) // 2
        bg_y = (screen_height - bg_height) // 2  # Center vertically

        # Draw elegant background
        bg_surface = pygame.Surface((bg_width, bg_height))
        bg_surface.fill((20, 30, 60))  # Dark blue background
        screen.blit(bg_surface, (bg_x, bg_y))
        
        # Draw golden border
        border_rect = pygame.Rect(bg_x - 3, bg_y - 3, bg_width + 6, bg_height + 6)
        pygame.draw.rect(screen, (255, 215, 0), border_rect, 4)  # Gold border
        
        # Draw quote text
        current_y = bg_y + padding
        for text_surface in rendered_lines:
            text_x = bg_x + (bg_width - text_surface.get_width()) // 2  # Center text
            screen.blit(text_surface, (text_x, current_y))
            current_y += line_height
        
        # Draw "Timeless Wisdom" header
        header_font = pygame.font.Font(None, 40)
        header_surface = header_font.render("~ Timeless Wisdom ~", True, (255, 215, 0))
        header_x = bg_x + (bg_width - header_surface.get_width()) // 2
        header_y = bg_y + 10
        screen.blit(header_surface, (header_x, header_y))