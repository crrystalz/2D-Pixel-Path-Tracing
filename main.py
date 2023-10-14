import pygame
import math

# Constants
PIXEL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
LIGHT_INTENSITY = 255
SUN_INTENSITY = 30000
SOLID_COLOR = (0, 0, 255)  # Blue solid pixel

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((PIXEL_SIZE * GRID_WIDTH, PIXEL_SIZE * GRID_HEIGHT))
pygame.display.set_caption("2D Ray Tracing with Shadows")

# Light Source Positions
light_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2]
sun_column = GRID_WIDTH - 1

# Solid Pixel Position
solid_pos = [70, 30]

def calculate_brightness(distance, max_intensity, shadow_factor=1):
    return (max_intensity * shadow_factor) / (distance ** 2 + 1)

def is_ray_obstructed(start, end, obstacle):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    for t in range(1, max(abs(dx), abs(dy))):
        x = start[0] + dx * t // max(abs(dx), abs(dy))
        y = start[1] + dy * t // max(abs(dy), abs(dx))
        if [x, y] == obstacle:
            return True
    return False

def draw_lighting(light_pos, solid_pos):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            brightness = 0
            
            # Light from light_pos
            if not is_ray_obstructed(light_pos, [x, y], solid_pos):
                distance_light = math.sqrt((x - light_pos[0]) ** 2 + (y - light_pos[1]) ** 2)
                brightness += calculate_brightness(distance_light, LIGHT_INTENSITY)
            else:
                distance_light = math.sqrt((x - light_pos[0]) ** 2 + (y - light_pos[1]) ** 2)
                shadow_factor = max(1 - 1 / (0.1 * distance_light + 1), 0)
                brightness += calculate_brightness(distance_light, LIGHT_INTENSITY, shadow_factor)
            
            # Light from sun_column
            if not any(is_ray_obstructed([sun_column, sun_y], [x, y], solid_pos) for sun_y in range(GRID_HEIGHT)):
                distances_sun = [math.sqrt((x - sun_column) ** 2 + (y - sun_y) ** 2) for sun_y in range(GRID_HEIGHT)]
                min_distance_sun = min(distances_sun)
                brightness += calculate_brightness(min_distance_sun, SUN_INTENSITY)
            else:
                distances_sun = [math.sqrt((x - sun_column) ** 2 + (y - sun_y) ** 2) for sun_y in range(GRID_HEIGHT)]
                min_distance_sun = min(distances_sun)
                shadow_factor = max(1 - 1 / (0.1 * min_distance_sun + 1), 0)
                brightness += calculate_brightness(min_distance_sun, SUN_INTENSITY, shadow_factor)

            brightness = min(brightness, 255)
            pygame.draw.rect(win, (brightness, brightness, brightness), (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    
    pygame.draw.rect(win, SOLID_COLOR, (solid_pos[0] * PIXEL_SIZE, solid_pos[1] * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

# Main Loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    win.fill((0, 0, 0))
    draw_lighting(light_pos, solid_pos)
    pygame.display.flip()

pygame.quit()
