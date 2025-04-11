import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NASA Vacation Test")

# Load custom image from assets folder
# Make sure you have a file like 'earth.jpg' inside your assets folder!
image_path = os.path.join("assets", "pink-cartoon-planet.jpg")
try:
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    print(f"Image not found at: {image_path}")
    pygame.quit()
    sys.exit()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))  # draw the image
    pygame.display.flip()           # update the screen

pygame.quit()
sys.exit()