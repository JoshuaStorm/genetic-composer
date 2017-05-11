###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: The "client-end" score generator                            ##
###############################################################################

import Population

class ScoreGenerator:


    # Base the melody score on the its cohesion with the harmony



    # Description:
    #   Create a score generator. If a corpus is passed, use the for Score Delta heuristic.
    #   Otherwise, only use Good Music Heuristic.
    # Parameters:
    #   size (number): The size of the population to generate off of.
    #   length (number): The length of the score to be generated. Currently relates to "number of notes".
    #   corpus ([music21 Score]) -  optional: The goal corpus. Use "Score Delta Heuristic".
    def __init__(self, size, length, corpus=None):
        self.history = []
        # TODO: Do I just want to hardcore the population size?
        self.population = Population.Population(size, length, corpus)
        self.corpus = corpus

    # Description:
    #   Generate a score of at least the given threshold.
    # Parameters:
    #   threshold (number): The goal corpus
    def generate(self, threshold, deterministic=False):
        greatestChild = self.population.getGeneration(deterministic)
        while greatestChild.getFitness() < threshold:
            greatestChild = self.population.getGeneration(deterministic)
        return greatestChild

    # Description:
    #   Return the history of the score. Ie. it is just the best score from each
    #   iteration of the genetic algorithm.
    #   NOTE: generate() must first be called before calling history()
    def history(self):
        pass
