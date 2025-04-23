import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 1018, 573
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Start Button Test")
clock = pygame.time.Clock()

# Load image
try:
    start_btn_img = pygame.image.load(os.path.join("assets", "start_button.png")).convert_alpha()
except:
    print("Could not load start button image. Check the file path.")
    pygame.quit()
    sys.exit()

# Button position
btn_x = (WIDTH // 2) - (start_btn_img.get_width() // 2)
btn_y = (HEIGHT // 2) - (start_btn_img.get_height() // 2)

# Main loop
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    window.fill((255, 255, 255))

    # Draw button
    window.blit(start_btn_img, (btn_x, btn_y))

    # Update display
    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()