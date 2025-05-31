import pygame
import random

HAZARD_RADIUS = 20
PLAYER_COLLISION_MARGIN_LEFT = 37
PLAYER_COLLISION_MARGIN_RIGHT = 37
PLAYER_COLLISION_MARGIN_TOP = 10
PLAYER_COLLISION_MARGIN_BOTTOM = 5

TILE_ORIG_SIZE = 16
TILE_GAME_SIZE = 64
TILESET_WIDTH_MINIGAME = 45
EMPTY_TILE_ID = -1

# Define minigame map layout (smaller, arena-style)
MINIGAME_MAP = [
    # 15x15 arena with walls around edges
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 46, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 48, -1],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [-1,136,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,137,138]
]

MINIGAME_COLLISION_MAP = [
    # Collision data matching the map
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class MinigameHazard:
    """Represents moving hazards in the minigame"""
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.last_collision_result = False  # For debug display
        
    def update(self, map_width, map_height):
        """Update hazard movement"""
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
            
        # Bounce off walls
        if self.x <= 64 or self.x >= map_width - 64:
            self.direction = 'left' if self.x >= map_width - 64 else 'right'
        if self.y <= 64 or self.y >= map_height - 64:
            self.direction = 'up' if self.y >= map_height - 64 else 'down'
            
        
    def check_player_collision(self, player_rect):
        """Check if hazard hits player"""
        hazard_radius = 15
        
        # Player collision area (same as debug visualization)
        player_left = player_rect.left + PLAYER_COLLISION_MARGIN_LEFT
        player_right = player_rect.right - PLAYER_COLLISION_MARGIN_RIGHT
        player_top = player_rect.top + PLAYER_COLLISION_MARGIN_TOP
        player_bottom = player_rect.bottom - PLAYER_COLLISION_MARGIN_BOTTOM
        
        # Hazard collision area
        hazard_left = self.x - HAZARD_RADIUS
        hazard_right = self.x + HAZARD_RADIUS
        hazard_top = self.y - HAZARD_RADIUS
        hazard_bottom = self.y + HAZARD_RADIUS

        
        # Check overlap
        x_overlap = hazard_right >= player_left and hazard_left <= player_right
        y_overlap = hazard_bottom >= player_top and hazard_top <= player_bottom
        
        print(f"x_overlap: {x_overlap}, y_overlap: {y_overlap}")


        self.last_collision_result = x_overlap and y_overlap
        return self.last_collision_result
            
        #return x_overlap and y_overlap
    
def get_minigame_map_data():
    return {
        "name": "minigame_arena",
        "map_layout": MINIGAME_MAP,
        "building_layout": None,
        "collision_layout": MINIGAME_COLLISION_MAP,
        "decoration_layout": None,
        "tile_size": TILE_GAME_SIZE,
        "tile_orig_size": TILE_ORIG_SIZE,
        "tileset_path": "cloud_tileset_custom.png",
        "tileset_width": TILESET_WIDTH_MINIGAME,
        "entry_point_tile": (7, 7),  # Center of arena
        "static_entity_data": [],
        "map_interactables": []
    }