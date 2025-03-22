import pygame

WIDTH, HEIGHT = 1000, 800

class Chariot:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.speed = 5
        self.image = pygame.image.load("assets/chariot.png")
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.shield_active = False
        self.shield_timer = 0
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
        for boundary in track_bounds:
            if self.rect.colliderect(boundary):
                self.health -= .5
                print(f"Collision! Health: {self.health}")
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > 6000:
            self.shield_active = False
        
       # if self.rect.colliderect(finish_zone):
        #    self.laps += 1
        #    print(f"Collision! lap: {self.laps}")
      
    #def bounce(self):
    #    self.x -= self.speed * 2
    #    self.y -= self.speed * 2
    #    self.rect.topleft = (self.x, self.y)
  

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))

class ShieldPowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
