#############
# imports
#############

import cv2
from cv2 import circle
import pygame
import random

from HandDetector import HandDetector

#############
## GLOBALS ##
#############

# Define the size of the game window
WIDTH = 1100
HEIGHT = 650
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("Best game")

#game stuff
FPS = 60

######################
## HELPER FUNCTIONS ##
######################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

###################
## MAIN FUNCTION ##
###################

def main():
    # make a hand detector
    handDetector = HandDetector()

    gameIsRunning  = True

    # circle vars
    circleX = 0
    circleY = 0
    circleZ = 0
    circleColor = (0,255,255)

    # keeps track of whether hand is open or closed
    handIsOpen = True

    # rectangle object
    aRect = pygame.Rect(300,300,200,100)
    rectColor = (255,0,255)

    # while the opencv window is running
    while (not handDetector.shouldClose) and gameIsRunning:
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        WINDOW.fill((42,42,42))
        
        pygame.draw.rect(WINDOW, rectColor, aRect)

        # if there is at least one hand seen, then
        # print out the landmark positions
        if len(handDetector.landmarkDictionary) > 0: 
            circleX = handDetector.landmarkDictionary[0][9][0]
            circleY = handDetector.landmarkDictionary[0][9][1]
            circleZ = abs(handDetector.landmarkDictionary[0][9][2])*5

            circleX = WIDTH - mapToNewRange(circleX, 0, 640, 0, WIDTH)
            circleY = mapToNewRange(circleY, 0, 480, 0, HEIGHT)
            

            # detects if hand is open or not
            if handDetector.landmarkDictionary[0][12][1] < handDetector.landmarkDictionary[0][9][1] :
                handIsOpen = True
                circleColor = (0,255,255)
            else:
                handIsOpen = False
                circleColor = (255,0,0)
       
            # check collision between rectangle and hand point
            if(aRect.collidepoint(circleX,circleY)):
                rectColor = (255,255,0)
                if not handIsOpen:
                    rectColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            else:
                rectColor = (255,0,255)

            #draw circle at point 9
            pygame.draw.circle(WINDOW, circleColor, (circleX,circleY), 25)

            print(handIsOpen)
        
 
        # for all the game events
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                gameIsRunning = False

        # put code here that should be run every frame of your game             
        pygame.display.update()

        
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()



