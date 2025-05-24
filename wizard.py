import pygame
from entity import Entity

class Wizard(Entity):
    def __init__(self, x, y, interaction_radius=30, interaction_offset_y=28):
        # Entity's __init__ loads the image and sets self.image and self.rect
        super().__init__(x, y, "images/npcs/theWizard.png")
        self.id = "wizard" # Unique ID for this interactable

        # Scale the loaded image to player's dimensions (e.g., 128x128)
        player_size = (84, 128) # Assuming player size is 128x128
        self.image_right = pygame.transform.scale(self.image, player_size)
        self.image_left = pygame.transform.flip(self.image_right, True, False) # Flip horizontally

        self.facing_right = True # Initial facing direction
        self.image = self.image_right # Set current image to the scaled right-facing one

        # Update rect with the new scaled image and position
        # current_center = self.rect.center # Preserve center if needed, or just top-left
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # Reset position based on initial x, y

        # Timer for changing direction
        self.last_flip_time = pygame.time.get_ticks()
        self.flip_interval = 3000 # 3 seconds in milliseconds

        # Interaction properties
        self.interaction_radius = interaction_radius
        # Calculate the static center of the interaction circle based on initial wizard position
        self.interaction_center_x = self.rect.centerx
        self.interaction_center_y = self.rect.bottom + interaction_offset_y # Offset below the wizard
        self.static_interaction_center = (self.interaction_center_x, self.interaction_center_y)
        self.interaction_message = "Press E to Talk to The Wizard. Press Q to Move On"


    def get_interaction_properties(self):
        """Returns a dictionary of properties needed for interaction management."""
        return {
            "id": self.id,
            "center": self.static_interaction_center, # Use the pre-calculated static center
            "radius": self.interaction_radius,
            "message": self.interaction_message,
            "color": (135, 206, 250),  # LightSkyBlue
            "thickness": 3
        }

    def update(self, *args): # Accept *args to be compatible with Group.update()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flip_time > self.flip_interval:
            self.facing_right = not self.facing_right # Toggle direction
            
            if self.facing_right:
                self.image = self.image_right
            else:
                self.image = self.image_left
            
            # When the image changes, its dimensions might change if they are not uniform.
            # The rect needs to be updated to reflect the new image,
            # and its position (e.g., center) should be preserved.
            old_center = self.rect.center
            self.rect = self.image.get_rect() # Rect is already based on scaled images
            self.rect.center = old_center
            
            self.last_flip_time = current_time # Reset timer
