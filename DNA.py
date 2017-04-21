###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: An abstraction of our genetic "DNA" for our scores.                        ##
###############################################################################

from music21 import *
import random


###########################################################################
#                              Utilities                                  #
###########################################################################

# Description:
#   Helper function to generate a score from arbitrary data
# Parameters:
#   data ([7bits]): An array of arbitrary 7 bits
def generateScore(data):
    # Iterate over every byte
    melody = stream.Part()
    harmony = stream.Part()
    i = 0
    while i < len(data):
        # Get the melodic note
        midi = data[i]              # Any MIDI note
        quarter = data[i + 1] / 4.0 # Up to a maxima
        # TODO: Reconsider rest logic, this feels very arbitrary
        if data[i + 2] > 100:
            thisRest = note.Rest(quarterLength=quarter)
            melody.append(thisRest)
        else:
            thisNote = note.Note(midi, quarterLength=quarter)
            melody.append(thisNote)

        # TODO: Do more than just triads?
        midi = [data[i + 3], data[i + 4], data[i + 5]]
        quarter = data[i + 6] / 4.0
        # TODO: Reconsider rest logic, this feels very arbitrary
        if data[i + 7] > 100:
            thisRest = note.Rest(quarterLength=quarter)
            harmony.append(thisRest)
        else:
            thisChord = chord.Chord(midi, quarterLength=quarter)
            harmony.append(thisChord)
        i = i + 8

    score = stream.Stream([melody, harmony])
    return score


###########################################################################
#                              DNA Class                                  #
###########################################################################

class DNA:
    # Description:
    #   Create a random strand of DNA
    # Parameters:
    #   length (number): The length of this 'strand' of DNA in number of notes
    #   heuristic (String): "good", "delta" or "both". Which heuristic to use, see ScoreAnalyzer.py
    def __init__(self, length, heuristic="good"):
        data = []
        # Eight 7-bits are needed per note (melody+harmony notes)
        for i in range(0, length * 8):
            data.append(random.randint(0, 127))

        self.random = data
        self.score = generateScore(data)
        self.fitness = 0 # ScoreAnalyzer.fitness(self.score, heuristic)

    # Description:
    #   Return this DNA's fitness, how "good" this DNA is. Darwin would be proud.
    def getFitness(self):
        return self.fitness

    # Description:
    #   I remember learning about this many years ago, but the theory and implementation seem vastly different.
    #   Crossover these strands of DNA to produce a child. Birds, bees, and all that jazz.
    # Parameters:
    #   partner (DNA): The other DNA to breed this DNA with
    def breed(self, partner):
        # Use the random midpoint method,
        # choose a random "midpoint" to pick the DNA from self and the rest from partner
        if len(self.random) != len(partner.random):
            raise ValueError("Attempted to breed DNA of differing lengths.")

        length = len(self.random)
        midpoint = random.randint(0, length)
        crossBred = []
        for i in range(0, length):
            if i < midpoint:
                crossBred.append(self.random[i])
            else:
                crossBred.append(partner.random[i])

        child = DNA(0)
        child.random = crossBred
        child.score = generateScore(crossBred)
        child.fitness = 0 # ScoreAnalyzer.fitness(self.score, heuristic)
        return child

    # Description:
    #   In order to ensure enough variation, allow subtle mutations
    # Parameters:
    #   rate (number): The probability by which this DNA will mutate
    def mutate(rate):
        for i in range(0, len(self.random)):
            if random.random() < rate:
                self.random = random.randint(0, 127)

    # Description:
    #   Return this DNA as a score
    def getScore(self):
        return self.score
