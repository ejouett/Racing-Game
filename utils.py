import pygame
import random
import math

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
        self.speed_boost_active = False # new

    def move(self, keys, track_bounds):
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
            self.x, self.y = prev_x, prev_y  # Revert to previous position
            self.rect.topleft = (self.x, self.y)  # Update rect position

         # might put back   self.rect.topleft = (self.x, self.y)

    #def draw(self, screen):
    #    pygame.draw.rect(screen, (0, 0, 255), self.rect)


    def activate_speed_boost(self): # new
        self.speed = 7
        self.speed_boost_active = True
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # Reset speed after 5 seconds


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
  

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))


class AIOpponent(Chariot):
    def __init__(self, x, y, ai_path):
        super().__init__(x, y)
        #self.path = ai_path
        #self.path = [(500, 680), (700, 500), (900, 300), (700, 150), (500, 100), (300, 150), (100, 300), (300, 500)]
        #self.path = [(100, 200), (300, 250), (500, 300), (700, 350), (900, 400), (1100, 450), (1300, 500), (1500, 550)]
        #self.path_index = 0
        self.speed = 4  # AI speed

        #self.x = x
        #self.y = y
        #self.speed = 4  # AI speed of 4
        #self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.track_path = ai_path  # List of waypoints
        self.target_index = 0  # Start at first waypoint
        self.laps_completed = 0
        self.total_laps = 5  # Same as the player

    
    def move(self, track_bounds):
        if self.target_index < len(self.track_path):
            target_x, target_y = self.track_path[self.target_index]
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)

            if distance > 2:  # Move towards the waypoint
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            else:
                self.target_index += 1  # Move to the next waypoint

            if self.target_index >= len(self.track_path):  # Lap completed
                self.target_index = 0
                self.laps_completed += 1

            if self.laps_completed >= self.total_laps:
                print("AI Wins!")
                pygame.quit()
                #sys.exit()


        new_rect = self.rect.move(dx, dy)
        for boundary in track_bounds:
            if boundary.colliderect(new_rect):
                return  # AI doesn't move into boundaries

        self.rect.topleft = (self.x, self.y)  # Update AI position
    '''
    def move(self, track_bounds):
        if self.path_index >= len(self.path):
            self.path_index = 0  # Loop AI movement

        target_x, target_y = self.path[self.path_index]
        dx = target_x - self.x
        dy = target_y - self.y

        # Normalize movement
        if abs(dx) > abs(dy):
            dx = self.speed if dx > 0 else -self.speed
            dy = 0
        else:
            dy = self.speed if dy > 0 else -self.speed
            dx = 0

        new_rect = self.rect.move(dx, dy)


       # if any(boundary.colliderect(new_rect) for boundary in track_bounds):
       #     self.path_index = (self.path_index + 1) % len(self.path)  # Move to the next waypoint
       #     return
        # Only move if AI doesn't collide with boundaries
        if not any(boundary.colliderect(new_rect) for boundary in track_bounds):
            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x, self.y)
        else:
            #self.path_index += 1  # Try next waypoint
            (self.path_index + 1) % len(self.path)  # Move to the next waypoint
            #return
        '''
    
    ''' 
        dx, dy = random.choice([(5, 0), (-5, 0), (0, 5), (0, -5)])
        new_rect = self.rect.move(dx, dy)

        for boundary in track_bounds:
            if boundary.colliderect(new_rect):
                return  # AI doesn't move into boundaries

        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)  
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
        self.rect = pygame.Rect(x, y, 40, 40)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))

    def apply_effect(self, player):
        player.activate_speed_boost()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)