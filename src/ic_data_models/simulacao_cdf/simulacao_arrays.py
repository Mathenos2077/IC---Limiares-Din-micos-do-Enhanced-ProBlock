from utils import FactChecker
import utils
import numpy as np
from scipy.stats import norm


factCheckers = []
weightedVotes = []


expScoreEstaticoArray = [2, 8, 5, 2, 5, 8, 7, 7, 4, 7]
freqScoreArray = [1, 1, 2, 0, 2, 0, 2, 2, 0, 1]
accScoreArray = [2, 8, 7, 4, 3, 4, 4, 8, 5, 8]
subjectScoreArray = [5, 1, 5, 4, 3, 1, 1, 4, 1, 3]
confidenceScoreArray = [3, 3, 1, 2, 2, 3, 1, 3, 3, 3]
newsVoteArray = [2, -2, 2, 0, -2, -2, -2, -2, -2, -2]

coScoreMedioArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(len(expScoreEstaticoArray)):
    factCheckers.append(FactChecker(
        expScoreEstaticoArray[i], 
        freqScoreArray[i], 
        accScoreArray[i], 
        subjectScoreArray[i], 
        confidenceScoreArray[i], 
        newsVoteArray[i], 
        coScoreMedioArray[i] 
    ))
    weightedVotes.append(factCheckers[i].getWeightedVote())


cdf = round(utils.getCDF(weightedVotes), 4)

limiarScore = round(utils.getLimiarScore(factCheckers), 4)
limDown = round(limiarScore / 2, 2)
limDownEx = round(limDown / 2, 2)
limUp = round(1 - (limiarScore / 2), 2)
limUpEx = round((1 + limUp) / 2, 2)


print("WeightedVotes = ", weightedVotes)

print("CDF = ", cdf)

print("\n---------------   LIMIARES ANTIGOS   -----------------------\n")
print("     Completamente Falsa: ", 0, " < CDF <= ", 0.4)
print("            Inconclusivo: ", 0.4, " < CDF <= ", 0.6)
print("Completamente Verdadeira: ", 0.6, " < CDF <= ", 1)

print("\n---------------   NOVOS LIMIARES     -----------------------\n")
print("LimiarScore = ", limiarScore)
print("  Conteúdo Notoriamente Inverídico: ", 0 , " <= CDF <= ", limDownEx)
print("Conteúdo Sugestivamente Inverídico: ", limDownEx, " < CDF <= ", limDown)
print("                      Inconclusivo: ", limDown, " < CDF <= ", limUp)
print("  Conteúdo Sugestivamente Verídico: ", limUp, " < CDF <= ", limUpEx)
print("    Conteúdo Notoriamente Verídico: ", limUpEx, " < CDF <= ", 1)
print("--------------------------------------")
