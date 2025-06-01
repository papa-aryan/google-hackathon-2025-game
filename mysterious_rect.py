import pygame
import threading
import textwrap
from staticAPI import get_AI_question

class MysteriousRect:
    def __init__(self, x, y, width=60, height=60, interaction_radius=50):
        self.id = f"mysterious_rect_{x}_{y}"  # Unique ID for this interactable
        
        # Rectangle properties
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Bright red
        self.thickness = 3  # Outline thickness

        self.WRAP_WIDTH = 50
        
        # Interaction properties
        self.interaction_radius = interaction_radius
        self.interaction_center_x = self.rect.centerx
        self.interaction_center_y = self.rect.centery
        self.static_interaction_center = (self.interaction_center_x, self.interaction_center_y)
        
        self.prompt_talk = "Press E to interact with the mysterious rectangle. \n Press Q to walk away."
        self.interaction_message = self.prompt_talk
        self.is_fetching_response = False
        self.response_fetch_thread = None
        self.new_message_to_type = False  # AI speaking state

    def request_new_response(self):
        """Request a new AI response for interaction"""
        if not self.is_fetching_response:
            self.is_fetching_response = True
            self.interaction_message = "The rectangle is thinking..."
            self.new_message_to_type = True
            self.response_fetch_thread = threading.Thread(target=self._fetch_and_update_response)
            self.response_fetch_thread.daemon = True
            self.response_fetch_thread.start()

    def _fetch_and_update_response(self):
        """Fetch AI response for interaction (runs in separate thread)"""
        try:
            response = get_AI_question()
            
            if response and response != "Could not fetch a joke.":
                # Store raw response, let get_wrapped_message_for_display() handle wrapping
                self.interaction_message = f"The rectangle asks:\n\"{response}\""
            else:
                self.interaction_message = "The rectangle seems lost in thought. Please try again later."
        except Exception as e:
            print(f"Error fetching AI response for Mysterious Rectangle: {e}")
            self.interaction_message = "The rectangle is having trouble speaking right now."
        finally:
            self.is_fetching_response = False
            self.new_message_to_type = True

    def get_wrapped_message_for_display(self, screen_width):
        """Returns the interaction message properly wrapped for screen display"""
        # First, handle existing manual newlines properly
        lines_from_manual_breaks = self.interaction_message.split('\n')
        final_lines = []
        
        # Use font-based wrapping like QuizManager does
        max_width = screen_width - 120  # Leave margin for popup
        font = pygame.font.Font(None, 72)  # Same as interaction_font
        
        for line in lines_from_manual_breaks:
            if not line.strip():  # Empty line, keep it
                final_lines.append("")
                continue
                
            words = line.split(' ')
            wrapped_lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        wrapped_lines.append(current_line)
                        current_line = word
                    else:
                        wrapped_lines.append(word)
            
            if current_line:
                wrapped_lines.append(current_line)
            
            final_lines.extend(wrapped_lines)
        
        return '\n'.join(final_lines)


    def reset_interaction_state(self):
        """Reset the rectangle's interaction state"""
        self.interaction_message = self.prompt_talk
        self.is_fetching_response = False
        self.new_message_to_type = False

    def get_display_message(self, screen_width):
        """Returns the properly formatted message for display - handles both typing and final display"""
        # Always return wrapped message for display
        return self.get_wrapped_message_for_display(screen_width)

    def get_typing_message(self, typed_length, screen_width):
        """Returns the message formatted for typing display"""
        # Get the full wrapped message
        full_wrapped = self.get_wrapped_message_for_display(screen_width)
        # Return only the portion that should be typed so far
        return full_wrapped[:typed_length]


    def get_interaction_properties(self):
        """Returns interaction properties for the interaction manager"""
        return {
            "id": self.id,
            "center": self.static_interaction_center,
            "radius": self.interaction_radius,
            "message": self.interaction_message,  # Raw message for length calculation
            "needs_custom_display": True,
            "needs_custom_typing": True  # New flag for typing
        }

    def draw(self, screen, camera, player_rect_center=None):
        """Draw the mysterious rectangle with interactive visual feedback"""
        # Calculate screen position with camera offset
        rect_screen_pos = pygame.Rect(
            self.rect.x + camera.camera.x,
            self.rect.y + camera.camera.y,
            self.rect.width,
            self.rect.height
        )
    
        # Change color based on player proximity
        color_to_use = self.color  # Default red
        thickness_to_use = self.thickness  # Default thickness
        
        if player_rect_center:
            player_pos = pygame.math.Vector2(player_rect_center)
            rect_center = pygame.math.Vector2(self.static_interaction_center)
            distance = player_pos.distance_to(rect_center)
            
            if distance < self.interaction_radius:
                color_to_use = (0, 255, 255)  # Cyan when player is near
                thickness_to_use = 5  # Thicker outline when interactive
        
        # Draw only the outline (not filled)
        pygame.draw.rect(screen, color_to_use, rect_screen_pos, thickness_to_use)