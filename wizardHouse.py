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
    [0, 0, 0, 0, 0, 0, 0, 0, 16, 16],
    [0, 0, 0, 0, 0, 0, 0, 0, 16, 16],
    [0, 0, 0, 0, 0, 0, 0, 0, 16, 16],
    [0, 0, 0, 32, 32, 32, 0, 0, 0, 0],
    [0, 0, 0, 32, 32, 32, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

HOUSE_BUILDING_MAP = [
    [EMPTY_TILE_ID] * 10 for _ in range(len(HOUSE_MAP))
]

HOUSE_COLLISION_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1], # Example: Table collision
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1], # Example: Table collision
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# New decoration layer
# Dimensions should match HOUSE_MAP
# Use EMPTY_TILE_ID for no decoration, and other tile IDs from InteriorTiles.png for decorations
# These are placeholder IDs, update them with actual IDs from InteriorTiles.png
HOUSE_DECORATION_MAP = [
    [EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID],
    [EMPTY_TILE_ID, 80, EMPTY_TILE_ID, EMPTY_TILE_ID, 48, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID], # Example: a plant (tile ID 48)
    [EMPTY_TILE_ID, 80, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID],
    [EMPTY_TILE_ID, 80, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, 52, EMPTY_TILE_ID, EMPTY_TILE_ID], # Example: a carpet (tile ID 52)
    [EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID],
    [EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID],
    [EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID],
    [EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID, EMPTY_TILE_ID],
]

PLAYER_START_X_TILE = 4
PLAYER_START_Y_TILE = 5

def get_wizard_house_data():
    return {
        "name": "wizard_house", # Added name for consistency
        "map_layout": HOUSE_MAP,
        "building_layout": HOUSE_BUILDING_MAP,
        "decoration_layout": HOUSE_DECORATION_MAP, # ADDED: Decoration layer
        "collision_layout": HOUSE_COLLISION_MAP,
        "tile_size": TILE_GAME_SIZE, # Game size for rendering
        "tileset_path": 'InteriorTiles.png', # Use new tileset path
        "tileset_width": TILESET_WIDTH_HOUSE, # Tileset width for this map
        "tile_orig_size": TILE_ORIG_SIZE, # ADDED: Original tile size for this tileset
        "entry_point_tile": (PLAYER_START_X_TILE, PLAYER_START_Y_TILE)
    }
