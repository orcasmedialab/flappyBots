
#botAlgorithm.py

import pygad
import pygad.nn
import pygad.gann
import threading
import numpy as np

###############################
####### Definitions ###########
###############################
#Neural Network Settings
hiddenLayers = [4, 4] #each cell denotes the number of neurons in each layer
numOutputs = 2
#Genetic Algorithm Settings
numParentsMating = 4
numGenerations = 0 #default value. Make sure this matches numberIterations in gameControlly.py
mutationNumGenes = 1
parentSelectionType = "sss"
crossoverType = "single_point"
mutationType = "random"
keepParents = 1
suppressWarnings = True

lock = threading.Lock()


class botAlgorithm():
    def __init__(self, numBots, numInputs):
        self.numSolutions = numBots
        self.numInputs = numInputs
        self.numClasses = numOutputs

        self.gannInstance = pygad.gann.GANN(
            num_solutions = self.numSolutions,
            num_neurons_input = self.numInputs,
            num_neurons_hidden_layers = hiddenLayers,
            num_neurons_output = self.numClasses
        )

        self.populationVectors = pygad.gann.population_as_vectors(
            population_networks = self.gannInstance.population_networks
        )

        self.initialPopulation = self.populationVectors.copy()


    def getIntialPop(self):
        return self.initialPopulation
    
    def getPopNetwork(self):
        return self.gannInstance.population_networks
    
    def updateWeights(self, populationMatricies):
        self.gannInstance.update_population_trained_weights(
                population_trained_weights=populationMatricies)
    
    def calculateInstruction(self, inputs, solutionIndex):
        instruction = pygad.nn.predict(
            last_layer = self.gannInstance.population_networks[solutionIndex],
            data_inputs = inputs
        )
        return instruction
    

class geneticOptimizer(threading.Thread):
    def __init__(self, algoClass, numIters):
        super(geneticOptimizer, self).__init__()
        self.botAlgorithm = algoClass
        initialPopulation = self.botAlgorithm.getIntialPop()
        self.setNumGenerations(numIters)

        self.scores = np.zeros(len(initialPopulation))
        self.scoreReady = False
        self.gannUpdated = True
        self.populationMatricies = None
        self.iterationsCompleted = 0

        self.goInstance = pygad.GA(
            num_generations = self.numGenerations,
            initial_population = initialPopulation,
            num_parents_mating = numParentsMating,
            fitness_func = self.fitnessFunction,
            fitness_batch_size = len(initialPopulation),
            parent_selection_type = parentSelectionType,
            keep_parents = keepParents,
            crossover_type = crossoverType,
            mutation_type = mutationType,
            mutation_num_genes = mutationNumGenes,
            suppress_warnings = suppressWarnings,
            on_generation = self.callbackGeneration
        )

    def setNumGenerations(self, numIters):
        global numGenerations
        if numIters != None:
            numGenerations = numIters - 1
        self.numGenerations = numGenerations


    def fitnessFunction(self, goInstance, solution, solutionIndex):
        while True:
            lock.acquire()
            if self.scoreReady:
                #self.scoreReady = False #moved to callback function
                lock.release()
                #print('Score set: ', self.scores, sep = '')
                return self.scores[solutionIndex]
            lock.release()
            #print('Score: ', max(self.scores), 
            #        ',  Generation: ', (self.iterationsCompleted + 1),
            #        sep = '')
    
    def callbackGeneration(self, goInstance):
        self.generatePopMatricies()
        self.botAlgorithm.updateWeights(self.populationMatricies)
        self.gannUpdated = True
        self.scoreReady = False  #ToDo: resolve redundant calls of fitnessFunction()
        self.iterationsCompleted += 1
        #print('CALLBACK')
        return
    
    def setScore(self, newScore):
        self.scores = newScore
        self.scoreReady = True

    def getGenUpdateFlag(self):
        return self.gannUpdated
    
    def resetGenUpdateFlag(self):
        self.gannUpdated = False

    def generatePopMatricies(self):
        self.populationMatricies = pygad.gann.population_as_matrices(
                population_networks = self.botAlgorithm.getPopNetwork(),
                population_vectors = self.goInstance.population)

    def run(self):
        if self.numGenerations > 0:
            self.goInstance.run()
            print('End of Genetic Optimization')


