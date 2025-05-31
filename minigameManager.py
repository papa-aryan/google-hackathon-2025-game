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
        self.duration = 60000  # 60 seconds in milliseconds
        self.hazards = []
        self.pending_collectible_points = 0
        self.player_death_callback = None
        self.completion_callback = None
        self.debug_mode = True  # debug mode toggle

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
        
    def should_disable_main_game_elements(self):
        """Returns True if main game elements should be disabled (during minigame)"""
        return self.is_active
        
    def start_minigame(self, collectible_points=1):
        """Start the 60-second survival minigame"""
        self.is_active = True
        self.start_time = pygame.time.get_ticks()
        self.pending_collectible_points = collectible_points
        self.hazards = self._spawn_hazards()
        print("Minigame started! Survive for 60 seconds!")
        
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
            
        # Update hazards
        for hazard in self.hazards:
            hazard.update(map_width, map_height)
            if hazard.check_player_collision(player_rect):
                print("Player hit by hazard! Game over!")
                self._player_died()
                return
                
    def _spawn_hazards(self):
        """Spawn moving hazards for the minigame"""
        hazards = []
        for _ in range(5):  # Start with 5 hazards
            x = random.randint(600, 1200)
            y = random.randint(300, 800)
            hazards.append(MinigameHazard(x, y))
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