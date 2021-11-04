'''
class and functions for the gameDesign file

Our github page: https://github.com/PCTO-OneTwoCode
'''

#################

# INCLUDE LIBRARIES

############
import pygame
import numpy as np
import datetime
import sys
import cv2
import importlib
from time import sleep
from pygame.locals import *
from GraphicMain.operations import *
from GraphicMain.classAndFunctions import *
import os

#this variable contains the absolute path of this python file
pathname = os.path.dirname(os.path.realpath(__file__))


###################################

# FUNCTIONS

##################################

#this function controls if the precedent blue object position is enough distant from the corrent one
def controlCord(answer, prec_answer):
    if prec_answer.getCordY() - answer.getCordY() <= 200 and prec_answer.getCordX() - answer.getCordX() <= 200:
       return True
    else: return False


#this function replaces a cowboy sprite with a tombstone
def finalShoot(all_sprites, spr_ToChange):
    tombstone = pygame.sprite.Sprite(all_sprites)
    #load the sprite image
    tombstone.image = pygame.image.load(os.path.join(pathname ,"Sprites/tombstone.png")).convert_alpha()
    tombstone.rect = spr_ToChange.image.get_rect()
    #set the tombstone x and y coordinates
    tombstone.rect.x = spr_ToChange.rect.x 
    tombstone.rect.y = spr_ToChange.rect.y + (DIMCOW[1]-DIMTOMB[1])
    #remove the dead cowboy sprite
    spr_ToChange.kill()
    return all_sprites


#prints a group of sprite on the screen
def print_group(group,screen):
    for sprite in group:
        screen.blit(sprite.image, (sprite.rect.x,sprite.rect.y))
    pygame.display.update()
        

#this function is called at the end of the game
#the loser cowboy is killed by the winner 
def final_animation( screen, surf_title, winRed, all_sprites,spr_red, spr_blue,numberSpriters):

    #turn the red cowboy to right
    spr_redReverse = pygame.sprite.Sprite(all_sprites)
    spr_redReverse.image = pygame.image.load(os.path.join(pathname, "Sprites/redCowBoyInverted.png")).convert_alpha()
    spr_redReverse.rect = spr_red.image.get_rect()
    spr_redReverse.rect.x = spr_red.rect.x 
    spr_redReverse.rect.y = spr_red.rect.y
    #remove the not inverted cowboy  
    spr_red.kill()


    #turn the blue cowboy to left
    spr_blueReverse = pygame.sprite.Sprite(all_sprites)
    spr_blueReverse.image = pygame.image.load(os.path.join(pathname, "Sprites/blueCowBoy.png")).convert_alpha()
    spr_blueReverse.rect = spr_blue.image.get_rect()
    spr_blueReverse.rect.x = spr_blue.rect.x 
    spr_blueReverse.rect.y = spr_blue.rect.y 
    #remove the not inverted cowboy
    spr_blue.kill()

    #update elements on the screen
    surf_title.update(screen)
    all_sprites.draw(screen)
    numberSpriters.draw(screen)
    print_group(all_sprites,screen)

    #wait for 1 second
    sleep(1)

    #generate the GO signal, after it is printed one cowboy shoot the other one
    number = pygame.sprite.Sprite(numberSpriters)
    number.image = pygame.image.load(os.path.join(pathname, "Sprites/counter"+str(5)+".png")).convert_alpha()
    number.image = pygame.transform.scale(number.image , (100,100))
    number.rect = number.image.get_rect()
    number.rect.x =WINDOW_WIDTH /2-(100/2)
    number.rect.y =10


    #update another time the screen 
    surf_title.update(screen)
    all_sprites.draw(screen)
    numberSpriters.draw(screen)

    #sleep another second (this create suspance)
    sleep(1)

    #one cowboy shoot, so the user hear a fire sound
    fire = pygame.mixer.Sound(os.path.join(pathname, "theme/fire.wav"))#upload the gun sound
    pygame.mixer.Sound.set_volume(fire,1)
    pygame.mixer.Sound.play(fire)
    
    #if the red wins, the blue is killed
    if winRed:
        all_sprites = finalShoot(all_sprites, spr_blueReverse)
        winLabel = SimpleText(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 'YOU WIN!\npress a key')
    else:
        #on the contrary it replace red with a tombstone
        all_sprites = finalShoot(all_sprites, spr_redReverse)
        winLabel = SimpleText(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 'YOU LOSE :(\n press a key')

    #the screen is update another time
    winLabel.update(screen)
    surf_title.update(screen)
    all_sprites.draw(screen)
    numberSpriters.draw(screen)
    print_group(all_sprites,screen)

    return



def mainGraphic(screen, silent, lowerBound):
    

    #these are the color range detected by our opencv algorithm
    upperBound=np.array([102,255,255])

    #create a cam object to record live videos
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))
   
    #pygame initialization 
    pygame.init()
    
    #song
    soundTrack = pygame.mixer.Sound(os.path.join(pathname, "theme/fight.wav"))
    pygame.mixer.Sound.set_volume(soundTrack,0.4)#0.6 is volume
    if not silent: pygame.mixer.Sound.play(soundTrack,-1)#with -1 sound will restart forever

    #sprite creation

    #here it creates two group of sprites
    all_sprites = pygame.sprite.Group()
    numberSpriters=pygame.sprite.Group()

    #red cowboy
    spr_red = pygame.sprite.Sprite(all_sprites)
    spr_red.image = pygame.image.load(os.path.join(pathname, "Sprites/redCowBoyYou.png")).convert_alpha()

    spr_red.rect = spr_red.image.get_rect()

    #set position
    spr_red.rect.x = WINDOW_WIDTH/2-DIMCOW[0] 
    spr_red.rect.y = WINDOW_HEIGHT-DIMCOW[1]

    

    #blue cowboy
    spr_blue = pygame.sprite.Sprite(all_sprites)
    spr_blue.image = pygame.image.load(os.path.join(pathname, "Sprites/blueCowBoyInverted.png")).convert_alpha()
    spr_blue.rect = spr_red.image.get_rect()

    #set position
    spr_blue.rect.x = WINDOW_WIDTH / 2 
    spr_blue.rect.y = WINDOW_HEIGHT-DIMCOW[1]
    
    
    #background 
    surf_title = Background(WINDOW_WIDTH, WINDOW_HEIGHT, os.path.join(pathname, 'Background/sfondo.jpg'))  
   
    #this count the number of answered questions
    count=1
    
    #this variable manage the finite state diagram that control game events
    gameStatus = 0

    #if move is true, the cowboys move
    move = False
    #if selected_question is true, the user has to select an anwer
    selected_question = False
    #if answered is true, the algorithm generate a new question for the user
    answered = False
    #this variable let us cronometer the answer time
    timer = False
    #if winred is equal to 1, the red cowboy wins
    winRed = 1

    #if the user answer 4 question, the cicle end 
    while count > 0 and count < 5:
        #draw these two group of sprites
        surf_title.update(screen)
        all_sprites.draw(screen)
        numberSpriters.draw(screen)
        
        #finite state diagram

        if gameStatus == 0:
            question, result = initQuestion()
            question.update(screen)
            gameStatus = 1
        elif gameStatus == 1:
            question.update(screen)
            answers = initAnswers(result)
            gameStatus = 2
        elif gameStatus == 2:
            question.update(screen)
            if selected_question:
                gameStatus = 3
                selected_question = False
        elif gameStatus == 3:
            for answer in answers:
                answer.update(screen)
            if answered:
                gameStatus = 0
                count += 1
                move = True
                answered = False
                selected_question = False
        

        #read frame from the camera
        _, img=cam.read()
        #resize the image
        img = cv2.resize(img,(WINDOW_WIDTH,WINDOW_HEIGHT))
        #flip the image horizontally
        img = cv2.flip(img, 1)
        #calculate the counturs of the image
        conts = calculateCountours(img, lowerBound, upperBound, kernelClose, kernelOpen)
        #calculate the maximum blue rectangle found
        max_dim = calculateMaxDim(conts)


        #if the rectangle width isn't bigger than 400px, the algorithm doesn't run
        if max_dim[1] >= 400:

            #this calculate the center of the rectangle
            center_x = max_dim[0] + ((max_dim[1] - max_dim[0]) / 2)
            center_y = max_dim[2] + ((max_dim[3] - max_dim[2]) / 2) 

            #if the user select a question the timer start
            if question.collide(center_x,center_y) and not selected_question:
                if not timer:
                    timer = True
                    start_time = datetime.datetime.now()
                elif datetime.datetime.now() >= start_time + datetime.timedelta(seconds=5):
                    #when the timer end selected_question is true, so the user has to select the answer
                    selected_question = True
                    timer = False
                    firstAnswer = True
            
            #if the user has to answer the timer start
            if not answered and selected_question:
                if not timer:
                    start_time = datetime.datetime.now()
                    timer = True
                else:
                    #for each answer it controls if the user has selected it
                    for answer in answers:
                        #if it is the first answer after choosing a question, it set prec_answer as answer 
                        if firstAnswer:
                            prec_answer = answer
                            firstAnswer = False
                        #if the answer collide with the user, the selected answer change color and become yellow
                        if answer.collide(center_x,center_y) and not answered and controlCord(answer, prec_answer):
                            prec_answer = answer
                            answer.changeColor((255,255,0))
                            pygame.display.update()
                        else:
                            answer.changeColor((255,255,255))
                        
                        #if the 5 second timer ends, the jingle is riproduced. The jingle is positive if the answer
                        #is correct, or negative if the answer is wrong
                        if datetime.datetime.now() >= start_time + datetime.timedelta(seconds=5) and not answered:
                            if answer.isCorrect(result) and answer.collide(center_x,center_y):
                                answered = True
                                riproduceJingle(os.path.join(pathname, 'theme/correctAnswer.wav'))
                            else:
                                riproduceJingle(os.path.join(pathname, 'theme/wrongAnswer.wav'))
                                winRed = 0
                                #if the answer is wrong the count is set to 5, so the while loop ends
                                count = 5
                                
                            timer = False
                            firstAnswer = True
                            selected_question = False
                        #end if
                    #end for
                #end if
            #end if                    
                
            #draw on the pygame screen the user position
            rect = pygame.Rect(center_x - (WINDOW_WIDTH//6), center_y - (WINDOW_HEIGHT//4), center_x + (WINDOW_WIDTH//6), center_y + (WINDOW_HEIGHT//4))
            pygame.draw.rect(screen, BLUE, rect, 3) 
            cv2.rectangle(img, (max_dim[0], max_dim[2]), (max_dim[1], max_dim[3]), 10)
            cv2.imshow('opencv', img)
            
            cv2.waitKey(10)
        
        #end if


        pygame.display.flip()
        for event in pygame.event.get():
            controlExit(event)

        #move cowboys 
        if move:
            spr_blue.rect.x += int(WINDOW_WIDTH/20)#
            spr_red.rect.x -= int(WINDOW_WIDTH/20)#
            move = False
        
        #increment number counter sprite
        number = pygame.sprite.Sprite(numberSpriters)
        number.image = pygame.image.load(os.path.join(pathname, "Sprites/counter"+str(count)+".png")).convert_alpha()
        number.image = pygame.transform.scale(number.image , (100,100))
        number.rect = number.image.get_rect()
        number.rect.x = WINDOW_WIDTH /2-(100/2)
        number.rect.y =10
            
    #end while loop       

    #turns the cowboys
    final_animation(screen,surf_title,winRed,all_sprites,spr_red,spr_blue,numberSpriters)

    #stop the music
    pygame.mixer.music.stop()#stop music
    pygame.mixer.Sound.stop(soundTrack)

    #while the user doesn't press a key, the program doesn't end
    endGame = False
    while not endGame:
        for event in pygame.event.get():
            controlExit(event)
            if backToMain(event): 
                endGame = True

    return 0
#end mainGraphic