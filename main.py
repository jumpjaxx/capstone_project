import pygame
import sys
import os
from resort_management import load_planets  # Custom module

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1018, 573
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Low-G Horizons")
clock = pygame.time.Clock()

# Load images
try:
    bg_img = pygame.image.load(os.path.join("assets", "misc", "spacescrolling.jpg")).convert()
    logo_img = pygame.image.load(os.path.join("assets", "misc", "Low - G Horizon.svg")).convert_alpha()
    start_btn_idle = pygame.image.load(os.path.join("assets", "misc", "start_button.png")).convert_alpha()
    start_btn_pressed = pygame.image.load(os.path.join("assets", "misc", "pushed_start.png")).convert_alpha()

    planet1_img = pygame.image.load(os.path.join("assets", "planets", "hot-color-planet.png")).convert_alpha()
    planet2_img = pygame.image.load(os.path.join("assets", "planets", "new_hot_planets.png")).convert_alpha()
    planet3_img = pygame.image.load(os.path.join("assets", "planets", "new_futuristic_planet.png")).convert_alpha()
except Exception as e:
    print("Image load error:", e)
    pygame.quit()
    sys.exit()

# Scale assets
start_btn_idle = pygame.transform.scale(start_btn_idle, (200, 80))
start_btn_pressed = pygame.transform.scale(start_btn_pressed, (200, 80))
planet_size = (180, 180)
planet1_img = pygame.transform.scale(planet1_img, planet_size)
planet2_img = pygame.transform.scale(planet2_img, planet_size)
planet3_img = pygame.transform.scale(planet3_img, planet_size)

# Scroll background
bg_width = bg_img.get_width()
scroll_x = 0
scroll_speed = 0.4

# Game state
game_state = "menu"

# Animation values
logo_y = -logo_img.get_height()
logo_target_y = 0
start_btn_y = HEIGHT + 100
start_btn_target_y = 400  # Mid-screen below the logo
start_btn_pressed_state = False
start_btn_clicked = False

# Load planets
description_font = pygame.font.SysFont("arial", 18)
planets_info = [
    (planet1_img, (200, 150), "Blazing Exo-Resort of Untamed Luxury with Exotic Wildlife and Molten Fire Spas.", False),
    (planet2_img, (WIDTH // 2, 450), "Luxurious and Futuristic Paradise with hovering gardens and rich foods.", False),
    (planet3_img, (WIDTH - 200, 150), "Adventure meets elegance with anti-grav sled rides, glowing ice cavern tours, and cosmic stargazing lounges.", True),
]

def wrap_text(text, font, max_width):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        test = f"{current_line} {word}".strip()
        if font.size(test)[0] <= max_width:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def draw_planet_screen(surface):
    surface.blit(bg_img, (0, 0))
    for i, (img, (x, y), desc, has_detail) in enumerate(planets_info):
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
        mx, my = pygame.mouse.get_pos()
        if rect.collidepoint(mx, my):
            lines = wrap_text(desc, description_font, 300)
            box = pygame.Rect(x - 150, y + 100, 300, len(lines)*22 + 20)
            pygame.draw.rect(surface, (0,0,0), box.inflate(10,10), border_radius=8)
            pygame.draw.rect(surface, (50,50,120), box, border_radius=8)
            for j, line in enumerate(lines):
                txt = description_font.render(line, True, (255,255,255))
                surface.blit(txt, (box.x+10, box.y+10+j*22))

def draw_menu(surface):
    global logo_y, start_btn_y
    surface.blit(bg_img, (scroll_x, 0))
    surface.blit(bg_img, (scroll_x + bg_width, 0))

    # Animate logo
    if logo_y < logo_target_y:
        logo_y += 4
    else:
        logo_y = logo_target_y
    surface.blit(logo_img, (WIDTH//2 - logo_img.get_width()//2 + 35, logo_y))


    # Animate button
    if start_btn_y > start_btn_target_y:
        start_btn_y -= 4
    else:
        start_btn_y = start_btn_target_y
    img = start_btn_pressed if start_btn_pressed_state else start_btn_idle
    surface.blit(img, (WIDTH//2 - img.get_width()//2, start_btn_y))

# Main loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                mx, my = event.pos
                rect = start_btn_idle.get_rect(topleft=(WIDTH//2 - start_btn_idle.get_width()//2, start_btn_y))
                if rect.collidepoint(mx, my):
                    start_btn_pressed_state = True
        if event.type == pygame.MOUSEBUTTONUP:
            if game_state == "menu" and start_btn_pressed_state:
                start_btn_clicked = True
                start_btn_pressed_state = False
                game_state = "planet_select"

    # Update background scroll
    scroll_x -= scroll_speed
    if scroll_x <= -bg_width:
        scroll_x = 0

    window.fill((0, 0, 0))
    if game_state == "menu":
        draw_menu(window)
    elif game_state == "planet_select":
        draw_planet_screen(window)

    pygame.display.flip()

pygame.quit()
sys.exit()