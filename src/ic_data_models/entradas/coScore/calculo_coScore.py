import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

assertLevel = ctrl.Antecedent(np.linspace(0, 1, 101), "assertLevel")
confidenceScore = ctrl.Antecedent(np.linspace(0, 1, 101), "confidenceScore")
coEscore = ctrl.Consequent(np.linspace(0, 1, 101), "coEscore")

assertLevelC = ["erroGravíssimo", "erroGrave", "erroRazoável", "acertoRazoável", "acertoCompleto"]
confidenceC = ["naoConfiante", "neutro", "confiante"]
coEscoreC = ["muitoIncoerente", "incoerente", "neutro", "coerente", "muitoCoerente"]

sigma3 = np.abs(1.00 - 0.50) / (2 * np.sqrt(2 * np.log(2))) # sigma calculado para func. pert. com 3 conjuntos
sigma5 = np.abs(0.50 - 0.25) / (2 * np.sqrt(2 * np.log(2))) # sigma calculado para func. pert. com 5 conjuntos
g = 0.125
assertLevel[assertLevelC[0]] = fuzz.gaussmf(assertLevel.universe, 0.00, sigma5)
assertLevel[assertLevelC[1]] = fuzz.gaussmf(assertLevel.universe, 0.25, sigma5)
assertLevel[assertLevelC[2]] = fuzz.gaussmf(assertLevel.universe, 0.50, sigma5)
assertLevel[assertLevelC[3]] = fuzz.gaussmf(assertLevel.universe, 0.75, sigma5)
assertLevel[assertLevelC[4]] = fuzz.gaussmf(assertLevel.universe, 1.00, sigma5)

confidenceScore[confidenceC[0]] = fuzz.gaussmf(confidenceScore.universe, 0.00, sigma3)
confidenceScore[confidenceC[1]] = fuzz.gaussmf(confidenceScore.universe, 0.50, sigma3)
confidenceScore[confidenceC[2]] = fuzz.gaussmf(confidenceScore.universe, 1.00, sigma3)

coEscore[coEscoreC[0]] = fuzz.gaussmf(assertLevel.universe, 0.00, sigma5)
coEscore[coEscoreC[1]] = fuzz.gaussmf(assertLevel.universe, 0.25, sigma5)
coEscore[coEscoreC[2]] = fuzz.gaussmf(assertLevel.universe, 0.50, sigma5)
coEscore[coEscoreC[3]] = fuzz.gaussmf(assertLevel.universe, 0.75, sigma5)
coEscore[coEscoreC[4]] = fuzz.gaussmf(assertLevel.universe, 1.00, sigma5)

rules = []

rules.append(ctrl.Rule(assertLevel[assertLevelC[0]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[1]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[0]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[0]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[0]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[0]]))

rules.append(ctrl.Rule(assertLevel[assertLevelC[1]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[1]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[1]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[1]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[1]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[0]]))

rules.append(ctrl.Rule(assertLevel[assertLevelC[2]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[2]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[2]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[2]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[2]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[1]]))

rules.append(ctrl.Rule(assertLevel[assertLevelC[3]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[3]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[3]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[3]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[3]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[3]]))

rules.append(ctrl.Rule(assertLevel[assertLevelC[4]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[3]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[4]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[4]]))
rules.append(ctrl.Rule(assertLevel[assertLevelC[4]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[4]]))

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

sim.input["assertLevel"] = 0
sim.input["confidenceScore"] = 1
sim.compute()
min = sim.output["coEscore"]

sim.input["assertLevel"] = 1
sim.input["confidenceScore"] = 1
sim.compute()
max = sim.output["coEscore"]

def getCoEscoreIndividual_5var(rules, accLevelIndividual, confidenceScoreIndividual, normalizar=False):

    sim.input["assertLevel"] = accLevelIndividual
    sim.input["confidenceScore"] = confidenceScoreIndividual
    sim.compute()

    if normalizar == True:
        coEscoreFinal = (sim.output["coEscore"] - min) / (max - min) # Normalizado
        return coEscoreFinal
    
    coEscoreFinal = sim.output["coEscore"] # Não normalizado
    return coEscoreFinal


assertLevel = [0.00, 0.25, 0.50, 0.75, 1.00]
confidenceScore = [0.00, 0.50, 1.00]

for assertLevelValue in assertLevel:
    for confidenceScoreValue in confidenceScore:
        coScore = getCoEscoreIndividual_5var(rules, assertLevelValue, confidenceScoreValue, True)
        print("assertLevel = ", assertLevelValue, "  &&  confidenceScore = ", confidenceScoreValue, "  ---->   coScore = ", coScore)