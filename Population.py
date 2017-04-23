###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: An abstraction of our breeding population.                  ##
##               Effectively just a fancy collection of DNA.                 ##
###############################################################################

import DNA
import random

class Population:

    # Description:
    #   Create a population of DNA
    # Parameters:
    #   size (number): The number of 'strands' of DNA in this populace
    #   length (number): The length of each 'strand' of DNA
    #   rate (number): 0.0-1.0 rate at which a child mutates
    #   goal (Object/Score/Corpus/Collection/?): The goal item to base our fitness on
    def __init__(self, size, length, rate=0.01, goal=None):
        if size < 2:
            print "Size of population must be greater than 1"
            return
        if length < 1:
            print "Length of DNA must be greater than 0"
            return

        self.size = size
        self.length = length
        self.rate = rate
        self.goal = goal
        self.populace = []
        self.__totalFitness = 0 # The total fitness score of the population, for producing relative probabilities

        for i in range(0, size):
            newDNA = DNA.DNA(length)
            self.__totalFitness += newDNA.getFitness()
            self.populace.append(newDNA)

    # Description:
    #   Breed the next generation, return the best child
    def getGeneration(self):
        probabilities = []
        # Produce relative probabilities
        for dna in self.populace:
            probabilities.append(dna.getFitness() / self.__totalFitness)

        # Produce a new population via that whole spooky birds and bees stuff
        newPopulace = []
        newTotalFitness = 0
        fittestChild = None
        while len(newPopulace) < self.size:
            rand = random.random()
            cumulativeProbability = 0
            parent1 = None
            for index, value in enumerate(self.populace):
                cumulativeProbability += probabilities[index]
                if cumulativeProbability > rand:
                    parent1 = self.populace[index]
                    break

            rand = random.random()
            cumulativeProbability = 0
            parent2 = None
            for index, value in enumerate(self.populace):
                cumulativeProbability += probabilities[index]
                if cumulativeProbability > rand:
                    parent2 = self.populace[index]
                    break

            child = parent1.breed(parent2)
            rand = random.random()
            child.mutate(self.rate)
            newTotalFitness += child.getFitness()
            newPopulace.append(child)
            if fittestChild is None:
                fittestChild = child
            elif child.getFitness() > fittestChild.getFitness():
                fittestChild = child

        self.populace = newPopulace
        self.__totalFitness = newTotalFitness
        print "Fittest fitness: " + str(fittestChild.getFitness())
        return fittestChild

    # Description:
    #   Return the current group in the population
    def getPopulace(self):
        return self.populace
