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

except Exception as e:
    print("Could not load an image:", e)
    pygame.quit()
    sys.exit()

# Load planets 
planets = load_planets()


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
    (planet1_img, planet1_pos, "Blazing Exo-Resort of Untamed Luxury with Exotic Wildlife and Molten Fire Spas.", False),
    (planet2_img, planet2_pos, "Luxurious and Furturistic Paradise with hovering gardens and rich foods.", False),
    (planet3_img, planet3_pos, " Adventure meets elegance with anti-grav sled rides, glowing ice cavern tours, and cosmic stargazing lounges .", True)
]

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

def draw_planet_detail(surface, planet_id):
    surface.blit(bg_img, (0, 0))  # You can swap this with a specific background per planet if needed

    font = pygame.font.SysFont("arial", 22, bold=False)
    text = resort_data[planet_id]["description"]
    wrapped_lines = wrap_text(text, font, WIDTH - 100)
    
    box_height = 160
    box_rect = pygame.Rect(40, HEIGHT - box_height - 40, WIDTH - 80, box_height)
    pygame.draw.rect(surface, (0, 0, 0), box_rect.inflate(8, 8), border_radius=10)
    pygame.draw.rect(surface, (30, 30, 60), box_rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), box_rect, width=2, border_radius=10)

    for i, line in enumerate(wrapped_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        surface.blit(text_surf, (box_rect.x + 15, box_rect.y + 15 + i * font.get_height()))

    # Back and Continue buttons
    pygame.draw.rect(surface, (80, 80, 160), (40, HEIGHT - 60, 120, 40), border_radius=10)
    pygame.draw.rect(surface, (80, 160, 80), (WIDTH - 160, HEIGHT - 60, 120, 40), border_radius=10)
    
    back_text = font.render("Back", True, (255, 255, 255))
    continue_text = font.render("Continue", True, (255, 255, 255))
    surface.blit(back_text, (60, HEIGHT - 50))
    surface.blit(continue_text, (WIDTH - 140, HEIGHT - 50))

# Main loop
running = True
while running:
    clock.tick(60)
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

            if game_state == "planet_select":
                mouse_x, mouse_y = event.pos
                for i, (img, (px, py), _, _) in enumerate(planets_info):
                    planet_rect = img.get_rect(center=(px, py))
                    if planet_rect.collidepoint(mouse_x, mouse_y):
                        selected_planet = f"planet{i+1}"
                        transitioning = True
                        game_state = f"transition_to_{selected_planet}"

            if game_state == "planet_detail":
                mouse_x, mouse_y = event.pos

                # Back button
                if pygame.Rect(40, HEIGHT - 60, 120, 40).collidepoint(mouse_x, mouse_y):
                    game_state = "planet_select"  # Go back to planet selection

                # Continue button
                elif pygame.Rect(WIDTH - 160, HEIGHT - 60, 120, 40).collidepoint(mouse_x, mouse_y):
                    game_state = "next_screen"  # Proceed to the next screen

        if event.type == pygame.MOUSEBUTTONUP:
            if game_state == "menu" and start_btn_pressed_state:
                start_btn_pressed_state = False
                start_btn_clicked = True
                transitioning = True
                game_state = "transition_to_planets"

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

    if game_state == "planet_select":
        draw_planet_screen(window, 0)

    elif game_state == "planet_detail":
        draw_planet_detail(window, selected_planet)

    pygame.display.flip()

pygame.quit()
sys.exit()
