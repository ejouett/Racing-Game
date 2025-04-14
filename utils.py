import pygame
import random
import math

WIDTH, HEIGHT = 1000, 800

SHIELD_IMAGE = pygame.image.load("assets/Updated Shield Transparent Pixelated.png")
SHIELD_IMAGE = pygame.transform.scale(SHIELD_IMAGE, (40, 40))

SPEED_BOOST_IMAGE = pygame.image.load("assets/Speedboost v3 transparent.png")
SPEED_BOOST_IMAGE = pygame.transform.scale(SPEED_BOOST_IMAGE, (40, 40))

# Load AI chariot images
AI_CHARIOT_IMAGES = [
    pygame.transform.scale(pygame.image.load("assets/chariot pixel art.png"), (60, 40)),
    pygame.transform.scale(pygame.image.load("assets/chariot 2 pixel art.png"), (60, 40)),
    pygame.transform.scale(pygame.image.load("assets/chariot 3 pixel art.png"), (60, 40)),
    pygame.transform.scale(pygame.image.load("assets/chariot 3 pixel art.png"), (60, 40))
]

class Chariot:
    def __init__(self, x, y, chariot_type=0):
        self.x, self.y = x, y
        self.speed = 4
        #self.image = pygame.image.load("assets/chariot pixel art.png")
        #self.image = pygame.transform.scale(self.image, (60, 40))
        #self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.shield_active = False
        self.shield_timer = 0
        self.laps = 0
        self.speed_boost_active = False # new
        self.passed_finish = False  # New attribute


        self.chariot_type = chariot_type  # Store selected chariot index

        # Load different chariot images
        self.chariot_images = [
            pygame.image.load("assets/chariot pixel art.png"),
            pygame.image.load("assets/chariot 2 pixel art.png"),
            pygame.image.load("assets/chariot 3 pixel art.png")
        ]
        self.image = pygame.transform.scale(self.chariot_images[self.chariot_type], (60, 40))
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def move(self, keys, track_bounds, finish_zone):
        prev_x, prev_y = self.x, self.y
        
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 60:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 40:
            self.y += self.speed


        self.rect.topleft = (self.x, self.y)  # Update position

    # Check for collisions and revert position if necessary
        if self.check_collision(track_bounds):
            #self.x -= (self.x - prev_x) * 0.5
            #self.y -= (self.y - prev_y) * 0.5
            self.x, self.y = prev_x, prev_y  # Revert to previous position
            self.rect.topleft = (self.x, self.y)  # Update rect position

        
        if self.rect.colliderect(finish_zone):
            if not self.passed_finish:
                self.laps += 1
                self.passed_finish = True  # Prevent counting again until they leave
        else:
            self.passed_finish = False  # Reset flag once they've left the finish line

         # might put back   self.rect.topleft = (self.x, self.y)
        #if self.rect.colliderect(finish_zone):
        
          #  self.laps += 1
         #   print(f"Collision! lap: {self.laps}")
    #def draw(self, screen):
    #    pygame.draw.rect(screen, (0, 0, 255), self.rect)


    def activate_speed_boost(self): # new
        self.speed = 6
        self.speed_boost_active = True
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Reset speed after 5 seconds


    def check_collision(self, track_bounds):
        for boundary in track_bounds:
            if self.rect.colliderect(boundary):
                #self.health -= .5
                if not self.shield_active:
                    self.health -= 0.5  # Reduce health if no shield
                    print(f"Collision! Health: {self.health}")
                   
                return True  # Collision detected
        return False  # No collision
        
        '''
        print(f"Collision! Health: {self.health}")
            
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > 6000:
            self.shield_active = False
        '''
       # if self.rect.colliderect(finish_zone):
        #    self.laps += 1
        #    print(f"Collision! lap: {self.laps}")
      
    #def bounce(self):
    #    self.x -= self.speed * 2
    #    self.y -= self.speed * 2
    #    self.rect.topleft = (self.x, self.y)

    def respawn(self):
        self.x = random.randint(100, 900)
        self.y = random.randint(100, 700)
        self.rect.topleft = (self.x, self.y)

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))


class AIOpponent(Chariot):
    def __init__(self, x, y, ai_path, ai_index):
        super().__init__(x, y)
        self.image = AI_CHARIOT_IMAGES[ai_index]  # Assign AI-specific image
        self.speed = 4 + random.uniform(-0.5, 0.5) # AI speed

        #self.x = x
        #self.y = y
        #self.speed = 4  # AI speed of 4
        #self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.track_path = ai_path  # List of waypoints
        self.target_index = 0  # Start at first waypoint
        self.laps_completed = 0
        self.total_laps = 5  # Same as the player
        self.passed_finish = False  # New attribute
       

        #self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect = self.image.get_rect(topleft=(x, y))

    
    def move(self, track_bounds, finish_zone):
        if self.target_index < len(self.track_path):
            target_x, target_y = self.track_path[self.target_index]
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)

            if distance > 2:  # Move towards the waypoint
                self.x += (dx / distance) * self.speed * 0.8
                self.y += (dy / distance) * self.speed * 0.8
            else:
                self.target_index += 1  # Move to the next waypoint

            if self.target_index >= len(self.track_path):  # Lap completed
                self.target_index = 0
                self.laps_completed += 1

            if self.laps_completed >= self.total_laps:
                print("AI Wins!")
                pygame.quit()
                #sys.exit()


        if self.rect.colliderect(finish_zone):
            if not self.passed_finish:
                self.laps += 1
                print(f"AI Laps: {self.laps}")
                self.passed_finish = True  # Prevent counting again until they leave
        else:
            self.passed_finish = False  # Reset flag once they've left the finish line


        new_rect = self.rect.move(dx, dy)
        for boundary in track_bounds:
            if boundary.colliderect(new_rect):
                return  # AI doesn't move into boundaries

        self.rect.topleft = (self.x, self.y)  # Update AI position
   
class PowerUp:
    def __init__(self, x, y, image):
        self.x, self.y = x, y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, SHIELD_IMAGE)

    def apply_effect(self, chariot):
        chariot.activate_shield()


class SpeedBoost(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, SPEED_BOOST_IMAGE)

    def apply_effect(self, chariot):
        chariot.activate_speed_boost()


'''
class ShieldPowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def apply_effect(self, player): # new
        player.activate_shield()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        


class SpeedBoost:
    def __init__(self, x, y):
        #self.image = pygame.image.load("assets/poweruppixel.png")
        #self.image = pygame.transform.scale(self.image, (40, 40))
        #self.rect = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(x, y, 40, 40)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))

    def apply_effect(self, player):
        player.activate_speed_boost()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        '''