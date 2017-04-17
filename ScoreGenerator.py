###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: The "client-end" score generator                            ##
###############################################################################

class ScoreGenerator:

    # Description:
    #   Create a score generator. If a corpus is passed, use the for Score Delta heuristic.
    #   Otherwise, only use Good Music Heuristic.
    # Parameters:
    #   corpus ([music21 Score]) -  optional: The goal corpus
    def __init__(self, corpus=None):
        pass

    # Description:
    #   Generate a score of at least the given threshold.
    # Parameters:
    #   threshold (number): The goal corpus
    def generate(self, threshold):
        pass

    # Description:
    #   Return the history of the score. Ie. it is just the best score from each
    #   iteration of the genetic algorithm.
    #   NOTE: generate() must first be called before calling history()
    def history(self):
        pass
