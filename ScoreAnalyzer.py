###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: A score analyzer that uses one of two heuristics:           ##
##               The Good Music Heuristic or the Score Delta Heuristic       ##
##               It should be noted, these are truly heuristics.             ##
##               These are note necessarily rigorous/objective analyses.     ##
###############################################################################

from music21 import *

###########################################################################
#                              Utilities                                  #
###########################################################################


# TODO: Make these more sophisticated, right now just have boilerplate analyses

# Description:
#   Give this melody a 0.0-1.0 score based on its conjunct melodic motion.
#   NOTE: Currently just measures average chromatic jump
# Parameters:
#   melody (music21 Part): The melody to be analyzed
def analyzeMelodicMotion(melody):
    prevMidi = None
    totalDistance = 0.0
    totalNotes = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for note in melody:
        if note.isRest: continue
        totalNotes += 1.0
        thisMidi = note.pitch.midi
        if prevMidi is not None:
            totalDistance += abs(thisMidi - prevMidi)
        prevMidi = thisMidi
    return (100 - (totalDistance / totalNotes)) / 100.0

# Description:
#   Give this harmony a 0.0-1.0 score based on its harmonic consonance.
#   NOTE: Currently just returns a relative measure of prevalence of consonant intervals.
#   TODO: At least do some special handling to find consonnant 4ths
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
def analyzeHarmonicConsonance(harmony):
    # Award 1 point for in same octave.
    # Award 1 point for perfect consonance
    # Award 0.5 point for imperfect consonance
    cumulativeScore = 0.0
    totalChords = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for chord in harmony:
        if chord.isRest: continue
        totalChords += 1
        note1 = chord[0]
        for note2 in chord:
            if note1 is note2: continue
            thisInterval = interval.notesToInterval(note1, note2).simpleName
            # Perfect consonances: 5th, 4th, unison/octave
            if thisInterval[0] == "P":
                cumulativeScore += 1
            # Imperfect consonances: M6, m6, M3, m3
            elif thisInterval[1] == "6" or thisInterval == "3":
                cumulativeScore += 0.5
            # If they're within the same octave
            if abs(note1.pitch.midi - note2.pitch.midi) < 12:
                cumulativeScore += 1
    return cumulativeScore / (4 * totalChords)

# Description:
#   Give this harmony a 0.0-1.0 score based on its harmonic consistency.
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
# TODO: This entire function, even being hacky with it is harder than the other ones
def analyzeHarmonicConsistency(harmony):
    return 0.5

# Map the number of notes used to a score, somewhat arbitrary based solely on the
# line in Dmitri's book "Tonal music tends to use relatively small macroharmonies, often involving five to eight notes."
MACRO_SCORES = [0.0, 0.1, 0.15, 0.25, 0.5, 0.65, 0.8, 1.0, 0.8, 0.65, 0.5, 0.25, 0.15 ]
# Description:
#   Give this harmony a 0.0-1.0 score based on its macroharmonic makeup
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeMacroharmony(melody, harmony):
    notesUsed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for note in melody:
        if note.isRest: continue
        index = note.pitch.midi % 12
        notesUsed[index] = 1
    for chord in harmony:
        if chord.isRest: continue
        for note in chord:
            index = note.pitch.midi % 12
            notesUsed[index] = 1

    numberNotesUsed = 0
    for value in notesUsed:
        numberNotesUsed += value

    return MACRO_SCORES[numberNotesUsed]

# Description:
#   Give this harmony a 0.0-1.0 score based on its centricity
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeCentricity(melody, harmony):
    notesUsed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalNotes = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for note in melody:
        if note.isRest: continue
        index = note.pitch.midi % 12
        notesUsed[index] += 1.0
        totalNotes += 1.0
    # TODO: Base it off the chord, not the notes of the chord?
    for chord in harmony:
        if chord.isRest: continue
        for note in chord:
            index = note.pitch.midi % 12
            notesUsed[index] += 1.0
            totalNotes += 1.0
    # Convert to relative frequencies
    maxFreq = 0.0
    secondFreq = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for value in notesUsed:
        freq = value / totalNotes
        if freq > maxFreq:
            maxFreq = freq
        elif freq > secondFreq:
            secondFreq = freq

    # TODO: Something more intelligent. Currently just saying "more root == more better!"
    return (maxFreq / secondFreq - 1)


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
