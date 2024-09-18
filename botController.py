
#botController.py

import numpy as np
import botAlgorithm as ba


numInputs = 4 #must be consistent with what's returned by game and what model expects


class botController():
    def __init__(self, numBirds):
        self.numBirds = numBirds
        self.currentState = dict()
        self.botAlgorithm = ba.botAlgorithm(self.numBirds, numInputs)

    def compileParams(self):
        params = np.empty([self.numBirds, numInputs])
        params[:, 0] = self.currentState['pipeX']
        params[:, 1] = self.currentState['pipeY']
        params[:, 2] = self.currentState['birdY']
        params[:, 3] = self.currentState['birdVel']

        return params


    def getInstructions(self, gameState):
        self.currentState = gameState
        jumpInstructions = np.zeros(self.numBirds) #Optimize numpy initializations

        if self.currentState['gameOver'] == False:
            inputs = np.zeros((2, numInputs)) #Optimize numpy initializations
            params = self.compileParams()
            #print('Game Parameters:\n', params)

            for inputIndex in range(params.shape[0]): 
                if np.isnan(params[inputIndex, -1]) == False:
                    #dumb solutions to resolve single-dimension bug in nn.py:308
                    inputs[0, :] = params[inputIndex, :]
                    instruction = self.botAlgorithm.calculateInstruction(inputs, inputIndex)
                    jumpInstructions[inputIndex] = round(instruction[0].item())
                    #print('Jump Instructions:\n', jumpInstructions)
        
        return jumpInstructions


