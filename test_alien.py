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
import os, sys
import pygame
import aliens
import random

#-----------------------------------
print('Global variables')
#-----------------------------------

# Window
size = width, height = 320, 240                                 # Size of the window
background_color = 100, 100, 100                                      # Background color
text_color = 50, 50, 50                                         # Text color


# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#-----------------------------------
# Main function
#-----------------------------------

def main():
    print('main')
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    # Initialize everything   
    pygame.init()                                               # Initialize all pygame modules
    screen = pygame.display.set_mode(size)                      # Initialise screen window
    pygame.display.set_caption("Alien test")              # Caption text
    
    # Create background
    background = pygame.Surface(screen.get_size())              # Using the same surface of the screen
    background = background.convert()
    background.fill(background_color)                           # Define background

    # Include text in background
    if pygame.font:
        font = pygame.font.Font(None, 36)                               # Defining font
        text = font.render("Alien Test", 1, (text_color))             # Defining text
        textpos = text.get_rect(centerx=background.get_width()/2)       # Positioning text in the center
        background.blit(text, textpos)

    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    alien_list = pygame.sprite.Group()
    
    # This is a list of every sprite. 
    # All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare game Objects
    clock = pygame.time.Clock()
    alien = aliens.Alien(WHITE,20,20)

    # Set a random location for the alien
    # alien.rect.x = random.randrange(width)
    alien.rect.x = 10
    # alien.rect.y = random.randrange(height)
    alien.rect.y = 10
 

    # Add the block to the list of objects
    alien_list.add(alien)
    all_sprites_list.add(alien)

    allsprites = pygame.sprite.RenderPlain((alien))

    # Main Loop
    going = True
    while going:                                                        # Infinit Loop
        clock.tick(60)                                                  # Used to help control our game's framerate

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

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()