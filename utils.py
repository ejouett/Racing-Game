import pygame
import random
import math

WIDTH, HEIGHT = 1000, 800

SHIELD_IMAGE = pygame.image.load("assets/Updated Shield Transparent Pixelated.png")
SHIELD_IMAGE = pygame.transform.scale(SHIELD_IMAGE, (40, 40))

SPEED_BOOST_IMAGE = pygame.image.load("assets/Speedboost v3 transparent.png")
SPEED_BOOST_IMAGE = pygame.transform.scale(SPEED_BOOST_IMAGE, (40, 40))

DUST_IMAGE = pygame.image.load("assets/dusty.png")
DUST_IMAGE = pygame.transform.scale(DUST_IMAGE, (30, 30))

CRASH_IMAGE = pygame.image.load("assets/crash.png")
CRASH_IMAGE = pygame.transform.scale(CRASH_IMAGE, (60, 60))

ARROW_IMAGE = pygame.image.load("assets/arrow.png")
ARROW_IMAGE = pygame.transform.scale(ARROW_IMAGE, (50, 50))

'''
# Load AI chariot images
AI_CHARIOT_IMAGES = [
    pygame.transform.scale(pygame.image.load("assets/chariot pixel art.png"), (40, 30)),
    pygame.transform.scale(pygame.image.load("assets/Poseidon Chariot Pixelated Transparent.png"), (40, 30)),
    pygame.transform.scale(pygame.image.load("assets/Zeus Chariot Pixelated Transparent.png"), (40, 30)),
    pygame.transform.scale(pygame.image.load("assets/Hades Chariot Pixelated Transparent.png"), (40, 30))
]
'''
# Load AI chariot images (flip horizontally so horses are in front)
AI_CHARIOT_IMAGES = [
    #pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/chariot pixel art.png"), (40, 30)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/Poseidon Chariot Pixelated Transparent.png"), (40, 30)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/Zeus Chariot Pixelated Transparent.png"), (40, 30)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/Hades Chariot Pixelated Transparent.png"), (40, 30)), True, False)
]

class Chariot:
    def __init__(self, x, y, chariot_type=0):
        #self.x, self.y = x, y
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
        self.x, self.y = pygame.math.Vector2(x, y)
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.speed = 4
       # self.image = image
        self.acceleration = 0.2
        self.max_speed = 6
        self.friction = 0.05
        self.drift_factor = 0.85  # adjust for
        self.drift_mode = False
        self.normal_drift = 0.2
        self.active_drift = 0.85
        self.drifting = False
        self.drift_rotation_multiplier = 2.0
        self.drift_speed_multiplier = 0.85
        self.dust_particles = []  #dust list for visual effect when turning
        self.crash_particles = []





        self.chariot_type = chariot_type  # Store selected chariot index

        # Load different chariot images for the player to choose from
        self.chariot_images = [
            pygame.image.load("assets/chariot pixel art.png"),
            pygame.image.load("assets/chariot 2 pixel art.png"),
            pygame.image.load("assets/chariot 3 pixel art.png")
        ]
        self.image = pygame.transform.scale(self.chariot_images[self.chariot_type], (40, 30))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    #move/update fuction with physics incorporated to make driving realistic
    def move(self, keys, track_bounds, finish_zone):
        prev_pos = self.pos.copy()

        # Drift toggle (space bar) press space bar to drift corners
        self.drift_mode = keys[pygame.K_SPACE]
        drift_factor = self.active_drift if self.drift_mode else self.normal_drift

        # Speed control gain speed as you push UP and reduce with DOWN to be more realistic
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            self.speed -= self.acceleration
        else:
            self.speed *= (1 - self.friction)

        self.speed = max(-self.max_speed / 2, min(self.speed, self.max_speed))

        # Steering with angle & left & right like actual car instead of just going straight in a direction
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3

        # Forward vector based on angle
        forward = pygame.math.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)))

        # Drifting physics
        self.velocity = (self.velocity * drift_factor) + (forward * self.speed * (1 - drift_factor))
        self.pos += self.velocity

        # Clamp to screen
        self.pos.x = max(0, min(WIDTH - 60, self.pos.x))
        self.pos.y = max(0, min(HEIGHT - 40, self.pos.y))

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Collision with track bounds
        if self.check_collision(track_bounds):
            self.pos = prev_pos
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Lap logic/counter for every time player crosses finish line
        if self.rect.colliderect(finish_zone):
            if not self.passed_finish:
                self.laps += 1
                self.passed_finish = True
        else:
            self.passed_finish = False

        #implement dust coming from chariot when turning
        if abs(self.velocity.x) > 1 or abs(self.velocity.y) > 1:
            if self.drift_mode or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.dust_particles.append(DustParticle(self.pos.x, self.pos.y))



         # might put back   self.rect.topleft = (self.x, self.y)


    def activate_speed_boost(self): # new
        self.speed = 6
        self.speed_boost_active = True
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Reset speed after 5 seconds


    def check_collision(self, track_bounds):
        for boundary in track_bounds:
            if self.rect.colliderect(boundary):
                self.crash_particles.append(CrashParticle(self.pos.x, self.pos.y))
                #self.health -= .5
                if not self.shield_active:
                    self.health -= 0.5  # Reduce health if no shield
                    print(f"Collision! Health: {self.health}")
                   
                # Apply bounce back force based on collision direction
                collision_normal = pygame.math.Vector2(
                    self.rect.centerx - boundary.centerx,
                    self.rect.centery - boundary.centery
                ).normalize()

                bounce_strength = 5  # You can tweak this value

                # Move player slightly away from the boundary
                self.pos += collision_normal * bounce_strength
                self.velocity *= -0.3  # Invert and dampen speed to simulate bounce

                # Update rect position
                self.rect.topleft = (int(self.pos.x), int(self.pos.y))

                return True  # Collision detected
        return False  # No collision
        
        '''
            
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > 6000:
            self.shield_active = False
        '''
      
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
        for dust in self.dust_particles[:]:
            dust.update()
            dust.draw(screen)
            if dust.life <= 0:
                self.dust_particles.remove(dust)

        for crash in self.crash_particles[:]:
            crash.update()
            crash.draw(screen)
            if crash.life <= 0:
                self.crash_particles.remove(crash)
                
        rotated_image = pygame.transform.rotate(self.image, self.angle + 180)
        rect = rotated_image.get_rect(topleft=self.pos)
        screen.blit(rotated_image, rect)
        #screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))


class AIOpponent(Chariot):
    def __init__(self, x, y, ai_path, ai_index):
        super().__init__(x, y)
        self.image = AI_CHARIOT_IMAGES[ai_index]  # Assign AI-specific image
        self.speed = 9 + random.uniform(-0.5, 0.5) # AI speed
        #self.angle = 0
        #self.pos = pygame.math.Vector2(x, y)
        self.x = x
        self.y = y
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.angle = 0
        #self.speed = 4  # AI speed of 4
        #self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.track_path = ai_path  # List of waypoints
        self.target_index = 0  # Start at first waypoint
        self.laps_completed = 0
        self.total_laps = 5  # Same as the player
        self.passed_finish = False  # New attribute
        #self.x, self.y = pygame.math.Vector2(x, y)
        #self.velocity = pygame.math.Vector2(0, 0)
        self.dust_particles = []
        #self.friction = 0.03
        #self.max_speed = 6.5 + random.uniform(-0.3, 0.3)

        


        #self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect = self.image.get_rect(topleft=(x, y))
        #self.rect.topleft = (self.x, self.y)

    
    def move(self, track_bounds, finish_zone):
        target = pygame.math.Vector2(self.track_path[self.target_index])
        direction = (target - self.pos)
        
        if direction.length() > 0:
            direction = direction.normalize()

        # AI speed is slightly less than player
        self.velocity = direction * self.max_speed * 0.6 
        # Simulate acceleration new
        '''
        desired_velocity = direction * self.max_speed * .9
        steering = desired_velocity - self.velocity
        max_steering = 0.15
        if steering.length() > max_steering:
            steering.scale_to_length(max_steering)

        self.velocity += steering
        self.velocity *= (1 - self.friction)  # Apply friction
        '''
        #end
        self.pos += self.velocity 

        # Update angle (face movement direction)
        if self.velocity.length() > 0:
            self.angle = -math.degrees(math.atan2(self.velocity.y, self.velocity.x))
            

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Check for reaching waypoint
        if self.pos.distance_to(target) < 20:
            self.target_index = (self.target_index + 1) % len(self.track_path)


        if self.velocity.length() > 0.5:
            self.dust_particles.append(DustParticle(self.pos.x, self.pos.y))


        
        # Collision handling
        if self.check_collision(track_bounds):
            # Revert to last position (optional)
            pass

        # Lap tracking
        if self.rect.colliderect(finish_zone):
            if not self.passed_finish:
                self.laps += 1
                self.passed_finish = True
        else:
            self.passed_finish = False

        #self.rect.topleft = (self.x, self.y)  # Update AI position
        #self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        #self.rect = self.image.get_rect(topleft=(self.x, self.y))
  
    '''
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle + 180)
        rect = rotated_image.get_rect(topleft=self.pos)
        screen.blit(rotated_image, rect)
    '''

class DustParticle:
    def __init__(self, x, y):
        self.image = DUST_IMAGE.copy()
        self.pos = pygame.Vector2(x, y)
        self.life = 20  # Frames it will stay

    def update(self):
        self.life -= 1

    def draw(self, screen):
        screen.blit(self.image, self.pos)



class CrashParticle:
    def __init__(self, x, y):
        self.image = CRASH_IMAGE.copy()
        self.pos = pygame.Vector2(x, y)
        self.life = 10  # Frames it will stay

    def update(self):
        self.life -= 1

    def draw(self, screen):
        screen.blit(self.image, self.pos)
   

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.angle = 0
        self.image = ARROW_IMAGE.copy()
        self.image = pygame.transform.rotate(self.image, self.angle + 90)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 5
        if self.rect.top > 850:
            self.kill()



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