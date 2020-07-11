#!/usr/bin/env python
#-----------------------------------
# Documents
#-----------------------------------
# Pygame documentation
# https://www.pygame.org/docs/

# 1
#-----------------------------------
# Import section
#-----------------------------------
# Import sys and pygame modules
import os, sys
import pygame
# Imports specifics into the code
from pygame.locals import *
from pygame.compat import geterror

# Error if not font or mixer
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

#-----------------------------------
print('Global variables')
#-----------------------------------

# Window
size = width, height = 320, 240                                 # Size of the window
background_color = 0, 0, 0                                      # Background color
text_color = 50, 50, 50                                         # Text color

#directories
main_dir = os.path.split(os.path.abspath(__file__))[0]
print ('main_dir: ' + main_dir)
data_dir = os.path.join(main_dir, "data")
print ('data_dir: ' + data_dir)

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
    pygame.display.set_caption("test set caption")              # Caption text
    #pygame.mouse.set.visible(0)                                 # Hide mouse ?
    
    # Create background
    background = pygame.Surface(screen.get_size())              # Using the same surface of the screen
    background = background.convert()
    background.fill(background_color)                           # Define background

    # Include text in background
    if pygame.font:
        font = pygame.font.Font(None, 36)                               # Defining font
        text = font.render("test message", 1, (text_color))             # Defining text
        textpos = text.get_rect(centerx=background.get_width()/2)       # Positioning text in the center
        background.blit(text, textpos)

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare game Objects
    clock = pygame.time.Clock()
    allsprites = pygame.sprite.RenderPlain(())

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