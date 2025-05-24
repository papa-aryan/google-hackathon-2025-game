import pygame
import tilemap # To get main map data
import wizardHouse # To get wizard house map data

class MapManager:
    def __init__(self):
        self.maps = {
            "main_map": tilemap.get_main_map_data(),
            "wizard_house": wizardHouse.get_wizard_house_data()
        }
        self.current_map_name = "main_map"
        self.current_map_data = self.maps[self.current_map_name]

    def switch_map(self, map_name, player):
        if map_name in self.maps:
            self.current_map_name = map_name
            self.current_map_data = self.maps[map_name]
            print(f"Switched to map: {map_name}")

            # Update game-wide map dimensions
            new_map_width_pixels = len(self.current_map_data["map_layout"][0]) * self.current_map_data["tile_size"]
            new_map_height_pixels = len(self.current_map_data["map_layout"]) * self.current_map_data["tile_size"]
            
            # Access main.py's global map dimensions and update them
            # This is a bit of a hack; a better way would be to pass a callback or use a global state manager
            import main
            main.map_width = new_map_width_pixels
            main.map_height = new_map_height_pixels
            main.update_map_dimensions_from_manager(new_map_width_pixels, new_map_height_pixels)


            # Position player at the entry point of the new map
            entry_point_tile = self.current_map_data.get("entry_point_tile")
            if entry_point_tile:
                player.rect.topleft = (
                    entry_point_tile[0] * self.current_map_data["tile_size"],
                    entry_point_tile[1] * self.current_map_data["tile_size"]
                )
            else: # Default to top-left if no entry point defined
                player.rect.topleft = (0,0)
            
            # Potentially hide/show NPCs based on the current map
            # For example, the wizard should only be on the main_map
            if map_name == "wizard_house":
                if main.wizard in main.all_sprites:
                    main.all_sprites.remove(main.wizard)
                    main.interaction_manager.remove_interactable(main.wizard.id) # Assumes such a method exists
            elif map_name == "main_map":
                if main.wizard not in main.all_sprites:
                    main.all_sprites.add(main.wizard)
                    main.interaction_manager.add_interactable(main.wizard)


        else:
            print(f"Error: Map '{map_name}' not found.")

    def get_current_map_layout(self):
        return self.current_map_data["map_layout"]

    def get_current_building_layout(self):
        return self.current_map_data.get("building_layout") # Use .get for optional layers

    def get_current_collision_layout(self):
        return self.current_map_data["collision_layout"]

    def get_current_tile_size(self):
        return self.current_map_data["tile_size"]

    def can_move(self, world_x, world_y):
        """Checks if the given world coordinates are walkable on the current map."""
        tile_size = self.get_current_tile_size()
        tile_x = world_x // tile_size
        tile_y = world_y // tile_size
        
        collision_layout = self.get_current_collision_layout()

        if 0 <= tile_y < len(collision_layout) and 0 <= tile_x < len(collision_layout[0]):
            return collision_layout[tile_y][tile_x] == 0
        return False # Out of bounds is not walkable
