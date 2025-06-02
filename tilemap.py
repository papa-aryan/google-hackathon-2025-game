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
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11], # 30 elements just nu
    [11, 46, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 48, -1, -1, -1, -1, -1],  
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, -1, 46, 47, 48, -1],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,241,242,242,242,243, 92, 92, 92, 92, 93, -1, 91, 92, 56, 57],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,286,287,287,287,288, 92, 92, 92, 92, 93, -1, 91, 92, 92,147],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,331,332,332,332,333, 92, 92, 92, 92, 93, -1,188, 92, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,191, -1,233, 98, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,192,137,235,236, -1, -1, 91, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,101,237,182,183, -1, -1, 52, 53, 92, 93],
    [32, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,191, -1, -1, -1, -1, 52, 99, 92, 92, 93],
    [32,136,137,137,137, 94, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,101,236, -1, -1, -1, 52, 99, 92, 92, 92, 93],
    [32,181,182,182,182, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,191, -1, -1, -1, -1,142, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,101,236, -1, -1, -1, -1, 91, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, -1, -1, -1, -1, -1, 91, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, 11, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92,101,234,235, 98, 93, -1, -1, -1, -1, 52, 53, 92, 92, 92, 92, 93],
    [11, 11, 11, 11, -1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93,181,183, 91, 93, -1, -1, -1, 52, 99, 92, 92, 92,192,137,138],
    [11, 11, 11, 11, 52, 53, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, -1, -1, 91, 93, -1, -1, -1,142, 92, 92, 92,101,237,182,183],
    [11, 11, 11, 11,142, 92, 92, 92, 92,101,234,235, 98, 92, 92, 92,192,235,236, -1, 52, 53, 56, 57, -1, -1, 91, 92, 92, 92, 93], 
    [32, 40, 41, 41, 91, 92, 92, 92, 92, 93,181,183,188, 92, 92,101,237,183, -1, 52, 99, 92, 92,102, 47, 47, 49, 92,192,137,138],
    [32, 40, -1, 52, 53, 92, 92, 92, 92, 93, -1, -1,233,234,137,138, -1, -1, -1,142, 92, 92, 92, 92, 92, 92, 92,101,237,182,183],
    [-1, -1, 52, 99, 92, 92, 92, 92, 92,191, -1, -1, -1,181,182,183, -1, -1, -1, 91, 92, 92, 92, 92, 92, 92, 92, 93],    
    [-1, -1,142, 92, 92, 92, 92, 92,101,236, -1, -1, -1, -1, -1, -1, -1, -1, -1, 91, 241,242,243, 92, 92, 92, 92, 93],    
    [32, 40, 91, 92, 92, 92, 92, 92, 56, 57, -1, -1, -1 ,-1, -1, -1, -1, -1, -1, 91, 286,287,288, 92, 92, 92, 92, 93],  
    [32, 52, 53, 92, 92, 92, 92, 92, 92,102, 47, 47, 47, 48, -1, -1, -1, -1, -1, 91, 331,332,333, 92, 92, 92, 92,191],  
    [-1,142, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, -1, -1, -1, -1, -1,136,137,137,137,137,137,137,235,236],    
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93, -1, -1, -1, -1, -1,181,182,182,182,182,182,182,183],    
    [-1, 91, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 93],    
    [-1,136,137,137,137,137,137,137,137,137,137,137,137,138],        
    [-1,181,182,182,182,182,182,182,182,182,182,182,182,183], # 30 elements     
    [-1],

]

_new_map_width_tiles = 35
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
    [-1, -1, -1, -1, -1, -1, -1,622],
    [-1, -1, -1, -1, -1, -1,666,667,668],
    [-1, -1, -1, -1, -1, -1,711,712,713],
    [-1, -1, -1, -1, -1, -1,756,757,758],
    [-1, -1, -1, -1, -1, -1,682,684,683],
    [-1, -1, -1, -1, -1, -1,476,477,478],
    [-1, -1, -1, -1, -1, -1,521,522,523],
    [-1, -1, -1, -1, -1, -1,566, -1,568, -1, -1, -1,961,962],
    [-1],
    [-1],
    [-1],  
    [-1],
    [-1],
    [-1],
    [-1],
    [-1],
    [-1],
    [-1],
    [-1],
    [-1],
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


# Collectibles system - track collectible positions and respawn timers
collectibles = {}  # {(row, col): {"timer": 0, "collected": False, "original_tile": 933}}

def init_collectibles():
    """Initialize collectibles from BUILDING_MAP after it's created"""
    global collectibles
    collectibles = {}

    # Get player starting position from map data
    start_x_tile, start_y_tile = 13, 14  # Use the same values as entry_point_tile
    exclusion_radius = 4  # 3 tile radius around player spawn
    
    # Find all walkable positions (COLLISION_MAP = 0)
    walkable_positions = []
    for row_idx in range(len(COLLISION_MAP)):
        for col_idx in range(len(COLLISION_MAP[row_idx])):
            if COLLISION_MAP[row_idx][col_idx] == 0:  # Walkable tile
                # Calculate distance from player spawn point
                distance = ((row_idx - start_y_tile) ** 2 + (col_idx - start_x_tile) ** 2) ** 0.5
                
                # Only add if outside exclusion radius
                if distance > exclusion_radius:
                    walkable_positions.append((row_idx, col_idx))

    # Randomly select 5 positions for coins
    import random
    if len(walkable_positions) >= 5:
        selected_positions = random.sample(walkable_positions, 5)
        
        # Place coins at selected positions
        for row_idx, col_idx in selected_positions:
            BUILDING_MAP[row_idx][col_idx] = 933  # Place collectible tile
            collectibles[(row_idx, col_idx)] = {
                "timer": 0, 
                "collected": False, 
                "original_tile": 933
            }
        
        print(f"Initialized {len(collectibles)} collectible coins avoiding {exclusion_radius}-tile radius around player spawn ({start_y_tile}, {start_x_tile})")
    else:
        print(f"Warning: Not enough valid positions found. Only {len(walkable_positions)} available outside spawn area.")

def update_collectibles():
    """Update collectible timers and respawn items"""
    global BUILDING_MAP
    import random

    for (row, col), data in list(collectibles.items()):  # Use list() to avoid modification during iteration
        if data["collected"]:
            data["timer"] += 1
            if data["timer"] >= 480:  # Respawn after 480 frames
                # Remove the old collectible entry
                del collectibles[(row, col)]
                
                # Find all current walkable positions (excluding occupied collectible spots)
                walkable_positions = []
                occupied_positions = set(collectibles.keys())  # Positions with active collectibles
                
                for row_idx in range(len(COLLISION_MAP)):
                    for col_idx in range(len(COLLISION_MAP[row_idx])):
                        if (COLLISION_MAP[row_idx][col_idx] == 0 and  # Walkable tile
                            (row_idx, col_idx) not in occupied_positions and  # Not occupied by collectible
                            BUILDING_MAP[row_idx][col_idx] == EMPTY_TILE_ID):  # Not occupied by building
                            walkable_positions.append((row_idx, col_idx))
                # Spawn at new random location if available
                if walkable_positions:
                    new_row, new_col = random.choice(walkable_positions)
                    BUILDING_MAP[new_row][new_col] = 933  # Place collectible tile
                    collectibles[(new_row, new_col)] = {
                        "timer": 0, 
                        "collected": False, 
                        "original_tile": 933
                    }
                    print(f"Collectible respawned at new location ({new_row}, {new_col}) - was at ({row}, {col})")
                else:
                    print("Warning: No available positions for collectible respawn")

def collect_item(world_x, world_y, tile_size):
    """Check if player collected an item at given world position"""
    tile_x = world_x // tile_size
    tile_y = world_y // tile_size
    
    # Check for collectibles (coins)
    if (tile_y, tile_x) in collectibles and not collectibles[(tile_y, tile_x)]["collected"]:
        collectibles[(tile_y, tile_x)]["collected"] = True
        if tile_y < len(BUILDING_MAP) and tile_x < len(BUILDING_MAP[tile_y]):
            BUILDING_MAP[tile_y][tile_x] = EMPTY_TILE_ID  # Remove from map
        print(f"Item collected at tile ({tile_y}, {tile_x})")
        return "collectible"  # Return type instead of True
    
    # Check for quote tracker tiles (961, 962)
    if (tile_y < len(BUILDING_MAP) and tile_x < len(BUILDING_MAP[tile_y]) and 
        BUILDING_MAP[tile_y][tile_x] in [961, 962]):
        return "quote_tracker"  # Return quote tracker type
    
    return None  # No interaction


# Collision map (0 = walkable, 1 = wall)
# Manually define COLLISION_MAP similar to wizardHouse.py
# Dimensions should be _new_map_height_tiles (30) x _new_map_width_tiles (30)
COLLISION_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 35 elements
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1] 
]




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
    start_x_tile, start_y_tile = 13, 14 # Example starting tile
    
    # Initialize collectibles when map data is requested
    init_collectibles()
    
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
