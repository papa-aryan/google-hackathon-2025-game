# READ THIS COMMENT CAREFULLY!
# THE CODE BELOW IT SIMPLY EXAMPLE CODE PROVIDED FOR CONTEXT!
# IT IS JUST TO SHOWCASE HOW THE MAP MANAGER MIGHT BE IMPLEMENTED.
# obviously there is no "village.tmx" or "house_interior.tmx" files in this context.
# the "main map" is currently defined in tilemap.py (with multiple layers)

class MapManager:
    def __init__(self):
        self.maps = {
            "village": load_map("village.tmx"),
            "house":   load_map("house_interior.tmx")
        }
        self.current = self.maps["village"]

    def load(self, name):
        self.current = self.maps[name]
        # reset camera bounds, collision, etc. based on new map
