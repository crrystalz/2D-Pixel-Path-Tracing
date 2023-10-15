import pygame

class ObjectManager:
    def __init__(self, window, pixel_size, grid_width, grid_height):
        self.win = window
        self.pixel_size = pixel_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.lights = []
        self.solids = []
    
    def draw_objects(self):
        for light in self.lights:
            pygame.draw.rect(
                self.win,
                (255, 255, 0),
                (
                    light[0] * self.pixel_size,
                    light[1] * self.pixel_size,
                    self.pixel_size,
                    self.pixel_size,
                ),
            )
        for solid in self.solids:
            pygame.draw.rect(
                self.win,
                (0, 0, 255),
                (
                    solid[0] * self.pixel_size,
                    solid[1] * self.pixel_size,
                    self.pixel_size,
                    self.pixel_size,
                ),
            )
            
    def add_light(self, x, y):
        if [x, y] not in self.lights and [x, y] not in self.solids:
            self.lights.append([x, y])
            
    def add_solid(self, x, y):
        if [x, y] not in self.lights and [x, y] not in self.solids:
            self.solids.append([x, y])
