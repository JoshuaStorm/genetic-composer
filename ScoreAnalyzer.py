###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: A score analyzer that uses one of two heuristics:           ##
##               The Good Music Heuristic or the Score Delta Heuristic       ##
##               It should be noted, these are truly heuristics.             ##
##               These are note necessarily rigorous/objective analyses.     ##
##               NOTE: Due to speed constraints, this ScoreAnalyzer analyzes ##
##               a score as it appears as an arbitrary data stream, not a    ##
##               Music21 score as one may suspect                            ##
###############################################################################

from music21 import *
import numpy
import sys


###########################################################################
#                              Utilities                                  #
###########################################################################


# TODO: Make these more sophisticated, right now just have boilerplate analyses

# Description:
#   Give this melody a 0.0-1.0 score based on the average motion of the melody
#   NOTE: Currently just measures average chromatic jump
# Parameters:
#   melody (music21 Part): The melody to be analyzed
def analyzeMelodicMotion(melody):
    prevMidi = None
    totalDistance = 0.0
    totalNotes = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for note in melody:
        if note[0] == -1: continue
        totalNotes += 1.0
        thisMidi = note[0]
        if prevMidi is not None:
            totalDistance += abs(thisMidi - prevMidi)
        prevMidi = thisMidi
    # 58 is chosen to avoid negative values, in most cases.
    return 1 - (totalDistance / (58 * totalNotes))


# Map intervals to scores:
#   unison/octave, augmented unison/minor 2nd, major 2nd, minor 3rd, major 3rd, perfect 4th, augmented 4th, perfect 5th, minor 6th, major 6th, minor 7th, major 7th
#   These are relatively arbitrary, with preference toward consonance.
INTERVAL_SCORES = [0.5, 0.25, 0.25, 1, 0.75, 0.5, 0.25, 1, 0.5, 0.5, 0.75, 0.75]


# Improvement: analyz chord as a unit, consider voicing

# Description:
#   Give this harmony a 0.0-1.0 score based on its harmonic consonance.
#   NOTE: Currently just returns a relative measure of prevalence of consonant intervals.
#   TODO: At least do some special handling to find consonnant 4ths
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
def analyzeHarmonicConsonance(harmony):
    # Award 1 point for perfect consonance
    # Award 0.5 point for imperfect consonance
    cumulativeScore = 0.0
    totalIntervals = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for chord in harmony:
        if chord[0] == -1: continue
        note1 = chord[0][0]
        for note2 in chord[0]:
            if note1 is note2: continue
            totalIntervals += 1
            thisInterval = abs(note1 - note2) % 12
            cumulativeScore += INTERVAL_SCORES[thisInterval]

    return cumulativeScore / totalIntervals

# Description:
#   Give this harmony a 0.0-1.0 score based on its harmonic consistency.
#   Currently just gives a better score for fewer structures
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
# TODO: This entire function, even being hacky with it is harder than the other ones
def analyzeHarmonicConsistency(harmony):
    structures = [[0 for i in range(12)] for j in range(12)]
    totalStructures = 0.01

    # Find the structures
    for chord in harmony:
        if chord[0] == -1: continue
        interval1 = abs(chord[0][0] - chord[0][1]) % 12
        interval2 = abs(chord[0][0] - chord[0][2]) % 12
        if interval1 > interval2:
            structures[interval1][interval2] += 1.0
        else:
            structures[interval2][interval1] += 1.0
        totalStructures += 1

    # Find the most common structures
    mostCommon = [0.0, 0.0, 0.0, 0.0, 0.0]

    for structure in structures:
        thisMax = max(structure)

        if thisMax >= mostCommon[0]:
            mostCommon[4] = mostCommon[3]
            mostCommon[3] = mostCommon[2]
            mostCommon[2] = mostCommon[1]
            mostCommon[1] = mostCommon[0]
            mostCommon[0] = thisMax
        elif thisMax >= mostCommon[1]:
            mostCommon[4] = mostCommon[3]
            mostCommon[3] = mostCommon[2]
            mostCommon[2] = mostCommon[1]
            mostCommon[1] = thisMax
        elif thisMax >= mostCommon[2]:
            mostCommon[4] = mostCommon[3]
            mostCommon[3] = mostCommon[2]
            mostCommon[2] = thisMax
        elif thisMax >= mostCommon[3]:
            mostCommon[4] = mostCommon[3]
            mostCommon[3] = thisMax
        elif thisMax >= mostCommon[4]:
            mostCommon[4] = thisMax

    # Score better for up to the top three most common structures being more common
    return (mostCommon[0] + mostCommon[1] + mostCommon[2]) / totalStructures

# Map the number of notes used to a score, somewhat arbitrary based solely on the
# line in Dmitri's book "Tonal music tends to use relatively small macroharmonies, often involving five to eight notes."
MACRO_SCORES = [0.0, 0.1, 0.15, 0.25, 0.5, 0.65, 0.8, 1.0, 0.8, 0.65, 0.5, 0.25, 0.0 ]
# Description:
#   Give this harmony a 0.0-1.0 score based on its macroharmonic makeup
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeMacroharmony(melody, harmony):
    notesUsed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for note in melody:
        if note[0] == -1: continue
        index = note[0] % 12
        notesUsed[index] += 1
    for chord in harmony:
        if chord[0] == -1: continue
        for note in chord[0]:
            index = note % 12
            notesUsed[index] += 1


    avg = numpy.mean(notesUsed)
    std = numpy.std(notesUsed)

    # If a note is used fewer than two StdDevs below the mean, treat it like None
    # Are used, but add a slight negative modifier
    # NOTE: This is my attempt to make this score less discrete
    twoStdDevs = avg - 2 * std
    oneStdDev = avg - std
    i = 0
    mod = 1
    while i < len(notesUsed):
        if notesUsed[i] < twoStdDevs:
            notesUsed[i] = 0
            mod -= 0.05
        elif notesUsed[i] < oneStdDev:
            notesUsed[i] = 0
            mod -= 0.10
        i += 1

    numberNotesUsed = 0
    for value in notesUsed:
        if value > 0: numberNotesUsed += 1

    return MACRO_SCORES[numberNotesUsed] * mod

# Description:
#   Give this melody and harmony a 0.0-1.0 score based on its centricity
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeCentricity(melody, harmony):
    notesUsed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalNotes = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for note in melody:
        if note[0] == -1: continue
        index = note[0] % 12
        notesUsed[index] += 1.0
        totalNotes += 1.0
    # TODO: Base it off the chord, not the notes of the chord?
    for chord in harmony:
        if chord[0] == -1: continue
        for note in chord[0]:
            index = note % 12
            notesUsed[index] += 1.0
            totalNotes += 1.0
    # Convert to relative frequencies
    maxFreq = 0.1
    secondFreq = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    for value in notesUsed:
        freq = value / totalNotes
        if freq > maxFreq:
            maxFreq = freq
        elif freq > secondFreq:
            secondFreq = freq

    # TODO: Something more intelligent. Currently just saying "more root == more better!"
    return 1 - (secondFreq / maxFreq)



COHESION_SCORES = [1, 0.25, 0.25, 0.75, 0.75, 0.5, 0.25, 1, 0.5, 0.5, 0.75, 1]

# Description:
#   Give this harmony a 0.0-1.0 score based on its cohesion. Ie. how well the harmony and melody go together
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
# TODO: Actually based analyze of position in score, not just assuming nextChord occurs at same time as nextNote
def analyzeCohesion(melody, harmony):
    cumulativeScore = 0.0
    totalIntervals = 0.1 # Set this to 0.1 to avoid incredibly improbable error due to division by zero TODO: More elegant fix?
    quarterLength = 0

    i = 0
    j = 0
    while i < len(melody) and j < len(harmony):
        melodyNote = melody[i][0]
        chordNotes = harmony[j][0]

        # Rest
        if chordNotes == -1:
            j += 1
            continue
        if melodyNote == -1:
            i += 1
            continue

        for note in chordNotes:
            interval = abs(melodyNote - note) % 12
            cumulativeScore += COHESION_SCORES[interval]
            totalIntervals += 1
        i += 1
        # If the melody has progressed beyond the chord, iterate chord
        if quarterLength >= harmony[j][1]:
            j += 1

    return cumulativeScore / totalIntervals

# Description:
#   Give this harmony a 0.0-1.0 score based on the consistency of note length
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeNoteLength(melody, harmony):
    durations = {}
    totalDurations = 0.01

    for note in melody:
        if note[1] not in durations:
            durations[note[1]] = 1
        else:
            durations[note[1]] += 1
        totalDurations += 1.0
    for chord in harmony:
        if chord[1] not in durations:
            durations[chord[1]] = 1
        else:
            durations[chord[1]] += 1
        totalDurations += 1.0

    max = 0.0
    secondMax = 0.0
    for key in durations:
        if durations[key] >= max:
            secondMax = max
            max = durations[key]
        elif durations[key] > secondMax:
            secondMax = durations[key]

    return (max / totalDurations) + (secondMax / totalDurations)


# Description:
#   Give this harmony a 0.0-1.0 score based on consistency of octave.
# Parameters:
#   melody (music21 Part): The melody to be analyzed
#   harmony (music21 Part): The harmony to be analyzed
def analyzeOctave(melody, harmony):
    octaveSums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalNotes = 0.01
    for note in melody:
        if note == -1: continue
        octave = note[0] / 12
        octaveSums[octave] += 1
        totalNotes += 1

    mostCommonMelodyOctave = 0
    for octave in octaveSums:
        proportion = octave / totalNotes
        if proportion > mostCommonMelodyOctave:
            mostCommonMelodyOctave = proportion

    octaveSums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalNotes = 0.01
    for chord in harmony:
        if chord[0] == -1: continue
        for note in chord[0]:
            octave = note / 12
            octaveSums[octave] += 1
            totalNotes += 1

    mostCommonHarmonyOctave = 0
    for octave in octaveSums:
        proportion = octave / totalNotes
        if proportion > mostCommonHarmonyOctave:
            mostCommonHarmonyOctave = proportion

    return (mostCommonMelodyOctave + mostCommonHarmonyOctave) / 2.0


# Description:
#   Give this harmony a 0.0-1.0 score based on common notes between chords.
#   This will hopefully increase the conistency of chord progressions
# Parameters:
#   harmony (music21 Part): The harmony to be analyzed
def analyzeCommonNotes(harmony):
    totalChords = 0.01
    score = 0
    # Award points for notes being the same between two chords
    i = 0
    while (i + 1) < len(harmony):
        chord1 = harmony[i]
        chord2 = harmony[i + 1]
        # Check for rests
        if chord1[0] == -1 or chord2[0] == -1:
            i += 1
            continue

        untuple1 = [chord1[0][0], chord1[0][1], chord1[0][2]]
        untuple1.sort()
        untuple2 = [chord2[0][0], chord2[0][1], chord2[0][2]]
        untuple2.sort()

        if (untuple1[0] % 12) == (untuple2[0] % 12):
            score += 1
        if (untuple1[1] % 12) == (untuple2[1] % 12):
            score += 1
        if (untuple1[2] % 12) == (untuple2[2] % 12):
            score += 1

        i += 1
        totalChords += 1

    return score / (totalChords * 3)


###########################################################################
#                         Score Analyzer Class                            #
###########################################################################

class ScoreAnalyzer:

    # Description:
    #   Create a score analyzer of the input score
    # Parameters:
    #   score (dataScore, see DNA.py): The data to be analyzed. Assumed to have melody and harmony parts
    def __init__(self, dataScore):
        self.melody = dataScore["melody"]
        self.harmony = dataScore["harmony"]

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
        cohesion = analyzeCohesion(self.melody, self.harmony)
        noteLength = analyzeNoteLength(self.melody, self.harmony)
        octave = analyzeOctave(self.melody, self.harmony)
        commonNotes = analyzeCommonNotes(self.harmony)

        return [motion, consonance, consistency, macroharmony, centricity, cohesion, noteLength, octave, commonNotes]

    # Description:
    #   Analyze the score with the Score Delta Heuristic, return a 0.00-1.00 score
    # Parameters:
    #   corpus ([music21 Score]): Collection of scores to compare for analysis
    def getDeltaAnalysis(self, corpus):
        pass
