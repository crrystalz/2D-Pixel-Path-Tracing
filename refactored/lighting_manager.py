import pygame
import math

class LightingManager:
    def __init__(self, window, pixel_size, world):
        self.win = window
        self.pixel_size = pixel_size
        self.world = world
    
    def calculate_lighting(self, x, y, flashlight_on, flashlight_pos):
        # Create a transparent surface to draw the lighting on
        lighting_surface = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)

        # Iterate over all pixels in the window
        for i in range(self.win.get_width()//self.pixel_size):
            for j in range(self.win.get_height()//self.pixel_size):
                
                # Default intensity
                intensity = 0
                
                # If the flashlight is on, calculate intensity based on flashlight position
                if flashlight_on:
                    distance = math.sqrt((x - i)**2 + (y - j)**2)
                    intensity = max(min(255 - distance*20, 255), 0)
                
                # If there is a light source in the world, calculate intensity based on light source position
                for light in self.world.lights:
                    distance = math.sqrt((light[0] - i)**2 + (light[1] - j)**2)
                    intensity = max(intensity, max(min(255 - distance*20, 255), 0))

                # Draw a semi-transparent square of the computed intensity at the pixel position on the lighting surface
                pygame.draw.rect(lighting_surface, (0, 0, 0, 255 - intensity), (i*self.pixel_size, j*self.pixel_size, self.pixel_size, self.pixel_size))
        
        # Apply the lighting surface onto the main window
        self.win.blit(lighting_surface, (0, 0))
