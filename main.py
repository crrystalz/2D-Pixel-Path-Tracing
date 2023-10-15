import pygame
import math

# Constants
PIXEL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
LIGHT_INTENSITY = 10000
SUN_INTENSITY = 300000
SHADOW_INTENSITY = 10
SOLID_COLOR = (0, 0, 255)
UI_WIDTH = 50

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode(
    (PIXEL_SIZE * GRID_WIDTH + UI_WIDTH, PIXEL_SIZE * GRID_HEIGHT)
)
pygame.display.set_caption("2D Pixel Path Tracing Engine")

# Create a font for the title and button text
font = pygame.font.Font(None, 36)

# Light Source Positions
light_positions = []
sun_pos = [GRID_WIDTH - 1, 0]
solid_positions = []

# Define UI Icon Rectangles
light_icon_rect = pygame.Rect(UI_WIDTH // 4, 20, UI_WIDTH // 2, UI_WIDTH // 2)
solid_icon_rect = pygame.Rect(UI_WIDTH // 4, 80, UI_WIDTH // 2, UI_WIDTH // 2)
flashlight_icon_rect = pygame.Rect(UI_WIDTH // 4, 140, UI_WIDTH // 2, UI_WIDTH // 2)

# Functions
def calculate_brightness(distance, max_intensity, shadow_factor=1):
    return (max_intensity * shadow_factor) / (distance**2 + 1)

def is_ray_obstructed(start, end, obstacle):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    for t in range(1, int(max(abs(dx), abs(dy)))):
        x = start[0] + int(dx * t // max(abs(dx), abs(dy)))
        y = start[1] + int(dy * t // max(abs(dy), abs(dx)))
        if [x, y] == obstacle:
            return True
    return False

def calculate_shadow_brightness(x, y, light_positions, solid_positions):
    shadow_brightness = 0
    for light_pos in light_positions:
        distance = math.sqrt((x - light_pos[0]) ** 2 + (y - light_pos[1]) ** 2)
        shadow_factor = 1
        for solid_pos in solid_positions:
            if is_ray_obstructed([x, y], light_pos, solid_pos):
                shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance)
                break
        shadow_brightness += calculate_brightness(
            distance, LIGHT_INTENSITY, shadow_factor
        )

    distance_to_sun = math.sqrt((x - sun_pos[0]) ** 2 + (y - sun_pos[1]) ** 2)
    sun_shadow_factor = 1
    for solid_pos in solid_positions:
        if is_ray_obstructed([x, y], sun_pos, solid_pos):
            sun_shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance_to_sun)
            break
    sun_brightness = calculate_brightness(
        distance_to_sun, SUN_INTENSITY, sun_shadow_factor
    )

    total_brightness = shadow_brightness + sun_brightness
    return total_brightness

def draw_lighting(light_positions, flashlight_pos, sun_pos, solid_positions):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            shadow_brightness = calculate_shadow_brightness(
                x, y, light_positions, solid_positions
            )

            distance_to_sun = math.sqrt((x - sun_pos[0]) ** 2 + (y - sun_pos[1]) ** 2)
            sun_shadow_factor = 1
            for solid_pos in solid_positions:
                if is_ray_obstructed([x, y], sun_pos, solid_pos):
                    sun_shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance_to_sun)
                    break
            sun_brightness = calculate_brightness(
                distance_to_sun, SUN_INTENSITY, sun_shadow_factor
            )

            flashlight_brightness = 0
            if flashlight_pos:
                distance_to_flashlight = math.sqrt(
                    (x - flashlight_pos[0]) ** 2 + (y - flashlight_pos[1]) ** 2
                )
                flashlight_shadow_factor = 1
                for solid_pos in solid_positions:
                    if is_ray_obstructed([x, y], flashlight_pos, solid_pos):
                        flashlight_shadow_factor = max(
                            0, 1 - SHADOW_INTENSITY / distance_to_flashlight
                        )
                        break
                flashlight_brightness = calculate_brightness(
                    distance_to_flashlight, LIGHT_INTENSITY, flashlight_shadow_factor
                )

            total_brightness = (
                shadow_brightness + sun_brightness + flashlight_brightness
            ) / 3

            brightness = min(max(int(total_brightness), 0), 255)

            if [x, y] not in solid_positions:
                pygame.draw.rect(
                    win,
                    (brightness, brightness, brightness),
                    (x * PIXEL_SIZE + UI_WIDTH, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                )
            else:
                pygame.draw.rect(
                    win,
                    SOLID_COLOR,
                    (x * PIXEL_SIZE + UI_WIDTH, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                )

def draw_ui(selected_tool):
    pygame.draw.rect(win, (150, 150, 150), (0, 0, UI_WIDTH, PIXEL_SIZE * GRID_HEIGHT))
    pygame.draw.circle(win, (255, 255, 0), (UI_WIDTH // 2, 30), 20)
    pygame.draw.rect(
        win, SOLID_COLOR, (UI_WIDTH // 4, 70, UI_WIDTH // 2, UI_WIDTH // 2)
    )
    pygame.draw.polygon(
        win,
        (255, 255, 0),
        [(UI_WIDTH // 2, 145), (UI_WIDTH // 2 - 15, 160), (UI_WIDTH // 2 + 15, 160)],
    )
    if selected_tool == "light":
        pygame.draw.circle(win, (255, 0, 0), (UI_WIDTH // 2, 30), 22, 2)
    elif selected_tool == "solid":
        pygame.draw.rect(
            win, (255, 0, 0), (UI_WIDTH // 4, 70, UI_WIDTH // 2, UI_WIDTH // 2), 2
        )
    elif selected_tool == "flashlight":
        pygame.draw.polygon(
            win,
            (255, 0, 0),
            [
                (UI_WIDTH // 2, 145),
                (UI_WIDTH // 2 - 15, 160),
                (UI_WIDTH // 2 + 15, 160),
            ],
            2,
        )

# Main Menu Loop
show_menu = True
while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if run_button_rect.collidepoint(mx, my):
                show_menu = False

    # Clear the screen
    win.fill((0, 0, 0))

    # Draw title
    title_text = font.render("2D Pixel Path Tracing Engine", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(win.get_width() // 2, 100))
    win.blit(title_text, title_rect)

    # Draw "Run" button
    run_button = pygame.Rect(300, 300, 200, 50)
    run_button_rect = pygame.draw.rect(win, (0, 255, 0), run_button)
    button_text = font.render("Run", True, (0, 0, 0))
    button_rect = button_text.get_rect(center=run_button_rect.center)
    win.blit(button_text, button_rect)

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
        if event.type == pygame.QUIT:
            run_game = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            adding_new_objects = False
            active_tool = None
            selected_tool = None

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if mx < UI_WIDTH:
                if light_icon_rect.collidepoint(mx, my):
                    active_tool = "light"
                    selected_tool = (
                        "light" if active_tool != selected_tool else None
                    )
                elif solid_icon_rect.collidepoint(mx, my):
                    active_tool = "solid"
                    selected_tool = (
                        "solid" if active_tool != selected_tool else None
                    )
                elif flashlight_icon_rect.collidepoint(mx, my):
                    active_tool = "flashlight"
                    selected_tool = (
                        "flashlight" if active_tool != selected_tool else None
                    )
                adding_new_objects = (
                    active_tool is not None and active_tool == selected_tool
                )

            elif adding_new_objects and active_tool == "light":
                grid_x = (mx - UI_WIDTH) // PIXEL_SIZE
                grid_y = my // PIXEL_SIZE
                if (
                    [grid_x, grid_y] not in light_positions
                    and [grid_x, grid_y] not in solid_positions
                ):
                    light_positions.append([grid_x, grid_y])

            elif adding_new_objects and active_tool == "solid":
                grid_x = (mx - UI_WIDTH) // PIXEL_SIZE
                grid_y = my // PIXEL_SIZE
                if (
                    [grid_x, grid_y] not in light_positions
                    and [grid_x, grid_y] not in solid_positions
                ):
                    solid_positions.append([grid_x, grid_y])

    if selected_tool == "flashlight":
        flashlight_on = True
        mx, my = pygame.mouse.get_pos()
        flashlight_pos = [(mx - UI_WIDTH) // PIXEL_SIZE, my // PIXEL_SIZE]
    else:
        flashlight_on = False
        flashlight_pos = []

    win.fill((0, 0, 0))
    draw_lighting(
        light_positions, flashlight_pos, sun_pos, solid_positions
    )
    draw_ui(selected_tool)
    pygame.display.flip()

pygame.quit()