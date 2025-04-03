import pygame

BUTTON_WIDTH, BUTTON_HEIGHT = 300, 100
WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255)
RED, GREEN = (200, 0, 0), (0, 200, 0)
BUTTON_RADIUS = 15  # Size of chariot selection buttons


class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        
        # Load background image
        self.background = pygame.image.load("assets/homescreen_Backround.png")
        self.background = pygame.transform.scale(self.background, (1000, 800))


        #NEWWWWW
        # Load chariot images
        self.chariot_images = [
            pygame.image.load("assets/chariot pixel art.png"),
            pygame.image.load("assets/chariot 2 pixel art.png"),
            pygame.image.load("assets/chariot 3 pixel art.png")
        ]
        self.chariot_images = [pygame.transform.scale(img, (100, 100)) for img in self.chariot_images]

        # Chariot selection variables
        self.chariot_positions = [(150, 50), (400, 50), (650, 50)]
        self.button_positions = [(200, 160), (450, 160), (700, 160)]
        self.selected_chariot = None



        # Buttons for track selection
        self.buttons = {
            "Colosseum Map 1": pygame.Rect(350, 250, BUTTON_WIDTH, BUTTON_HEIGHT),
            "Colosseum Map 2": pygame.Rect(350, 400, BUTTON_WIDTH, BUTTON_HEIGHT),
            "Greek Track": pygame.Rect(350, 550, BUTTON_WIDTH, BUTTON_HEIGHT),
            "Modern track": pygame.Rect(350, 690, BUTTON_WIDTH, BUTTON_HEIGHT)
        }
        self.track_paths = {
            "Colosseum Map 1": "assets/colosseum_track.png",
            "Colosseum Map 2": "assets/greektracks.png",
            "Greek Track": "assets/ancient_greece.png",
            "Modern track": "assets/modern_track.png"
        }

        # Load and scale track images
        self.track_images = {
            name: pygame.transform.scale(pygame.image.load(path), (BUTTON_WIDTH, BUTTON_HEIGHT))
            for name, path in self.track_paths.items()
        }

        #self.help_button = pygame.Rect(850, 30, 120, 50)
        # Load help button image newwww
        self.help_button_img = pygame.image.load("assets/pixelated tutorial button.png")
        self.help_button_img = pygame.transform.scale(self.help_button_img, (100, 50))
        self.help_button_rect = self.help_button_img.get_rect(topleft=(850, 30))


        # Survival Mode buttons NEW
        self.mode_buttons = {
            name: (button.x + BUTTON_WIDTH + 40, button.y + BUTTON_HEIGHT // 2)
            for name, button in self.buttons.items()
        }
        self.selected_modes = {name: "race" for name in self.buttons}  # Default to race mode



    def draw_text(self, text, position):
        rendered_text = self.font.render(text, True, BLACK)
        self.screen.blit(rendered_text, position)

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))  # Draw background
            #NEWWWW
            self.draw_text("Select a Chariot", (370, 10))

            # Draw chariots and selection buttons
            for i, pos in enumerate(self.chariot_positions):
                self.screen.blit(self.chariot_images[i], pos)
                
                # Draw selection button
                button_color = GREEN if self.selected_chariot == i else RED
                pygame.draw.circle(self.screen, button_color, self.button_positions[i], BUTTON_RADIUS)




            self.draw_text("Select a Race Track", (350, 200))
            # Draw track selection buttons
            for name, button in self.buttons.items():
                #pygame.draw.rect(self.screen, BLUE, button)
                self.draw_text(name, (button.x - 300, button.y + 30))
                self.screen.blit(self.track_images[name], (button.x, button.y))  # Draw track image
                pygame.draw.rect(self.screen, BLACK, button, 3)  # Optional: Outline for visibility

                # Draw Survival Mode toggle  NEW
                mode_x, mode_y = self.mode_buttons[name]
                mode_color = GREEN if self.selected_modes[name] == "survival" else RED
                pygame.draw.circle(self.screen, mode_color, (mode_x, mode_y), BUTTON_RADIUS)


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
                    x, y = event.pos

                    # Check chariot selection
                    for i, (bx, by) in enumerate(self.button_positions):
                        if (x - bx) ** 2 + (y - by) ** 2 <= BUTTON_RADIUS ** 2:
                            self.selected_chariot = i  # Select chariot
                            print("chariot selected:", self.selected_chariot)



                    # Toggle survival mode NEW
                    for name, (mode_x, mode_y) in self.mode_buttons.items():
                        if (x - mode_x) ** 2 + (y - mode_y) ** 2 <= BUTTON_RADIUS ** 2:
                            self.selected_modes[name] = "survival" if self.selected_modes[name] == "race" else "race"
                            print(f"{name}: Mode set to {self.selected_modes[name]}")


                    # Open help screen
                    if self.help_button_rect.collidepoint(event.pos):
                        self.show_help_screen()

                    # NEWWWW select track
                    #if self.selected_chariot in [0, 1, 2]:
                    if self.selected_chariot is not None:
                        print(f"Chariot selected: {self.selected_chariot}")
                        for name, button in self.buttons.items():
                            if button.collidepoint(event.pos):
                                game_mode = self.selected_modes[name] #NEWWWWW
                                print(f"Track selected: {name}")
                                return (self.track_paths[name], self.selected_chariot, game_mode)  # Always return tuple

                    
                      
                    #for name, button in self.buttons.items():
                    #    if button.collidepoint(event.pos):
                    #        return self.track_paths[name]
                        

            pygame.display.update()

    def show_help_screen(self):
        help_running = True
        while help_running:
            self.screen.fill(WHITE)
            self.draw_text("How to Play:", (350, 100))

            instructions = [
                "1. Choose your chariot. Click Red button to make Green.",
                "2. Choose Game mode, survival or race. Red is Race",
                "3. If you click button to green it will be survival.",
                "4. Surival is race with added objects you must dodge",
                "5. Use arrow keys to move your chariot.",
                "6. Avoid crashing into the track boundaries and AI.",
                "7. Reach 5 laps before running out of health or losing.",
                "8. Collect power-ups to boost your abilities.",
                "9. Click 'Exit' to return to the home screen."
            ]

            y_position = 200
            for instruction in instructions:
                self.draw_text(instruction, (50, y_position))
                y_position += 50

            # Back button
            back_button = pygame.Rect(400, 670, 200, 50)
            pygame.draw.rect(self.screen, BLUE, back_button)
            self.draw_text("Back", (450, 680))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        help_running = False  # Return to the home screen

            pygame.display.update()
