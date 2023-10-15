import math

class Utilities:
    @staticmethod
    def calculate_brightness(distance, max_intensity, shadow_factor=1):
        return (max_intensity * shadow_factor) / (distance**2 + 1)

    @staticmethod
    def is_ray_obstructed(start, end, obstacle):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        for t in range(1, int(max(abs(dx), abs(dy)))):
            x = start[0] + int(dx * t // max(abs(dx), abs(dy)))
            y = start[1] + int(dy * t // max(abs(dy), abs(dx)))
            if [x, y] == obstacle:
                return True
        return False

    @staticmethod
    def calculate_shadow_brightness(x, y, light_positions, solid_positions, light_intensity, shadow_intensity, sun_intensity, sun_pos):
        shadow_brightness = 0
        for light_pos in light_positions:
            distance = math.sqrt((x - light_pos[0]) ** 2 + (y - light_pos[1]) ** 2)
            shadow_factor = 1
            for solid_pos in solid_positions:
                if Utilities.is_ray_obstructed([x, y], light_pos, solid_pos):
                    shadow_factor = max(0, 1 - shadow_intensity / distance)
                    break
            shadow_brightness += Utilities.calculate_brightness(
                distance, light_intensity, shadow_factor
            )

        distance_to_sun = math.sqrt((x - sun_pos[0]) ** 2 + (y - sun_pos[1]) ** 2)
        sun_shadow_factor = 1
        for solid_pos in solid_positions:
            if Utilities.is_ray_obstructed([x, y], sun_pos, solid_pos):
                sun_shadow_factor = max(0, 1 - shadow_intensity / distance_to_sun)
                break
        sun_brightness = Utilities.calculate_brightness(
            distance_to_sun, sun_intensity, sun_shadow_factor
        )

        total_brightness = shadow_brightness + sun_brightness
        return total_brightness
