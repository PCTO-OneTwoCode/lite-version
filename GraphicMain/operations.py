'''
class and functions for the gameDesign file

Our github page: https://github.com/PCTO-OneTwoCode
'''

#################

# INCLUDE LIBRARIES

############

import random
import pygame
from pygame.locals import *

#this function generate a random moltiplication
def createMultiplication(l):
    l[1][0] = random.randint(1,10)
    l[1][1] = random.randint(1,10) 
    l[0] = l[1][0] * l[1][1]
    l[2] = "*" 
    return l


#this function generate a random division
def createDivision(l):
    l[0] = random.randint(1,10)
    l[1][1] = random.randint(1,10)
    l[1][0] = l[0] * l[1][1]
    l[2] = "/"
    return l


#this function generate a random addition
def createAddition(l):
    l[0] = random.randint(50,100)
    l[1][0] = random.randint(20,50)
    l[1][1] = l[0] - l[1][0]
    l[2] = "+"
    return l


#this function generate a random subtracion
def createSubtracion(l):
    l[0] = random.randint(0,40)
    l[1][0] = random.randint(40,100)
    l[1][1] = l[1][0] - l[0]
    l[2] = "-"
    return l
    

#this function generates a random operation, it can be a moltiplication, division, addittion or subtracion 
def createOperations():
    chose = random.randint(0,3)
    temp = [0,[0,0]," "]
    if chose == 0:
        return createMultiplication(temp)
    elif chose == 1:
        return createDivision(temp)   
    elif chose == 2:
        return createAddition(temp)
    return createSubtracion(temp)
          
    
#this function returns a string containing an operation with its solution
def createStringOperationWithSolution():
    operation = createOperations()
    return (f"{operation[1][0]} {operation[2]} {operation[1][1]} = {operation[0]}")  


#this function returns a string containing an operation without its solution
def createStringOperationWithoutSolution():
    operation = createOperations()
    return (f"{operation[1][0]} {operation[2]} {operation[1][1]} = ...")  

