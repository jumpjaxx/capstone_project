import pygame
import sys
import os
import load_images


# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1018, 573
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Low-G Horizons")
clock = pygame.time.Clock()

# Load images
try:
    bg_img = pygame.image.load(os.path.join("assets", "spacescrolling.jpg")).convert()
    logo_img = pygame.image.load(os.path.join("assets", "Low - G Horizon.svg")).convert_alpha()
    start_btn_idle = pygame.image.load(os.path.join("assets", "start_button.png")).convert_alpha()
    start_btn_pressed = pygame.image.load(os.path.join("assets", "pushed_start.png")).convert_alpha()
except:
    print("Could not load an image. Check the file path!")
    pygame.quit()
    sys.exit()

# Optional: Scale button smaller
start_btn_idle = pygame.transform.scale(start_btn_idle, (200, 80))
start_btn_pressed = pygame.transform.scale(start_btn_pressed, (200, 80))

# Background scrolling
bg_width = bg_img.get_width()
scroll_x = 0
scroll_speed = 0.4

# Logo animation
start_time = pygame.time.get_ticks()
logo_y = -logo_img.get_height()
logo_target_y = -105

# Start button animation
start_btn_y = HEIGHT + start_btn_idle.get_height()  # Start off-screen
start_btn_target_y = HEIGHT // 2
start_btn_visible = False
start_btn_pressed_state = False
start_btn_clicked = False

# Main loop
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if start_btn_visible and not start_btn_clicked:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
                btn_rect = start_btn_idle.get_rect(topleft=(btn_x, start_btn_y))
                if btn_rect.collidepoint(mouse_x, mouse_y):
                    start_btn_pressed_state = True

            if event.type == pygame.MOUSEBUTTONUP:
                if start_btn_pressed_state:
                    print("Start button released — go to next screen!")
                    start_btn_pressed_state = False
                    start_btn_clicked = True  # you’ll add your screen transition here

    # Animate logo
    if current_time - start_time > 1000:
        if logo_y < logo_target_y:
            logo_y += 5
            if logo_y > logo_target_y:
                logo_y = logo_target_y

    # Animate start button after 2 seconds
    if current_time - start_time > 2000:
        start_btn_visible = True
        if start_btn_y > start_btn_target_y:
            start_btn_y -= 5
            if start_btn_y < start_btn_target_y:
                start_btn_y = start_btn_target_y

    # Scroll background
    scroll_x -= scroll_speed
    if abs(scroll_x) > bg_width:
        scroll_x = 0

    # Draw everything
    window.blit(bg_img, (scroll_x, 0))
    window.blit(bg_img, (scroll_x + bg_width, 0))

    # Draw logo
    if current_time - start_time > 1000:
        window.blit(logo_img, (WIDTH // 2 - logo_img.get_width() // 2 + 30, logo_y))

    # Draw button
    if start_btn_visible:
        btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
        current_btn_img = start_btn_pressed if start_btn_pressed_state else start_btn_idle
        window.blit(current_btn_img, (btn_x, start_btn_y))

    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()