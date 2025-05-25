import pygame

# Constants for the Wizard's House map
TILE_ORIG_SIZE = 32 # Original size of tiles in InteriorTiles.png
TILE_GAME_SIZE = 64 # Size tiles will be rendered at in game
TILESET_WIDTH_HOUSE = 16 # Actual width of InteriorTiles.png in tiles
EMPTY_TILE_ID = -1

# Wizard House Map Data (A simple 10x8 room)
# Tile IDs are placeholders; adjust them to match your 'cloud_tileset.png'
# 100: Wall tile, 41: Floor tile, 150: Door/Exit tile
# Table: 200-202 (top row), 245-247 (bottom row)
HOUSE_MAP = [
    [1 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 6 , -1],
    [17, 18, 19, 19, 19, 19, 19, 19, 19, 20, 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 32, 32, 32, 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 32, 32, 32, 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [33, 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 38],
    [-1],
    [-1]

]

HOUSE_BUILDING_MAP = [
    [EMPTY_TILE_ID] * 10 for _ in range(len(HOUSE_MAP))
]

HOUSE_COLLISION_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# New decoration layer
# Dimensions should match HOUSE_MAP
# Use EMPTY_TILE_ID for no decoration, and other tile IDs from InteriorTiles.png for decorations
# These are placeholder IDs, update them with actual IDs from InteriorTiles.png
HOUSE_DECORATION_MAP = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 80, 80, -1, -1, -1, -1, -1, -1, -1], # Example: a plant (tile ID 48)
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]

PLAYER_START_X_TILE = 4
PLAYER_START_Y_TILE = 5

class ExitPortal:
    def __init__(self, x_tile_idx, y_tile_idx, tile_size, radius, message, id="exit_portal"): # Added id parameter
        self.id = id # Use the provided id
        # Calculate center in pixels from tile indices (center of the tile)
        self.center_x = (x_tile_idx + 0.5) * tile_size
        self.center_y = (y_tile_idx + 0.5) * tile_size
        self.radius = radius
        self.message = message
        self.color = (0, 255, 0)  # Green color for the exit portal circle
        self.thickness = 3       # Thickness of the circle outline

    def get_interaction_properties(self):
        """Returns a dictionary of properties needed for interaction management."""
        return {
            "id": self.id,
            "center": (self.center_x, self.center_y), # This is in world coordinates
            "radius": self.radius,
            "message": self.message,
            "color": self.color,
            "thickness": self.thickness
        }

def get_wizard_house_data():
    # Define the portal for the wizard's house - THIS WILL BE REMOVED
    # Placing it at tile (column 9, row 8) which is HOUSE_MAP[8][9]
    # This corresponds to the 10th column and 9th row (0-indexed).
    # portal_tile_x = 9 
    # portal_tile_y = 8 
    # exit_portal = ExitPortal(
    #     x_tile_idx=portal_tile_x,
    #     y_tile_idx=portal_tile_y,
    #     tile_size=TILE_GAME_SIZE, # Use TILE_GAME_SIZE for pixel calculation
    #     radius=30, # Similar radius to the wizard's interaction
    #     message="Press E to go back to Town. Press Q to stay with the Wizard",
    #     id="wizard_house_exit_portal" # Assign specific ID
    # )

    # Create the new interactive circle for the "stay query"
    # Adjusted position to be up and to the left
    stay_query_circle = ExitPortal(
        x_tile_idx=7,  # Moved left
        y_tile_idx=7,  # Moved up
        tile_size=TILE_GAME_SIZE,
        radius=30,
        message="Press E to go back to Town. Press Q to stay with the Wizard", # User-specified message
        id="wizard_house_stay_query_circle" # Unique ID for the new circle
    )

    return {
        "map_layout": HOUSE_MAP,
        "building_layout": HOUSE_BUILDING_MAP,
        "collision_layout": HOUSE_COLLISION_MAP,
        "decoration_layout": HOUSE_DECORATION_MAP,
        "tile_size": TILE_GAME_SIZE,
        "tile_orig_size": TILE_ORIG_SIZE,
        "tileset_path": "InteriorTiles.png",
        "tileset_width": TILESET_WIDTH_HOUSE,
        "entry_point_tile": (PLAYER_START_X_TILE, PLAYER_START_Y_TILE),
        "map_interactables": [stay_query_circle] # Only include the single, adjusted circle
    }
