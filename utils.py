import pygame
Width, height = 1000, 800
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
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < Width - 60:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < height - 40:
            self.y += self.speed
        if dx or dy:
            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x, self.y)

    def check_collision(self, track_bounds):
        if not self.shield_active:
            for boundary in track_bounds:
                if self.rect.colliderect(boundary):
                    self.health -= 10
                    #self.bounce()
                    #self.shield_active
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > 6000:
            self.shield_active = False

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
