
#botController.py

import numpy as np


numInputs = 4 #must be consistent with what's returned by game and what model expects


class botController():
    def __init__(self, numBirds):
        self.numBirds = numBirds
        self.currentState = dict()
        self.currentBird = 0 #ToDo: Delete if not needed

    def compileInputs(self):
        inputs = np.empty([self.numBirds, numInputs])
        inputs[:, 0] = self.currentState['pipeX']
        inputs[:, 1] = self.currentState['pipeY']
        inputs[:, 2] = self.currentState['birdY']
        inputs[:, 3] = self.currentState['birdVel']

        return inputs


    def getInstructions(self, gameState):
        self.currentState = gameState

        if self.currentState['gameOver'] == False:
            inputs = self.compileInputs()


