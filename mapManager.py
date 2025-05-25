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
        self.current_map_specific_interactables = [] # Stores interactables loaded for the current map

    def switch_map(self, map_name, player, wizard_sprite, all_sprites_group, interaction_mgr, update_dimensions_func): # MODIFIED SIGNATURE
        if map_name in self.maps:
            # Clear existing map-specific interactables from the previous map
            for interactable in self.current_map_specific_interactables:
                interaction_mgr.remove_interactable(interactable.id)
            self.current_map_specific_interactables = []

            self.current_map_name = map_name
            self.current_map_data = self.maps[map_name]
            print(f"Switched to map: {map_name}")

            # CORRECTED KEY and ADDED tileset_width argument
            # Ensure tilemap.init_tilemap is called to load the correct tileset
            tilemap.init_tilemap(
                self.current_map_data["tileset_path"],
                self.current_map_data["tileset_width"], 
                self.current_map_data["tile_orig_size"] 
            )

            # Load and register new map-specific interactables for the current map
            new_map_interactables = self.current_map_data.get("map_interactables", [])
            for interactable_obj in new_map_interactables:
                interaction_mgr.add_interactable(interactable_obj)
                self.current_map_specific_interactables.append(interactable_obj)
            print(f"Loaded {len(self.current_map_specific_interactables)} map-specific interactables for {map_name}.")


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
                if wizard_sprite in all_sprites_group: # Check if it's there before removing
                    all_sprites_group.remove(wizard_sprite)
                interaction_mgr.remove_interactable(wizard_sprite.id) # Use ID for removal
                print(f"Wizard removed from house map.")
            elif map_name == "main_map":
                if wizard_sprite not in all_sprites_group: # Check if it's not there before adding
                    all_sprites_group.add(wizard_sprite)
                # Ensure wizard is re-added if not already present (e.g. after being removed from another map)
                # Check if wizard is already in interactables to avoid duplicate processing if logic changes
                # For now, simply adding it back is the existing pattern.
                interaction_mgr.add_interactable(wizard_sprite) 
                print(f"Wizard added to main map.")


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

    def refresh_active_map_after_reload(self, update_dimensions_func, interaction_mgr=None): # Added interaction_mgr
        """
        Refreshes the current map's data after its source module has been reloaded.
        This method assumes that importlib.reload() has been called on the relevant
        map module (e.g., tilemap.py, wizardHouse.py) before this is called.
        Now also handles refreshing map-specific interactables if interaction_mgr is provided.
        """
        print(f"Refreshing data for map: {self.current_map_name} from reloaded modules.")
        
        # Clear old map-specific interactables if manager is provided
        if interaction_mgr:
            for interactable in self.current_map_specific_interactables:
                interaction_mgr.remove_interactable(interactable.id)
            self.current_map_specific_interactables = []
            print("Cleared old map-specific interactables before refresh.")

        fresh_map_data = None
        if self.current_map_name == "main_map":
            fresh_map_data = tilemap.get_main_map_data()
        elif self.current_map_name == "wizard_house":
            fresh_map_data = wizardHouse.get_wizard_house_data()
        else:
            print(f"Warning: Unknown map name '{self.current_map_name}' during refresh.")
            return

        if fresh_map_data:
            self.maps[self.current_map_name] = fresh_map_data
            self.current_map_data = fresh_map_data

            # Re-initialize tilemap's rendering system with the current map's tileset.
            # This is crucial because reloading the tilemap module resets its globals
            # like tileset_img and tile_rects.
            tilemap.init_tilemap(
                self.current_map_data["tileset_path"],
                self.current_map_data["tileset_width"],
                self.current_map_data["tile_orig_size"]
            )

            # Reload map-specific interactables if manager is provided
            if interaction_mgr:
                new_map_interactables = self.current_map_data.get("map_interactables", [])
                for interactable_obj in new_map_interactables:
                    interaction_mgr.add_interactable(interactable_obj)
                    self.current_map_specific_interactables.append(interactable_obj)
                print(f"Reloaded {len(self.current_map_specific_interactables)} map-specific interactables for {self.current_map_name}.")

            # Update game-wide map dimensions based on the reloaded data
            new_map_width_pixels = len(self.current_map_data["map_layout"][0]) * self.current_map_data["tile_size"]
            new_map_height_pixels = len(self.current_map_data["map_layout"]) * self.current_map_data["tile_size"]
            update_dimensions_func(new_map_width_pixels, new_map_height_pixels)
            
            print(f"Map '{self.current_map_name}' data refreshed and dimensions updated.")
        else:
            print(f"Error: Could not get fresh map data for '{self.current_map_name}'.")


    def can_move(self, world_x, world_y):
        """Checks if the given world coordinates are walkable on the current map."""
        tile_size = self.get_current_tile_size()
        tile_x = world_x // tile_size
        tile_y = world_y // tile_size
        
        collision_layout = self.get_current_collision_layout()

        if 0 <= tile_y < len(collision_layout) and 0 <= tile_x < len(collision_layout[0]):
            return collision_layout[tile_y][tile_x] == 0
        return False # Out of bounds is not walkable
