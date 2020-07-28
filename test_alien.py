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
from aliens import Alien
#from sslist import ss_alien1
import random
import constants
import sslist
import spritesheet
import math



#-----------------------------------
# Main function
#-----------------------------------

def main():
    print('main')
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    # Initialize everything   
    pygame.init()                                                               # Initialize all pygame modules
    # Set the height and width of the screen
    size_multiplier = 3
    size = [constants.SCREEN_WIDTH*size_multiplier, constants.SCREEN_HEIGHT*size_multiplier]
    screen = pygame.display.set_mode(size)                                      # Initialise screen window
    pygame.display.set_caption("Alien test")                                    # Caption text
    
    # Create background
    background = pygame.Surface(screen.get_size())                              # Using the same surface of the screen
    background = background.convert()
    background.fill(constants.background_color)                                 # Define background

    # Include text in background
    if pygame.font:
        font = pygame.font.Font(None, 36)                                       # Defining font
        text = font.render("Alien Test", 1, (constants.text_color))             # Defining text
        textpos = text.get_rect(centerx=background.get_width()/2)               # Positioning text in the center
        background.blit(text, textpos)

    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    #alien_list = pygame.sprite.Group()
    
    # This is a list of every sprite. 
    # All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare game Objects
    clock = pygame.time.Clock()
    file = "img/ss3.png"
    #alien = aliens.Alien(WHITE,20,20)
    #alien = Alien(file, constants.BLACK, sslist.ss_ufo, size_multiplier)

    # Set a random location for the alien
    # alien.rect.x = random.randrange(width)
    #alien.rect.x = 100
    # alien.rect.y = random.randrange(height)
    #alien.rect.y = 100
 
    relx=0
    rely=0
    i=0
    for x in sslist.ss_ls:
        a = Alien(file, constants.BLACK, x, size_multiplier)
        print(x[0],x[1],x[2],x[3])
        div = math.floor(i/5)
        print(div)
        #relx = (div*relx)+10+x[2]
        #rely = (div*rely)+10+x[3]
        a.rect.x = div*x[2]
        a.rect.y = div*x[3]
        i+=1
        print("obj", i, "x:",a.rect.x,"y:",a.rect.y)
        all_sprites_list.add(a)


    # Add the block to the list of objects
    #alien_list.add(alien)
    #all_sprites_list.add(alien)

    #allsprites = pygame.sprite.RenderPlain((alien))
    allsprites = pygame.sprite.RenderPlain((all_sprites_list))

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