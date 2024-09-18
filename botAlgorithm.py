
#botAlgorithm.py

import pygad
import pygad.gann
import pygad.nn
import numpy

###############################
####### Definitions ###########
###############################
#Neural Network Settings
hiddenLayers = [4, 4] #each cell denotes the number of neurons in each layer
numOutputs = 2
#Genetic Algorithm Settings
#initial_population = population_vectors.copy()
num_parents_mating = 4
num_generations = 500
mutation_percent_genes = 5
parent_selection_type = "sss"
crossover_type = "single_point"
mutation_type = "adaptive "
keep_parents = 1


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

    def calculateInstruction(self, inputs, solutionIndex):
        #solutionIndex = 0 #not sure what this means here
        instruction = pygad.nn.predict(
            last_layer = self.gannInstance.population_networks[solutionIndex],
            data_inputs = inputs
        )
        return instruction

