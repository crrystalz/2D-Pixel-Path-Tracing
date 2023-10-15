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
    max_dist = int(max(abs(dx), abs(dy)))
    for t in range(1, max_dist):
        x = start[0] + dx * t // max_dist
        y = start[1] + dy * t // max_dist
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

    return shadow_brightness + sun_brightness


def draw_lighting(light_positions, flashlight_pos, sun_pos, solid_positions):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            total_brightness = 0

            # Existing light and sun calculations
            if light_positions or sun_pos:
                total_brightness += calculate_shadow_brightness(x, y, light_positions, solid_positions)

            # Flashlight brightness calculations if flashlight_pos is provided
            if flashlight_pos:
                flashlight_brightness = 0
                distance_to_flashlight = math.sqrt((x - flashlight_pos[0]) ** 2 + (y - flashlight_pos[1]) ** 2)
                flashlight_shadow_factor = 1
                for solid_pos in solid_positions:
                    if is_ray_obstructed([x, y], flashlight_pos, solid_pos):
                        flashlight_shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance_to_flashlight)
                        break
                flashlight_brightness += calculate_brightness(distance_to_flashlight, LIGHT_INTENSITY, flashlight_shadow_factor)
                total_brightness += flashlight_brightness
            
            brightness = min(max(int(total_brightness), 0), 255)

            current_color = win.get_at((x * PIXEL_SIZE + UI_WIDTH, y * PIXEL_SIZE))[:3]
            combined_brightness = [min(a + b, 255) for a, b in zip(current_color, (brightness, brightness, brightness))]

            if [x, y] not in solid_positions:
                pygame.draw.rect(
                    win,
                    combined_brightness,
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
    # Draw Icons
    pygame.draw.rect(win, (255, 255, 0) if selected_tool == 'light' else (255, 255, 255), light_icon_rect)
    pygame.draw.rect(win, (0, 0, 255) if selected_tool == 'solid' else (255, 255, 255), solid_icon_rect)
    pygame.draw.rect(win, (255, 165, 0) if selected_tool == 'flashlight' else (255, 255, 255), flashlight_icon_rect)
    # Add text or icons...
    win.blit(font.render("Light", True, (0, 0, 0)), (5, 20))
    win.blit(font.render("Solid", True, (0, 0, 0)), (5, 80))
    win.blit(font.render("Flashlight", True, (0, 0, 0)), (5, 140))


def main():
    run = True
    clock = pygame.time.Clock()
    selected_tool = 'light'
    flashlight_pos = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = (mouse_x - UI_WIDTH) // PIXEL_SIZE, mouse_y // PIXEL_SIZE
                if 0 <= mouse_x < UI_WIDTH:
                    if light_icon_rect.collidepoint(mouse_x, mouse_y):
                        selected_tool = 'light'
                    elif solid_icon_rect.collidepoint(mouse_x, mouse_y):
                        selected_tool = 'solid'
                    elif flashlight_icon_rect.collidepoint(mouse_x, mouse_y):
                        selected_tool = 'flashlight'
                else:
                    if selected_tool == 'light':
                        light_positions.append([grid_x, grid_y])
                    elif selected_tool == 'solid':
                        solid_positions.append([grid_x, grid_y])
                    elif selected_tool == 'flashlight':
                        flashlight_pos = [grid_x, grid_y]

        # Update flashlight position if the tool is selected
        if selected_tool == 'flashlight':
            flashlight_on = True
            mx, my = pygame.mouse.get_pos()
            flashlight_pos = [(mx - UI_WIDTH) // PIXEL_SIZE, my // PIXEL_SIZE]
        else:
            flashlight_on = False
            flashlight_pos = []

        win.fill((0, 0, 0))

        # Drawing with pre-existing light positions
        draw_lighting(light_positions, None, sun_pos, solid_positions)
        # Overlaying flashlight if enabled
        if flashlight_on:
            draw_lighting([], flashlight_pos, [], solid_positions)
            
        draw_ui(selected_tool)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()