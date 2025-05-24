import pygame

# Constants for the Wizard's House map
TILE_ORIG_SIZE = 16
TILE_GAME_SIZE = 64
TILESET_WIDTH = 45
EMPTY_TILE_ID = -1

# Wizard House Map Data (A simple 10x8 room)
# Tile IDs are placeholders; adjust them to match your 'cloud_tileset.png'
# 100: Wall tile, 41: Floor tile, 150: Door/Exit tile
# Table: 200-202 (top row), 245-247 (bottom row)
HOUSE_MAP = [
    [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    [100,  41,  41,  41,  41,  41,  41,  41,  41, 100],
    [100,  41,  41,  41,  41,  41,  41,  41,  41, 100],
    [100,  41,  41, 200, 201, 202,  41,  41,  41, 100],
    [100,  41,  41, 245, 246, 247,  41,  41,  41, 100],
    [100,  41,  41,  41,  41,  41,  41,  41,  41, 100],
    [100,  41,  41,  41, 150, 150,  41,  41,  41, 100], # Door at (4,6) and (5,6)
    [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
]

HOUSE_BUILDING_MAP = [
    [EMPTY_TILE_ID] * 10 for _ in range(len(HOUSE_MAP))
]

HOUSE_COLLISION_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

PLAYER_START_X_TILE = 4
PLAYER_START_Y_TILE = 5

def get_wizard_house_data():
    return {
        "name": "wizard_house", # Added name for consistency
        "map_layout": HOUSE_MAP,
        "building_layout": HOUSE_BUILDING_MAP,
        "collision_layout": HOUSE_COLLISION_MAP,
        "tile_size": TILE_GAME_SIZE,
        "tileset_path": 'cloud_tileset.png', # Assuming same tileset as main map
        "entry_point_tile": (PLAYER_START_X_TILE, PLAYER_START_Y_TILE)
    }
