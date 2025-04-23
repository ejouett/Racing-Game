import pygame
import random
#from utils import Chariot, ShieldPowerUp
from utils import Chariot, AIOpponent, ShieldPowerUp, SpeedBoost, PowerUp, DustParticle, CrashParticle, Arrow
#from track_data import TRACK_DETAILS


WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)

#new
TRACK_DETAILS = { 
    "assets/colosseum_track.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        #right, left, top, bottom, middle
        "bounds": [pygame.Rect(850, 50, 750, 700), pygame.Rect(0, 50, 250, 700), pygame.Rect(80, 0, 750, 140), pygame.Rect(25, 775, 800, 50), pygame.Rect(450, 260, 200, 350), pygame.Rect(800, 650, 250, 700), pygame.Rect(750, 700, 250, 700), pygame.Rect(775, 0, 450, 180), pygame.Rect(800, 800, 350, 220), pygame.Rect(0, 0, 320, 190), pygame.Rect(0, 0, 340, 160), pygame.Rect(0, 650, 300, 700), pygame.Rect(0, 700, 340, 700)],
        "ai_path": [(500, 680), (670, 620), (700, 500), (720, 400), (700, 230), (500, 150), (360, 200), (300, 300), (300, 500), (400, 640)]
      
    },
    "assets/greektracks.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 160, 20, 60),
        # right, left, top, bottom, middle, upper right, upper left.
        "bounds": [pygame.Rect(850, 50, 750, 700), pygame.Rect(0, 50, 250, 700), pygame.Rect(80, 0, 750, 130), pygame.Rect(25, 750, 800, 50), pygame.Rect(450, 260, 200, 350), pygame.Rect(800, 50, 700, 300), pygame.Rect(0, 50, 300, 300), pygame.Rect(800, 650, 250, 700), pygame.Rect(750, 700, 250, 700), pygame.Rect(775, 0, 450, 180), pygame.Rect(800, 800, 350, 220), pygame.Rect(0, 0, 320, 190), pygame.Rect(0, 0, 340, 160), pygame.Rect(0, 650, 300, 700), pygame.Rect(0, 700, 340, 700)], 
        "ai_path": [(500, 680), (670, 620), (700, 550), (710, 500), (720, 400), (690, 220), (590, 180), (510, 155), (370, 200), (320, 300), (310, 500), (350, 590), (400, 640)]
    },
     "assets/modern_track.png": {
        "start": (510, 630),
        "finish": pygame.Rect(450, 550, 85, 20),
        #right, top, left, bottom, bottom right, inside top rec, middle inside rec, middle left inside, bottom inside horizontal rec, very bottom inside, rightside indent outside, leftside indent outside
        "bounds": [pygame.Rect(960, 0, 300, 800), pygame.Rect(0, 0, 1250, 50), pygame.Rect(0, 0, 350, 1250), pygame.Rect(0, 790, 980, 160), pygame.Rect(350, 555, 80, 300), pygame.Rect(480, 140, 350, 100), pygame.Rect(615, 250, 210, 180), pygame.Rect(480, 400, 180, 70), pygame.Rect(560, 480, 70, 230), pygame.Rect(630, 710, 200, 8), pygame.Rect(770, 520, 200, 110), pygame.Rect(340, 320, 160, 5)],
        "ai_path": [(510, 630), (480, 730), (810, 745), (885, 705), (820, 650), (690, 650), (690, 450), (880, 450), (880, 90), (400, 80), (400, 250), (450, 260), (550, 300), (450, 340), (400, 350), (400, 450), (450, 480)]
    },
    "assets/ancient_greece.png": {
        "start": (800, 300),
        "finish": pygame.Rect(535, 470, 60, 20),
        #right, top, left, bottom, bottom right corner, top right corner, top left corner, bottom left corner
        "bounds": [pygame.Rect(980, 150, 700, 500), pygame.Rect(0, 0, 980, 160), pygame.Rect(0, 0, 100, 800), pygame.Rect(0, 770, 980, 160), pygame.Rect(970, 650, 980, 160), pygame.Rect(950, 670, 980, 160), pygame.Rect(950, 710, 980, 160), pygame.Rect(900, 700, 980, 160), pygame.Rect(880, 250, 400, 55), pygame.Rect(810, 150, 400, 50), pygame.Rect(200, 160, 60, 50), pygame.Rect(100, 210, 60, 70), pygame.Rect(100, 280, 40, 40), pygame.Rect(100, 600, 30, 200), pygame.Rect(100, 680, 50, 200), pygame.Rect(100, 740, 140, 50), pygame.Rect(780, 740, 400, 50), pygame.Rect(785, 420, 80, 150), pygame.Rect(240, 450, 80, 160), pygame.Rect(260, 350, 75, 100), pygame.Rect(330, 260, 45, 100), pygame.Rect(350, 240, 380, 1), pygame.Rect(680, 260, 40, 60), pygame.Rect(490, 530, 120, 60), pygame.Rect(350, 675, 400, 1), pygame.Rect(680, 350, 13, 170)],    #, pygame.Rect(960, 660, 980, 160)
        "ai_path": [(800, 300), (750, 230), (730, 190), (700, 180), (550, 180), (350, 180), (280, 220), (220, 300), (150, 400), (130, 500), (180, 600), (330, 695), (700, 695), (850, 630), (890, 590), (900, 380), (800, 350), (720, 395), (700, 580), (620, 620), (450, 630), (340, 580), (340, 480), (430, 250), (505, 240), (620, 280), (510, 480)]
    }
    
}


class RaceScreen:
    def __init__(self, screen, track_image_path, selected_chariot, game_mode, player_name=""):
        self.screen = screen
        self.track_img = pygame.image.load(track_image_path)
        self.track_img = pygame.transform.scale(self.track_img, (1100, 850))
        self.selected_chariot = selected_chariot  # Store selected chariot

        self.game_mode = game_mode  # Store the mode

        #self.falling_objects = []  # Objects in survival mode
        self.falling_objects = pygame.sprite.Group()

        self.player_name = player_name

         # Load background image for how to play screen
        self.background_race_result = pygame.image.load("assets/greektheme.png")
        self.background_race_result = pygame.transform.scale(self.background_race_result, (1000, 800))

        """
        # Apply chariot abilities
        if self.selected_chariot == "health":
            self.player_health = 120  # Default is 100
        elif self.selected_chariot == "speed":
            self.player_speed = 5.5  # Default is 5
        elif self.selected_chariot == "bullets":
            self.player_bullets = 2  # Default is 0
        """
        if track_image_path == "assets/modern_track.png":
            self.track_img = pygame.transform.scale(self.track_img, (1300, 850))

        # Ensure track details exist
        if track_image_path not in TRACK_DETAILS:
            raise ValueError(f"Track details not found for: {track_image_path}")

      
        self.track_data = TRACK_DETAILS[track_image_path] #new
        #self.player = Chariot(*self.track_data["start"])  # Spawn at track's start position
        self.start_pos = self.track_data["start"]
        self.finish_zone = self.track_data["finish"]
        self.track_bounds = self.track_data["bounds"]
        self.ai_path = self.track_data.get("ai_path", [])
        self.score = 0
       # self.player.laps = 0
        # Exit Button
        #newwwww
        self.player = Chariot(*self.start_pos, chariot_type=selected_chariot, name=self.player_name)

    
        #self.player = Chariot(*self.start_pos)
        self.ai_opponents = [AIOpponent(self.start_pos[0] - (i * 40), self.start_pos[1], self.ai_path, i) for i in range(3)]
        #self.ai_opponents = [AIOpponent(self.start_pos[0] + (i * 50), self.start_pos[1]) for i in range(4)]
        self.powerups = self.generate_powerups()
        #self.dust_particles = []


        self.exit_button = pygame.Rect(20, 720, 150, 50)
        self.font = pygame.font.Font(None, 36)

        '''      
        if self.game_mode == "survival":
            self.obstacles = [
                pygame.Rect(random.randint(300,  800), random.randint(50, 1050), 40, 40)
                for _ in range(50)
            ]
        '''
    def spawn_falling_objects(self):
        """Spawn objects in survival mode."""
        if random.random() < 0.02:  # 2% chance per frame
            x = random.randint(50, 1000)
            #self.falling_objects.append(pygame.Rect(x, 0, 30, 30))
            arrow = Arrow(x, 0)
            self.falling_objects.add(arrow)
        

    def move_falling_objects(self):
        """Move and detect collisions."""
        '''
        for obj in self.falling_objects[:]:
            obj.y += 5
            pygame.draw.rect(self.screen, RED, obj)
            if obj.y > 850:
                self.falling_objects.remove(obj)
            elif self.player.rect.colliderect(obj):
                if not self.player.shield_active:
                    self.player.health -= 10
                self.falling_objects.remove(obj)
            '''
        #self.falling_objects.update()
        #self.falling_objects.draw(self.screen)

        for arrow in self.falling_objects:
            self.falling_objects.update()
            self.falling_objects.draw(self.screen)

            if self.player.rect.colliderect(arrow.rect):
                if not self.player.shield_active:
                    self.player.health -= 10
                arrow.kill()


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



    def reset_game(self):
        #result = "restart"
        return "restart"
        # Reset player, AI, laps, positions, etc.
       # self.__init__(self.screen)  # Simple but works

    def go_to_home(self):
        result = "home"
        return result
        # Handle what comes back from home.run() go to home screen


    def show_end_screen(self, win):
        running = True
        font = pygame.font.Font(None, 70)
        button_font = pygame.font.Font(None, 40)

        result_text = "You Win!" if win else "You Lose!"
        result_color = (0, 200, 0) if win else (200, 0, 0)
        # Draw Restart button
        if result_text.lower() == "you win!":
            if self.player.health > 90:
                grade = "A"
            elif self.player.health > 70:
                grade = "B"
            elif self.player.health > 50:
                grade = "C"
            elif self.player.health > 0:
                grade = "D"
            else:
                grade = "F"
        else: 
            grade = "F"

        grade_font = pygame.font.SysFont(None, 50)
        grade_text = grade_font.render(f"Grade: {grade}", True, (0, 0, 0))
        grade_rect = grade_text.get_rect(center=(500, 330))
            # Buttons
        # Draw Restart button
        
        home_button = pygame.Rect(400, 400, 200, 50)
        #replay_text = button_font.render("Press R to Replay", True, (0, 0, 0))

        while running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_race_result, (0, 0))
            title = font.render(result_text, True, result_color)
            self.screen.blit(title, (400, 200))
            pygame.draw.rect(self.screen, (0, 0, 200), home_button)
            self.screen.blit(button_font.render("Back to Home", True, (255, 255, 255)), (home_button.x + 20, home_button.y + 10))
            #self.screen.blit(replay_text, (380, 300))
            self.screen.blit(grade_text, grade_rect)
            lap_text = font.render(f"Lap: {self.player.laps}/5", True, (0, 0, 0))
            self.screen.blit(lap_text, (750, 70))  # Adjust based on your resolution

          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()  # You'll implement this
                        return 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button.collidepoint(event.pos):
                        self.go_to_home()  # You'll implement this
                        return
                    
            

    
            pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(30)
            self.screen.fill(WHITE)
            self.screen.blit(self.track_img, (0, 0))

            #if self.game_mode == "survival":
            #    self.run_survival_mode()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.collidepoint(event.pos):
                        return "exit"  # Go back to home screen
                
            #For When keys are pressed and player is moving
            keys = pygame.key.get_pressed()
            self.player.move(keys, self.track_bounds, self.finish_zone)
            #self.player.move(keys)
            self.player.check_collision(self.track_bounds) #new
            if keys[pygame.K_r]:  # If "R" key is pressed during game you restart the map
                return "restart"
           

            # AI Movement / new
            for ai in self.ai_opponents:
                ai.move(self.track_bounds, self.finish_zone)
            
        
            # Power-ups handles collide, apply, and remove
            for powerup in self.powerups[:]:
                if self.player.rect.colliderect(powerup):
                    #self.player.activate_shield()
                    powerup.apply_effect(self.player) # new
                    self.powerups.remove(powerup)
                    #self.powerups.respawn(powerup)
            
            # Draw elements
                    #draw laps
            lap_text = self.font.render(f"Lap: {self.player.laps}/5", True, (0, 0, 0))
            self.screen.blit(lap_text, (800, 20))  # Adjust based on your resolution

            
                # Draw Exit Button
            self.draw_exit_button()

            # Draw health bar
            self.draw_health_bar(self.screen, self.player.health)

            
            #Check if its survival mode and spawn objects
            if self.game_mode == "survival":
                self.spawn_falling_objects()
                self.move_falling_objects()
                
                
                
            # Draw all elements / new
            self.player.draw(self.screen)
            self.player.draw_names(self.screen) #new
            for ai in self.ai_opponents:
                ai.draw(self.screen)
                ai.draw_name(self.screen) #new
            

            #draw powerups
            for powerup in self.powerups: #new
                powerup.draw(self.screen)

          
            #Go to end screen after match to see grade and result 
            if self.player.laps >= 2:
                self.show_end_screen(win=True)
            elif any(ai.laps >= 2 for ai in self.ai_opponents):
                self.show_end_screen(win=False)
            elif self.player.health <= 0:
                self.show_end_screen(win=False)


            if self.player.health <= 0:
                print("Game Over! You lost!")
                return "lose"

            if self.player.laps >= 2:
            #NO /if self.player.rect.colliderect(self.finish_zone): #new
                print("Congratulations! You won!")
                return "win"
            
            
            for ai in self.ai_opponents:
                if ai.laps >= 2:
                    print("AI wins! You lost.")
                    return "lose"
            pygame.draw.rect(self.screen, (200, 0, 0), self.finish_zone) # new

            pygame.display.update()



    