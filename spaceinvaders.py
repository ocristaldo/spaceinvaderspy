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

#-----------------------------------
# Main function
#-----------------------------------

def main():
    
    # Initialize everything   
    pygame.init()                                               # Initialize all pygame modules

    # Set the screen in full screen
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((300,200))

    # Get the screen info
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    # Set window Title
    pygame.display.set_caption("Space Invaders")                # Caption text
    pygame.mouse.set_visible(False)                                 # Hide mouse ?
    
    # Create background
    background = pygame.Surface(screen.get_size())              # Using the same surface of the screen
    background = background.convert()
    background.fill(constants.BACKGROUND_COLOR)                           # Define background

    # Include text in background
    if pygame.font:
        font = pygame.font.Font(None, 56)                               # Defining font
        text = font.render("Space Invaders Demo", 1, (constants.BACKGROUND_TEXT_COLOR))             # Defining text
        textpos = text.get_rect(centerx=math.floor(background.get_width()/2))       # Positioning text in the center
        background.blit(text, textpos)

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare game Objects
    clock = pygame.time.Clock()
    
    # Main Loop
    going = True
    while going:                                                        # Infinit Loop
        clock.tick(60)                                                  # Used to help control our game's framerate

        # draw the window onto the screen
        pygame.display.update()

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
        screen.blit(background, (0, 0))
        pygame.display.flip()
    
    pygame.quit()
    # Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

