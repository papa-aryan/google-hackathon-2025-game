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
    def __init__(self, x, y, speed=3.0):
        self.x = x
        self.y = y
        self.speed = speed  # This will be updated by MinigameManager
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.last_collision_result = False  # For debug display
        
        # Add these lines for spontaneous direction changes
        self.direction_change_timer = 0
        self.direction_change_interval = random.randint(60, 300)  # 2-5 seconds at 60fps

    def update_with_collision(self, map_width, map_height, speed):
        """Update hazard movement with collision detection"""
        # Store current position
        old_x, old_y = self.x, self.y
        
        # Increment direction change timer
        self.direction_change_timer += 1
        
        # Spontaneous direction change (even when not hitting walls)
        if self.direction_change_timer >= self.direction_change_interval:
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.direction_change_timer = 0
            self.direction_change_interval = random.randint(60, 300)  # Reset interval
        
        # Calculate movement
        if self.direction == 'up':
            new_y = self.y - speed
            new_x = self.x
        elif self.direction == 'down':
            new_y = self.y + speed
            new_x = self.x
        elif self.direction == 'left':
            new_x = self.x - speed
            new_y = self.y
        elif self.direction == 'right':
            new_x = self.x + speed
            new_y = self.y
        
        # Check collision with collision map
        if self._can_move_to(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            # Bounce off wall by changing direction AND reset timer
            self._bounce_off_wall()
            self.direction_change_timer = 0  # Reset timer when bouncing
            self.direction_change_interval = random.randint(60, 180)  # Shorter interval after bounce

    def _can_move_to(self, x, y):
        """Check if hazard can move to given position using collision map"""
        # Convert world coordinates to tile coordinates
        tile_x = int(x // TILE_GAME_SIZE)
        tile_y = int(y // TILE_GAME_SIZE)
        
        # Check bounds
        if tile_y < 0 or tile_y >= len(MINIGAME_COLLISION_MAP) or tile_x < 0 or tile_x >= len(MINIGAME_COLLISION_MAP[0]):
            return False
        
        # Check if tile is walkable (0 = walkable, 1 = wall)
        return MINIGAME_COLLISION_MAP[tile_y][tile_x] == 0
    
    def _bounce_off_wall(self):
        """Change direction when hitting a wall"""
        if self.direction == 'up':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'up'
        elif self.direction == 'left':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'left'
        
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