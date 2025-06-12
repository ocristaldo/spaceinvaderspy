#-----------------------------------
# Import section
#-----------------------------------
import os, sys, math
import pygame
import constants
import sslist

def get_multiplier(heigh):
    return math.floor(heigh/constants.ORIGINAL_HEIGHT)

def get_gamesize(multiplier):
    return (multiplier*constants.ORIGINAL_WIDTH, multiplier*constants.ORIGINAL_HEIGHT)
    
def get_center(screen_w):
    return math.floor(screen_w/2)

def get_00(screen_w, game_w):
    return get_center(screen_w)-math.floor(game_w/2)

def log(txt,obj):
    print (txt,str(obj))

def get_char_Sprite(char):
    return eval('sslist.ss_' + char)