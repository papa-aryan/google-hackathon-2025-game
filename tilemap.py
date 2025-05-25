import pygame # Ensure pygame is imported

# Constants
TILE_ORIG_SIZE = 16
TILE_GAME_SIZE = 64
MAIN_MAP_TILESET_WIDTH = 45  # Tileset width for cloud_tileset.png

# Special ID for empty tiles in the building layer
EMPTY_TILE_ID = -1

# Load tileset image
tileset_img = None # Will be loaded by the main game
tile_rects = {} # Initialize tile_rects globally

# Define the map using tile IDs
# Original MAP was 12 rows, 20 columns.
# New MAP will be 20 rows, 30 columns.
_original_map_rows = [
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11], # 30 elements just nu
    [11, 46, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 48],  
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 191],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 192, 137, 235, 236],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 101, 237, 182, 183],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 191],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 101, 236],
    [32, 136, 137, 137, 137, 94, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],
    [32, 181, 182, 182, 182, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 191],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 95, 137, 137, 137, 137, 235, 236],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, 182, 182, 182, 182, 183],
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
    [-1, -1, -1, -1, -1, -1, -1, 622],
    [-1, -1, -1, -1, -1, -1, 666, 667, 668],
    [-1, -1, -1, -1, -1, -1, 711, 712, 713],
    [682, 683, -1, -1, -1, -1, 756, 757, 758],
    [727, 728, -1, -1, -1, -1, 682, 684, 683],
    [727, 728, -1, -1, -1, -1, 476, 477, 478],
    [-1, -1, -1, -1, -1, -1, 521, 522, 523, -1, -1, 961, 962],
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
COLLISION_MAP = [] 
# Define a list of tile IDs that are considered walkable for the base map layer
# Expanded based on visual inspection of _original_map_rows and common ground tiles.
walkable_base_tile_ids = [
    11, 32, 40, 41, 42, 46, 47, 48, 49, 50, 91, 92, 93, 94, 95, 
    101, 136, 137, 138, 181, 182, 183, 191, 192, 235, 236, 237
]

for r_idx in range(_new_map_height_tiles):
    row = []
    for c_idx in range(_new_map_width_tiles):
        collidable = 0  # Default to walkable
        # Check for borders
        if r_idx == 0 or r_idx == _new_map_height_tiles - 1 or \
           c_idx == 0 or c_idx == _new_map_width_tiles - 1:
            collidable = 1
        # Check for buildings (these take precedence over walkable base tiles)
        elif BUILDING_MAP[r_idx][c_idx] != EMPTY_TILE_ID:
            collidable = 1
        # Check if the base map tile itself is non-walkable
        elif MAP[r_idx][c_idx] not in walkable_base_tile_ids:
            collidable = 1
        row.append(collidable)
    COLLISION_MAP.append(row)


# Function to get tile rectangle from tileset
tile_rects = {}

def init_tilemap(tileset_path_from_main, tileset_actual_width_tiles, tileset_tile_original_size): # MODIFIED: Added tileset_tile_original_size
    global tileset_img, tile_rects
    tile_rects = {} 
    try:
        print(f"Attempting to load tileset: {tileset_path_from_main} (orig tile size: {tileset_tile_original_size})")
        loaded_img = pygame.image.load(tileset_path_from_main)
        tileset_img = loaded_img.convert_alpha()
        print(f"Tileset '{tileset_path_from_main}' loaded successfully. Size: {tileset_img.get_size()}")

        tileset_actual_height_pixels = tileset_img.get_height()
        # Use the passed tileset_tile_original_size for row calculation
        num_tile_rows_in_tileset = tileset_actual_height_pixels // tileset_tile_original_size
        total_tiles_in_tileset = tileset_actual_width_tiles * num_tile_rows_in_tileset 

        for i in range(total_tiles_in_tileset):
            row, col = divmod(i, tileset_actual_width_tiles) 
            # Use the passed tileset_tile_original_size for Rect creation
            rect = pygame.Rect(col * tileset_tile_original_size, row * tileset_tile_original_size, tileset_tile_original_size, tileset_tile_original_size)
            tile_rects[i] = rect
        print(f"Initialized {len(tile_rects)} tile rects using tileset width {tileset_actual_width_tiles} and orig tile size {tileset_tile_original_size}.")

    except pygame.error as e:
        print(f"CRITICAL PYGAME ERROR loading tileset '{tileset_path_from_main}': {e}")
        tileset_img = None # Ensure it's None on failure
    except Exception as e:
        print(f"CRITICAL UNEXPECTED ERROR during init_tilemap: {e}")
        tileset_img = None # Ensure it's None on failure


def get_tile_rect(tile_id):
    return tile_rects.get(tile_id)

# Renamed and modified to accept tile_size and ensure tileset_img is loaded
def _draw_layer_internal(surface, layer_data, camera, current_tile_size):
    global tileset_img # Ensure access to the loaded tileset
    if tileset_img is None: # Explicitly check for None
        # Error message will be printed by init_tilemap if loading failed
        return

    for row_idx, row in enumerate(layer_data):
        for col_idx, tile_id in enumerate(row):
            if tile_id != EMPTY_TILE_ID: 
                tile_img_rect = get_tile_rect(tile_id)
                if tile_img_rect:
                    screen_x = col_idx * current_tile_size + camera.camera.x
                    screen_y = row_idx * current_tile_size + camera.camera.y
                    
                    if screen_x + current_tile_size > 0 and screen_x < surface.get_width() and \
                       screen_y + current_tile_size > 0 and screen_y < surface.get_height():
                        scaled_tile = pygame.transform.scale(
                            tileset_img.subsurface(tile_img_rect), 
                            (current_tile_size, current_tile_size)
                        )
                        surface.blit(scaled_tile, (screen_x, screen_y))

# Modified to accept map layouts and tile_size as parameters
def draw_map(surface, camera, map_layout, building_layout, decoration_layout, tile_size):
    if map_layout:
        _draw_layer_internal(surface, map_layout, camera, tile_size)
    if building_layout: # Check if building_layout exists
        _draw_layer_internal(surface, building_layout, camera, tile_size)
    if decoration_layout: # ADDED: Draw decoration layer
        _draw_layer_internal(surface, decoration_layout, camera, tile_size)


def can_move(world_x, world_y):
    # This function is effectively replaced by MapManager.can_move
    # However, it might be called if old references exist.
    # For safety, it could delegate or raise an error if called.
    # print("Warning: tilemap.can_move called. This should be handled by MapManager.")
    # For now, let it pass as it's not directly used by player movement in main.py
    pass
    

def get_main_map_data():
    # This function provides the data structure for the main map
    # Player start position for the main map (example: tile 10,10)
    # Ensure these are within the bounds of MAP and COLLISION_MAP
    start_x_tile, start_y_tile = 1, 1 # Example starting tile
    return {
        "name": "main_map", # Added name for consistency
        "map_layout": MAP,
        "building_layout": BUILDING_MAP, # Can be None if no building layer
        "collision_layout": COLLISION_MAP, # Make sure this is correctly generated
        "tile_size": TILE_GAME_SIZE, # Game size for rendering
        "tileset_path": 'cloud_tileset.png', # Path to the main map's tileset
        "tileset_width": MAIN_MAP_TILESET_WIDTH, # Tileset width for this map
        "tile_orig_size": TILE_ORIG_SIZE, # ADDED: Original tile size for the main map tileset (global TILE_ORIG_SIZE)
        "entry_point_tile": (start_x_tile, start_y_tile) # Player's starting tile coordinates
    }
