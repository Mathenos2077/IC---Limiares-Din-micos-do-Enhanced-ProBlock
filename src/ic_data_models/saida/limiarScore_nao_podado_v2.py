import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl


# Definição das variáveis e seus conjuntos fuzzy com respectivas funções de pertinência
coEscore = ctrl.Antecedent(np.linspace(0, 1, 101), "coEscore")
ic = ctrl.Antecedent(np.linspace(0, 1, 101), "ic")
subjectScore = ctrl.Antecedent(np.linspace(0, 1, 101), "subjectScore")
limiarScore = ctrl.Consequent(np.linspace(0, 1, 101), "limiarScore")

coEscoreC = ["muitoIncoerente", "incoerente", "neutro", "coerente", "muitoCoerente"]
icC = ["muito inconvicto","inconvicto", "intermediario", "convicto", "muito convicto"]
subjectScoreC = ["leigo", "intermediario", "especialista"]
limiarScoreC = ["extr. baixo", "muito baixo", "baixo", "levemente baixo", "intermediario", "levemente alto", "alto", "muito alto", "extr. alto"]

g = 0.125
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
coEscore[coEscoreC[0]] = fuzz.gaussmf(coEscore.universe, 0*g, sigma)
coEscore[coEscoreC[1]] = fuzz.gaussmf(coEscore.universe, 2*g, sigma)
coEscore[coEscoreC[2]] = fuzz.gaussmf(coEscore.universe, 4*g, sigma)
coEscore[coEscoreC[3]] = fuzz.gaussmf(coEscore.universe, 6*g, sigma)
coEscore[coEscoreC[4]] = fuzz.gaussmf(coEscore.universe, 8*g, sigma)


ic[icC[0]] = fuzz.gaussmf(ic.universe, 0*g, sigma)
ic[icC[1]] = fuzz.gaussmf(ic.universe, 2*g, sigma)
ic[icC[2]] = fuzz.gaussmf(ic.universe, 4*g, sigma)
ic[icC[3]] = fuzz.gaussmf(ic.universe, 6*g, sigma)
ic[icC[4]] = fuzz.gaussmf(ic.universe, 8*g, sigma)

g = 0.250
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
subjectScore[subjectScoreC[0]] = fuzz.gaussmf(subjectScore.universe, 0*g, sigma)
subjectScore[subjectScoreC[1]] = fuzz.gaussmf(subjectScore.universe, 2*g, sigma)
subjectScore[subjectScoreC[2]] = fuzz.gaussmf(subjectScore.universe, 4*g, sigma)

g = 0.0625
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
limiarScore[limiarScoreC[0]] = fuzz.gaussmf(limiarScore.universe, 0*g, sigma)
limiarScore[limiarScoreC[1]] = fuzz.gaussmf(limiarScore.universe, 2*g, sigma)
limiarScore[limiarScoreC[2]] = fuzz.gaussmf(limiarScore.universe, 4*g, sigma)
limiarScore[limiarScoreC[3]] = fuzz.gaussmf(limiarScore.universe, 6*g, sigma)
limiarScore[limiarScoreC[4]] = fuzz.gaussmf(limiarScore.universe, 8*g, sigma)
limiarScore[limiarScoreC[5]] = fuzz.gaussmf(limiarScore.universe, 10*g, sigma)
limiarScore[limiarScoreC[6]] = fuzz.gaussmf(limiarScore.universe, 12*g, sigma)
limiarScore[limiarScoreC[7]] = fuzz.gaussmf(limiarScore.universe, 14*g, sigma)
limiarScore[limiarScoreC[8]] = fuzz.gaussmf(limiarScore.universe, 16*g, sigma)

# Definição da nova base de regras (COMPLETA - sem poda)
rules = []

# Grupo 1: IC = 0
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[1]]))

# Grupo 2: IC = 1
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[2]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[3]]))

# Grupo 3: IC = 2
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[5]]))

# Grupo 4: IC = 3
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[3]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[7]]))

# Grupo 5: IC = 4
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[0]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[1]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[2]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[3]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[0]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[1]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[4]] & coEscore[coEscoreC[4]] & subjectScore[subjectScoreC[2]], limiarScore[limiarScoreC[8]]))

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

sim.input["ic"] = 0
sim.input["coEscore"] = 0
sim.input["subjectScore"] = 0
sim.compute()
min_score = sim.output["limiarScore"]
sim.input["ic"] = 1
sim.input["coEscore"] = 1
sim.input["subjectScore"] = 1
sim.compute()
max_score = sim.output["limiarScore"]

def getLimiarScore_Nao_Podado_v2(coScoreTotal, IC, subejctScoreTotal, isNormalizado=False):
    sim.input["ic"] = IC
    sim.input["coEscore"] = coScoreTotal
    sim.input["subjectScore"] = subejctScoreTotal
    sim.compute()


    if isNormalizado == True:
        return (sim.output["limiarScore"] - min_score) / (max_score - min_score) # Normalizado
    else:
        return sim.output["limiarScore"] # Não normalizado

if __name__ == "__main__":
    print("LimiarScore: ", getLimiarScore_Nao_Podado_v2(
        1, # IC
        1, # coScoreTotal
        1, # subjectScoreTotal
        True # isNormalizado  
    ))