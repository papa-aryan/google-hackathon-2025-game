import pygame
import random
import time
from minigameMap import MinigameHazard

class MinigameManager:
    def __init__(self):
        self.is_active = False
        self.start_time = 0
        self.duration = 60000  # 60 seconds in milliseconds
        self.hazards = []
        self.pending_collectible_points = 0
        self.player_death_callback = None
        self.completion_callback = None
        
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