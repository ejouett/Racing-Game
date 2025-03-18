import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ancient Greek Chariot Racing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Load assets
chariot_img = pygame.image.load("assets/chariot.png")
chariot_img = pygame.transform.scale(chariot_img, (60, 40))
track_img = pygame.image.load("assets/colosseum_track.png")  # Ensure this is an open track image
track_img = pygame.transform.scale(track_img, (WIDTH, HEIGHT))

# Player class
class Chariot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = chariot_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.laps = 0
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 60:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 40:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def check_collision(self, track_bounds):
        #if not self.shield_active:
        for boundary in track_bounds:
            if self.rect.colliderect(boundary):
                self.health -= 2
                self.bounce()

    
    def bounce(self):
        self.x -= self.speed * 2
        self.y -= self.speed * 2
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, RED, (10, 10, self.health * 2, 20))  # Health bar

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
        #self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Main function
def main():
    clock = pygame.time.Clock()
    run = True
    
    player = Chariot(WIDTH // 2, HEIGHT - 120)
    obstacles = []
    
    #track_bounds = [pygame.Rect(80, 80, WIDTH - 160, HEIGHT - 160)] 

    while run:
        clock.tick(30)
        SCREEN.fill(WHITE)
        SCREEN.blit(track_img, (0, 0))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Move player
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.check_collision(obstacles)
        
        # Spawn obstacles
        if random.randint(1, 30) == 1:
            obstacles.append(Obstacle(random.randint(0, WIDTH - 40), -40))
        
        # Move obstacles
        for obstacle in obstacles[:]:
            obstacle.move()
            if obstacle.y > HEIGHT:
                player.health -= 3
                obstacles.remove(obstacle)
            #if player.rect.colliderect(obstacle.rect):
                #player.health -= 3
                #print("Game Over!")
                #run = False
            
        # Draw everything
        player.draw(SCREEN)
        for obstacle in obstacles:
            obstacle.draw(SCREEN)

        if player.health <= 0:
            print("Game Over! You lost!")
            run = False

         # Lap tracking (simplified)
       # if player.y < 40:
       #     player.laps += 1
       #     player.y = HEIGHT - 120
        
       # if player.laps >= 5:
       #     print("Congratulations! You won the race!")
            #run = False
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
