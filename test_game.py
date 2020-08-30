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
from helper import log

#-----------------------------------
# Main variables
#-----------------------------------


#-----------------------------------
# Main function
#-----------------------------------

def main():
    
    # Initialize everything   
    pygame.init()                                               # Initialize all pygame modules

    # Set the screen in full screen
    #screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((800,600))

    # Get the screen info
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    # Set the size multiplier based on the screen size
    size_multiplier = helper.get_multiplier(screen_h)
    game_size = helper.get_gamesize(size_multiplier)
    game_w = game_size[0]
    game_h = game_size[1]
    game_00 = helper.get_00(screen_w, game_size[0])
    
    log("multiplier: ", size_multiplier)
    log("screen: ", screen.get_size())
    log("game size: ", game_size)
    log("00 position: ", game_00)

    # Set window Title
    pygame.display.set_caption("Space Invaders")                # Caption text
    pygame.mouse.set_visible(False)                                 # Hide mouse ?
    
    # Create background
    background = pygame.Surface(screen.get_size())              # Using the same surface of the screen
    background = background.convert()
    background.fill(constants.BACKGROUND_COLOR)                           # Define background

    # Create Game background
    game_background = pygame.Surface(game_size)
    game_background = game_background.convert()
    game_background.fill(constants.GAME_BACKGROUND_COLOR) 

    # Include text in background
    if pygame.font:
        font = pygame.font.Font(None, 56)                               # Defining font
        text = font.render("Space Invaders Game Demo", 1, (constants.BACKGROUND_TEXT_COLOR))             # Defining text
        textpos = text.get_rect(centerx=helper.get_center(game_w))       # Positioning text in the center
        game_background.blit(text, textpos)

        log("screen rec: ", text.get_rect(centerx=helper.get_center(screen_w)))
        log("screen center: ", helper.get_center(screen_w))
        

    # Display the background
    # screen.blit(background, (0, 0))
    screen.blit(game_background, (game_00, 0))
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
        #screen.blit(background, (0, 0))
        #pygame.display.flip()
    
    pygame.quit()
    # Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

#-----------------------------------
# function
#-----------------------------------

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Update the player location. """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]