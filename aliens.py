import pygame
from spritesheet import SpriteSheet



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

    sprite_width = 10
    sprite_heigh = 10
    sprite_file = "/"
    name=""

    #def __init__(self, key_color, file):
        
        # Call the parent class (Sprite) constructor
        #super().__init__()

        

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        #self.rect = self.image.get_rect()
    
        # Draw the ellipse
        # pygame.draw.ellipse(self.image, color, [0, 0, width, height])


    def __init__(self, file, key_color, sprite_sheet_data, multiplier):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        #sprite_sheet = SpriteSheet("img/ss3.png")
        # Set the background color and set it to be transparent
        #self.image = pygame.Surface([self.sprite_width, self.sprite_heigh])
        #self.image = pygame.transform.scale(self.image, (new_width, new_heigh))
        #self.image.set_colorkey(key_color)
        #self.image.fill(BLUE)
        # self.image.set_colorkey(color)

        sprite_sheet = SpriteSheet(file)
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
 
        self.name = sprite_sheet_data[4]

        # Set the background color and set it to be transparent
        #self.image = pygame.Surface([width, height])
        #new_width = width * 4
        #new_heigh = heigh * 4
        
        new_width = sprite_sheet_data[2]*multiplier
        new_heigh = sprite_sheet_data[3]*multiplier

        self.image = pygame.transform.scale(self.image, (new_width, new_heigh))
        self.image.set_colorkey(key_color)
        #self.image.fill(BLUE)
        # self.image.set_colorkey(color)

        self.rect = self.image.get_rect()