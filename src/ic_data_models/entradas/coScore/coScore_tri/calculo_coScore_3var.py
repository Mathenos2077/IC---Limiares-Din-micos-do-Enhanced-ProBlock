import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def getCoEscoreIndividual_3var(accLevelIndividual, confidenceScoreIndividual):
    accLevel = ctrl.Antecedent(np.linspace(0, 1, 101), "accLevel")
    confidenceScore = ctrl.Antecedent(np.linspace(0, 1, 101), "confidenceScore")
    coEscore = ctrl.Consequent(np.linspace(0, 1, 101), "coEscore")

    accLevelC = ["0", "1", "2", "3", "4"]
    confidenceC = ["naoConfiante", "neutro", "confiante"]
    coEscoreC = ["incoerente", "neutro", "coerente"]

    g = 0.125
    accLevel[accLevelC[0]] = fuzz.trimf(accLevel.universe, [0, 0, 2*g])
    accLevel[accLevelC[1]] = fuzz.trimf(accLevel.universe, [0, 2*g, 4*g])
    accLevel[accLevelC[2]] = fuzz.trimf(accLevel.universe, [2*g, 4*g, 6*g])
    accLevel[accLevelC[3]] = fuzz.trimf(accLevel.universe, [4*g, 6*g, 8*g])
    accLevel[accLevelC[4]] = fuzz.trimf(accLevel.universe, [6*g, 8*g, 10*g])

    confidenceScore[confidenceC[0]] = fuzz.trimf(confidenceScore.universe, [-5.0, 0, 0.5])
    confidenceScore[confidenceC[1]] = fuzz.trimf(confidenceScore.universe, [0, 0.5, 1])
    confidenceScore[confidenceC[2]] = fuzz.trimf(confidenceScore.universe, [0.5, 1.0, 1.5])

    g = 0.250
    coEscore[coEscoreC[0]] = fuzz.trimf(coEscore.universe, [0, 0, 2*g])
    coEscore[coEscoreC[1]] = fuzz.trimf(coEscore.universe, [0, 2*g, 4*g])
    coEscore[coEscoreC[2]] = fuzz.trimf(coEscore.universe, [2*g, 4*g, 6*g])

    rules = []

    rules.append(ctrl.Rule(accLevel[accLevelC[0]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[0]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[0]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[0]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[0]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[0]]))

    rules.append(ctrl.Rule(accLevel[accLevelC[1]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[1]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[1]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[0]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[1]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[0]]))

    rules.append(ctrl.Rule(accLevel[accLevelC[2]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[1]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[2]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[1]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[2]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[1]]))

    rules.append(ctrl.Rule(accLevel[accLevelC[3]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[2]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[3]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[2]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[3]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[1]]))

    rules.append(ctrl.Rule(accLevel[accLevelC[4]] & confidenceScore[confidenceC[0]], coEscore[coEscoreC[2]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[4]] & confidenceScore[confidenceC[1]], coEscore[coEscoreC[2]]))
    rules.append(ctrl.Rule(accLevel[accLevelC[4]] & confidenceScore[confidenceC[2]], coEscore[coEscoreC[2]]))


    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)

    accLevelValues = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    confidenceScoreValues = [0.0, 0.5, 1.0]


    sim.input["accLevel"] = 0
    sim.input["confidenceScore"] = 1
    sim.compute()
    min = sim.output["coEscore"]

    sim.input["accLevel"] = 1
    sim.input["confidenceScore"] = 1
    sim.compute()
    max = sim.output["coEscore"]


    sim.input["accLevel"] = accLevelIndividual
    sim.input["confidenceScore"] = confidenceScoreIndividual
    sim.compute()

    coEscoreFinal = (sim.output["coEscore"] - min) / (max - min) # Normalizado
    #coEscoreFinal = sim.output["coEscore"] # Não normalizado

    return coEscoreFinal

coEscoreFinal = getCoEscoreIndividual_3var(
    0.2, # accLevel
    0.0  # confidenceScore
)
print("coEscore = ", round(coEscoreFinal, 2))


