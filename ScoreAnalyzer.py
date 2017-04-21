###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: A score analyzer that uses one of two heuristics:           ##
##               The Good Music Heuristic or the Score Delta Heuristic       ##
##               It should be noted, these are truly heuristics.             ##
##               These are note necessarily rigorous/objective analyses.     ##
###############################################################################


###########################################################################
#                              Utilities                                  #
# TODO: Make these more sophisticated                                     #
###########################################################################

# Description:
#   Give this melody a 0.0-1.0 score based on its conjunct melodic motion.
# Parameters:
#   melody (music21 Part): The melody to be analyzed
def analyzeMelodicMotion(melody):
    pass

# Description:
#   Give this harmony a 0.0-1.0 score based on its harmonic consonance.
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
def analyzeHarmonicConsonance(harmony):
    pass

# Description:
#   Give this harmony a 0.0-1.0 score based on its harmonic consistency.
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
def analyzeHarmonicConsistency(harmony):
    pass

# Description:
#   Give this harmony a 0.0-1.0 score based on its macroharmonic makeup
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeMacroharmony(melody, harmony):
    pass

# Description:
#   Give this harmony a 0.0-1.0 score based on its centricity
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeCentricity(melody, harmony):
    pass



###########################################################################
#                         Score Analyzer Class                            #
###########################################################################

class ScoreAnalyzer:

    # Description:
    #   Create a score analyzer of the input score
    # Parameters:
    #   score (music21 Score): The score to be analyzed. Assumed to have melody and harmony music21 Parts
    def __init__(self, score):
        self.melody = score.getElementById('melody')
        self.harmony = score.getElementById('harmony')

    # Description:
    #   Analyze the score with the Good Music Heuristic, return a 0.00-1.00 score
    # Special thanks:
    #   Special thanks to Dmitri Tymoczko's "Geometry of Music" for giving me inspiration for this heuristic
    def getGoodMusicAnalysis(self):
        motion = analyzeMelodicMotion(self.melody)
        consonance = analyzeHarmonicConsonance(self.harmony)
        consistency = analyzeHarmonicConsistency(self.harmony)
        macroharmony = analyzeMacroharmony(self.melody, self.harmony)
        centricity = analyzeCentricity(self.melody, self.harmony)
        return (motion + consonance + consistency + macroharmony + centricity) / 5.0

    # Description:
    #   Analyze the score with the Score Delta Heuristic, return a 0.00-1.00 score
    # Parameters:
    #   corpus ([music21 Score]): Collection of scores to compare for analysis
    def getDeltaAnalysis(self, corpus):
        pass
