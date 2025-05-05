import pygame
import sys
import os
from resort_management import load_planets  # Your custom module
from resort_management import load_resort_data

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

    # Load planet surface images
    planet1_surface = pygame.image.load(os.path.join("assets", "resort_views", "futuristic_resort.png")).convert_alpha()
    planet2_surface = pygame.image.load(os.path.join("assets", "resort_views", "desert-planet.jpg")).convert_alpha()
    planet3_surface = pygame.image.load(os.path.join("assets", "resort_views", "cold-planet.jpg")).convert_alpha()

    # Load buttons
    back_button = pygame.image.load(os.path.join("assets", "misc", "back_button_bigger.png")).convert_alpha()
    continue_button = pygame.image.load(os.path.join("assets", "misc", "continue_button.png")).convert_alpha()

except Exception as e:
    print("Could not load an image:", e)
    pygame.quit()
    sys.exit()

# Load planets 
planets = load_planets()
start_btn_visible = True  # Ensure the start button is visible in the menu

# Optional: Scale button smaller
start_btn_idle = pygame.transform.scale(start_btn_idle, (200, 80))
start_btn_pressed = pygame.transform.scale(start_btn_pressed, (200, 80))

# Optional: Scale planet images
planet_size = (180, 180)
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
logo_target_y = 100

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
planet1_pos = (200, 150)                # Top-left
planet2_pos = (WIDTH // 2, 450)         # Middle-bottom
planet3_pos = (WIDTH - 200, 150)        # Top-right
planet_radius = 100

planets_info = [
    (planet1_img, planet1_pos, "Blazing Exo-Resort of Untamed Luxury with Exotic Wildlife and Molten Fire Spas.", False),
    (planet2_img, planet2_pos, "Luxurious and Futuristic Paradise with hovering gardens and rich foods.", False),
    (planet3_img, planet3_pos, "Adventure meets elegance with anti-grav sled rides, glowing ice cavern tours, and cosmic stargazing lounges.", True)
]

# Planet surface info
planet_surfaces = [planet1_surface, planet2_surface, planet3_surface]

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def draw_planet_screen(surface):
    surface.blit(bg_img, (0, 0))  # Background image

    # Loop through planets_info and display planet images
    for i, (img, (x, y), desc, has_detail) in enumerate(planets_info):
        planet_rect = img.get_rect(center=(x, y))
        surface.blit(img, planet_rect)  # Draw the planet image
        
        # Draw the hover info box if the mouse is over a planet
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if planet_rect.collidepoint(mouse_x, mouse_y):
            font = pygame.font.SysFont("arial", 18)
            wrapped_lines = wrap_text(desc, font, 300)  # Wrap text within a box width
            box_rect = pygame.Rect(x - 150, y + 100, 300, len(wrapped_lines) * 22 + 20)  # Box size
            pygame.draw.rect(surface, (0, 0, 0), box_rect.inflate(10, 10), border_radius=8)  # Shadow
            pygame.draw.rect(surface, (50, 50, 120), box_rect, border_radius=8)  # Box background
            # Draw the description text
            for j, line in enumerate(wrapped_lines):
                text_surf = font.render(line, True, (255, 255, 255))
                surface.blit(text_surf, (box_rect.x + 10, box_rect.y + 10 + j * 22))

        # Handle clicks on planets
        if planet_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            if has_detail:  # Only allow planet click if the planet has a detail screen
                selected_planet = f"planet{i+1}"  # Save the selected planet (planet1, planet2, etc.)
                transitioning = True
                game_state = f"transition_to_planet{i+1}"  # Transition state

def draw_planet_detail(surface, planet_id):
    surface.blit(bg_img, (0, 0))  # Background image

    # Get the planet surface image
    surface_img = planet_surfaces[planet_id]

    # Draw the planet surface (larger image)
    surface.blit(surface_img, (WIDTH // 2 - surface_img.get_width() // 2, HEIGHT // 2 - surface_img.get_height() // 2))

    # Draw the description box at the bottom
    font = pygame.font.SysFont("arial", 22, bold=False)
    wrapped_lines = wrap_text(planets_info[planet_id][2], font, WIDTH - 100)
    box_height = 160
    box_rect = pygame.Rect(40, HEIGHT - box_height - 40, WIDTH - 80, box_height)
    pygame.draw.rect(surface, (0, 0, 0), box_rect.inflate(8, 8), border_radius=10)  # Shadow
    pygame.draw.rect(surface, (30, 30, 60), box_rect, border_radius=10)  # Box background
    pygame.draw.rect(surface, (255, 255, 255), box_rect, width=2, border_radius=10)  # Border

    # Draw the text
    for i, line in enumerate(wrapped_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        surface.blit(text_surf, (box_rect.x + 15, box_rect.y + 15 + i * font.get_height()))

    # Back and Continue buttons
    surface.blit(back_button, (40, HEIGHT - 70))
    surface.blit(continue_button, (WIDTH - 180, HEIGHT - 70))

# Main loop
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle click on start button
            if game_state == "menu" and start_btn_visible and not start_btn_clicked:
                mouse_x, mouse_y = event.pos
                btn_x = (WIDTH // 2) - (start_btn_idle.get_width() // 2)
                btn_rect = start_btn_idle.get_rect(topleft=(btn_x, start_btn_y))
                if btn_rect.collidepoint(mouse_x, mouse_y):
                    start_btn_pressed_state = True

            # Handle clicks on planets in planet_select screen
            if game_state == "planet_select":
                mouse_x, mouse_y = event.pos
                for i, (img, (px, py), _, _) in enumerate(planets_info):
                    planet_rect = img.get_rect(center=(px, py))
                    if planet_rect.collidepoint(mouse_x, mouse_y):
                        selected_planet = i  # Store the index, not the string like "planet1"
                        transitioning = True
                        game_state = f"transition_to_planet{i+1}"

            # Handle clicks on back/continue buttons in planet_detail
            if game_state == "planet_detail":
                mouse_x, mouse_y = event.pos

                # Back button
                if pygame.Rect(40, HEIGHT - 70, 120, 50).collidepoint(mouse_x, mouse_y):
                    game_state = "planet_select"  # Go back to planet selection

                # Continue button
                elif pygame.Rect(WIDTH - 180, HEIGHT - 70, 120, 50).collidepoint(mouse_x, mouse_y):
                    print(f"Continuing from Planet {selected_planet + 1}...")
                    game_state = "next_screen"  # Proceed to the next screen

        if event.type == pygame.MOUSEBUTTONUP:
            if game_state == "menu":
                if start_btn_pressed_state:
                    start_btn_clicked = True
                    game_state = "planet_select"
                    start_btn_pressed_state = False

    # Draw each screen based on the game state
    window.fill((0, 0, 0))

    if game_state == "menu":
        # Draw the background first
        window.blit(bg_img, (scroll_x, 0))
        window.blit(bg_img, (scroll_x + bg_width, 0))

        # Animate and draw the logo
        if logo_y < logo_target_y:
            logo_y += 5  # Adjust speed as needed
        window.blit(logo_img, (WIDTH // 2 - logo_img.get_width() // 2, logo_y))

        # Animate and draw the start button
        if start_btn_y > start_btn_target_y:
            start_btn_y -= 5  # Adjust speed as needed
        if start_btn_visible:
            button_image = start_btn_pressed if start_btn_pressed_state else start_btn_idle
            window.blit(button_image, (WIDTH // 2 - button_image.get_width() // 2, start_btn_y))

    elif game_state == "planet_select":
        # Draw the planet selection screen
        draw_planet_screen(window)

    elif game_state == "planet_detail":
        # Draw the planet detail screen
        draw_planet_detail(window, selected_planet)

    # Scroll the background
    scroll_x -= scroll_speed
    if scroll_x <= -bg_width:
        scroll_x = 0
    window.blit(bg_img, (scroll_x, 0))
    window.blit(bg_img, (scroll_x + bg_width, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()
