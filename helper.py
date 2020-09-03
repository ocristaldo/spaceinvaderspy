#-----------------------------------
# Import section
#-----------------------------------
import os, sys, math
import pygame
import constants
import sslist

def get_multiplier(heigh):
    return math.floor(heigh/constants.ORIGINAL_HEIGH)

def get_gamesize(multiplier):
    return (multiplier*constants.ORIGINAL_WIDHT, multiplier*constants.ORIGINAL_HEIGH)
    
def get_center(screen_w):
    return math.floor(screen_w/2)

def get_00(screen_w, game_w):
    return get_center(screen_w)-math.floor(game_w/2)

def log(txt,obj):
    print (txt,str(obj))

def get_char_Sprite(char):
    return eval('sslist.ss_' + char)

def get_screen(game):
    
    # Get the screen info
    screen_info = game.display.Info()
    screen_size = [0]*2
    screen_size[0]=screen_info.current_w
    screen_size[1]=screen_info.current_h
    return Screen(screen_size, screen_size[0],screen_size[1])

def get_game_screen(screen):
    
    size_multiplier = get_multiplier(screen.heigh)
    game_size = get_gamesize(size_multiplier)
    game_00 = get_00(screen.width, game_size[0])
    return GameScreen(game_size, game_size[0],game_size[1], size_multiplier, game_00)

class Screen():
    """ Class used to store screen properties. """
 
    def __init__(self, size, width, heigh):
        self.size = size
        self.width = width
        self.heigh = heigh
        
class GameScreen():
    """ Class used to store screen properties. """
 
    def __init__(self, size, width, heigh, multiplier, game00):
        self.size = size
        self.width = width
        self.heigh = heigh
        self.multiplier = multiplier
        self.game00 = game00