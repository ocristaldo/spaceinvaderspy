#!/usr/bin/env python
#-----------------------------------
# Documents
#-----------------------------------
# Pygame documentation
# https://www.pygame.org/docs/
#
# Games programming
# http://programarcadegames.com/index.php
#

#-----------------------------------
# Import section
#-----------------------------------
# Import sys and pygame modules
import os, sys, math
import pygame
import constants
import helper
from game import Game
#import game

#-----------------------------------
# Main function
#-----------------------------------

def main():
    
    # Initialize everything   
    pygame.init()                                               # Initialize all pygame modules

    # Set the screen in full screen
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    
    # Get the window info
    window = helper.get_screen(pygame)
    
    # Set the size multiplier and define the game screen size
    gameScreen = helper.get_game_screen(window)

    # Set window Title
    pygame.display.set_caption("Space Invaders")                # Caption text
    pygame.mouse.set_visible(False)                             # Hide mouse ?
    
    # Create background
    background = pygame.Surface(window.size)             # Using the same surface of the screen
    background = background.convert()
    background.fill(constants.BACKGROUND_COLOR)                 # Define background

    # Create Game background
    game_background = pygame.Surface(gameScreen.size)
    game_background = game_background.convert()
    game_background.fill(constants.GAME_BACKGROUND_COLOR) 

    # Prepare game clock
    clock = pygame.time.Clock()
    
    game_engine = Game(gameScreen)
    
    # Main Loop
    going = True
    while going:                                                # Infinit Loop
        
        # Process events (keystrokes, mouse clicks, etc)
        done = game_engine.process_events()
 
        # Update object positions, check for collisions
        game_engine.run_logic()
 
        # Draw the current frame
        game_engine.display_frame(screen)
 
        # Pause for the next frame
        
        clock.tick(60)                                          # Used to help control our game's framerate

        # draw the window onto the screen
        #pygame.display.update()

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                going = False
            elif event.type == pygame.MOUSEBUTTONUP:
                going = False

        # Draw Everything
        #screen.blit(background, (0, 0))
        screen.blit(game_background, (gameScreen.game00, 0))
        pygame.display.flip()
    
    pygame.quit()
    # Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

