import pygame
import sslist
from spritesheet import SpriteSheet





#-----------------------------------
# classes
#-----------------------------------

class GameLevel():
    # define 
    
    def __init__(self, game):
        
        # init game
        self.game = game
        
        
    def start():
        #fire start event
        return
        
    def stop():
        #fire stop event
        return
        

class Layout ():
    
    def __init__(self, game):
        
        self.game = game
    
    # alien line 1
    def getline1():
        #eval()
        alienline = [0]*3
        alienline[0] = sslist.ss_alien11
        alienline[1] = sslist.ss_alien12 
        return alienline
    
    # alien line 2
    def getline2():
        alienline = [0]*3
        alienline[0] = sslist.ss_alien21
        alienline[1] = sslist.ss_alien22
        return alienline
    
    # alien line 3
    def getline3():
        alienline = [0]*3
        alienline[0] = sslist.ss_alien31
        alienline[1] = sslist.ss_alien32
        return alienline