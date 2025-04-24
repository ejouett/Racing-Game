import pygame

WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255)

class PlayerProfileScreen:
    def __init__(self, screen, player_name, wins, losses):
        self.screen = screen
        self.player_name = player_name
        self.wins = wins
        self.losses = losses
        #self.points = points
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)

        # Load chariot images and info
        self.chariot_info = [
            {
                "image": pygame.transform.flip(pygame.transform.scale(
                    pygame.image.load("assets/chariot pixel art.png"), (100, 100)), True, False),
                #"image": pygame.transform.scale(pygame.image.load("assets/chariot pixel art.png"), (100, 100)),
                "name": "Chariot of Hermes",
                "ability": "Speed Boost on straights"
            },
            {
                "image": pygame.transform.scale(pygame.image.load("assets/chariot 2 pixel art.png"), (100, 100)),
                "name": "Ares’ War Cart",
                "ability": "Increased damage resistance"
            },
            {
                "image": pygame.transform.scale(pygame.image.load("assets/chariot 3 pixel art.png"), (100, 100)),
                "name": "Athena’s Strategem",
                "ability": "Better control and maneuvering"
            }
        ]

    def draw_text(self, text, position, font=None):
        font = font or self.font
        rendered = font.render(text, True, BLACK)
        self.screen.blit(rendered, position)

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            self.draw_text("Player Profile", (400, 30), self.big_font)

            # Stats
            self.draw_text(f"Name: {self.player_name}", (100, 100))
            self.draw_text(f"Wins: {self.wins}", (100, 140))
            self.draw_text(f"Losses: {self.losses}", (100, 180))
            #self.draw_text(f"Points: {self.points}", (100, 220))
            #level = self.points // 50
            level = self.wins // 50
            self.draw_text(f"Level: {level}", (100, 220))
            self.draw_text("Leveling Up: win 5 matched to level up!", (100, 300))

            # Chariots
            self.draw_text("Chariots & Abilities:", (100, 360), self.big_font)
            for i, info in enumerate(self.chariot_info):
                y_offset = 400 + i * 120
                self.screen.blit(info["image"], (100, y_offset))
                self.draw_text(info["name"], (220, y_offset))
                self.draw_text(f"Ability: {info['ability']}", (220, y_offset + 40))

            # Back button
            back_button = pygame.Rect(400, 720, 200, 50)
            pygame.draw.rect(self.screen, BLUE, back_button)
            self.draw_text("Back", (470, 730))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        running = False

            pygame.display.update()
