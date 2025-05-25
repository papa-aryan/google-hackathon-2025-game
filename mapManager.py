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

    def switch_map(self, map_name, player, wizard_sprite, all_sprites_group, interaction_mgr, update_dimensions_func): # MODIFIED SIGNATURE
        if map_name in self.maps:
            self.current_map_name = map_name
            self.current_map_data = self.maps[map_name]
            print(f"Switched to map: {map_name}")

            # CORRECTED KEY and ADDED tileset_width argument
            tilemap.init_tilemap(
                self.current_map_data["tileset_path"],
                self.current_map_data["tileset_width"], # Pass the specific width
                self.current_map_data["tile_orig_size"] # Pass the specific original tile size
            )


            # Update game-wide map dimensions
            new_map_width_pixels = len(self.current_map_data["map_layout"][0]) * self.current_map_data["tile_size"]
            new_map_height_pixels = len(self.current_map_data["map_layout"]) * self.current_map_data["tile_size"]
            

            update_dimensions_func(new_map_width_pixels, new_map_height_pixels) # MODIFIED CALL


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
            if map_name == "wizard_house":
                if wizard_sprite in all_sprites_group: # MODIFIED
                    all_sprites_group.remove(wizard_sprite) # MODIFIED
                    interaction_mgr.remove_interactable(wizard_sprite.id) # MODIFIED
            elif map_name == "main_map":
                if wizard_sprite not in all_sprites_group: # MODIFIED
                    all_sprites_group.add(wizard_sprite) # MODIFIED
                    interaction_mgr.add_interactable(wizard_sprite) # MODIFIED


        else:
            print(f"Error: Map '{map_name}' not found.")

    def get_current_map_layout(self):
        return self.current_map_data["map_layout"]

    def get_current_building_layout(self):
        return self.current_map_data.get("building_layout") # Use .get for optional layers

    def get_current_decoration_layout(self):
        return self.current_map_data.get("decoration_layout") # ADDED: Getter for decoration layer

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
