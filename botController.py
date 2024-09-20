
#botController.py

import numpy as np
import botAlgorithm as ba


numInputs = 4 #must be consistent with what's returned by game and what model expects


class botController():
    def __init__(self, numBirds):
        self.numBirds = numBirds
        self.currentState = dict()
        self.botAlgorithm = ba.botAlgorithm(self.numBirds, numInputs)
        self.jumpInstructions = np.zeros(self.numBirds)
        self.params = np.empty([self.numBirds, numInputs])
        self.inputs = np.zeros((2, numInputs))

    def compileParams(self):
        self.params[:, 0] = self.currentState['pipeX']
        self.params[:, 1] = self.currentState['pipeY']
        self.params[:, 2] = self.currentState['birdY']
        self.params[:, 3] = self.currentState['birdVel']


    def getInstructions(self, gameState):
        self.currentState = gameState

        if self.currentState['gameOver'] == False:
            self.compileParams()
            #print('Game Parameters:\n', params)

            for inputIndex in range(self.numBirds): 
                if np.isnan(self.params[inputIndex, -1]) == False:
                    #dumb solutions to resolve single-dimension bug in nn.py:308
                    self.inputs[0, :] = self.params[inputIndex, :]
                    instruction = self.botAlgorithm.calculateInstruction(self.inputs, inputIndex)
                    self.jumpInstructions[inputIndex] = round(instruction[0].item())
                    #print('Jump Instructions:\n', jumpInstructions)
        
        return self.jumpInstructions


