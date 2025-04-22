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

# Load images
try:
    bg_img = pygame.image.load(os.path.join("assets", "spacescrolling.jpg")).convert()
    logo_img = pygame.image.load(os.path.join("assets", "Low - G Horizon.svg")).convert_alpha()
    start_btn_idle = pygame.image.load(os.path.join("assets", "start_button.png")).convert_alpha()
    start_btn_pressed = pygame.image.load(os.path.join("assets", "pushed_start.png")).convert_alpha()
except:
    print("🚨 Could not load an image. Check the file path!")
    pygame.quit()
    sys.exit()

# Background scrolling
bg_width = bg_img.get_width()
scroll_x = 0
scroll_speed = 0.4

# Timing & positions
start_time = pygame.time.get_ticks()
logo_y = -logo_img.get_height()
logo_target_y = -105

# Button animation & states
start_btn_y = HEIGHT + start_btn_idle.get_height()
start_btn_target_y = 400
start_btn_visible = False
start_btn_pressed_state = False
start_btn_clicked = False

# Control flags
show_logo = False
running = True
clock = pygame.time.Clock()

# Main game loop
while running:
    
    start_btn_visible = True
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if start_btn_visible and not start_btn_clicked:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                start_btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
                start_btn_rect = start_btn_idle.get_rect(topleft=(start_btn_x, start_btn_y))
                if start_btn_rect.collidepoint(mouse_x, mouse_y):
                    start_btn_pressed_state = True

            if event.type == pygame.MOUSEBUTTONUP:
                if start_btn_pressed_state:
                    print("🚀 START button released — transition to next screen")
                    start_btn_pressed_state = False
                    start_btn_clicked = True
                    #todo: transition to next screen here

    # Animate logo
    if current_time - start_time > 1000:
        show_logo = True
    if show_logo and logo_y < logo_target_y:
        logo_y += 5

    # Animate start button (comes up 2 sec after start)
    if current_time - start_time > 2000:
        start_btn_visible = True
    if start_btn_visible and start_btn_y > start_btn_target_y:
        start_btn_y -= 5

    # Scroll background
    scroll_x -= scroll_speed
    if abs(scroll_x) > bg_width:
        scroll_x = 0

    # Draw everything
    window.blit(bg_img, (scroll_x, 0))
    window.blit(bg_img, (scroll_x + bg_width, 0))

    if show_logo:
        window.blit(logo_img, (WIDTH//2 - logo_img.get_width()//2 + 30, logo_y))

    if start_btn_visible:
        start_btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
        current_btn_img = start_btn_pressed if start_btn_pressed_state else start_btn_idle
        window.blit(current_btn_img, (start_btn_x, start_btn_y))

    
    pygame.display.flip()

# Clean exit
pygame.quit()
sys.exit()