import pygame

# Constants
TILE_ORIG_SIZE = 32
TILE_GAME_SIZE = 64
TILESET_WIDTH = 8  # 8 tiles wide

# Load tileset image
tileset_img = None # Will be loaded by the main game

# Define the map using tile IDs
# Original MAP was 12 rows, 20 columns.
# New MAP will be 20 rows, 30 columns.
_original_map_rows = [
    [24, 32, 33, 33, 34, 24, 24, 23, 11, 41, 32, 32, 33, 33, 34, 24, 24, 23, 11, 40, 11, 11, 11, 11, 11, 40, 11, 16, 40, 11], # 30 elements just nu
    [32, 32, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 34, 24, 23, 11, 41],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 16, 16],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 16, 16],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 16, 16],  
    [32, 40, 41, 41, 41, 8, 9, 9, 9, 9, 10, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 16, 16],  
    [32, 40, 41, 41, 41, 16, 11, 11, 11, 11, 18, 41, 41, 41, 41, 68, 68, 68, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 16, 16],  
    [32, 40, 41, 41, 41, 16, 11, 11, 11, 11, 18, 41, 41, 41, 41, 37, 49, 76, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 16, 16],  
    [32, 40, 41, 41, 41, 16, 11, 11, 11, 11, 18, 41, 41, 41, 41, 41, 71, 23, 11, 41],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 41],  
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41],
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 73, 73, 73, 49, 49, 11, 41],
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41],
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 75, 75, 49, 49, 11, 41],
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41],
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41],
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41],
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 41],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 41],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 41],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 41],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 41],  
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41]
]

_new_map_width_tiles = 30
_new_map_height_tiles = 30
_fill_tile_id = 41 # Tile ID to use for new areas

MAP = []
for r_idx in range(_new_map_height_tiles):
    new_row = []
    if r_idx < len(_original_map_rows): # If it's an existing row index
        original_row = _original_map_rows[r_idx]
        new_row.extend(original_row)
        # Extend the row if it's shorter than the new width
        if len(original_row) < _new_map_width_tiles:
            new_row.extend([_fill_tile_id] * (_new_map_width_tiles - len(original_row)))
    else: # It's a completely new row
        new_row.extend([_fill_tile_id] * _new_map_width_tiles)
    MAP.append(new_row)


# Collision map (0 = walkable, 1 = wall)
# Original COLLISION was 12 rows, 20 columns.
# New COLLISION will be 20 rows, 30 columns.
_original_collision_rows = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
_fill_collision_value = 0 # 0 for walkable

COLLISION = []
for r_idx in range(_new_map_height_tiles):
    new_collision_row = []
    if r_idx < len(_original_collision_rows):
        original_collision_row = _original_collision_rows[r_idx]
        new_collision_row.extend(original_collision_row)
        if len(original_collision_row) < _new_map_width_tiles:
            new_collision_row.extend([_fill_collision_value] * (_new_map_width_tiles - len(original_collision_row)))
    else:
        new_collision_row.extend([_fill_collision_value] * _new_map_width_tiles)
    COLLISION.append(new_collision_row)


def init_tilemap(tileset_image_path):
    global tileset_img
    tileset_img = pygame.image.load(tileset_image_path).convert_alpha()

def get_tile(row, col):
    rect = pygame.Rect(col * TILE_ORIG_SIZE, row * TILE_ORIG_SIZE, TILE_ORIG_SIZE, TILE_ORIG_SIZE)
    tile = tileset_img.subsurface(rect)
    tile = pygame.transform.scale(tile, (TILE_GAME_SIZE, TILE_GAME_SIZE))
    return tile

def get_tile_by_id(tile_id):
    row = tile_id // TILESET_WIDTH
    col = tile_id % TILESET_WIDTH
    return get_tile(row, col)

def draw_map(surface, camera):
    for row_index, row_data in enumerate(MAP):
        for col_index, tile_id in enumerate(row_data):
            tile_surface = get_tile_by_id(tile_id)
            # Calculate the position of the tile
            tile_x = col_index * TILE_GAME_SIZE
            tile_y = row_index * TILE_GAME_SIZE
            # Apply camera offset
            surface.blit(tile_surface, (tile_x + camera.camera.x, tile_y + camera.camera.y))

def can_move(x, y):
    # Convert pixel position to tile position
    tile_x = x // TILE_GAME_SIZE
    tile_y = y // TILE_GAME_SIZE
    
    # Check bounds of the collision map
    if 0 <= tile_y < len(COLLISION) and 0 <= tile_x < len(COLLISION[0]):
        return COLLISION[tile_y][tile_x] == 0 # True if walkable (0)
    return False # Out of bounds is not walkable
