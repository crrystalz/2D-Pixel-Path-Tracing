import pygame

class UIManager:
    def __init__(self, window, pixel_size, ui_width):
        self.win = window
        self.pixel_size = pixel_size
        self.ui_width = ui_width

        # Create a font for the title and button text
        self.font = pygame.font.Font(None, 36)

        # Define UI Icon Rectangles
        self.light_icon_rect = pygame.Rect(self.ui_width // 4, 20, self.ui_width // 2, self.ui_width // 2)
        self.solid_icon_rect = pygame.Rect(self.ui_width // 4, 80, self.ui_width // 2, self.ui_width // 2)
        self.flashlight_icon_rect = pygame.Rect(self.ui_width // 4, 140, self.ui_width // 2, self.ui_width // 2)

        # Selected tool: None, "light", "solid", or "flashlight"
        self.selected_tool = None

        # Flashlight status
        self.flashlight_on = False
        self.flashlight_pos = []

        # Run button rect will be used in main loop
        self.run_button_rect = pygame.Rect(300, 300, 200, 50)

    def draw_menu(self):
        # Draw title
        title_text = self.font.render("2D Pixel Path Tracing Engine", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.win.get_width() // 2, 100))
        self.win.blit(title_text, title_rect)

        # Draw "Run" button
        self.run_button_rect = pygame.draw.rect(self.win, (0, 255, 0), self.run_button_rect)
        button_text = self.font.render("Run", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=self.run_button_rect.center)
        self.win.blit(button_text, button_rect)

    def draw_ui(self):
        pygame.draw.rect(self.win, (150, 150, 150), (0, 0, self.ui_width, self.pixel_size * 60))
        pygame.draw.circle(self.win, (255, 255, 0), (self.ui_width // 2, 30), 20)
        pygame.draw.rect(self.win, (0, 0, 255), (self.ui_width // 4, 70, self.ui_width // 2, self.ui_width // 2))
        pygame.draw.polygon(self.win, (255, 255, 0), [(self.ui_width // 2, 145), (self.ui_width // 2 - 15, 160), (self.ui_width // 2 + 15, 160)])
        if self.selected_tool == "light":
            pygame.draw.circle(self.win, (255, 0, 0), (self.ui_width // 2, 30), 22, 2)
        elif self.selected_tool == "solid":
            pygame.draw.rect(self.win, (255, 0, 0), (self.ui_width // 4, 70, self.ui_width // 2, self.ui_width // 2), 2)
        elif self.selected_tool == "flashlight":
            pygame.draw.polygon(self.win, (255, 0, 0), [(self.ui_width // 2, 145), (self.ui_width // 2 - 15, 160), (self.ui_width // 2 + 15, 160)], 2)

    def handle_mouse_down(self, mx, my):
        # UI handling logic when mouse is clicked.
        if mx < self.ui_width:
            if self.light_icon_rect.collidepoint(mx, my):
                self.selected_tool = "light" if self.selected_tool != "light" else None
            elif self.solid_icon_rect.collidepoint(mx, my):
                self.selected_tool = "solid" if self.selected_tool != "solid" else None
            elif self.flashlight_icon_rect.collidepoint(mx, my):
                self.selected_tool = "flashlight" if self.selected_tool != "flashlight" else None
        
        # Update flashlight status based on selected tool
        if self.selected_tool == "flashlight":
            self.flashlight_on = True
            self.flashlight_pos = [(mx - self.ui_width) // self.pixel_size, my // self.pixel_size]
        else:
            self.flashlight_on = False
            self.flashlight_pos = []

    def get_flashlight_status(self):
        # Returns the flashlight status (on/off) and position
        return self.flashlight_on, self.flashlight_pos
