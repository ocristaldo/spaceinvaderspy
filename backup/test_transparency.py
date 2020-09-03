#-----------------------------------
# Import section
#-----------------------------------
# Import sys and pygame modules
import os, sys
import pygame
import constants

def main():
    # Initialize everything   
    pygame.init()                                                               # Initialize all pygame modules
    
    # Set the height and width of the screen
    screen = pygame.display.set_mode((300,200))                                      # Initialise screen window
    
    #Window Title
    pygame.display.set_caption("Transparency test")  
    
    #SpriteSheet file
    file = "img/ss3.png"

    # Load the sprite sheet.
    image = pygame.image.load(file).convert()

    # Set Key_Color as the transparent color
    image.set_colorkey(constants.KEY_COLOR)
    print(constants.KEY_COLOR)

    # Main Loop
    going = True
    while going:                                                        # Infinit Loop
        
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
        screen.blit(image, (0,0))
        pygame.display.update()
    
    pygame.quit()

# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
    