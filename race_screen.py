import pygame
import random
#from utils import Chariot, ShieldPowerUp
from utils import Chariot, AIOpponent, ShieldPowerUp, SpeedBoost
#from track_data import TRACK_DETAILS

WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)

#new
TRACK_DETAILS = { 
    "assets/colosseum_track.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        "bounds": [pygame.Rect(850, 50, 750, 700), pygame.Rect(0, 50, 250, 700), pygame.Rect(80, 0, 750, 140), pygame.Rect(25, 775, 800, 50), pygame.Rect(450, 260, 200, 350)],
        "ai_path": [(500, 680), (670, 620), (700, 500), (720, 400), (700, 230), (500, 150), (360, 200), (300, 300), (300, 500), (400, 640)]
      #  "boundsLeft": [pygame.Rect(0, 50 , 250, 700)],
       # "boundsTop": [pygame.Rect(80, 0, 750, 140)],
      #  "boundsBottom": [pygame.Rect(25, 775, 800, 50)]
    },
    "assets/greektracks.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        #"bounds": [pygame.Rect(800, 620, 300, 300)],
        # right, left, top, bottom, middle, upper right, upper left.
        "bounds": [pygame.Rect(850, 50, 750, 700), pygame.Rect(0, 50, 250, 700), pygame.Rect(80, 0, 750, 130), pygame.Rect(25, 750, 800, 50), pygame.Rect(450, 260, 210, 350), pygame.Rect(800, 50, 700, 300), pygame.Rect(0, 50, 300, 300)], 
        "ai_path": [(500, 680), (670, 620), (700, 500), (720, 400), (700, 230), (500, 150), (360, 200), (300, 300), (300, 500), (400, 640)]
        #[(500, 680), (700, 500), (900, 300), (700, 150), (500, 100), (300, 150), (100, 300), (300, 500)]

    },
     "assets/modern_track.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        "bounds": [pygame.Rect(800, 620, 300, 300)],
        "ai_path": [(500, 680), (700, 500), (900, 300), (700, 150), (500, 100), (300, 150), (100, 300), (300, 500)]
    },
    "assets/ancient_greece.png": {
        "start": (600, 750),
        "finish": pygame.Rect(540, 320, 50, 20),
        "bounds": [pygame.Rect(800, 150, 700, 500)],
        "ai_path": [(500, 680), (700, 500), (900, 300), (700, 150), (500, 100), (300, 150), (100, 300), (300, 500)]
    }
    
}


class RaceScreen:
    def __init__(self, screen, track_image_path):
        self.screen = screen
        self.track_img = pygame.image.load(track_image_path)
        self.track_img = pygame.transform.scale(self.track_img, (1100, 850))


        if track_image_path == "assets/modern_track.png":
            self.track_img = pygame.transform.scale(self.track_img, (1300, 850))


        # Ensure track details exist
        if track_image_path not in TRACK_DETAILS:
            raise ValueError(f"Track details not found for: {track_image_path}")

       # self.track_details = TRACK_DETAILS[track_image_path]

        # Set start position safely
       # self.start_pos = self.track_details.get("start")
       # if self.start_pos is None:
       #     raise ValueError(f"Missing 'start' position in track details for: {track_image_path}")


        #self.track_details = TRACK_DETAILS[track_image_path]
        self.track_data = TRACK_DETAILS[track_image_path] #new
        #NO / self.powerups = [ShieldPowerUp(random.randint(100, 900), random.randint(100, 700)) for _ in range(3)]
        #self.finish_zone = pygame.Rect(550, 150, 20, 90) #new
        #self.track_bounds = [pygame.Rect(80, 80, 840, 701)]  # Adjust for track
        #self.player = Chariot(*self.track_data["start"])  # Spawn at track's start position
        self.start_pos = self.track_data["start"]
        self.finish_zone = self.track_data["finish"]
        self.track_bounds = self.track_data["bounds"]
        self.ai_path = self.track_data.get("ai_path", [])
       # self.player.laps = 0
        # Exit Button
        #new 3 lines
        self.player = Chariot(*self.start_pos)
        self.ai_opponents = [AIOpponent(self.start_pos[0] + (i * 50), self.start_pos[1], self.ai_path) for i in range(4)]
        #self.ai_opponents = [AIOpponent(self.start_pos[0] + (i * 50), self.start_pos[1]) for i in range(4)]
        self.powerups = self.generate_powerups()

        self.exit_button = pygame.Rect(20, 720, 150, 50)
        self.font = pygame.font.Font(None, 36)

    def draw_exit_button(self):
        pygame.draw.rect(self.screen, RED, self.exit_button)
        text = self.font.render("Exit", True, WHITE)
        self.screen.blit(text, (self.exit_button.x + 50, self.exit_button.y + 10))
        

    def generate_powerups(self):
        powerups = []
        while len(powerups) < 3:
            x, y = random.randint(100, 900), random.randint(100, 700)
            # Ensure power-ups only spawn inside the track (not inside boundary areas)
            valid = all(not bound.collidepoint(x, y) for bound in self.track_bounds)

            if valid:
                powerups.append(random.choice([ShieldPowerUp(x, y), SpeedBoost(x, y)]))
        return powerups
    
    def draw_health_bar(self, surface, health):
        max_health = 100  # Assuming max health is 100
        bar_width = 200  # Total bar width
        bar_height = 20  # Height of the health bar
        x, y = 10, 10  # Top-right corner

        health_ratio = max(health / max_health, 0)  # Prevent negative health
        #pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))  # Red background
        pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * health_ratio, bar_height))  # Green foreground
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)  # White border


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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.collidepoint(event.pos):
                        return "exit"  # Go back to home screen
                

            keys = pygame.key.get_pressed()
            self.player.move(keys, self.track_bounds)
            #self.player.move(keys)
            self.player.check_collision(self.track_bounds) #new
    
            
            # AI Movement / new
            for ai in self.ai_opponents:
                ai.move(self.track_bounds)
            

            # Power-ups
            for powerup in self.powerups[:]:
                if self.player.rect.colliderect(powerup):
                    #self.player.activate_shield()
                    powerup.apply_effect(self.player) # new
                    self.powerups.remove(powerup)

            # Draw elements
            #self.player.draw(self.screen)
            #for powerup in self.powerups:
            #    powerup.draw(self.screen)

                # Draw Exit Button
            self.draw_exit_button()

            # Draw health bar
            self.draw_health_bar(self.screen, self.player.health)

            # Draw all elements / new
            self.player.draw(self.screen)
            for ai in self.ai_opponents:
                ai.draw(self.screen)

            for powerup in self.powerups: #new
                powerup.draw(self.screen)

            # Check lap completion / new
            if self.player.rect.colliderect(self.finish_zone):
                self.player.laps += 1
                print(f"Player Laps: {self.player.laps}")
              
            # Check if AI crosses the finish line
            for ai in self.ai_opponents:
                if ai.rect.colliderect(self.finish_zone):
                    ai.laps += 1
                    print(f"AI Laps: {ai.laps}")
            
            # Check game over conditions
            if self.player.health <= 0:
                print("Game Over! You lost!")
                return "lose"

            if self.player.laps >= 50:
            #NO /if self.player.rect.colliderect(self.finish_zone): #new
                print("Congratulations! You won!")
                return "win"
            #NO /if self.player.rect.colliderect(self.finish_zone):
                 # new
             #   print("Congratulations! You won!")
             #   return "win"
            for ai in self.ai_opponents:
                if ai.laps >= 55:
                    print("AI wins! You lost.")
                    return "lose"
            pygame.draw.rect(self.screen, (200, 0, 0), self.finish_zone) # new

            pygame.display.update()
