
#gameController.py

import pygame
from pygame.locals import *
import gameResources as gr
import numpy as np
import sys
import time


###############################
####### Definitions ###########
###############################
#Gametime Run Settings
framerate = 60 #fps
resetTime = 5 #sec
numberIterations = 1 #if zero, run indefinitely
guiEnabled = True
collisionsEnabled = True
realTime = True
#bird stuff
numBirds = 100
flapProbability = 30 # p=1/30, flap with probability p each time called


class gameController():
    def __init__(self):
        #initiate all game resources
        pygame.init()
        self.clock = pygame.time.Clock()
        #init environment
        self.screenWidth = gr.screenWidth
        self.groundHeight = gr.groundHeight
        self.birdWorld = gr.environment(guiEnabled)
        self.birdGroup = gr.birdGroup(numBirds)
        #init gameplay
        self.gameplay = gr.gameplay(self.birdGroup, self.birdWorld, collisionsEnabled)
        self.completeRuns = 0 #number of runs executed
        self.reinitializeCounter()

    def reinitializeCounter(self):
        self.resetCounter = 0
        print('  Iteration #', (self.completeRuns + 1), sep='')


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
        #stores "None"s if bird is dead
        gameState['birdY'] = self.birdGroup.getBirdHeights()
        gameState['birdVel'] = self.birdGroup.getBirdVelocities()
        
        return gameState


    #returns a boolean array with each value having a 1/flapProbability of being True
    def randJumpGenerator(self):
        jumpInstructionSet = np.random.choice([False, True], size = (numBirds,), 
                p = [(flapProbability-1) / flapProbability, 1./flapProbability])
        return jumpInstructionSet


    def step(self, jumpInstructionSet):
        if realTime:
            self.clock.tick(framerate)

        self.birdWorld.update(self.birdGroup)
        self.birdGroup.update(jumpInstructionSet)
        self.gameplay.update()

        if self.isGameOver():
            self.completeRuns += 1
            if realTime and (self.resetCounter < (framerate * resetTime)):
                self.resetCounter += 1
            else:
                if (numberIterations == 0) or (self.completeRuns < numberIterations):
                    self.resetGame()
                else:
                    time.sleep(resetTime)
                    sys.exit()



