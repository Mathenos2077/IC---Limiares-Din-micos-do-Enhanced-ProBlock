from utils import FactChecker
import utils
import numpy as np
from scipy.stats import norm
import random
import matplotlib.pyplot as plt

# Essa simulação objetifica analisar os efeitos que o confidenceScore possui no CDF.
# Compara três situações:
#   - confidenceScore antigo (variando de 1 a 3)
#   - confidenceScore novo (variando de um novo invervalo, 
#       definido pelas variáveis A e B ([A, B]))
#   - confidenceScore neutro (constante igual a 1)


GERAR_ALEATORIO = False # Mude para False para usar as pontuações manuais abaixo
N = 5  # Número de avaliadores por rodada (caso GERAR_ALEATORIO = True)
A, B = 0.9, 1.1 # Intervalo [A, B] do confidenceScore com novo peso 
# Arrays para pontuações manuais (caso GERAR_ALEATORIO = False)
yrsScoreArray =           [3, 3, 3, 3, 3]
orgScoreArray =           [5, 5, 5, 5, 5]
freqScoreArray =        [2, 2, 2, 2, 2]
accScoreArray =         [8, 8, 8, 8, 8]
subjectScoreArray =     [5, 5, 5, 5, 5]
newsVoteArray =         [2, 2, 2, -2, -2]
confidenceScoreArray =  [3, 3, 3, 3, 3]
coScoreMedioArray =     [0.1, 0.5, 0.9, 0.3, 0.8]

checkersOld = []
checkersNew = []
checkersEmpty = []


if not GERAR_ALEATORIO:
    N = len(yrsScoreArray)

# Gera os fact-checkers
for j in range(N):
    if GERAR_ALEATORIO:
        yrsScore = random.randint(1, 3)
        orgScore = random.randint(1, 5)
        freqScore = random.uniform(0, 2)
        accScore = random.uniform(0, 8)
        subjectScore = random.uniform(1, 5)
        newsVote = random.randint(-2, 2)
        confidenceScore = random.randint(1, 3)
        coScoreMedio = random.uniform(0, 1)
    else:
        yrsScore = yrsScoreArray[j]
        orgScore = orgScoreArray[j]
        freqScore = freqScoreArray[j]
        accScore = accScoreArray[j]
        subjectScore = subjectScoreArray[j]
        newsVote = newsVoteArray[j]
        confidenceScore = confidenceScoreArray[j]
        coScoreMedio = coScoreMedioArray[j]

    # Fact-checker com confidenceScore antigo (1 à 3)
    checkerOld = FactChecker(
        yrsScore,
        orgScore,
        freqScore,
        accScore,
        subjectScore,
        newsVote,
        confidenceScore,
        coScoreMedio
    )
    checkersOld.append(checkerOld)

    # Fact-checker com confidenceScore no intervalo [A, B]
    confidenceScoreNew = A + ((confidenceScore - 1) / 2) * (B - A)
    checkerNew = FactChecker(
        yrsScore,
        orgScore,
        freqScore,
        accScore,
        subjectScore,
        newsVote,
        confidenceScoreNew,
        coScoreMedio
    )
    checkersNew.append(checkerNew)

    # Fact-checker com confidenceScore neutro
    confidenceScoreEmpty = 1
    checkerEmpty = FactChecker(
        yrsScore,
        orgScore,
        freqScore,
        accScore,
        subjectScore,
        newsVote,
        confidenceScoreEmpty,
        coScoreMedio
    )
    checkersEmpty.append(checkerEmpty)

weightedVotesOld = [checker.getWeightedVote() for checker in checkersOld]
weightedVotesNew = [checker.getWeightedVote() for checker in checkersNew]
weightedVotesEmpty = [checker.getWeightedVote() for checker in checkersEmpty]

cdfOld = round(utils.getCDF(weightedVotesOld), 4)
cdfNew = round(utils.getCDF(weightedVotesNew), 4)
cdfEmpty = round(utils.getCDF(weightedVotesEmpty), 4)

def printAvaliacao(checkers, weightedVotes, cdf):
    for i in range(len(checkers)):
        checker = checkers[i]
        yrsScore = checker.yrsScore
        orgScore = checker.orgScore
        freqScore = checker.freqScore
        accScore = checker.accScore
        subjectScore = checker.subjectScore
        newsVote = checker.newsVote
        confidenceScore = checker.confidenceScore
        coScoreMedio = checker.coScoreMedio
        
        print(f"  Avaliador {i+1}: Yrs={yrsScore}, Org={orgScore}, Freq={freqScore:.2f}, Acc={accScore:.2f}, Subj={subjectScore:.2f}, Vote={newsVote}, Conf={confidenceScore}, Co={coScoreMedio:.2f}, WeightedVote={weightedVotes[i]:.2f}")
    print("CDF = ", cdf)


print("-------------- SIMULAÇÃO: VARIAÇÃO DO CONFIDENCE SCORE --------------\n")

print("-----> ConficendeScore antigo ([1, 3])")
printAvaliacao(checkersOld, weightedVotesOld, cdfOld)

print(f"\n-----> ConficendeScore novo ([{A}, {B}])")
printAvaliacao(checkersNew, weightedVotesNew, cdfNew)

print(f"\n-----> ConficendeScore neutro (1)")
printAvaliacao(checkersEmpty, weightedVotesEmpty, cdfEmpty)