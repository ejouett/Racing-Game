import pygame

BUTTON_WIDTH, BUTTON_HEIGHT = 300, 100
WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255)

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        
        # Load background image
        self.background = pygame.image.load("assets/homescreen_Backround.png")
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Buttons for track selection
        self.buttons = {
            "Colosseum Map": pygame.Rect(350, 250, BUTTON_WIDTH, BUTTON_HEIGHT),
            "Greek Track": pygame.Rect(350, 400, BUTTON_WIDTH, BUTTON_HEIGHT),
            "New Track": pygame.Rect(350, 550, BUTTON_WIDTH, BUTTON_HEIGHT),
            "New modern track": pygame.Rect(350, 700, BUTTON_WIDTH, BUTTON_HEIGHT)
        }
        self.track_paths = {
            "Colosseum Map": "assets/colosseum_track.png",
            "Greek Track": "assets/greektracks.png",
            "New Track": "assets/ancient_greece.png",
            "New modern track": "assets/modern_track.png"
        }

        # Help button (Top right)
        #self.help_button = pygame.Rect(850, 30, 120, 50)
        # Load help button image newwww
        self.help_button_img = pygame.image.load("assets/pixelated tutorial button.png")
        self.help_button_img = pygame.transform.scale(self.help_button_img, (100, 50))
        self.help_button_rect = self.help_button_img.get_rect(topleft=(850, 30))

    def draw_text(self, text, position):
        rendered_text = self.font.render(text, True, BLACK)
        self.screen.blit(rendered_text, position)

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))  # Draw background
            self.draw_text("Select a Race Track", (350, 150))
            # Draw track selection buttons
            for name, button in self.buttons.items():
                pygame.draw.rect(self.screen, BLUE, button)
                self.draw_text(name, (button.x + 20, button.y + 30))

            # Draw Help button
            #pygame.draw.rect(self.screen, (150, 0, 0), self.help_button)
            #self.draw_text("Help", (self.help_button.x + 30, self.help_button.y + 10))
            # Draw Help button image newwwww
            self.screen.blit(self.help_button_img, self.help_button_rect)
            self.draw_text("How to Play", (800, 85))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.help_button_rect.collidepoint(event.pos):
                        self.show_help_screen()
                    for name, button in self.buttons.items():
                        if button.collidepoint(event.pos):
                            return self.track_paths[name]

            pygame.display.update()

    def show_help_screen(self):
        help_running = True
        while help_running:
            self.screen.fill(WHITE)
            self.draw_text("How to Play:", (350, 100))

            instructions = [
                "1. Use arrow keys to move your chariot.",
                "2. Avoid crashing into the track boundaries.",
                "3. Reach the finish line before running out of health.",
                "4. Collect power-ups to boost your abilities.",
                "5. Click 'Exit' to return to the home screen."
            ]

            y_position = 200
            for instruction in instructions:
                self.draw_text(instruction, (200, y_position))
                y_position += 50

            # Back button
            back_button = pygame.Rect(400, 600, 200, 50)
            pygame.draw.rect(self.screen, BLUE, back_button)
            self.draw_text("Back", (450, 610))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        help_running = False  # Return to the home screen

            pygame.display.update()
