import pygame
import random
#import pygame
from intro_screen import IntroScreen
from home_screen import HomeScreen
from race_screen import RaceScreen

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ancient Greek Chariot Racing")

# Main function to control screens
def main():
    clock = pygame.time.Clock()
    current_screen = "intro"  # Start at intro NEWW
    #current_screen = "home"  # Start at home screen
    selected_map = None
    selected_chariot = None 
    player_name = ""                    #NEWW
    
    intro_screen = IntroScreen(SCREEN) #NEWW
    #home_screen = HomeScreen(SCREEN) NEW ^^^
    race_screen = None  # Will be initialized when race starts
    home_screen = None  #NEW

    running = True
    while running:
        SCREEN.fill((255, 255, 255))  # Clear screen
        clock.tick(30)


        if current_screen == "intro":
            player_name = intro_screen.run()
            if player_name:
                home_screen = HomeScreen(SCREEN, player_name)
                current_screen = "home"

        elif current_screen == "home":
            #selected_map = home_screen.run()
            #if selected_map:
            #    race_screen = RaceScreen(SCREEN, selected_map)
            #    current_screen = "race"
            result = home_screen.run()
            if result is not None:  # Ensure result is valid before unpacking
                selected_map, selected_chariot, game_mode = result
                if selected_map and selected_chariot:
                    #game_mode = home_screen.selected_modes.get(selected_map, "race")  # Get selected mode
                    race_screen = RaceScreen(SCREEN, selected_map, selected_chariot, game_mode,player_name=home_screen.player_name)
                    current_screen = "race"
                    race_result = race_screen.run()

                    if race_result == "win":
                        home_screen.wins += 1
                        current_screen = "home"
                    elif race_result == "lose":
                        home_screen.losses += 1
                        current_screen = "home"
                    elif race_result in ["exit", "quit"]:
                        current_screen = "home"
                    elif race_result == "restart":
                        race_screen = RaceScreen(SCREEN, selected_map, selected_chariot, game_mode, player_name=home_screen.player_name)


        
        elif current_screen == "race":
            race_result = race_screen.run()
            if race_result in ["win", "lose", "exit", "quit"]:  # Return to home on finish
                current_screen = "home"
            elif race_result == "restart":
                # Restart race with the same settings
                race_screen = RaceScreen(SCREEN, selected_map, selected_chariot, game_mode, player_name=home_screen.player_name)
                current_screen = "race"
        

      

         
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

