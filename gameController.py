
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
flapCooldown = 30


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

    def randJumpGenerator(self):
        jumpIS = np.random.choice([False, True], size = (numBirds,), 
                p = [(flapCooldown-1) / flapCooldown, 1./flapCooldown])
        return jumpIS


    def step(self):
        if realTime:
            self.clock.tick(fps)

        self.birdWorld.update(self.birdGroup)
        jumpIS = self.randJumpGenerator()
        self.birdGroup.update(jumpIS)
        self.gameplay.update()



