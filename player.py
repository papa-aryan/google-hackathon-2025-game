import pygame

from entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "images/rested.png") # Initial image
        # Load all animation images
        self.image_rested = pygame.transform.scale(self.image, (128, 128))
        self.image_up = pygame.transform.scale(pygame.image.load("images/walkingUp.png").convert_alpha(), (128, 128))
        self.image_down = pygame.transform.scale(pygame.image.load("images/walkingDown.png").convert_alpha(), (128, 128))
        self.image_right = pygame.transform.scale(pygame.image.load("images/walkingLeftRight.png").convert_alpha(), (128, 128))
        self.image_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load("images/walkingLeftRight.png").convert_alpha(), (128,128)), True, False)
        self.image = self.image_rested # Set initial image after scaling
        self.rect = self.image.get_rect(topleft=(x,y)) # Update rect with scaled image
        self.speed = 5

    def update_position(self, keys, map_width, map_height, last_direction_keydown_event=None, collision_check_func=None):
        dx, dy = 0, 0
        moved_by_tap = False

        if last_direction_keydown_event and keys[last_direction_keydown_event]:
            if last_direction_keydown_event in [pygame.K_UP, pygame.K_w]:
                dy = -self.speed
                moved_by_tap = True
            elif last_direction_keydown_event in [pygame.K_DOWN, pygame.K_s]:
                dy = self.speed
                moved_by_tap = True
            elif last_direction_keydown_event in [pygame.K_LEFT, pygame.K_a]:
                dx = -self.speed
                moved_by_tap = True
            elif last_direction_keydown_event in [pygame.K_RIGHT, pygame.K_d]:
                dx = self.speed
                moved_by_tap = True
        
        if moved_by_tap:
            if last_direction_keydown_event in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                dx = 0
            elif last_direction_keydown_event in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                dy = 0
        else:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -self.speed
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = self.speed

            if dy == 0:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    dx = -self.speed
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    dx = self.speed
            else:
                dx = 0
        
        new_image_candidate = self.image_rested
        if dy < 0:
            new_image_candidate = self.image_up
        elif dy > 0:
            new_image_candidate = self.image_down
        elif dx < 0:
            new_image_candidate = self.image_left
        elif dx > 0:
            new_image_candidate = self.image_right
        
        if self.image != new_image_candidate:
            self.image = new_image_candidate
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
        # Collision detection
        if collision_check_func:
            # Check future position before actually moving
            future_x = self.rect.x + dx
            future_y = self.rect.y + dy

            # Check collision at points on the lower half of the player's future rect
            player_w = self.rect.width
            player_h = self.rect.height
            
            # Y-coordinates for the lower half
            # The top of the lower half starts at y + height/2
            # The bottom of the lower half is at y + height - 1
            y_lower_half_top = future_y + player_h // 2
            y_lower_half_bottom = future_y + player_h - 1

            # X-coordinates
            x_left = future_x
            x_right = future_x + player_w - 1
            x_center = future_x + player_w // 2
            
            # If any of these points on the lower half collide, stop movement.
            # Point 1: Bottom-left of the player
            if not collision_check_func(x_left, y_lower_half_bottom):
                dx, dy = 0, 0
            # Point 2: Bottom-right of the player
            elif not collision_check_func(x_right, y_lower_half_bottom):
                dx, dy = 0, 0
            # Point 3: Center of the bottom edge (important for small obstacles/platforms)
            elif not collision_check_func(x_center, y_lower_half_bottom):
                dx, dy = 0, 0
            # Point 4: Top-left of the *lower half* of the player (at player's mid-height)
            elif not collision_check_func(x_left, y_lower_half_top):
                dx, dy = 0, 0
            # Point 5: Top-right of the *lower half* of the player (at player's mid-height)
            elif not collision_check_func(x_right, y_lower_half_top):
                dx, dy = 0, 0
            # (Optional) Point 6: Center of the top edge of the *lower half*
            # elif not collision_check_func(x_center, y_lower_half_top):
            #    dx, dy = 0, 0

        # Apply movement if no collision
        self.rect.x += dx
        self.rect.y += dy

        # Boundary checks (ensure player stays within map limits)
        self.rect.x = max(0, min(self.rect.x, map_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, map_height - self.rect.height))
