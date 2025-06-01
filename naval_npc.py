import pygame
import random
import textwrap
from entity import Entity

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
        self.current_speech = "Exchange 5 points for timeless wisdom?"
        self.speech_bubble_offset_y = -40  # Above the NPC
        
        # Interaction properties
        self.interaction_radius = interaction_radius
        self.interaction_center_x = self.rect.centerx
        self.interaction_center_y = self.rect.bottom
        self.static_interaction_center = (self.interaction_center_x, self.interaction_center_y)
        
        self.prompt_talk = "Press E to Interact with Naval. Press Q to Walk Away."
        self.interaction_message = "Hi"  # Simple static message
        self.new_message_to_type = False  # For consistency with interaction system
    
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
        self.interaction_message = "Hi"
        self.new_message_to_type = False

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