import pygame
import random
from utils import Chariot, ShieldPowerUp

WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)

class RaceScreen:
    def __init__(self, screen, track_image_path):
        self.screen = screen
        self.track_img = pygame.image.load(track_image_path)
        self.track_img = pygame.transform.scale(self.track_img, (1000, 800))

        self.player = Chariot(500, 700)
        self.powerups = [ShieldPowerUp(random.randint(100, 900), random.randint(100, 700)) for _ in range(3)]
        self.track_bounds = [pygame.Rect(80, 80, 840, 701)]  # Adjust for track
        
        
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(30)
            self.screen.fill(WHITE)
            self.screen.blit(self.track_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"

            keys = pygame.key.get_pressed()
            self.player.move(keys)
            #self.player.check_collision(self.track_bounds)

            # Power-ups
            for powerup in self.powerups[:]:
                if self.player.rect.colliderect(powerup.rect):
                    self.player.activate_shield()
                    self.powerups.remove(powerup)

            # Draw elements
            self.player.draw(self.screen)
            for powerup in self.powerups:
                powerup.draw(self.screen)

            # Check game over conditions
            if self.player.health <= 0:
                print("Game Over! You lost!")
                return "lose"

            if self.player.laps >= 5:
                print("Congratulations! You won!")
                return "win"

            pygame.display.update()
