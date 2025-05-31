import pygame
import random
import time
from minigameMap import MinigameHazard
from minigameMap import (HAZARD_RADIUS, PLAYER_COLLISION_MARGIN_LEFT, 
                        PLAYER_COLLISION_MARGIN_RIGHT, PLAYER_COLLISION_MARGIN_TOP, 
                        PLAYER_COLLISION_MARGIN_BOTTOM)

class MinigameManager:
    def __init__(self):
        self.is_active = False
        self.start_time = 0
        # if duration is halved, also halve the speed increase interval!!!!!
        self.duration = 30000  # 60 seconds in milliseconds
        self.hazards = []
        self.pending_collectible_points = 0
        self.player_death_callback = None
        self.completion_callback = None
        self.debug_mode = True  # debug mode toggle
        
        # Add these new properties for speed management
        self.base_speed = 2.5
        self.current_speed = self.base_speed
        self.speed_increase = 1.2
        self.speed_increase_interval = 5000  # 10 seconds in milliseconds
        self.last_speed_increase_time = 0
        self.speed_popup_text = ""
        self.speed_popup_start_time = 0
        self.speed_popup_duration = 2000  # 2 seconds

    def toggle_debug_mode(self):
        """Toggle debug visualization on/off"""
        self.debug_mode = not self.debug_mode
        print(f"Minigame debug mode: {'ON' if self.debug_mode else 'OFF'}")
        
    def draw_debug_info(self, screen, player_rect, camera):
        """Draw debug collision areas and info"""
        if not self.debug_mode or not self.is_active:
            return
            
        # Draw player collision area - NOW SYNCED WITH ACTUAL COLLISION
        debug_player_rect = pygame.Rect(
            player_rect.left + PLAYER_COLLISION_MARGIN_LEFT,
            player_rect.top + PLAYER_COLLISION_MARGIN_TOP,
            player_rect.width - PLAYER_COLLISION_MARGIN_LEFT - PLAYER_COLLISION_MARGIN_RIGHT,
            player_rect.height - PLAYER_COLLISION_MARGIN_TOP - PLAYER_COLLISION_MARGIN_BOTTOM
        )
        
        # Apply camera offset
        screen_player_rect = camera.apply_rect(debug_player_rect)
        pygame.draw.rect(screen, (0, 255, 0), screen_player_rect, 2)  # Green outline
        
        # Draw hazard collision areas - NOW SYNCED WITH ACTUAL COLLISION
        for hazard in self.hazards:
            hazard_rect = pygame.Rect(
                hazard.x - HAZARD_RADIUS,
                hazard.y - HAZARD_RADIUS,
                HAZARD_RADIUS * 2,  # Use actual radius
                HAZARD_RADIUS * 2
            )
            screen_hazard_rect = camera.apply_rect(hazard_rect)
            pygame.draw.rect(screen, (255, 0, 0), screen_hazard_rect, 2)  # Red outline
            
            # Draw hazard center point
            center_pos = camera.apply_point((hazard.x, hazard.y))
            pygame.draw.circle(screen, (255, 255, 0), center_pos, 3)  # Yellow center
            
        # Draw debug text
        debug_text = f"Debug: Player({player_rect.centerx}, {player_rect.centery}) HR:{HAZARD_RADIUS}"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(debug_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 100))
        
    def draw_speed_popup(self, screen):
        """Draw speed increase popup with improved visibility"""
        if not self.is_active:
            return
            
        current_time = pygame.time.get_ticks()
        if current_time - self.speed_popup_start_time < self.speed_popup_duration and self.speed_popup_text:
            # Calculate fade effect
            elapsed = current_time - self.speed_popup_start_time
            fade_progress = elapsed / self.speed_popup_duration
            alpha = max(50, int(255 * (1 - fade_progress)))  # Minimum alpha of 50
            
            # Create popup surface with background
            font = pygame.font.Font(None, 48)
            text_surface = font.render(self.speed_popup_text, True, (255, 255, 100))  # Bright yellow text
            
            # Create background with padding
            padding = 20
            bg_width = text_surface.get_width() + padding * 2
            bg_height = text_surface.get_height() + padding * 2
            
            # Create background surface
            bg_surface = pygame.Surface((bg_width, bg_height))
            bg_surface.set_alpha(alpha)
            bg_surface.fill((50, 50, 50))  # Dark gray background
            
            # Create border surface
            border_surface = pygame.Surface((bg_width + 4, bg_height + 4))
            border_surface.set_alpha(alpha)
            border_surface.fill((255, 150, 150))  # Light red border
            
            # Center the popup
            screen_width = screen.get_width()
            border_x = screen_width // 2 - border_surface.get_width() // 2
            border_y = 150
            bg_x = border_x + 2
            bg_y = border_y + 2
            text_x = bg_x + padding
            text_y = bg_y + padding
            
            # Apply fade effect to text
            text_surface.set_alpha(alpha)
            
            # Draw border, background, then text
            screen.blit(border_surface, (border_x, border_y))
            screen.blit(bg_surface, (bg_x, bg_y))
            screen.blit(text_surface, (text_x, text_y))

    def should_disable_main_game_elements(self):
        """Returns True if main game elements should be disabled (during minigame)"""
        return self.is_active
        
    def start_minigame(self, collectible_points=1, player_rect=None):
        """Start the 30-second survival minigame"""
        self.is_active = True
        self.start_time = pygame.time.get_ticks()
        self.pending_collectible_points = collectible_points
        
        # Reset speed system
        self.current_speed = self.base_speed
        self.last_speed_increase_time = 0
        self.speed_popup_text = ""
        
        self.hazards = self._spawn_hazards(player_rect)
        print("Minigame started! Survive for 30 seconds!")

    def update(self, player_rect, map_width, map_height):
        """Update minigame state"""
        if not self.is_active:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        
        # Check if time is up
        if elapsed_time >= self.duration:
            self._complete_minigame()
            return
        
        # Check for speed increases every 10 seconds
        if elapsed_time - self.last_speed_increase_time >= self.speed_increase_interval:
            self._increase_hazard_speed()
            self.last_speed_increase_time = elapsed_time
            
        # Update hazards with collision detection
        for hazard in self.hazards:
            hazard.update_with_collision(map_width, map_height, self.current_speed)
            if hazard.check_player_collision(player_rect):
                print("Player hit by hazard! Game over!")
                self._player_died()
                return
            
    def _increase_hazard_speed(self):
        """Increase hazard speed and show popup"""
        self.current_speed += self.speed_increase
        self.speed_popup_text = "Hazards' speed increased!"
        self.speed_popup_start_time = pygame.time.get_ticks()
        print(f"Hazard speed increased to {self.current_speed:.1f}")
                
    def _spawn_hazards(self, player_rect=None):
        """Spawn moving hazards for the minigame in valid positions"""
        hazards = []
            
        # Import collision map here to avoid circular imports
        from minigameMap import MINIGAME_COLLISION_MAP, TILE_GAME_SIZE
        
        # Get player position for distance check
        player_x = player_rect.centerx if player_rect else 800  # Default center if no player
        player_y = player_rect.centery if player_rect else 400
        min_distance = 200  # Minimum distance from player
        
        attempts = 0
        while len(hazards) < 6 and attempts < 100:  # Start with 6 hazards, max 100 attempts
            # Random position in world coordinates
            x = random.randint(100, 1400)
            y = random.randint(100, 700)
            
            # Convert to tile coordinates to check collision map
            tile_x = int(x // TILE_GAME_SIZE)
            tile_y = int(y // TILE_GAME_SIZE)
            
            # Calculate distance from player
            distance_from_player = ((x - player_x) ** 2 + (y - player_y) ** 2) ** 0.5
            
            # Check if position is valid (within bounds, on walkable tile, and far enough from player)
            if (0 <= tile_y < len(MINIGAME_COLLISION_MAP) and 
                0 <= tile_x < len(MINIGAME_COLLISION_MAP[0]) and
                MINIGAME_COLLISION_MAP[tile_y][tile_x] == 0 and
                distance_from_player >= min_distance):
                
                hazards.append(MinigameHazard(x, y, self.current_speed))
            
            attempts += 1
        
        if len(hazards) == 0:
            # Fallback: spawn at safe distance from player
            safe_x = player_x + min_distance + 50  # Guaranteed safe distance
            safe_y = player_y
            hazards.append(MinigameHazard(safe_x, safe_y, self.current_speed))
        
        return hazards
        
    def _complete_minigame(self):
        """Player survived the minigame"""
        self.is_active = False
        if self.completion_callback:
            self.completion_callback(self.pending_collectible_points)
            
    def _player_died(self):
        """Player died in minigame"""
        self.is_active = False
        if self.player_death_callback:
            self.player_death_callback()
            
    def set_callbacks(self, completion_callback, death_callback):
        """Set callbacks for minigame completion/failure"""
        self.completion_callback = completion_callback
        self.player_death_callback = death_callback
        
    def get_remaining_time(self):
        """Get remaining time in seconds"""
        if not self.is_active:
            return 0
        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = max(0, self.duration - elapsed)
        return remaining // 1000