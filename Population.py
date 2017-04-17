###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: An abstraction of our breeding population.                  ##
##               Effectively just a fancy collection of DNA.                 ##
###############################################################################


class Population:

    # Description:
    #   Create a population of DNA
    # Parameters:
    #   size (number): The number of 'strands' of DNA in this populace
    #   length (number): The length of each 'strand' of DNA
    #   goal (Object/Score/Corpus/Collection/?): The goal item to base our fitness on
    def __init__(self, size, length, goal):
        pass

    # Description:
    #   Breed the next generation, give us the best child
    def getGeneration(self):
        pass

    # Description:
    #   Find the fitness of each of this population's DNA
    def getFitnesses(self):
        pass
