import pygame
import sys
import os
from resort_management import load_planets

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
    
    
planets = load_planets()

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

# Game state control
game_state = "menu"  # could be 'menu', 'transition_to_planets', 'planet_select', 'transition_to_planetX'
transitioning = False
transition_offset = 0

# Planet positions
planet_radius = 50
planet1_pos = (250, 300)
planet2_pos = (450, 300)
planet3_pos = (650, 300)


def draw_planet_screen(surface, x_offset=0):
    surface.blit(bg_img, (x_offset, 0))  # re-use bg
    pygame.draw.circle(surface, (100, 100, 255), (x_offset + planet1_pos[0], planet1_pos[1]), planet_radius)
    pygame.draw.circle(surface, (255, 100, 100), (x_offset + planet2_pos[0], planet2_pos[1]), planet_radius)
    pygame.draw.circle(surface, (100, 255, 100), (x_offset + planet3_pos[0], planet3_pos[1]), planet_radius)


# Main loop
running = True
while running:
    clock.tick(60)
    
# Handle transitions
if transitioning:
    transition_offset += 20  # animation speed
    if transition_offset >= WIDTH:
        transitioning = False
        transition_offset = 0
        if game_state == "transition_to_planets":
            game_state = "planet_select"
        elif "transition_to_planet" in game_state:
            game_state = "planet_screen"  # Placeholder for planet view




    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu" and start_btn_visible and not start_btn_clicked:
                mouse_x, mouse_y = event.pos
                btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
                btn_rect = start_btn_idle.get_rect(topleft=(btn_x, start_btn_y))
                if btn_rect.collidepoint(mouse_x, mouse_y):
                    start_btn_pressed_state = True

        if event.type == pygame.MOUSEBUTTONUP:
            if game_state == "menu" and start_btn_pressed_state:
                start_btn_pressed_state = False
                start_btn_clicked = True
                transitioning = True
                game_state = "transition_to_planets"
            elif game_state == "planet_select":
                mx, my = event.pos
                for i, (px, py) in enumerate([planet1_pos, planet2_pos, planet3_pos]):
                    dist = ((mx - px)**2 + (my - py)**2)**0.5
                    if dist < planet_radius:
                        print(f"Planet {i+1} clicked!")
                        transitioning = True
                        game_state = f"transition_to_planet{i+1}"

                        mouse_x, mouse_y = event.pos
                        btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
                        btn_rect = start_btn_idle.get_rect(topleft=(btn_x, start_btn_y))
                        if btn_rect.collidepoint(mouse_x, mouse_y):
                            start_btn_pressed_state = True

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
# Draw based on game state and transition
if game_state in ["menu", "transition_to_planets"]:
    x_offset = -transition_offset
    window.blit(bg_img, (x_offset + scroll_x, 0))
    window.blit(bg_img, (x_offset + scroll_x + bg_width, 0))

    if current_time - start_time > 1000:
        window.blit(logo_img, (x_offset + WIDTH // 2 - logo_img.get_width() // 2 + 30, logo_y))

    if start_btn_visible:
        btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
        current_btn_img = start_btn_pressed if start_btn_pressed_state else start_btn_idle
        window.blit(current_btn_img, (x_offset + btn_x, start_btn_y))

if game_state in ["planet_select", "transition_to_planets"]:
    draw_planet_screen(window, WIDTH - transition_offset)

if game_state == "planet_screen":
    window.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 60)
    text = font.render("Planet Screen!", True, (255, 255, 255))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

pygame.display.flip()


# Quit
pygame.quit()
sys.exit()