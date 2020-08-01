
#-----------------------------------
# Import section
#-----------------------------------
# Import sys and pygame modules
import os, sys, math
import pygame
import constants

def main():
    # Initialize everything   
    pygame.init()                                                               # Initialize all pygame modules
    
    # Set the height and width of the screen
    screen = pygame.display.set_mode((300,200))                                      # Initialise screen window
    
    # Window Title
    pygame.display.set_caption("Text test")  
    
    # Create background
    background = pygame.Surface(screen.get_size())              # Using the same surface of the screen
    background = background.convert()
    background.fill(constants.BACKGROUND_COLOR)                           # Define background

    # Write Text
    if pygame.font:
        font = pygame.font.Font(None, 14)                               # Defining font
        t = []
        t.append('Game Info:')
        t.append(('Screen :{0}').format(str(screen)))
        print(t)
        print(''.join(t))
        text_info = ''.join(t)
        print(text_info)
        
        text = font.render(text_info, 1, (200,200,200))             # Defining text
        textpos = text.get_rect(centerx=math.floor(screen.get_width()/2))       # Positioning text in the center
        background.blit(text, textpos)

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
        screen.blit(background, (0, 0))
        pygame.display.update()
    
    pygame.quit()

# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
    

# Show info
def show_info(screen):
    # Include text in background
    if pygame.font:
        font = pygame.font.Font(None, 14)                               # Defining font
        text_info = "Game Info:\r"
        text_info += "Screen Width:{0}"
        text_info = text_info.format(screen_w)
        print(text_info)
        text = font.render(text_info, 1, (constants.BACKGROUND_TEXT_COLOR))             # Defining text
        #textpos = text.get_rect(centerx=background.get_width()/2)       # Positioning text in the center
        screen.blit(text, (0,0))