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
    logo_img = pygame.image.load(os.path.join("assets", "Low - G Horizon.svg")).convert_alpha()
except:
    print("🚨 Could not load an image. Check the file path!")
    pygame.quit()
    sys.exit()

bg_width = bg_img.get_width()
scroll_x = 0
scroll_speed = 0.4

start_time = pygame.time.get_ticks()
logo_y = -logo_img.get_height()
#btn_y = HEIGHT + start_btn_img.get_height()
logo_target_y = -114
#btn_target_y = 400

show_logo = False
#show_button = False
button_clicked = False

# Game loop
running = True
clock = pygame.time.Clock()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 FPS
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Animate logo
    if current_time - start_time > 1000:
        show_logo = True
    if show_logo and logo_y < logo_target_y:
        logo_y += 5  # Adjust speed if needed
        
    # Scroll background
    scroll_x -= scroll_speed
    if abs(scroll_x) > bg_width:
        scroll_x = 0

    # Draw scrolling background
    window.blit(bg_img, (scroll_x, 0))
    window.blit(bg_img, (scroll_x + bg_width, 0))
    
    # Draw logo
    if show_logo:
        window.blit(logo_img, (WIDTH//2 - logo_img.get_width()//2, logo_y))

    pygame.display.flip()
    

pygame.quit()
sys.exit()