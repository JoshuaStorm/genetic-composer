###############################################################################
##  Name:    Joshua Becker                                                   ##
##                                                                           ##
##  Description: An abstraction of our genetic "DNA".                        ##
###############################################################################


class DNA:
    # Description:
    #   Create a random strand of DNA
    # Parameters:
    #   length (number): The length of this 'strand' of DNA
    def __init__(self, length):
        pass

    # Description:
    #   Get this DNA's fitness, how "good" is this DNA? Darwin would be proud.
    def getFitness(self):
        pass

    # Description:
    #   I remember learning about this many years ago, but the theory and implementation are vastly different.
    #   Crossover these strands of DNA to produce a child. Birds, bees, and all that jazz.
    # Parameters:
    #   partner (DNA): The other DNA to breed this DNA with
    def breed(self, partner):
        pass

    # Description:
    #   In order to ensure enough variation, allow subtle mutations
    # Parameters:
    #   rate (number): The probability by which this DNA will mutate
    def mutate(rate):
        pass

    # Description:
    #   Turn this DNA into a score
    def toScore(self):
        pass
