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
    [1 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 6 , -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #25 wide
    [17, 18, 19, 19, 19, 19, 19, 19, 19, 20, 22, -1, 1 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 6 , -1, -1],
    [17, 34, 35, 35, 35, 35, 35, 35, 35, 36, 22, -1 , 17, 18, 19, 19, 19, 19, 19, 19, 19, 19, 20, 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 23, 2, 24, 34, 35, 35, 35, 35, 35, 35, 35, 35, 36, 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 19, 19, 19, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 35, 35, 35, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 7 , 3 , 8 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22, -1, 33, 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 38],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [17, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22],
    [33, 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 3 , 38],
    [-1],
    [-1]

]

HOUSE_BUILDING_MAP = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 57, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 73, -1, 140,141,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 142,143,-1, -1, 146,-1, -1, -1, -1,137, 137,-1, -1, 90, -1, -1, -1, -1, -1, -1],
    [-1, 162,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,153, -1, -1, -1, 106,-1, -1, -1, 207,-1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 89, 223,-1, -1],
    [-1, -1, 13, 14, 14, 14, 14, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 105,-1, -1, -1],
    [-1, 162,29, 30, 30, 30, 30, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 45, 46, 46, 46, 46, 47, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 164,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 180,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

]

HOUSE_COLLISION_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# New decoration layer
# Dimensions should match HOUSE_MAP
# Use EMPTY_TILE_ID for no decoration, and other tile IDs from InteriorTiles.png for decorations
# These are placeholder IDs, update them with actual IDs from InteriorTiles.png
HOUSE_DECORATION_MAP = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 80, 80, -1, -1, -1, -1, -1, -1, -1], 
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
        x_tile_idx=20, 
        y_tile_idx=4, # Adjusted to be near the wizard
        tile_size=TILE_GAME_SIZE,
        radius=30,
        message="Press E to Talk to the Wizard. Press Q to go back to Town", # User-specified message
        id="wizard_house_stay_query_circle" # Unique ID for the new circle
    )

    return {
        "name": "wizard_house",  # ADD THIS LINE
        "map_layout": HOUSE_MAP,
        "building_layout": HOUSE_BUILDING_MAP,
        "collision_layout": HOUSE_COLLISION_MAP,
        "decoration_layout": HOUSE_DECORATION_MAP,
        "tile_size": TILE_GAME_SIZE,
        "tile_orig_size": TILE_ORIG_SIZE,
        "tileset_path": "InteriorTiles.png",
        "tileset_width": TILESET_WIDTH_HOUSE,
        "entry_point_tile": (PLAYER_START_X_TILE, PLAYER_START_Y_TILE),
        "static_entity_data": [
            {
                "image_path": "images/npcs/wizardInHouse.png",
                "tile_x": 21,  # Near top-left
                "tile_y": 3,  # Near top-left
                "scale_to_size": (80, 128)  # Desired display size
            }
        ],
        "map_interactables": [stay_query_circle] # Only include the single, adjusted circle
    }
