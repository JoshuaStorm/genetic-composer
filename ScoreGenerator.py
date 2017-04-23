###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: The "client-end" score generator                            ##
###############################################################################

import Population

class ScoreGenerator:

    # Description:
    #   Create a score generator. If a corpus is passed, use the for Score Delta heuristic.
    #   Otherwise, only use Good Music Heuristic.
    # Parameters:
    #   length (number): The length of the score to be generated. Currently relates to "number of notes".
    #   corpus ([music21 Score]) -  optional: The goal corpus. Use "Score Delta Heuristic".
    def __init__(self, length, corpus=None):
        self.history = []
        # TODO: Do I just want to hardcore the population size?
        self.population = Population.Population(50, length, corpus)
        self.corpus = corpus

    # Description:
    #   Generate a score of at least the given threshold.
    # Parameters:
    #   threshold (number): The goal corpus
    def generate(self, threshold):
        greatestChild = self.population.getGeneration()
        while greatestChild.getFitness() < threshold:
            greatestChild = self.population.getGeneration()
        return greatestChild

    # Description:
    #   Return the history of the score. Ie. it is just the best score from each
    #   iteration of the genetic algorithm.
    #   NOTE: generate() must first be called before calling history()
    def history(self):
        pass
