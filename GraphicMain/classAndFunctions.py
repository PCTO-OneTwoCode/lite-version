'''
class and functions for the gameDesign file

Our github page: https://github.com/PCTO-OneTwoCode
'''

#################

# INCLUDE LIBRARIES

############

import pygame, sys
import random
import os
import cv2
import numpy as np
from time import sleep
from pygame.locals import *
from GraphicMain.operations import *
from config import *

#path of this python file
pathname = os.path.dirname(os.path.realpath(__file__))

#pygame initialization
pygame.init()

#white rgb code
WHITE = (255,255,255)

#blue rgb code
BLUE = (0,0,255)

#this list contains the 4 answers position on the screen
POSSIBLE_POSITIONS = [(WINDOW_WIDTH/4-200, WINDOW_HEIGHT/4),
                        (WINDOW_WIDTH/4-200, WINDOW_HEIGHT/4*3),
                        (WINDOW_WIDTH/4*3-200, WINDOW_HEIGHT/4),
                        (WINDOW_WIDTH/4*3-200, WINDOW_HEIGHT/4*3)]

'''------------------------------
CLASSES
-------------------------------'''

#a simple text is a text without borders
class SimpleText():
    def __init__(self, x, y, text, txtFont='freesansbold.ttf', size = 150, color = WHITE):
        self.x = x
        self.y = x
        #set the text font and size
        self.font = pygame.font.SysFont(txtFont, size)
        #render the text in a choose color
        self.img = self.font.render(text, True, color)
    
    #update the text status on the screen
    def update(self, screen):
        screen.blit(self.img, (self.x,self.y))


#we made a botton using an image with some particulare methods
class Button():
    #constructor
    def __init__(self, filepath, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width

        try:
            #load the image
            self.image = pygame.image.load(filepath)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(screen_width, self.screen_height)
        except Exception as e:
            #print the error on the screen
            print('error: ', str(e))

    #update the button status
    def collide(self,x,y):
        #controls if the user press the button
        if self.rect.collidepoint(x, y):
            return True
        else: return False        
        
    #update the botton status on the screen
    def update(self, screen):
        screen.blit(self.image, self.rect)


#a complex text is similar to the simple text, the difference is that this one as borders
class ComplexText():
    def __init__(self, x, y, text, txtFont='freesansbold.ttf', size=150, color=WHITE, thickness=10):
        self.x = x
        self.y = y
        self.color = color
        self.thickness = thickness
        self.text = text

        self.font = pygame.font.SysFont(txtFont, size)
        self.img = self.font.render(text, True, color)
        self.rect = self.img.get_rect()
    
    #return the text
    def getText(self):
        return self.text
        
    #update the text status on the screen
    def update(self,screen):
        screen.blit(self.img, (self.x,self.y))
        pygame.draw.rect(self.img, self.color, self.rect, self.thickness)
    
    #this function change the text color
    def changeColor(self,color):
        self.color = color


#a textBox is a complex object composed by a complex text and an invisible botton
#we use the button because the complex text is uncliccable so we need the button to make textbox easy
#to interate with mouse
class TextBox():
    #constructor
    def __init__(self,  x, y, text, txtFont='freesansbold.ttf', size=150, color=WHITE, thickness=10):
        self.x = x
        self.y = y
        self.txtFont = txtFont
        self.size = size
        self.thickness = thickness
        
        self.backBotton = Button(os.path.join(pathname, 'backBotton.png'), x, y)
        self.text = ComplexText( x, y, text, txtFont, size, color, thickness)

    #update the textbox status on the screen
    def update(self, screen):
        #the following line in commented because the button has to be invisible
        # self.backBotton.update()
        self.text.update(screen)

    #this function return true if the text and the given string (result) are equal
    def isCorrect(self, result): 
        if self.text.getText() == result:
            return True
        else: return False
    
    #return the textbox text
    def getText(self):
        return self.text.getText()
    
    #this functions return the textbox positions
    def getCordX(self):
        return self.x
    def getCordY(self):
        return self.y
    
    #this function change the text color
    def changeColor(self,color):
        self.text.changeColor(color)
    
    #this function control if the given coordinates are in the same
    #screen quarter of the texbox coordinates
    def collide(self, x, y):
        if self.x <= WINDOW_WIDTH/2:
            if self.y <= WINDOW_HEIGHT/2: textQuarter = 4
            else: textQuarter = 3
        else:
            if self.y <= WINDOW_HEIGHT/2: textQuarter = 1
            else: textQuarter = 2
        
        if x <= WINDOW_WIDTH/2:
            if y <= WINDOW_HEIGHT/2: pointerQuarter = 4
            else: pointerQuarter = 3
        else:
            if y <= WINDOW_HEIGHT/2: pointerQuarter = 1
            else: pointerQuarter = 2

        if textQuarter == pointerQuarter:
            return True
        else:
            return False


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
    def update(self, screen):
        screen.blit(self.fullScreenImage, self.rect)


#This class contains the background method
class Counter():
    #constructor
    def __init__(self, x, y, filepath):
        try:
            #load the image
            self.image = pygame.image.load(filepath)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x,y)
            
        except Exception as e:
            #print the exception on the screen
            print('error: ', str(e))

    #update the background status
    def update(self, screen):
        screen.blit(self.image, self.rect)


'''------------------------------
FUNCTIONS
-------------------------------'''


#this function return a textBox with a math question in a semi-random position and its result
def initQuestion():
    x, y = random.choice(POSSIBLE_POSITIONS)
    text = createStringOperationWithSolution()
    question = TextBox(x, y, text[:-2], size=115)
    return question, text[-2:]
        

#this function return a list of 4 textbox that contain 4 possible answer to the question
#only one of them is correct
def initAnswers(result):
    answers = []
    random_value = random.randint(0,3)
    x,y = POSSIBLE_POSITIONS[random_value] 
    answers.append(TextBox(x+175, y, result, size=150))
    for i in range(4):
        if i == random_value:
            continue
        x, y = POSSIBLE_POSITIONS[i]
        text = createStringOperationWithSolution()
        answers.append(TextBox(x+175, y, text[-2:], size=150))
    
    return answers


#this function control if the event given is to quit the game
def controlExit(event):
    if event.type == pygame.QUIT:
        quit()
        sys.exit()


#this function riproduce a given jingle
def riproduceJingle(path):
    jingle = pygame.mixer.Sound(path)
    pygame.mixer.Sound.set_volume(jingle, 1)
    pygame.mixer.Sound.play(jingle)


#this function finds the bigger rectangle in a given rectangle array
#we use this to reduce the noise in opencv color detection
def calculateMaxDim(conts):
    max_dim = [0, 0, 0, 0]
    for element in conts:
        x,y,w,h=cv2.boundingRect(element)
        if x + w > max_dim[1]:
            max_dim[0] = x
            max_dim[1] = x + w
            max_dim[2] = y
            max_dim[3] = y + h
    return max_dim


#this function returns a list of positions. this positions are the blue element
#in a given picture. the lower and upper bound given as arguments are the range of 
#color we wanna detect 
def calculateCountours(img, lowerBound, upperBound, kernelClose, kernelOpen):
    #convert BGR to HSV
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal = maskClose
    conts,_ = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    return conts


#this function control if a given event is a key pressed. If it is, it returns true
def backToMain(event):
    if event.type == pygame.KEYDOWN:
        return True
    return False

#this function returns the average color value of the image center
def getAverageColor(img, size_percentage=30):
    # Get image size
    height, width, _ = img.shape

    # Calculate center coordinate
    centerX = (width // 2 )
    centerY = (height // 2)

    # Calculate RightBorder 
    XRB = centerX + ((width * size_percentage) // 200)                    
    # Calculate LeftBorder
    XLB = centerX - ((width * size_percentage) // 200)
    # Calculate TopBorder
    YTB = centerY + ((height * size_percentage) // 200)
    # Calculate BottomBorder
    YBB = centerY - ((height * size_percentage) // 200)

    bgr_list = []

    # Creation of a list of BGR values for every pixel
    for x in range(XLB,XRB):
        for y in range(YBB,YTB):
            bgr_list.append(img[y,x]) # Append the BGR value to the list

    # Convert bgr_list in a numpy array
    numpy_bgr_array = np.array(bgr_list)
    # Calculate the average value of blue, green and red
    average_value = np.average(numpy_bgr_array,axis=0)

    # Convert the type of datas
    average_value = average_value.astype(int)

    # Map values in uint8 format type
    average_value = np.uint8([[[average_value[0],average_value[1],average_value[2]]]]) 
    
    return average_value

def main():
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    question, result = initQuestion()
    
    dom = True
    exitGame = False

    while not exitGame:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            controlExit(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                x, y = event.pos
                if question.collide(x,y) and dom:
                    answerBoxes = initAnswers(result)
                    dom = False
        if dom:
            question.update(screen)
        else:
            for el in answerBoxes:
                el.update(screen)
        pygame.display.update()



if __name__ == '__main__':
    main()
