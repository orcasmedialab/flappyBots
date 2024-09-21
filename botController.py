
#botController.py

import numpy as np
import botAlgorithm as ba
from botAlgorithm import lock


numInputs = 4 #must be consistent with what's returned by game and what model expects


class botController():
    def __init__(self, numBirds, numIters):
        self.numBirds = numBirds
        self.currentState = dict()
        self.jumpInstructions = np.zeros(self.numBirds)
        self.params = np.empty([self.numBirds, numInputs])
        self.inputs = np.zeros((2, numInputs))
        self.scoreUploaded = False

        self.botAlgorithm = ba.botAlgorithm(self.numBirds, numInputs)
        self.geneticOptimizer = self.startGaThread(numIters)


    def startGaThread(self, numIters):
        geneticOptimizer = ba.geneticOptimizer(self.botAlgorithm, numIters)
        geneticOptimizer.start()
        return geneticOptimizer
    
    def joinGaThread(self):
        self.geneticOptimizer.join()


    def compileParams(self):
        self.params[:, 0] = self.currentState['pipeX']
        self.params[:, 1] = self.currentState['pipeY']
        self.params[:, 2] = self.currentState['birdY']
        self.params[:, 3] = self.currentState['birdVel']


    def getInstructions(self, gameState):
        self.currentState = gameState

        if self.currentState['gameOver'] == False:
            self.scoreUploaded = False
            self.compileParams()
            #print('Game Parameters:\n', self.params)

            while True:
                lock.acquire()
                if self.geneticOptimizer.getGenUpdateFlag() == True:
                    for inputIndex in range(self.numBirds): 
                        if np.isnan(self.params[inputIndex, -1]) == False:
                            #dumb solutions to resolve single-dimension bug in nn.py:308
                            self.inputs[0, :] = self.params[inputIndex, :]
                            instruction = self.botAlgorithm.calculateInstruction(self.inputs, inputIndex)
                            self.jumpInstructions[inputIndex] = round(instruction[0].item())
                            #print('Jump Instructions:\n', self.jumpInstructions)
                    lock.release()
                    break
                lock.release()

        else:
            if self.scoreUploaded == False:
                self.geneticOptimizer.setScore(self.currentState['score'])
                self.scoreUploaded = True
                self.geneticOptimizer.resetGenUpdateFlag()
            
        
        return self.jumpInstructions


