import pygame
import os
import sys


# load images code 
try:
    bg_img = pygame.image.load(os.path.join("assets", "spacescrolling.jpg")).convert()
    logo_img = pygame.image.load(os.path.join("assets", "Low - G Horizon.svg")).convert_alpha()
    start_btn_idle = pygame.image.load(os.path.join("assets", "start_button.png")).convert_alpha()
    start_btn_pressed = pygame.image.load(os.path.join("assets", "pushed_start.png")).convert_alpha()
except:
    print("Could not load an image. Check the file path!")
    pygame.quit()
    sys.exit()