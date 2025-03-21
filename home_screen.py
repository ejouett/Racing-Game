import pygame

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 100
WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255)

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        
        # Define buttons for map selection
        self.colosseum_button = pygame.Rect(350, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.other_map_button = pygame.Rect(350, 450, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.ancientGreece_button = pygame.Rect(350, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
        
    def draw_text(self, text, position):
        rendered_text = self.font.render(text, True, BLACK)
        self.screen.blit(rendered_text, position)

    def run(self):
        while True:
            self.screen.fill(WHITE)

            # Draw UI
            self.draw_text("Select a Race Track", (350, 200))
            pygame.draw.rect(self.screen, BLUE, self.colosseum_button)
            self.draw_text("Colosseum Map", (380, 330))
            pygame.draw.rect(self.screen, BLUE, self.other_map_button)
            self.draw_text("greek colosseum", (360, 480))
            pygame.draw.rect(self.screen, BLUE, self.ancientGreece_button)
            self.draw_text("greektrack", (360, 630))
            

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.colosseum_button.collidepoint(event.pos):
                        return "assets/colosseum_track.png"
                    if self.other_map_button.collidepoint(event.pos):
                        return "assets/greektracks.png"  # Update with other maps
                    if self.ancientGreece_button.collidepoint(event.pos):
                        return "assets/ancient_greece.png" 

            pygame.display.update()
