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
        self.duration = 30000  # 30 seconds 
        self.hazards = []
        self.pending_collectible_points = 0
        self.player_death_callback = None
        self.completion_callback = None
        self.debug_mode = True  # debug mode toggle
        self.minigame_completed = False
        
        # Speed management properties
        self.base_speed = 2.5
        self.current_speed = self.base_speed
        self.speed_increase = 1.2
        self.speed_increase_interval = 5000  # 5 seconds
        self.last_speed_increase_time = 0
        self.speed_popup_text = ""
        self.speed_popup_start_time = 0
        self.speed_popup_duration = 2000  # 2 seconds
        
        # Add result popup properties
        self.show_result_popup = False
        self.result_popup_text = ""
        self.result_popup_start_time = 0
        self.result_popup_duration = 4000  # 4 seconds display time

        # Add hazard freeze period
        self.hazard_freeze_duration = 2000  # 2 seconds in milliseconds

    def toggle_debug_mode(self):
        """Toggle debug visualization on/off"""
        self.debug_mode = not self.debug_mode
        print(f"Minigame debug mode: {'ON' if self.debug_mode else 'OFF'}")
        
    def draw_debug_info(self, screen, player_rect, camera):
        """Draw debug collision areas and info"""
        if not self.debug_mode or not self.is_active:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        hazards_frozen = elapsed_time < self.hazard_freeze_duration
            
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
            # Change color based on frozen state
            hazard_color = (100, 100, 255) if hazards_frozen else (255, 0, 0)  # Blue if frozen, red if active
            pygame.draw.rect(screen, hazard_color, screen_hazard_rect, 2)
            
            # Draw hazard center point
            center_pos = camera.apply_point((hazard.x, hazard.y))
            center_color = (150, 150, 255) if hazards_frozen else (255, 255, 0)  # Light blue if frozen, yellow if active
            pygame.draw.circle(screen, center_color, center_pos, 3)
            
        # Draw debug text with freeze status
        freeze_text = " [FROZEN]" if hazards_frozen else ""
        debug_text = f"Debug: Player({player_rect.centerx}, {player_rect.centery}) HR:{HAZARD_RADIUS}{freeze_text}"
        font = pygame.font.Font(None, 30)
        text_surface = font.render(debug_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 50))
        
        # Add freeze countdown
        if hazards_frozen:
            remaining_freeze = (self.hazard_freeze_duration - elapsed_time) / 1000.0
            freeze_countdown = f"Hazards activate in: {remaining_freeze:.1f}s"
            freeze_font = pygame.font.Font(None, 40)
            freeze_surface = freeze_font.render(freeze_countdown, True, (100, 150, 255))
            screen.blit(freeze_surface, (10, 80))
        
    def draw_speed_popup(self, screen):
        """Draw speed increase popup with improved visibility"""
        if not self.is_active:
            return
            
        current_time = pygame.time.get_ticks()
        if current_time - self.speed_popup_start_time < self.speed_popup_duration and self.speed_popup_text:
            # Calculate fade effect
            elapsed = current_time - self.speed_popup_start_time
            fade_start_delay = 2000  # 2 seconds solid
            if elapsed < fade_start_delay:
                alpha = 255  # Full opacity
            else:
                fade_progress = (elapsed - fade_start_delay) / (self.result_popup_duration - fade_start_delay)
                alpha = max(50, int(255 * (1 - fade_progress)))
            
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

    def draw_result_popup(self, screen):
        """Draw minigame result popup with fade effect"""
        if not self.show_result_popup:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.result_popup_start_time
        
        if elapsed >= self.result_popup_duration:
            self.show_result_popup = False
            return
    
        # Calculate fade effect (same as speed popup)
        fade_progress = elapsed / self.result_popup_duration
        alpha = max(50, int(255 * (1 - fade_progress)))  # Minimum alpha of 50, fades to transparent
        
        # Create large, centered popup
        font = pygame.font.Font(None, 72)  # Large font
        lines = self.result_popup_text.split('\n')
        
        # Calculate total dimensions
        line_surfaces = []
        max_width = 0
        total_height = 0
        
        for line in lines:
            line_surface = font.render(line, True, (255, 255, 255))  # White text
            line_surfaces.append(line_surface)
            max_width = max(max_width, line_surface.get_width())
            total_height += line_surface.get_height()
        
        # Add padding
        padding = 40
        popup_width = max_width + padding * 2
        popup_height = total_height + padding * 2
    
        # Center on screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 4
        
        # Create background surface with alpha
        bg_surface = pygame.Surface((popup_width, popup_height))
        bg_surface.set_alpha(alpha)
        bg_surface.fill((50, 50, 50))  # Dark background
        
        # Create border surface with alpha
        border_surface = pygame.Surface((popup_width + 8, popup_height + 8))
        border_surface.set_alpha(alpha)
        border_surface.fill((255, 255, 255))  # White border
        
        # Draw border, then background
        border_x = popup_x - 4
        border_y = popup_y - 4
        screen.blit(border_surface, (border_x, border_y))
        screen.blit(bg_surface, (popup_x, popup_y))
        
        # Draw text lines with fade effect
        current_y = popup_y + padding
        for line_surface in line_surfaces:
            line_surface.set_alpha(alpha)  # Apply fade to text
            text_x = popup_x + (popup_width - line_surface.get_width()) // 2
            screen.blit(line_surface, (text_x, current_y))
            current_y += line_surface.get_height()

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
        if not self.is_active or self.minigame_completed:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        
        # Check if time is up
        if elapsed_time >= self.duration:
            self._complete_minigame()
            return

        # Check if hazards should be frozen (first 2 seconds)
        hazards_frozen = elapsed_time < self.hazard_freeze_duration
  
        # Check for speed increases every 10 seconds (but only after freeze period)
        if not hazards_frozen and elapsed_time - self.last_speed_increase_time >= self.speed_increase_interval:
            self._increase_hazard_speed()
            self.last_speed_increase_time = elapsed_time

        # Update hazards with collision detection (only if not frozen)
        if not hazards_frozen:
            for hazard in self.hazards:
                hazard.update_with_collision(map_width, map_height, self.current_speed)
                if hazard.check_player_collision(player_rect):
                    print("Player hit by hazard! Game over!")
                    self._player_died()
                    return
        else:
            # During freeze period, still check collisions but don't move hazards
            for hazard in self.hazards:
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
        
        # Get player position - ENSURE we have the correct coordinates
        if player_rect:
            player_x = player_rect.centerx
            player_y = player_rect.centery
            print(f"Using actual player position: ({player_x}, {player_y})")
        else:
            # Get the actual entry point from map data
            from minigameMap import get_minigame_map_data
            map_data = get_minigame_map_data()
            entry_tile_x, entry_tile_y = map_data["entry_point_tile"]
            player_x = entry_tile_x * TILE_GAME_SIZE + TILE_GAME_SIZE // 2
            player_y = entry_tile_y * TILE_GAME_SIZE + TILE_GAME_SIZE // 2
            print(f"Using fallback player position: ({player_x}, {player_y})")
        
        # Increase minimum distance for better safety
        min_distance = 400  # Increased from 300
        
        # Calculate arena bounds more precisely
        arena_width = len(MINIGAME_COLLISION_MAP[0]) * TILE_GAME_SIZE
        arena_height = len(MINIGAME_COLLISION_MAP) * TILE_GAME_SIZE
        
        # Add debug output for player position validation
        print(f"Player position: ({player_x}, {player_y})")
        print(f"Arena size: {arena_width}x{arena_height}")
        
        attempts = 0
        max_attempts = 300  # Increased attempts
        target_hazards = 5  # Reduced target to ensure quality over quantity
        
        while len(hazards) < target_hazards and attempts < max_attempts:
            # Generate spawn position with better distribution
            x = random.randint(TILE_GAME_SIZE * 2, arena_width - TILE_GAME_SIZE * 2)
            y = random.randint(TILE_GAME_SIZE * 2, arena_height - TILE_GAME_SIZE * 2)
            
            # Convert to tile coordinates
            tile_x = int(x // TILE_GAME_SIZE)
            tile_y = int(y // TILE_GAME_SIZE)
            
            # Calculate distance from player
            distance_from_player = ((x - player_x) ** 2 + (y - player_y) ** 2) ** 0.5
            
            # Enhanced validation
            if (0 <= tile_y < len(MINIGAME_COLLISION_MAP) and 
                0 <= tile_x < len(MINIGAME_COLLISION_MAP[0]) and
                MINIGAME_COLLISION_MAP[tile_y][tile_x] == 0 and
                distance_from_player >= min_distance):
                
                hazards.append(MinigameHazard(x, y, self.current_speed))
                print(f"Spawned hazard {len(hazards)} at ({x}, {y}), distance: {distance_from_player:.1f}")
            
            attempts += 1
        
        # Improved fallback with guaranteed distance
        if len(hazards) < target_hazards:
            print(f"Using enhanced fallback system")
            
            # Define specific safe zones around the arena perimeter
            safe_zones = [
                (TILE_GAME_SIZE * 2, TILE_GAME_SIZE * 2),  # Top-left corner area
                (arena_width - TILE_GAME_SIZE * 3, TILE_GAME_SIZE * 2),  # Top-right
                (TILE_GAME_SIZE * 2, arena_height - TILE_GAME_SIZE * 3),  # Bottom-left
                (arena_width - TILE_GAME_SIZE * 3, arena_height - TILE_GAME_SIZE * 3),  # Bottom-right
                (arena_width // 2, TILE_GAME_SIZE * 2),  # Top-center
                (arena_width // 2, arena_height - TILE_GAME_SIZE * 3),  # Bottom-center
            ]
            
            for safe_x, safe_y in safe_zones:
                if len(hazards) >= target_hazards:
                    break
                    
                distance_check = ((safe_x - player_x) ** 2 + (safe_y - player_y) ** 2) ** 0.5
                if distance_check >= min_distance:
                    tile_x = int(safe_x // TILE_GAME_SIZE)
                    tile_y = int(safe_y // TILE_GAME_SIZE)
                    
                    if (0 <= tile_y < len(MINIGAME_COLLISION_MAP) and 
                        0 <= tile_x < len(MINIGAME_COLLISION_MAP[0]) and
                        MINIGAME_COLLISION_MAP[tile_y][tile_x] == 0):
                        
                        hazards.append(MinigameHazard(safe_x, safe_y, self.current_speed))
                        print(f"Fallback hazard spawned at ({safe_x}, {safe_y}), distance: {distance_check:.1f}")
        
        print(f"Total hazards spawned: {len(hazards)}")
        return hazards

    def _complete_minigame(self):
        """Player survived the minigame"""
        # Don't set is_active = False yet - keep filtering NPCs during popup
        self.result_popup_text = "Minigame Completed!\n1 point added!"
        self.show_result_popup = True
        self.result_popup_start_time = pygame.time.get_ticks()
        self.minigame_completed = True  # New flag to track completion
        
        # Hide speed popup immediately
        self.speed_popup_text = ""
        
        if self.completion_callback:
            # Delay the callback to let popup show first
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def _player_died(self):
        """Player died in minigame"""
        # Don't set is_active = False yet - keep filtering NPCs during popup
        self.result_popup_text = "Minigame Over!\n1 point removed..."
        self.show_result_popup = True
        self.result_popup_start_time = pygame.time.get_ticks()
        self.minigame_completed = True  # New flag to track completion
        
        # Hide speed popup immediately
        self.speed_popup_text = ""
        
        if self.player_death_callback:
            # Delay the callback to let popup show first
            pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
            
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