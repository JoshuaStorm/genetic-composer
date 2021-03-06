###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: An abstraction of our genetic "DNA" for our scores.         ##
###############################################################################

from music21 import *
import random
import ScoreAnalyzer

###########################################################################
#                              Utilities                                  #
###########################################################################

# Description:
#   Helper function to generate a score from arbitrary data
# Parameters:
#   data ([7bits]): An array of arbitrary 7 bits
def generateScore(data):
    melody = stream.Part()
    melody.id = "melody"
    harmony = stream.Part()
    harmony.id = "harmony"

    i = 0
    while i < len(data):
        # Get the melodic note
        midi = data[i]                    # Any MIDI note
        quarter = (data[i + 1] % 16 + 1) / 4.0
        # TODO: *************STANDIN***************
        # quarter = 1
        # END: *************STANDIN***************
        # TODO: Reconsider rest logic, this feels very arbitrary
        if data[i + 2] > 115:
            thisRest = note.Rest(quarterLength=quarter)
            melody.append(thisRest)
        else:
            # STANDIN, forcing octave
            thisNote = note.Note((midi % 12) + 60, quarterLength=quarter)
            thisNote = note.Note(midi, quarterLength=quarter)
            # END: *************STANDIN***************
            melody.append(thisNote)

        # TODO: Do more than just triads?
        # TODO: STANDIN, forcing octave
        # midi = [data[i + 3] % 12 + 48, data[i + 4] % 12 + 48, data[i + 5] % 12 + 48]

        midi = [data[i + 3], data[i + 4], data[i + 5]]


        # END: *************STANDIN***************
        quarter = (data[i + 1] % 16 + 1) / 4.0
        # *************STANDIN***************
        # quarter = 1 # *************STANDIN***************
        # *************STANDIN***************
        # TODO: Reconsider rest logic, this feels very arbitrary
        if data[i + 7] > 115:
            thisRest = note.Rest(quarterLength=quarter)
            harmony.append(thisRest)
        else:
            thisChord = chord.Chord(midi, quarterLength=quarter)
            harmony.append(thisChord)
        i += 8

    score = stream.Stream([melody, harmony])
    return score

# Description:
#   Helper function to generate a score from arbitrary data.
#   Using this instead of Music21 to speedup generation (>x20 speedup)
# Parameters:
#   data ([7bits]): An array of arbitrary 7 bits
# DataScore Format:
#   { harmony: [[chordNotes], quarterLength] ; melody: [note, quarterLength] }
#   chordArray = [(midi, midi, midi, quarterLength)]
#   noteArray = [(midi, quarterLength)]
#   midi may be -1 to indicate a rest
def generateDataScore(data):
    melody = []
    harmony = []

    i = 0
    while i < len(data):
        # Get melody note
        midi = data[i]
        # midi = data[i] % 12 + 60
        quarter = (data[i + 1] % 16 + 1) / 4.0
        # quarter = 2

        # TODO: Reconsider rest logic, this feels very arbitrary
        if data[i + 2] > 115:
            melody.append((-1, quarter))
        else:
            melody.append((midi, quarter))

        # TODO: Do more than just triads?
        midi = [data[i + 3], data[i + 4], data[i + 5]]
        # midi = [data[i + 3] % 12 + 48, data[i + 4] % 12 + 48, data[i + 5] % 12 + 48]
        quarter = (data[i + 6] % 16 + 1) / 4.0
        # quarter = 2

        # TODO: Reconsider rest logic, this feels very arbitrary
        if data[i + 7] > 115:
            harmony.append((-1, quarter))
        else:
            harmony.append((midi, quarter))
        i += 8
    dataScore = {"melody": melody, "harmony": harmony}
    return dataScore



###########################################################################
#                              DNA Class                                  #
###########################################################################

class DNA:
    # Description:
    #   Create a random strand of DNA
    # Parameters:
    #   length (number): The length of this 'strand' of DNA in number of notes
    def __init__(self, length):
        data = []
        # Eight 7-bits are needed per note (melody+harmony notes)
        for i in range(0, length * 8):
            data.append(random.randint(0, 127))

        self.data = data
        self.dataScore = generateDataScore(self.data) # An inbetween the arbitrary data stream and the Music21 score stream
        self.score = None

        analyzer = ScoreAnalyzer.ScoreAnalyzer(self.dataScore)
        self.fitness = analyzer.getAnalysisScore()

    # Description:
    #   Return this DNA's fitness, how "good" this DNA is. Darwin would be proud.
    # Parameters:
    #   modifiers ([Number]): An array of numbers corresponding to which characteristics to emphasize.
    #                         In the order of: Motion, consonance, consistency, macroharmony,
    #                         centricity, cohesion, note length, octave, and common notes between chords.
    def getFitness(self, modifiers):
        i = 0
        sum = 0.0
        modSum = 0.0
        while i < len(self.fitness):
            sum += self.fitness[i] * modifiers[i]
            modSum += modifiers[i]
            i += 1
        return (sum / modSum)

    def getFitnessArray(self):
        return self.fitness

    # Description:
    #   I remember learning about this many years ago, but the theory and implementation seem vastly different.
    #   Crossover these strands of DNA to produce a child. Birds, bees, and all that jazz.
    # Parameters:
    #   partner (DNA): The other DNA to breed this DNA with
    def breed(self, partner):
        if len(self.data) != len(partner.data):
            raise ValueError("Attempted to breed DNA of differing lengths.")

        # Use the random midpoint method,
        # choose a random "midpoint" to pick the DNA from self and the rest from partner
        length = len(self.data)
        midpoint = random.randint(0, length)

        crossBred = []
        for i in range(0, length):
            if i < midpoint:
                crossBred.append(self.data[i])
            else:
                crossBred.append(partner.data[i])

        child = DNA(0)
        child.data = crossBred
        child.dataScore = generateDataScore(child.data)
        child.score = None
        analyzer = ScoreAnalyzer.ScoreAnalyzer(child.dataScore)
        child.fitness = analyzer.getAnalysisScore()
        return child

    # Description:
    #   In order to ensure enough variation, allow subtle mutations
    # Parameters:
    #   rate (number): The probability by which this DNA will mutate
    def mutate(self, rate):
        changed = False
        # Intended to speed up generation, only iterate through mutation if an initial threshold is passed
        if random.random() > (rate * 5):
            return

        for i in range(0, len(self.data)):
            if random.random() < rate:
                changed = True
                self.data[i] = random.randint(0, 127)
        if changed:
            self.dataScore = generateDataScore(self.data)

    # Description:
    #   Return this DNA as a score
    def getScore(self):
        if self.score is None:
            self.score = generateScore(self.data)
        return self.score
