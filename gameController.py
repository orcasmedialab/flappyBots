
#gameController.py

import pygame
from pygame.locals import *
import gameResources as gr
import numpy as np


###############################
####### Definitions ###########
###############################
#Gametime Run Settings
fps = 60
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

    def resetGame(self):
        print('call all reset functions')

    #returns a boolean array with each value having a 1/flapProbability of being True
    def randJumpGenerator(self):
        jumpInstructionSet = np.random.choice([False, True], size = (numBirds,), 
                p = [(flapProbability-1) / flapProbability, 1./flapProbability])
        return jumpInstructionSet


    def step(self, jumpInstructionSet):
        if realTime:
            self.clock.tick(fps)

        self.birdWorld.update(self.birdGroup)
        self.birdGroup.update(jumpInstructionSet)
        self.gameplay.update()



