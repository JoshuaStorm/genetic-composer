###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: A score analyzer that uses one of two heuristics:           ##
##               The Good Music Heuristic or the Score Delta Heuristic       ##
##               It should be noted, these are truly heuristics.             ##
##               These are note necessarily rigorous/objective analyses.     ##
###############################################################################


class ScoreAnalyzer:

    # Description:
    #   Create a score analyzer of the input score
    # Parameters:
    #   score (music21 Score): The score to be analyzed
    def __init__(self, score):
        pass

    # Description:
    #   Analyze the score with the Good Music Heuristic, return a 0.00-1.00 score
    # Special thanks:
    #   Special thanks to Dmitri Tymoczko's "Geometry of Music" for giving me inspiration for this heuristic
    def getGoodMusicAnalysis(self):
        pass

    # Description:
    #   Analyze the score with the Score Delta Heuristic, return a 0.00-1.00 score
    # Parameters:
    #   corpus ([music21 Score]): Collection of scores to compare for analysis
    def getDeltaAnalysis(self, corpus):
        pass
