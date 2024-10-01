
#yamlManager.py

import yaml
import numpy as np
from pathlib import Path
from time import gmtime, strftime


###############################
####### Definitions ###########
###############################
#Config import settings

#Logging exportsettings
loggingDir = 'solutions'
filenamePrefix = 'solutionSet'
separator = '_'
yamlExtension = '.yaml'


class botLogger():
    def __init__(self, networkStructure, numSolutions, runTime):
        #Note: May want to import more than just network structure
        self.network = networkStructure 
        self.runTime = runTime
        self.numSolutions = numSolutions
        self.solutionSet = dict()

        self.currentGen = 0
        
        self.createLoggingDir()
        self.createFilename()


    def createLoggingDir(self):
        self.loggingPath = './' + loggingDir
        Path(self.loggingPath).mkdir(parents = True, exist_ok = True)

    def createFilename(self):
        self.filename = filenamePrefix + separator + str(self.runTime['filename'])
        self.filenameWithExt = self.filename + yamlExtension
        self.relativeFilename = self.loggingPath + '/' + self.filenameWithExt

    def solutionCompiler(self, popMat):
        genText = 'Gen ' + str(self.currentGen)
        solutionDict = dict()
        for solution in range(self.numSolutions):
            solText = 'Solution ' + str(solution)
            if isinstance(popMat[solution][0], np.ndarray):
                solutionDict[solText] = np.concatenate(
                    [arr.flatten() for arr in popMat[solution]]
                ).tolist()
            else:
                solutionDict[solText] = popMat[solution].tolist()
            #print(solutionDict[solText], '\n')

        self.solutionSet[genText] = solutionDict
        self.currentGen += 1


    def saveGeneration(self, populationMat, scores):
        self.solutionCompiler(populationMat)

        with open(self.relativeFilename, 'w') as outfile:
            yaml.dump(
                self.solutionSet, 
                outfile, 
                default_flow_style = False
            )



