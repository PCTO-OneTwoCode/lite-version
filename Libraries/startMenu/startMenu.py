'''
Start menu

https://github.com/PCTO-OneTwoCode
'''

#import libraries
import pygame, sys, time
import random
import os
from pygame.locals import *
from config import *

#this is the path of this python file
pathname = os.path.dirname(os.path.realpath(__file__))

#pygame and pymixer initializations
pygame.init()
pygame.mixer.init()



#----------------------------------------
# CLASSES
#----------------------------------------

#This class contains the background method
class Background():
    #constructor
    def __init__(self, x, y, filepath=os.path.join(pathname, 'sprites/background.jpg')):
        try:
            #load the image
            self.image = pygame.image.load(filepath)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(0,0)
            #resize it using the screen sizes
            self.fullScreenImage = pygame.transform.scale(self.image, (x,y))
            
        except Exception as e:
            #print the exception on the screen
            print('error: ', str(e))

    #update the background status
    def update(self,screen):
        self.rect.move(self.rect.center[0]+5,self.rect.center[1])
        screen.blit(self.fullScreenImage, self.rect)


#this class contain the title displayed on the screen
class Title():
    #constructor
    def __init__(self, x, y, filepath=os.path.join(pathname, 'sprites/title.png')):
        try:
            #load the image and move it to the right position
            self.image = pygame.image.load(filepath)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)
            #self.image = pygame.transform.scale(image,(50,50))
        except Exception as e:
            #print the error on the screen
            print('error: ', str(e))

    #this method update the title status
    def update(self,screen):
        screen.blit(self.image, self.rect)


#this class has been made to control buttons
class Button():
    #constructor
    def __init__(self, filepath, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width

        try:
            #load the image
            self.image = pygame.image.load(filepath)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(0,self.screen_height)
        except Exception as e:
            #print the error on the screen
            print('error: ', str(e))

    #return the y cordinate of the button        
    def getY(self):
        return self.rect.center[1]

    #update the button status
    def update(self,screen,x,y):
        #controls if the user press the button
        if self.rect.collidepoint(x, y):
            return True
        screen.blit(self.image, self.rect)

    #change the image of the button if it is the volume button
    def changeStatus(self, imgName, x, y, soundTrack, silent):
        #if the buttom is pressed change the button status
        if self.rect.collidepoint(x, y):
            #load the button click sound
            soundEffect = pygame.mixer.Sound(os.path.join(pathname, "btnClick.wav"))
            pygame.mixer.Sound.set_volume(soundEffect,0.5)#0.5 is the volume
            pygame.mixer.Sound.play(soundEffect,0) #play the track
            
            try:
                #load a new button image
                self.image = pygame.image.load(imgName)
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(0,self.screen_height)
                #if the volume is on, it turns it off
                if not silent:
                    pygame.mixer.Sound.set_volume(soundTrack,0.0)#0.0 is the volume
                else: #else it turn it on
                    pygame.mixer.Sound.set_volume(soundTrack,0.5)#0.5 is the volume
                
            except Exception as e:
                #print the exception on the screen
                print('error: ', str(e))

        screen.blit(self.image, self.rect)
    
    #this function change the status of the volume button
    def changeStatusTo(self, screen, filepath, soundTrack, silent):
        #here it play the botton click sound to give a feedback to the user
        soundEffect = pygame.mixer.Sound(os.path.join(pathname, "btnClick.wav"))
        pygame.mixer.Sound.set_volume(soundEffect,0.5)#0.5 is the volume
        pygame.mixer.Sound.play(soundEffect,0) #play the track
            
        #load a new button image
        self.image = pygame.image.load(filepath)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0,self.screen_height)
        #if the volume is on, it turns it off
        if not silent:
            pygame.mixer.Sound.set_volume(soundTrack,0.0)#0.0 is the volume
        else: #else it turn it on
            pygame.mixer.Sound.set_volume(soundTrack,0.5)#0.5 is the volume
        
        #update the screen
        screen.blit(self.image, self.rect)
        

#this class manage the hay on the screen
class Hay(pygame.sprite.Sprite):
    #constructor
    def __init__(self, pos, filepath=os.path.join(pathname, 'sprites/hayl.png')):
        #initialize a new sprite
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        #load the sprite image
        self.image = pygame.image.load(filepath)
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.pos)
        #set the speed to -1, because the sprite moves from right to left
        self.speed = -1

    #this method update the sprite status
    def update(self,screen, time, width):
        #if the time is even, it moves the sprite from the right to the left
        if time%2 == 0:
            self.rect = self.rect.move([self.speed,0])
            if self.rect.center[0] <= 0: #if the sprite reaches the end of the screen it returns true
                return True
        #update screen
        screen.blit(self.image, self.rect)



#-------------------------
# FUNCTIONS
#-------------------------

#this function control if it is the case to quit the game
def controlExit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


#this function play the botton click sound
def bottonClick():
    soundEffect = pygame.mixer.Sound(os.path.join(pathname, "btnClick.wav"))
    pygame.mixer.Sound.set_volume(soundEffect,0.5)#0.5 is the volume
    pygame.mixer.Sound.play(soundEffect,0) #play the track


#this is the main function
def menu(screen, silent):
    #initialize background, title and hay objects
    background = Background(WINDOW_WIDTH, WINDOW_HEIGHT)
    title = Title(WINDOW_WIDTH//6 * 5, WINDOW_HEIGHT//6*5)
    hay = Hay((WINDOW_WIDTH,450))
    
    #initialize sound track
    soundTrack = pygame.mixer.Sound(os.path.join(pathname, "startMenu.wav"))
    if not silent: pygame.mixer.Sound.set_volume(soundTrack,0.5)#0.5 is the volume
    else: pygame.mixer.Sound.set_volume(soundTrack,0.0)#0.00 is the volume
    pygame.mixer.Sound.play(soundTrack,-1)#the -1 let the sound repeates when it ends
    

    #this dictionary cointains all of the buttons 
    buttonList = {}

    #initialize buttons
    btnPlay = Button(os.path.join(pathname, 'sprites/btnplay.png'), WINDOW_WIDTH, WINDOW_HEIGHT//4)
    btnExit = Button(os.path.join(pathname, 'sprites/btnexit.png'), WINDOW_WIDTH, btnPlay.getY() + 100)
    if not silent: 
        btnMode = Button(os.path.join(pathname, 'sprites/volume.png'), WINDOW_WIDTH, btnExit.getY() + 100)
    else:
        btnMode = Button(os.path.join(pathname, 'sprites/mute.png'), WINDOW_WIDTH, btnExit.getY() + 100)
    
    #append buttons to the button list
    buttonList[1] = btnPlay 
    buttonList[0] = btnExit
    buttonList[2] = btnMode
    
    #time count how many cicles the program perform
    time = 0
    #if this variable is true, the program ends
    endProgram = False
    
    #start end stop are true if the user say 'inizia' or 'esci'
    start = False
    stop = False

    while not endProgram and (start or stop == False):
        #updates elements on the screen
        background.update(screen)
        title.update(screen)
        if hay.update(screen, time, WINDOW_WIDTH):
            hay = Hay((WINDOW_WIDTH,450))  
        btnPlay.update(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
        btnExit.update(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
        btnMode.update(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        pos = (WINDOW_WIDTH, WINDOW_HEIGHT)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
            controlExit(event)

        if btnPlay.update(screen, pos[0],pos[1]):
            start = True
            endProgram = True
            bottonClick()
            userChoice = 1
        elif btnExit.update(screen, pos[0],pos[1]):
            stop = True
            endProgram = True
            bottonClick()
            userChoice = 0
        elif btnMode.update(screen, pos[0],pos[1]):
            if not silent:
                btnMode.changeStatusTo(screen, os.path.join(pathname,'sprites/mute.png'), soundTrack, silent)
                silent = True
            else:
                btnMode.changeStatusTo(screen, os.path.join(pathname,'sprites/volume.png'), soundTrack, silent)
                silent = False

        #update screen status
        pygame.display.update()
        time += 1 #increment time
                
    
    #stop the music
    pygame.mixer.Sound.stop(soundTrack)
    
    return userChoice, silent


#this run the menu if this file is used as stand-alone
if __name__ == "__main__":
    menu()
