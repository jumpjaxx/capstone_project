import pygame
import sys
import os
from resort_management import load_planets  # Your custom module

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1018, 573
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Low-G Horizons")
clock = pygame.time.Clock()

# Load images
try:
    bg_img = pygame.image.load(os.path.join("assets", "misc", "spacescrolling.jpg")).convert_alpha()
    logo_img = pygame.image.load(os.path.join("assets", "misc", "Low - G Horizon.svg")).convert_alpha()
    start_btn_idle = pygame.image.load(os.path.join("assets", "misc", "start_button.png")).convert_alpha()
    start_btn_pressed = pygame.image.load(os.path.join("assets", "misc", "pushed_start.png")).convert_alpha()

    # Load planet images
    planet1_img = pygame.image.load(os.path.join("assets", "planets", "hot-color-planet.png")).convert_alpha()
    planet2_img = pygame.image.load(os.path.join("assets", "planets", "new_hot_planets.png")).convert_alpha()
    planet3_img = pygame.image.load(os.path.join("assets", "planets", "new_futuristic_planet.png")).convert_alpha()

except Exception as e:
    print("Could not load an image:", e)
    pygame.quit()
    sys.exit()

# Load planets (if needed)
planets = load_planets()

# Optional: Scale button smaller
start_btn_idle = pygame.transform.scale(start_btn_idle, (200, 80))
start_btn_pressed = pygame.transform.scale(start_btn_pressed, (200, 80))

# Optional: Scale planet images
planet_size = (100, 100)
planet1_img = pygame.transform.scale(planet1_img, planet_size)
planet2_img = pygame.transform.scale(planet2_img, planet_size)
planet3_img = pygame.transform.scale(planet3_img, planet_size)

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
game_state = "menu"  # could be 'menu', 'transition_to_planets', 'planet_select', 'transition_to_planetX', 'planet_screen'
transitioning = False
transition_offset = 0

# Planet positions
# Repositioned planet positions
planet1_pos = (200, 150)                # Top-left
planet2_pos = (WIDTH // 2, 450)         # Middle-bottom
planet3_pos = (WIDTH - 200, 150)        # Top-right
planet_radius = 100

planets_info = [
    (planet1_img, planet1_pos),
    (planet2_img, planet2_pos),
    (planet3_img, planet3_pos)
]

def draw_planet_screen(surface, x_offset=0):
    surface.blit(bg_img, (x_offset, 0))  # Background reuse

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for img, (px, py) in planets_info:
        planet_rect = img.get_rect(center=(x_offset + px, py))  # Always define first

        # Check if mouse is hovering
        if planet_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.circle(surface, (255, 255, 255), (x_offset + px, py), planet_radius + 10)

        surface.blit(img, planet_rect)


# Main loop
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Handle events
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

            if game_state == "planet_select":
                mouse_x, mouse_y = event.pos
                for i, (img, (px, py)) in enumerate(planets_info):
                    planet_rect = img.get_rect(center=(px, py))
                    if planet_rect.collidepoint(mouse_x, mouse_y):
                        print(f"Planet {i+1} clicked!")
                        transitioning = True
                        game_state = f"transition_to_planet{i+1}"

        if event.type == pygame.MOUSEBUTTONUP:
            if game_state == "menu" and start_btn_pressed_state:
                start_btn_pressed_state = False
                start_btn_clicked = True
                transitioning = True
                game_state = "transition_to_planets"

    # Animate logo
    if current_time - start_time > 1000 and logo_y < logo_target_y:
        logo_y += 5
        if logo_y > logo_target_y:
            logo_y = logo_target_y

    # Animate start button
    if current_time - start_time > 2000:
        start_btn_visible = True
        if start_btn_y > start_btn_target_y:
            start_btn_y -= 5
            if start_btn_y < start_btn_target_y:
                start_btn_y = start_btn_target_y

    # Background scroll
    scroll_x -= scroll_speed
    if abs(scroll_x) > bg_width:
        scroll_x = 0

    # Handle transitions
    if transitioning:
        transition_offset += 20  # Move transition faster
        if transition_offset >= WIDTH:
            transitioning = False
            transition_offset = 0
            if game_state == "transition_to_planets":
                game_state = "planet_select"
            elif "transition_to_planet" in game_state:
                game_state = "planet_screen"

    # --- DRAWING ---
    window.fill((0, 0, 0))

    if game_state in ["menu", "transition_to_planets"]:
        x_offset = -transition_offset if transitioning else 0
        window.blit(bg_img, (x_offset + scroll_x, 0))
        window.blit(bg_img, (x_offset + scroll_x + bg_width, 0))
        if current_time - start_time > 1000:
            window.blit(logo_img, (x_offset + WIDTH // 2 - logo_img.get_width() // 2 + 30, logo_y))

        if start_btn_visible:
            btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
            current_btn_img = start_btn_pressed if start_btn_pressed_state else start_btn_idle
            window.blit(current_btn_img, (x_offset + btn_x, start_btn_y))

    elif game_state in ["planet_select", "transition_to_planet1", "transition_to_planet2", "transition_to_planet3"]:
        x_offset = -transition_offset if transitioning else 0
        draw_planet_screen(window, x_offset)

    elif game_state == "planet_screen":
        font = pygame.font.SysFont(None, 60)
        text = font.render("Planet Screen!", True, (255, 255, 255))
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
