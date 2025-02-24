import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ancient Greek Chariot Racing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Load assets
chariot_img = pygame.image.load("assets/chariot.png")
chariot_img = pygame.transform.scale(chariot_img, (80, 50))

# Player class
class Chariot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = chariot_img
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 80:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 50:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Obstacle class
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((50, 50))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def move(self):
        self.y += 5
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Main function
def main():
    clock = pygame.time.Clock()
    run = True
    
    player = Chariot(WIDTH // 2, HEIGHT - 100)
    obstacles = []
    
    while run:
        clock.tick(30)
        SCREEN.fill(WHITE)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Move player
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Spawn obstacles
        if random.randint(1, 30) == 1:
            obstacles.append(Obstacle(random.randint(0, WIDTH - 50), -50))
        
        # Move obstacles
        for obstacle in obstacles[:]:
            obstacle.move()
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
            if player.rect.colliderect(obstacle.rect):
                print("Game Over!")
                run = False
            
        # Draw everything
        player.draw(SCREEN)
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
