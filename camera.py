import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        """Apply camera offset to a rect and return new rect for screen drawing"""
        return pygame.Rect(
            rect.x + self.camera.x,
            rect.y + self.camera.y,
            rect.width,
            rect.height
        )

    def apply_point(self, point):
        """Apply camera offset to a point (x, y) and return screen coordinates"""
        return (point[0] + self.camera.x, point[1] + self.camera.y)

    def update(self, target, map_width, map_height):

        #x = -target.rect.centerx + int(self.width / 2)
        #y = -target.rect.centery + int(self.height / 2)
    
        x = -target.rect.centerx + int(pygame.display.get_surface().get_width() / 2)
        y = -target.rect.centery + int(pygame.display.get_surface().get_height() / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Prevent scrolling left past map edge
        y = min(0, y)  # Prevent scrolling up past map edge
        x = max(-(map_width - self.width), x)  # Prevent scrolling right past map edge
        y = max(-(map_height - self.height), y) # Prevent scrolling down past map edge

        self.camera = pygame.Rect(x, y, self.width, self.height)
