from utils import FactChecker
import utils
import numpy as np
from scipy.stats import norm

factCheckers = []
weightedVotes = []


factCheckers.append(FactChecker(
    8, # expScoreEstatico: 2 a 8 (int)
    2, # freqScore: 0 a 2 (float)
    8, # accScore: 0 a 8 (float)
    5, # subjectScore: 1 a 5 (float)
    2, # newsVote: -2 a 2 (int)
    3, # confidenceScore: 1 a 3 (int)
    1 # coScoreMedio: 0 a 1 (float)
))

factCheckers.append(FactChecker(
    2, # expScoreEstatico: 2 a 8 (int)
    0, # freqScore: 0 a 2 (float)
    0, # accScore: 0 a 8 (float)
    1, # subjectScore: 1 a 5 (float)
    -2, # newsVote: -2 a 2 (int)
    1, # confidenceScore: 1 a 3 (int)
    0 # coScoreMedio: 0 a 1 (float)
))

factCheckers.append(FactChecker(
    2, # expScoreEstatico: 2 a 8 (int)
    0, # freqScore: 0 a 2 (float)
    0, # accScore: 0 a 8 (float)
    1, # subjectScore: 1 a 5 (float)
    -2, # newsVote: -2 a 2 (int)
    1, # confidenceScore: 1 a 3 (int)
    0 # coScoreMedio: 0 a 1 (float)
))

factCheckers.append(FactChecker(
    2, # expScoreEstatico: 2 a 8 (int)
    0, # freqScore: 0 a 2 (float)
    0, # accScore: 0 a 8 (float)
    1, # subjectScore: 1 a 5 (float)
    -2, # newsVote: -2 a 2 (int)
    1, # confidenceScore: 1 a 3 (int)
    0 # coScoreMedio: 0 a 1 (float)
))


for item in factCheckers:
    weightedVotes.append(item.getWeightedVote())

cdf = round(utils.getCDF(weightedVotes), 4)

limiarScore = round(utils.getLimiarScore(factCheckers), 4)
limDown = round(limiarScore / 2, 2)
limDownEx = round(limDown / 2, 2)
limUp = round(1 - (limiarScore / 2), 2)
limUpEx = round((1 + limUp) / 2, 2)


print("WeightedVotes = ", weightedVotes)

print("CDF = ", cdf)

print("\n---------------   LIMIARES ANTIGOS   -----------------------\n")
print("     Completamente Falsa: ", 0, " < CDF <= ", 0.225)
print("            Inconclusivo: ", 0.225, " < CDF <= ", 0.775)
print("Completamente Verdadeira: ", 0.775, " < CDF <= ", 1)

print("\n---------------   NOVOS LIMIARES     -----------------------\n")
print("LimiarScore = ", limiarScore)
print("  Conteúdo Notoriamente Inverídico: ", 0 , " <= CDF <= ", limDownEx)
print("Conteúdo Sugestivamente Inverídico: ", limDownEx, " < CDF <= ", limDown)
print("                      Inconclusivo: ", limDown, " < CDF <= ", limUp)
print("  Conteúdo Sugestivamente Verídico: ", limUp, " < CDF <= ", limUpEx)
print("    Conteúdo Notoriamente Verídico: ", limUpEx, " < CDF <= ", 1)
print("--------------------------------------------------------------")
