import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# Define antecedentes e o consequente, bem como seus domínios
assertLevel = ctrl.Antecedent(np.linspace(0, 1, 101), "assertLevel")
confidenceScore = ctrl.Antecedent(np.linspace(0, 1, 101), "confidenceScore")
coEscore = ctrl.Consequent(np.linspace(0, 1, 101), "coEscore")

# Define conjuntos fuzzy
assertLevelC = ["0", "1", "2", "3", "4"]
confidenceC = ["naoConfiante", "neutro", "confiante"]
coEscoreC = ["muitoIncoerente", "incoerente", "neutro", "coerente", "muitoCoerente"]

# Define funções as de pertinência (triangulares simétricas)
g = 0.125
assertLevel[assertLevelC[0]] = fuzz.trimf(assertLevel.universe, [0, 0, 2*g])
assertLevel[assertLevelC[1]] = fuzz.trimf(assertLevel.universe, [0, 2*g, 4*g])
assertLevel[assertLevelC[2]] = fuzz.trimf(assertLevel.universe, [2*g, 4*g, 6*g])
assertLevel[assertLevelC[3]] = fuzz.trimf(assertLevel.universe, [4*g, 6*g, 8*g])
assertLevel[assertLevelC[4]] = fuzz.trimf(assertLevel.universe, [6*g, 8*g, 10*g])

confidenceScore[confidenceC[0]] = fuzz.trimf(confidenceScore.universe, [-5.0, 0, 0.5])
confidenceScore[confidenceC[1]] = fuzz.trimf(confidenceScore.universe, [0, 0.5, 1])
confidenceScore[confidenceC[2]] = fuzz.trimf(confidenceScore.universe, [0.5, 1.0, 1.5])

coEscore[coEscoreC[0]] = fuzz.trimf(coEscore.universe, [0, 0, 2*g])
coEscore[coEscoreC[1]] = fuzz.trimf(coEscore.universe, [0, 2*g, 4*g])
coEscore[coEscoreC[2]] = fuzz.trimf(coEscore.universe, [2*g, 4*g, 6*g])
coEscore[coEscoreC[3]] = fuzz.trimf(coEscore.universe, [4*g, 6*g, 8*g])
coEscore[coEscoreC[4]] = fuzz.trimf(coEscore.universe, [6*g, 8*g, 10*g])

# Definição de regras de inferência
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

# Início do sistema de simulação
system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

# Encontra o min e max possíveis, para normalizar os resultados entre 0 e 1 depois
sim.input["assertLevel"] = 0
sim.input["confidenceScore"] = 1
sim.compute()
min = sim.output["coEscore"]

sim.input["assertLevel"] = 1
sim.input["confidenceScore"] = 1
sim.compute()
max = sim.output["coEscore"]

# função para obter o coScoreIndividual
def getCoEscoreIndividual_5var(accLevelIndividual, confidenceScoreIndividual, normalizar=False):
    

    sim.input["assertLevel"] = accLevelIndividual
    sim.input["confidenceScore"] = confidenceScoreIndividual
    sim.compute()

    if normalizar == True:
        coEscoreFinal = (sim.output["coEscore"] - min) / (max - min) # Normalizado
        return coEscoreFinal
    
    coEscoreFinal = sim.output["coEscore"] # Não normalizado
    return coEscoreFinal

if __name__ == "__main__":
    assertLevel = [0.00, 0.25, 0.50, 0.75, 1.00]
    confidenceScore = [0.00, 0.50, 1.00]

    for assertLevelValue in assertLevel:
        for confidenceScoreValue in confidenceScore:
            coScore = getCoEscoreIndividual_5var(assertLevelValue, confidenceScoreValue, True)
            print("assertLevel = ", assertLevelValue, "  &&  confidenceScore = ", confidenceScoreValue, "  ---->   coScore = ", coScore)