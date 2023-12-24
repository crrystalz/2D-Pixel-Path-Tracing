import pygame
import math

# Constants
PIXEL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
LIGHT_INTENSITY = 10000
SUN_INTENSITY = 300000
SHADOW_INTENSITY = 10
SOLID_COLOR = (0, 0, 255)
UI_WIDTH = 0
UI_HIDE_WIDTH = 50
ICON_SIZE = 40
ICON_ENLARGE = 15

class LightSource:
    def __init__(self, position, intensity=LIGHT_INTENSITY):
        self.position = position
        self.intensity = intensity

class SolidObject:
    def __init__(self, position):
        self.position = position

class UIIcon:
    def __init__(self, tool, color, rect):
        self.tool = tool
        self.color = color
        self.rect = rect

class LightTracingEngine:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode(
            (PIXEL_SIZE * GRID_WIDTH + UI_WIDTH, PIXEL_SIZE * GRID_HEIGHT), pygame.SRCALPHA
        )
        pygame.display.set_caption("2D Pixel Path Tracing Engine")

        self.light_sources = [LightSource([GRID_WIDTH - 1, 0], SUN_INTENSITY)]  # Initialize with sun
        self.solid_objects = []
        self.icons = self.create_icons()
        self.selected_tool = 'light'
        self.flashlight_pos = None
        self.show_ui = False

    def create_icons(self):
        vertical_margin = (PIXEL_SIZE * GRID_HEIGHT - 3 * ICON_SIZE) // 4
        return [
            UIIcon("light", (255, 255, 0), pygame.Rect(UI_WIDTH // 4, vertical_margin, ICON_SIZE, ICON_SIZE)),
            UIIcon("solid", (0, 0, 255), pygame.Rect(UI_WIDTH // 4, 2 * vertical_margin + ICON_SIZE, ICON_SIZE, ICON_SIZE)),
            UIIcon("flashlight", (255, 165, 0), pygame.Rect(UI_WIDTH // 4, 3 * vertical_margin + 2 * ICON_SIZE, ICON_SIZE, ICON_SIZE)),
        ]

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)

    def handle_mouse_click(self, event):
        mouse_x, mouse_y = event.pos
        if self.show_ui:
            for icon in self.icons:
                if icon.rect.collidepoint(mouse_x, mouse_y):
                    self.selected_tool = icon.tool
                    if self.selected_tool == "flashlight":
                        # Initialize the flashlight position upon selection
                        self.flashlight_pos = [(mouse_x - UI_WIDTH) // PIXEL_SIZE, mouse_y // PIXEL_SIZE]
        else:
            grid_x, grid_y = (mouse_x - UI_WIDTH) // PIXEL_SIZE, mouse_y // PIXEL_SIZE
            if self.selected_tool == "light":
                self.light_sources.append(LightSource([grid_x, grid_y]))
            elif self.selected_tool == "solid":
                self.solid_objects.append(SolidObject([grid_x, grid_y]))
            elif self.selected_tool == "flashlight":
                self.flashlight_pos = [grid_x, grid_y]

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.show_ui = mouse_pos[0] < UI_HIDE_WIDTH

        if self.selected_tool == "flashlight":
            self.flashlight_pos = [(mouse_pos[0] - UI_WIDTH) // PIXEL_SIZE, mouse_pos[1] // PIXEL_SIZE]

    def render(self):
        self.win.fill((0, 0, 0, 0))  # Ensure transparency
        self.draw_lighting()
        self.draw_ui()
        pygame.display.flip()

    def draw_lighting(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                total_brightness = self.calculate_total_brightness(x, y)
                brightness = min(max(int(total_brightness), 0), 255)

                if [x, y] not in [obj.position for obj in self.solid_objects]:
                    pygame.draw.rect(
                        self.win,
                        (brightness, brightness, brightness),
                        (x * PIXEL_SIZE + UI_WIDTH, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                    )
                else:
                    pygame.draw.rect(
                        self.win,
                        SOLID_COLOR,
                        (x * PIXEL_SIZE + UI_WIDTH, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                    )

    def calculate_total_brightness(self, x, y):
        total_brightness = 0
        for light_source in self.light_sources:
            total_brightness += self.calculate_brightness_from_source(x, y, light_source)

        # Adding flashlight brightness calculation
        if self.selected_tool == "flashlight" and self.flashlight_pos is not None:
            total_brightness += self.calculate_brightness_from_source(x, y, LightSource(self.flashlight_pos))

        return total_brightness

    def calculate_brightness_from_source(self, x, y, light_source):
        distance = math.sqrt((x - light_source.position[0]) ** 2 + (y - light_source.position[1]) ** 2)
        shadow_factor = 1
        for solid in self.solid_objects:
            if self.is_ray_obstructed([x, y], light_source.position, solid.position):
                shadow_factor = max(0, 1 - SHADOW_INTENSITY / distance)
                break
        return (light_source.intensity * shadow_factor) / (distance**2 + 1)

    def is_ray_obstructed(self, start, end, obstacle):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        max_dist = int(max(abs(dx), abs(dy)))
        for t in range(1, max_dist):
            x = start[0] + dx * t // max_dist
            y = start[1] + dy * t // max_dist
            if [x, y] == obstacle:
                return True
        return False

    def draw_ui(self):
        for icon in self.icons:
            rect = icon.rect.inflate(ICON_ENLARGE, ICON_ENLARGE) if self.show_ui and icon.rect.collidepoint(pygame.mouse.get_pos()) else icon.rect
            pygame.draw.rect(
                self.win, icon.color, rect, border_radius=ICON_ENLARGE // 2
            )
            if icon.tool == self.selected_tool and self.show_ui:
                pygame.draw.rect(
                    self.win, (255, 255, 255), rect, 2, border_radius=ICON_SIZE // 2
                )

def main():
    engine = LightTracingEngine()
    engine.run()

if __name__ == "__main__":
    main()
