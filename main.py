import pygame
import sys
import os
from resort_management import load_planets

pygame.init()

# Window setup
WIDTH, HEIGHT = 1018, 573
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Low-G Horizons")
clock = pygame.time.Clock()

# Load images
def load_image(path, size=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        pygame.quit()
        sys.exit()

bg_img = load_image("assets/misc/spacescrolling.jpg")
logo_img = load_image("assets/misc/Low - G Horizon.svg")
start_btn_idle = load_image("assets/misc/start_button.png", (200, 80))
start_btn_pressed = load_image("assets/misc/pushed_start.png", (200, 80))

planet_imgs = [
    load_image("assets/planets/hot-color-planet.png", (180, 180)),
    load_image("assets/planets/new_hot_planets.png", (180, 180)),
    load_image("assets/planets/new_futuristic_planet.png", (180, 180))
]

resort_imgs = [
    load_image("assets/resort_views/futuristic_resort.png"),
    load_image("assets/resort_views/desert-planet.jpg"),
    load_image("assets/resort_views/cold-planet.jpg")
]

back_button = load_image("assets/misc/back_button_bigger.png")
continue_button = load_image("assets/misc/continue_button.png", (80, 80))

# Background scroll setup
bg_width = bg_img.get_width()
scroll_x = 0
scroll_speed = 0.4

# Animation state
logo_y = -logo_img.get_height()
logo_target_y = 100 - 50  # Moved up 50px
start_btn_y = HEIGHT + 80
start_btn_target_y = HEIGHT // 2 + 20  # Moved down 20px
start_btn_visible = True
start_btn_pressed_state = False

# Game state
game_state = "menu"
selected_planet = None

# Planet setup
planets = load_planets()
planet_positions = [(200, 150), (WIDTH // 2, 450), (WIDTH - 200, 150)]
planet_descriptions = [
    "Blazing Exo-Resort of Untamed Luxury with Exotic Wildlife and Molten Fire Spas.",
    "Luxurious and Futuristic Paradise with hovering gardens and rich foods.",
    "Adventure meets elegance with anti-grav sled rides, glowing ice cavern tours, and cosmic stargazing lounges."
]
detail_available = [True, True, True]

# Text utility
def wrap_text(text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test_line = f"{current} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

# Drawing functions
def draw_scrolling_background():
    window.blit(bg_img, (scroll_x, 0))
    window.blit(bg_img, (scroll_x + bg_width, 0))

def draw_menu():
    global logo_y, start_btn_y
    draw_scrolling_background()

    # Animate logo
    if logo_y < logo_target_y:
        logo_y += 5
    logo_x = WIDTH // 2 - logo_img.get_width() // 2 + 35  # Moved right 35px
    window.blit(logo_img, (logo_x, logo_y))

    # Animate button
    if start_btn_y > start_btn_target_y:
        start_btn_y -= 5

    if start_btn_visible:
        btn_img = start_btn_pressed if start_btn_pressed_state else start_btn_idle
        window.blit(btn_img, (WIDTH // 2 - btn_img.get_width() // 2, start_btn_y))

def draw_planet_select():
    draw_scrolling_background()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    font = pygame.font.SysFont("arial", 18)

    for i, (img, pos) in enumerate(zip(planet_imgs, planet_positions)):
        rect = img.get_rect(center=pos)
        window.blit(img, rect)
        if rect.collidepoint(mouse_x, mouse_y):
            lines = wrap_text(planet_descriptions[i], font, 300)
            tooltip_rect = pygame.Rect(pos[0] - 150, pos[1] + 100, 300, len(lines) * 22 + 20)
            pygame.draw.rect(window, (0, 0, 0), tooltip_rect.inflate(10, 10), border_radius=8)
            pygame.draw.rect(window, (50, 50, 120), tooltip_rect, border_radius=8)
            for j, line in enumerate(lines):
                text = font.render(line, True, (255, 255, 255))
                window.blit(text, (tooltip_rect.x + 10, tooltip_rect.y + 10 + j * 22))

def draw_planet_detail(index):
    draw_scrolling_background()
    surf = resort_imgs[index]
    window.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT // 2 - surf.get_height() // 2))

    font = pygame.font.SysFont("arial", 22)
    desc = planet_descriptions[index]
    lines = wrap_text(desc, font, WIDTH - 100)
    box_rect = pygame.Rect(40, HEIGHT - 200, WIDTH - 80, 160)
    pygame.draw.rect(window, (0, 0, 0), box_rect.inflate(8, 8), border_radius=10)
    pygame.draw.rect(window, (30, 30, 60), box_rect, border_radius=10)
    pygame.draw.rect(window, (255, 255, 255), box_rect, width=2, border_radius=10)

    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        window.blit(text, (box_rect.x + 15, box_rect.y + 15 + i * font.get_height()))

    # Back: moved up and to the right
    back_x = WIDTH - back_button.get_width() - 40
    back_y = HEIGHT - 110
    window.blit(back_button, (back_x, back_y))

    # Continue: moved up and to the left
    continue_x = 900
    continue_y = 480
    window.blit(continue_button, (continue_x, continue_y))

# Main loop
running = True
while running:
    clock.tick(60)
    window.fill((0, 0, 0))

    scroll_x -= scroll_speed
    if scroll_x <= -bg_width:
        scroll_x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if game_state == "menu":
                btn_rect = start_btn_idle.get_rect(topleft=(WIDTH // 2 - 100, start_btn_y))
                if btn_rect.collidepoint(mx, my):
                    start_btn_pressed_state = True

            elif game_state == "planet_select":
                for i, (img, pos) in enumerate(zip(planet_imgs, planet_positions)):
                    if detail_available[i]:
                        rect = img.get_rect(center=pos)
                        if rect.collidepoint(mx, my):
                            selected_planet = i
                            game_state = "planet_detail"

            elif game_state == "planet_detail":
                back_x = WIDTH - back_button.get_width() - 40
                back_y = 480
                continue_x = 40
                continue_y = HEIGHT - 110

                if pygame.Rect(back_x, back_y, back_button.get_width(), back_button.get_height()).collidepoint(mx, my):
                    game_state = "planet_select"
                elif pygame.Rect(continue_x, continue_y, continue_button.get_width(), continue_button.get_height()).collidepoint(mx, my):
                    print(f"Continue from Planet {selected_planet + 1}")
                    game_state = "next_screen"

        elif event.type == pygame.MOUSEBUTTONUP:
            if start_btn_pressed_state and game_state == "menu":
                game_state = "planet_select"
                start_btn_pressed_state = False

    # Render current state
    if game_state == "menu":
        draw_menu()
    elif game_state == "planet_select":
        draw_planet_select()
    elif game_state == "planet_detail":
        draw_planet_detail(selected_planet)

    pygame.display.flip()

pygame.quit()
sys.exit()
 