from config import *
from GraphicMain.classAndFunctions import *
import cv2
import numpy as np 


def calibrationTest():
    lowerBound=np.array([33,80,40])
    upperBound=np.array([102,255,255])

    #create a cam object to record live videos
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))
    ok = False
    while not ok:
        #read frame from the camera
        _, img=cam.read()
        #resize the image
        img = cv2.resize(img,(1000,600))
        #flip the image horizontally
        img = cv2.flip(img, 1)
        #calculate the counturs of the image
        conts = calculateCountours(img, lowerBound, upperBound, kernelClose, kernelOpen)
        #calculate the maximum blue rectangle found
        max_dim = calculateMaxDim(conts)
        cv2.rectangle(img, CALIBRATION_X, CALIBRATION_Y, WHITE, 2)
        cv2.rectangle(img, (max_dim[0], max_dim[2]), (max_dim[1],max_dim[3]), WHITE, 2)
        if max_dim[0] >= 300 and max_dim[1] <= 700:
            if max_dim[0] <= 350 and max_dim[1] >= 650:
                if max_dim[2] <= 250 and max_dim[3] >= 400:
                    if max_dim[2] >= 200 and max_dim[3] <= 450:
                        new_lower_bound = getAverageColor(img)
                        ok = True
        
        cv2.imshow('calibration', img)
        cv2.waitKey(10)
    
    cv2.destroyAllWindows()
    return lowerBound