import pygame
import ctypes
from apiTest import get_google_joke


try:
    # Try to set DPI awareness to match pixels to PC (Windows 8.1+)
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    print("used new version.")
except AttributeError:
    # Fallback for older Windows versions
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        print("used older version.")
    except AttributeError:
        print("Could not set DPI awareness. Display scaling issues might persist.")

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set screen dimensions
screen_width = 1440
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption('Pygame Window')

# Character properties
char_color = (255, 0, 0)  # Red
char_width = 50
char_height = 100
char_x = screen_width // 2 - char_width // 2  # Centered horizontally
char_y = screen_height // 2 - char_height // 2 # Centered vertically
char_speed = 1


# Game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                print("Space key pressed!")
            

    # Handle continuous key presses for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        char_x -= char_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        char_x += char_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:   
        char_y -= char_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        char_y += char_speed

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the character
    pygame.draw.rect(screen, char_color, (char_x, char_y, char_width, char_height))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
