# intro_screen.py
import pygame

#save_player_name(typed_name)

WHITE, BLACK = (255, 255, 255), (0, 0, 0)

class IntroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.name_input = ""
        self.active = True


         # Load background image
        self.background = pygame.image.load("assets/standingperson.png")
        self.background = pygame.transform.scale(self.background, (1000, 800))

    def draw_text(self, text, pos, size=50):
        font = pygame.font.Font(None, size)
        rendered = font.render(text, True, BLACK)
        self.screen.blit(rendered, pos)

    def run(self):
        clock = pygame.time.Clock()
        input_box = pygame.Rect(425, 500, 350, 55)
        self.screen.fill(WHITE)
        self.screen.blit(self.background, (0, 0))  # Draw background
        

        while True:
            #self.screen.fill(WHITE)
            self.draw_text("⚔️ WELCOME TO THE GREAT RACES ⚔️", (180, 100), 60)
            self.draw_text("You will race against Zeus, Hades, and Poseidon...", (100, 200))
            self.draw_text("Only the best survive. Choose your name, warrior:", (100, 300))
            self.draw_text("Enter Your Name:", (100, 510))
            pygame.draw.rect(self.screen, (200, 200, 200), input_box)

        #NEWWWW BLOCKed
            #name_surface = self.font.render(self.name_input, True, BLACK)
            #self.screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

            user_input =self.font.render(self.name_input, True, BLACK)
            self.screen.blit(user_input, (input_box.x + 10, input_box.y + 10))
            #save_player_name(user_input)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.name_input.strip() != "":
                        return self.name_input.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif len(self.name_input) < 15:
                        self.name_input += event.unicode

            #save_player_name(user_input)

            pygame.display.update()
            clock.tick(30)
