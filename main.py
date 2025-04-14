import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1018, 573
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Low-G Horizons")
window.fill((255, 255, 255))

pygame.display.flip()

# Load background image
try:
    bg_img = pygame.image.load(os.path.join("assets", "spacescrolling.jpg")).convert()
except:
    print("🚨 Could not load background image. Check the file path!")
    pygame.quit()
    sys.exit()

bg_width = bg_img.get_width()
scroll_x = 0
scroll_speed = 0.4

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Scroll background
    scroll_x -= scroll_speed
    if abs(scroll_x) > bg_width:
        scroll_x = 0

    # Draw scrolling background
    window.blit(bg_img, (scroll_x, 0))
    window.blit(bg_img, (scroll_x + bg_width, 0))

    pygame.display.flip()
    

pygame.quit()
sys.exit()