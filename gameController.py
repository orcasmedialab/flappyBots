
#gameController.py

import pygame
from pygame.locals import *
import numpy as np
import sys
import time

import gameResources as gr
from gameResources import maxScore


###############################
####### Definitions ###########
###############################
#Gametime Run Settings
framerate = 60 #fps
resetTime = 2 #sec
numberIterations = 1 #if zero, run indefinitely
maxScoreLimit = 3 #Stop program after hitting max score this many times
scoreLimitConsecutive = True #Must hit max score consecutively to exit
guiEnabled = True
collisionsEnabled = True
realTime = False
useBirdProgress = True #use distance traversed for score
#bird stuff
numBirds = 100
flapProbability = 30 # p=1/30, flap with probability p each time called


class gameController():
    def __init__(self, args):
        #initiate all game resources
        pygame.init()
        self.clock = pygame.time.Clock()
        self.updateGlobals(args)
        #init environment
        self.screenWidth = gr.screenWidth
        self.groundHeight = gr.groundHeight
        self.birdWorld = gr.environment(guiEnabled)
        self.birdGroup = gr.birdGroup(numBirds)
        #init gameplay
        self.gameplay = gr.gameplay(self.birdGroup, self.birdWorld, collisionsEnabled)
        self.completeRuns = 0 #number of runs executed
        self.maxScoreCounter = 0
        self.reinitializeCounter()

    def reinitializeCounter(self):
        self.resetCounter = 0
        print('  Iteration #', (self.completeRuns + 1), sep='')

    #Updates globals with command line arguments
    #Bad practice. Potentially change in future
    def updateGlobals(self, args):
        globals().update( (k,v) for k,v in args.items() if v is not None)

    
    def getNumBirds(self):
        global numBirds
        return numBirds

    def resetGame(self):
        self.reinitializeCounter()
        self.birdWorld.reset(self.birdGroup)
        self.gameplay.reset()

    def isGameOver(self):
        return self.gameplay.isGameOver()

    def gameStateCompiler(self):
        gameState = dict()
        #pipeX and pipeY refer to the coordinates of the top-right corner of upcoming bottom pipe
        #if no pipes exist, values are both assigned to -1
        pipeCorner = self.birdWorld.getPipeLocation()
        gameState['pipeX'] = pipeCorner[0]
        gameState['pipeY'] = pipeCorner[1]
        #birdY is a list of of "bird heights" in reference to the bottom of the bird sprite
        #birdVel is a list of all vertical velocities
        #Each stores "None" if bird is dead
        gameState['birdY'] = self.birdGroup.getBirdHeights()
        gameState['birdVel'] = self.birdGroup.getBirdVelocities()
        # State of game (i.e. gameover) and current or final score for all birds
        gameState['gameOver'] = self.isGameOver()
        gameState['score'] = self.gameplay.getScore(useBirdProgress)
        
        return gameState


    #returns a boolean array with each value having a 1/flapProbability of being True
    def randJumpGenerator(self):
        jumpInstructionSet = np.random.choice([False, True], size = (numBirds,), 
                p = [(flapProbability-1) / flapProbability, 1./flapProbability])
        return jumpInstructionSet

    def falseAfterSleep(self):
        time.sleep(resetTime)
        return False


    def step(self, jumpInstructionSet):
        if realTime:
            self.clock.tick(framerate)

        self.birdWorld.update(self.birdGroup)
        self.birdGroup.update(jumpInstructionSet)
        self.gameplay.update()

        if self.isGameOver():
            if self.resetCounter < (framerate * resetTime):
                self.resetCounter += 1
            else:
                self.completeRuns += 1
                if max(self.gameplay.getScore(False)) >= maxScore:
                    self.maxScoreCounter += 1
                elif scoreLimitConsecutive:
                    self.maxScoreCounter = 0
                
                if (maxScoreLimit != None) and (self.maxScoreCounter >= maxScoreLimit):
                    print('Max Score Limit reached.\nSolution cannot be improved further.')
                    return self.falseAfterSleep()
                elif (numberIterations == 0) or (self.completeRuns < numberIterations):
                    self.resetGame()
                else:
                    print('Program complete.')
                    return self.falseAfterSleep()
        
        return True



