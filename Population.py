###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: An abstraction of our breeding population.                  ##
##               Effectively just a fancy collection of DNA.                 ##
###############################################################################

import DNA
import random
import math

class Population:

    # Description:
    #   Create a population of DNA
    # Parameters:
    #   size (number): The number of 'strands' of DNA in this populace
    #   length (number): The length of each 'strand' of DNA
    #   rate (number): 0.0-1.0 rate at which a child mutates
    #   goal (Object/Score/Corpus/Collection/?): The goal item to base our fitness on
    def __init__(self, size, length, rate=0.01, modifiers=[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0], goal=None):
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
            self.__totalFitness += newDNA.getFitness(modifiers)
            self.populace.append(newDNA)

    # Description:
    #   Breed the next generation, return the best child
    # Parameters:
    #   deterministic (boolean) - optional: Whether to use the deterministic or probabilistic selection method
    #                                       Detereministic will require a larger population pool but may go faster.
    #   modifiers ([Number]): An array of numbers corresponding to which characteristics to emphasize.
    #                         In the order of: Motion, consonance, consistency, macroharmony,
    #                         centricity, cohesion, note length, octave, and common notes between chords.
    def getGeneration(self, modifiers, deterministic=False):
        if deterministic:
            return self.__getDeterministic(modifiers)
        else:
            return self.__getProbabilistic(modifiers)

    def __getDeterministic(self, modifiers):
        self.populace = sorted(self.populace, key=lambda dna: dna.getFitness(modifiers), reverse=True)
        newPopulace = []
        fittestChild = None
        newTotalFitness = 0
        i = 0
        while len(newPopulace) < self.size:
            # Breed this person with up to sqrt(size) lesser beings
            for j in range(0, int(math.sqrt(self.size - len(newPopulace)))):
                if len(newPopulace) >= self.size: break
                parent1 = self.populace[i]
                parent2 = self.populace[i + j]
                child = parent1.breed(parent2)
                child.mutate(self.rate)

                newTotalFitness += child.getFitness(modifiers)
                newPopulace.append(child)

                if fittestChild is None:
                    fittestChild = child
                elif child.getFitness(modifiers) > fittestChild.getFitness(modifiers):
                    fittestChild = child
            i += 1

        self.populace = newPopulace
        self.__totalFitness = newTotalFitness
        fitnessArray = fittestChild.getFitnessArray()
        print "---------------------------------------------"
        print "Cumulative: " + str(fittestChild.getFitness(modifiers))
        print "    Motion:       " + str(fitnessArray[0])
        print "    Consonance:   " + str(fitnessArray[1])
        print "    Consistency:  " + str(fitnessArray[2])
        print "    Macroharmony: " + str(fitnessArray[3])
        print "    Centricity:   " + str(fitnessArray[4])
        print "    Cohesion:     " + str(fitnessArray[5])
        print "    Note Length:  " + str(fitnessArray[6])
        print "    Octave:       " + str(fitnessArray[7])
        print "    Common Notes: " + str(fitnessArray[8])

        return fittestChild

    def __getProbabilistic(self, modifiers):
        probabilities = []
        # Produce relative probabilities
        for dna in self.populace:
            probabilities.append(dna.getFitness(modifiers) / self.__totalFitness)

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
                if cumulativeProbability >= rand:
                    parent1 = self.populace[index]
                    break

            rand = random.random()
            cumulativeProbability = 0
            parent2 = None
            for index, value in enumerate(self.populace):
                cumulativeProbability += probabilities[index]
                if cumulativeProbability >= rand:
                    parent2 = self.populace[index]
                    break

            child = parent1.breed(parent2)
            rand = random.random()
            child.mutate(self.rate)
            newTotalFitness += child.getFitness(modifiers)
            newPopulace.append(child)
            if fittestChild is None:
                fittestChild = child
            elif child.getFitness(modifiers) > fittestChild.getFitness(modifiers):
                fittestChild = child

        self.populace = newPopulace
        self.__totalFitness = newTotalFitness
        fitnessArray = fittestChild.getFitnessArray()
        print "---------------------------------------------"
        print "Cumulative: " + str(fittestChild.getFitness(modifiers))
        print "    Motion:       " + str(fitnessArray[0])
        print "    Consonance:   " + str(fitnessArray[1])
        print "    Consistency:  " + str(fitnessArray[2])
        print "    Macroharmony: " + str(fitnessArray[3])
        print "    Centricity:   " + str(fitnessArray[4])
        print "    Cohesion:     " + str(fitnessArray[5])
        print "    Note Length:  " + str(fitnessArray[6])
        print "    Octave:       " + str(fitnessArray[7])
        print "    Common Notes: " + str(fitnessArray[8])

        return fittestChild

    # Description:
    #   Return the current group in the population
    def getPopulace(self):
        return self.populace

# NOTE: Only exists for runtime analysis
def main():
    #  50, 20, 0.01 ->  0m37.947s real
    #  50, 40, 0.01 ->  1m10.397s real
    # 100, 20, 0.01 ->  1m10.164s real
    # 100, 40, 0.01 ->  2m17.146s real
    # 200, 20, 0.01 ->  2m20.199s real
    # 200, 40, 0.01 ->  4m35.943s real
    # 400, 80, 0.01 -> 18m53.981s real
    pop = Population(300, 60, rate=0.01)
    dna = pop.getGeneration()
    dna.getScore().show()

# main()
