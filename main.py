import pygame
import math
import random

# Constants
PIXEL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
NUM_SAMPLES = 4  # Number of shadow samples per pixel
LIGHT_INTENSITY = 10000
SUN_INTENSITY = 500  # Reduced sun intensity
SHADOW_INTENSITY = 10  # Weakened shadow intensity
SOLID_COLOR = (0, 0, 255)
UI_WIDTH = 50

# Define UI Icon Rectangles
light_icon_rect = pygame.Rect(UI_WIDTH // 4, 20, UI_WIDTH // 2, UI_WIDTH // 2)
solid_icon_rect = pygame.Rect(UI_WIDTH // 4, 80, UI_WIDTH // 2, UI_WIDTH // 2)
flashlight_icon_rect = pygame.Rect(UI_WIDTH // 4, 140, UI_WIDTH // 2, UI_WIDTH // 2)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode(
    (PIXEL_SIZE * GRID_WIDTH + UI_WIDTH, PIXEL_SIZE * GRID_HEIGHT)
)
pygame.display.set_caption("2D Ray Tracing Game")

# Light Source Positions
light_positions = []
sun_pos = [GRID_WIDTH - 1, 0]
solid_positions = []


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
    total_brightness = 0

    for _ in range(NUM_SAMPLES):
        shadow_brightness = 0

        # Perform jittered sampling within the pixel
        sample_x = x + random.uniform(0, 1)
        sample_y = y + random.uniform(0, 1)

        # Calculate shadow from each light source
        for light_pos in light_positions:
            distance = math.sqrt(
                (sample_x - light_pos[0]) ** 2 + (sample_y - light_pos[1]) ** 2
            )
            shadow_factor = 1

            # Check for shadows from solids
            for solid_pos in solid_positions:
                if is_ray_obstructed([sample_x, sample_y], light_pos, solid_pos):
                    shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance)
                    break

            shadow_brightness += calculate_brightness(
                distance, LIGHT_INTENSITY, shadow_factor
            )

        total_brightness += shadow_brightness

    # Average the sampled shadow values
    return total_brightness / NUM_SAMPLES


def draw_lighting(light_positions, flashlight_pos, sun_pos, solid_positions):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # Calculate the average shadow brightness using super-sampling
            shadow_brightness = calculate_shadow_brightness(
                x, y, light_positions, solid_positions
            )

            # Calculate brightness from the sun
            distance_to_sun = math.sqrt((x - sun_pos[0]) ** 2 + (y - sun_pos[1]) ** 2)
            sun_shadow_factor = 1
            for solid_pos in solid_positions:
                if is_ray_obstructed([x, y], sun_pos, solid_pos):
                    sun_shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance_to_sun)
                    break
            sun_brightness = calculate_brightness(
                distance_to_sun, SUN_INTENSITY, sun_shadow_factor
            )

            # Calculate brightness from the flashlight
            flashlight_brightness = 0
            if flashlight_pos:  # Check if flashlight is on
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

            # Combine shadow, sun, and flashlight brightness
            total_brightness = (
                shadow_brightness + sun_brightness + flashlight_brightness
            ) / 3

            # Ensure the brightness is within a valid range [0, 255]
            brightness = min(max(int(total_brightness), 0), 255)

            # Draw pixel
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

# Main Loop
run = True
selected_tool = None
active_tool = None
adding_new_objects = False
flashlight_on = False
flashlight_pos = []  # Initialize flashlight_pos as an empty list
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            adding_new_objects = False
            active_tool = None
            selected_tool = None

        # Mouse button down event handling, modified to check for `adding_new_objects`
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if mx < UI_WIDTH:  # UI clicked
                if light_icon_rect.collidepoint(mx, my):
                    active_tool = "light"
                    selected_tool = (
                        "light" if active_tool != selected_tool else None
                    )  # Toggle selection
                elif solid_icon_rect.collidepoint(mx, my):
                    active_tool = "solid"
                    selected_tool = (
                        "solid" if active_tool != selected_tool else None
                    )  # Toggle selection

                elif flashlight_icon_rect.collidepoint(mx, my):
                    active_tool = "flashlight"
                    selected_tool = (
                        "flashlight" if active_tool != selected_tool else None
                    )  # Toggle selection

                adding_new_objects = (
                    active_tool is not None and active_tool == selected_tool
                )  # Update adding state based on selection

            elif (
                adding_new_objects and active_tool != "flashlight"
            ):  # Grid clicked while adding objects
                grid_x = (mx - UI_WIDTH) // PIXEL_SIZE
                grid_y = my // PIXEL_SIZE
                if (
                    active_tool == "light"
                    and [grid_x, grid_y] not in light_positions
                    and [grid_x, grid_y] not in solid_positions
                ):
                    light_positions.append([grid_x, grid_y])
                elif (
                    active_tool == "solid"
                    and [grid_x, grid_y] not in light_positions
                    and [grid_x, grid_y] not in solid_positions
                ):
                    solid_positions.append([grid_x, grid_y])

    if selected_tool == "flashlight":
        flashlight_on = True
        mx, my = pygame.mouse.get_pos()
        flashlight_pos = [(mx - UI_WIDTH) // PIXEL_SIZE, my // PIXEL_SIZE]
    else:
        flashlight_on = False
        flashlight_pos = []  # Make sure flashlight_pos is always a list

    win.fill((0, 0, 0))
    draw_lighting(light_positions, flashlight_pos, sun_pos, solid_positions)  # Pass light_positions and flashlight_pos
    draw_ui(selected_tool)
    pygame.display.flip()

pygame.quit()