import pygame

# Constants
TILE_ORIG_SIZE = 16
TILE_GAME_SIZE = 64
TILESET_WIDTH = 45  # Tileset width in tiles

# Special ID for empty tiles in the building layer
EMPTY_TILE_ID = -1

# Load tileset image
tileset_img = None # Will be loaded by the main game

# Define the map using tile IDs
# Original MAP was 12 rows, 20 columns.
# New MAP will be 20 rows, 30 columns.
_original_map_rows = [
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11], # 30 elements just nu
    [11, 46, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 48, 11, 11],  
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 11, 11, 11],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 95, 137, 137, 137, 137, 138, 11, 11, 11],
    [32, 136, 137, 137, 137, 94, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [32, 181, 182, 182, 182, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 95, 137, 137, 137, 138],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 182, 182, 182, 183],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93], 
    [32, 40, 41, 41, 41, 136, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 138],
    [32, 40, 41, 41, 41, 181, 182, 182, 182, 182, 182, 182, 182, 182, 182, 182, 182, 183],
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 11],  
    [32, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 24, 23, 11, 11],  
    [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 11],        [32, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 24, 23, 11, 41]

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


# Define the building layer data
_original_building_rows = [
    [11],
    [11],
    [11, 11, 11, 11, 11, 11, 11, 622],
    [682, 683, 111, 111, 111, 111, 666, 667, 668],
    [682, 683, 684, 685, 686, 687, 711, 712, 713],
    [682, 683, 684, 685, 686, 687, 756, 757, 758],
    [727, 728, -1, -1, -1, -1, 682, 684, 683],
    [727, 728, -1, -1, -1, -1, 476, 477, 478],
    [-1, -1, -1, -1, -1, -1, 521, 522, 523, -1, 961, 962],
    [-1, -1, -1, -1, -1, -1, 566, -1, 568, -1]
]


# Building Map Layer (same dimensions as MAP, initialized with EMPTY_TILE_ID)
BUILDING_MAP = []
for r_idx in range(_new_map_height_tiles):
    new_row = []
    if r_idx < len(_original_building_rows):
        original_row = _original_building_rows[r_idx]
        # Iterate up to _new_map_width_tiles
        for c_idx in range(_new_map_width_tiles):
            if c_idx < len(original_row):
                new_row.append(original_row[c_idx])
            else:
                new_row.append(EMPTY_TILE_ID) # Fill short rows with empty
    else:
        # Fill new rows (if _original_building_rows is shorter than _new_map_height_tiles) with empty
        new_row.extend([EMPTY_TILE_ID] * _new_map_width_tiles)
    BUILDING_MAP.append(new_row)


# Collision map (0 = walkable, 1 = wall)
# Original COLLISION was 12 rows, 20 columns.
# New COLLISION will be 20 rows, 30 columns.
_original_collision_rows = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
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
    # Ensure tileset_img is loaded
    if tileset_img is None:
        # This case should ideally not be reached if init_tilemap is always called first.
        dummy_tile = pygame.Surface((TILE_ORIG_SIZE, TILE_ORIG_SIZE), pygame.SRCALPHA)
        dummy_tile.fill((0,0,0,0)) # Transparent
        return pygame.transform.scale(dummy_tile, (TILE_GAME_SIZE, TILE_GAME_SIZE))

    # Calculate the maximum valid 0-indexed column and row based on the actual image dimensions
    actual_max_col = (tileset_img.get_width() // TILE_ORIG_SIZE) - 1
    actual_max_row = (tileset_img.get_height() // TILE_ORIG_SIZE) - 1

    target_col = col
    target_row = row

    # Check if the conceptual (row, col) is outside the actual image's tile grid
    if not (0 <= target_row <= actual_max_row and 0 <= target_col <= actual_max_col):
        # Fallback to tile (0,0) if the requested tile is out of bounds.
        # First, check if tile (0,0) itself is valid for the loaded tileset.
        if not (0 <= 0 <= actual_max_row and 0 <= 0 <= actual_max_col):
            # Tileset image is too small even for a single tile (0,0).
            # This indicates a fundamental issue with tileset_img or TILE_ORIG_SIZE.
            # Return a transparent dummy tile.
            dummy_tile = pygame.Surface((TILE_ORIG_SIZE, TILE_ORIG_SIZE), pygame.SRCALPHA)
            dummy_tile.fill((0,0,0,0)) # Transparent
            return pygame.transform.scale(dummy_tile, (TILE_GAME_SIZE, TILE_GAME_SIZE))
        
        # Use (0,0) as the fallback tile coordinates
        target_row = 0
        target_col = 0
    
    # Now, target_row and target_col are within the actual tile grid of the image.
    rect = pygame.Rect(target_col * TILE_ORIG_SIZE, target_row * TILE_ORIG_SIZE, TILE_ORIG_SIZE, TILE_ORIG_SIZE)
    
    try:
        tile = tileset_img.subsurface(rect)
        tile = pygame.transform.scale(tile, (TILE_GAME_SIZE, TILE_GAME_SIZE))
        return tile
    except ValueError:
        # This might happen if TILE_ORIG_SIZE is incorrect or other unexpected issues.
        # Return a visible error tile (e.g., semi-transparent red)
        error_tile = pygame.Surface((TILE_ORIG_SIZE, TILE_ORIG_SIZE), pygame.SRCALPHA)
        error_tile.fill((255, 0, 0, 128)) # Semi-transparent red
        return pygame.transform.scale(error_tile, (TILE_GAME_SIZE, TILE_GAME_SIZE))

def get_tile_by_id(tile_id):
    row = tile_id // TILESET_WIDTH
    col = tile_id % TILESET_WIDTH
    return get_tile(row, col)

def draw_map(surface, camera):
    # Draw the base map layer
    for row_index, row_data in enumerate(MAP):
        for col_index, tile_id in enumerate(row_data):
            tile_surface = get_tile_by_id(tile_id)
            # Calculate the position of the tile
            tile_x = col_index * TILE_GAME_SIZE
            tile_y = row_index * TILE_GAME_SIZE
            # Apply camera offset
            surface.blit(tile_surface, (tile_x + camera.camera.x, tile_y + camera.camera.y))

    # Draw the building layer on top
    for row_index, row_data in enumerate(BUILDING_MAP):
        for col_index, tile_id in enumerate(row_data):
            if tile_id != EMPTY_TILE_ID: # Only draw if it's not an empty tile
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
    
    # Check bounds of the map (using COLLISION map dimensions as reference)
    if not (0 <= tile_y < len(COLLISION) and 0 <= tile_x < len(COLLISION[0])):
        return False # Out of bounds is not walkable

    # Check collision with the base layer's explicit collision map
    if COLLISION[tile_y][tile_x] != 0: # Not walkable if base collision map says so (1 = wall)
        return False
        
    # Check collision with the building layer
    # Assumes BUILDING_MAP has the same dimensions as COLLISION map
    if 0 <= tile_y < len(BUILDING_MAP) and 0 <= tile_x < len(BUILDING_MAP[0]):
        if BUILDING_MAP[tile_y][tile_x] != EMPTY_TILE_ID:
            return False # Not walkable if there's a building tile (any tile ID other than EMPTY_TILE_ID)
            
    return True # Walkable if no collision on base explicit collision or building layer
