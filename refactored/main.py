import pygame
from ui_manager import UIManager
from lighting_manager import LightingManager
from object_manager import ObjectManager
from pygame.locals import *

# Constants
PIXEL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
UI_WIDTH = 50

# Initialize Pygame
pygame.init()

win = pygame.display.set_mode((PIXEL_SIZE * GRID_WIDTH + UI_WIDTH, PIXEL_SIZE * GRID_HEIGHT))
pygame.display.set_caption("2D Pixel Path Tracing Engine")

obj_mgr = ObjectManager()
light_mgr = LightingManager(obj_mgr, win, PIXEL_SIZE, UI_WIDTH)
ui_mgr = UIManager(win, PIXEL_SIZE, UI_WIDTH)

# Main Menu Loop
show_menu = True
while show_menu:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if ui_mgr.run_button_rect.collidepoint(mx, my):
                show_menu = False

    win.fill((0, 0, 0))
    ui_mgr.draw_menu()
    pygame.display.flip()

# Main Game Loop
run_game = True
selected_tool = None
active_tool = None
adding_new_objects = False
flashlight_on = False
flashlight_pos = []

while run_game:
    for event in pygame.event.get():
        if event.type == QUIT:
            run_game = False

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            adding_new_objects = False
            active_tool = None
            selected_tool = None

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            ui_mgr.handle_mouse_down(mx, my)

    flashlight_on, flashlight_pos = ui_mgr.get_flashlight_status()
    light_mgr.draw_lighting(flashlight_on, flashlight_pos)
    ui_mgr.draw_ui()
    pygame.display.flip()

pygame.quit()
