import pygame
import random
#import pygame
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
    current_screen = "home"  # Start at home screen
    selected_map = None
    
    home_screen = HomeScreen(SCREEN)
    race_screen = None  # Will be initialized when race starts

    running = True
    while running:
        SCREEN.fill((255, 255, 255))  # Clear screen
        clock.tick(30)

        if current_screen == "home":
            selected_map = home_screen.run()
            if selected_map:
                race_screen = RaceScreen(SCREEN, selected_map)
                current_screen = "race"

        elif current_screen == "race":
            race_result = race_screen.run()
            if race_result in ["win", "lose", "exit", "quit"]:  # Return to home on finish
                current_screen = "home"

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

