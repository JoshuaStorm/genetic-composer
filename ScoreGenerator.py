###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: The "client-end" score generator                            ##
###############################################################################

import Population

import cProfile

# For runtime profiling, can safely ignore
def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='time')
    return profiled_func

class ScoreGenerator:


    # Base the melody score on the its cohesion with the harmony


    # Description:
    #   Create a score generator. If a corpus is passed, use the for Score Delta heuristic.
    #   Otherwise, only use Good Music Heuristic.
    # Parameters:
    #   size (number): The size of the population to generate off of.
    #   length (number): The length of the score to be generated. Currently relates to "number of notes".
    #   rate (number): The mutation rate. (See DNA.py, mutate())
    #   corpus ([music21 Score]) -  optional: The goal corpus. Use "Score Delta Heuristic".
    def __init__(self, size, length, rate=0.01, modifiers=[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0], corpus=None):
        if len(modifiers) != 9:
            print "Modifiers must be exactly 9 elements long."
            return

        self.history = []
        # TODO: Do I just want to hardcore the population size?
        self.population = Population.Population(size, length, rate, modifiers, corpus)
        self.corpus = corpus
        self.modifiers = modifiers

    # Description:
    #   Generate a score of at least the given threshold.
    # Parameters:
    #   threshold (number): The goal corpus
    #   deterministic (boolean): Whether or not to use the Detereministic or probabilistic generation methods.
    #                            Generally, determistic is faster but more likely to plateau.
    @do_cprofile
    def generate(self, threshold, deterministic=False):
        greatestChild = self.population.getGeneration(self.modifiers, deterministic)
        while greatestChild.getFitness(self.modifiers) < threshold:
            greatestChild = self.population.getGeneration(self.modifiers, deterministic)
        return greatestChild

    # Description:
    #   Return the history of the score. Ie. it is just the best score from each
    #   iteration of the genetic algorithm.
    #   NOTE: generate() must first be called before calling history()
    def history(self):
        pass
