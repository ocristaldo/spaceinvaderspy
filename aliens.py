import pygame



#-----------------------------------
# classes
#-----------------------------------

class Alien(pygame.sprite.Sprite):
    """
    This class represents the aliens.
    It derives from the "Sprite" class in Pygame.
    """

    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, color, width, height):
        """
        Ellipse Constructor. Pass in the color of the ellipse,
        and its size
        """
        # Call the parent class (Sprite) constructor
        super().__init__()
    
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # self.image.set_colorkey(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
    
        # Draw the ellipse
        # pygame.draw.ellipse(self.image, color, [0, 0, width, height])