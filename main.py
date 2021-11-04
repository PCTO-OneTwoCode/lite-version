'''
PCTO - One Two Code

Our github page: https://github.com/PCTO-OneTwoCode
'''


'''---------------------------
INCLUDE LIBRARIES
---------------------------'''

import time
import sys
import pygame
from Libraries.startMenu.startMenu import menu
from GraphicMain.gameDesign import mainGraphic
from GraphicMain.calibration import calibrationTest
from config import *

#initialize pygame
pygame.init()



def main():


    #this variable contains the returned value from the start menu
    exitMenu = -1
    #this variable contains the returned value from the game
    exitGame = -1
    #this variable is false if the sound is muted else it si true
    silent = False

    #this global variable contain the game screen
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    #while the menu isn't equal to 0, it runs the code
    while exitMenu != 0:
        #first it calls the start menu that return 2 variables
        exitMenu, silent = menu(screen, silent)

        #if exitMenu is equal to 0, the program ends
        if exitMenu == 0:
            exit(0)
        elif exitMenu == 1: #otherwise it starts the gameplay window
            lowerBound = calibrationTest()
            mainGraphic(screen, silent, lowerBound)


#this run the main function
if __name__ == "__main__":
    main()
