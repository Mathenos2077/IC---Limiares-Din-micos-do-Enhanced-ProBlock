import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# Definição das variáveis e seus conjuntos fuzzy
coEscore = ctrl.Antecedent(np.linspace(0, 1, 101), "coEscore")
ic = ctrl.Antecedent(np.linspace(0, 1, 101), "ic")
limiarScore = ctrl.Consequent(np.linspace(0, 1, 101), "limiarScore")

coEscoreC = ["muitoIncoerente", "incoerente", "neutro", "coerente", "muitoCoerente"]
icC = ["inconvicto", "intermediario", "convicto"] 
limiarScoreC = ["extr. baixo", "muito baixo", "baixo", "levemente baixo", "intermediario", "levemente alto", "alto", "muito alto", "extr. alto"]

g_co = 0.125
sigma_co = np.abs(2 * g_co) / (2 * np.sqrt(2 * np.log(2)))

coEscore[coEscoreC[0]] = fuzz.gaussmf(coEscore.universe, 0 * g_co, sigma_co)
coEscore[coEscoreC[1]] = fuzz.gaussmf(coEscore.universe, 2 * g_co, sigma_co)
coEscore[coEscoreC[2]] = fuzz.gaussmf(coEscore.universe, 4 * g_co, sigma_co)
coEscore[coEscoreC[3]] = fuzz.gaussmf(coEscore.universe, 6 * g_co, sigma_co)
coEscore[coEscoreC[4]] = fuzz.gaussmf(coEscore.universe, 8 * g_co, sigma_co)

g_ic = 0.25 
sigma_ic = np.abs(2 * g_ic) / (2 * np.sqrt(2 * np.log(2)))

ic[icC[0]] = fuzz.gaussmf(ic.universe, 0.0, sigma_ic)
ic[icC[1]] = fuzz.gaussmf(ic.universe, 0.5, sigma_ic)
ic[icC[2]] = fuzz.gaussmf(ic.universe, 1.0, sigma_ic)


g_lim = 0.0625
sigma_lim = np.abs(2 * g_lim) / (2 * np.sqrt(2 * np.log(2)))

limiarScore[limiarScoreC[0]] = fuzz.gaussmf(limiarScore.universe, 0 * g_lim, sigma_lim)
limiarScore[limiarScoreC[1]] = fuzz.gaussmf(limiarScore.universe, 2 * g_lim, sigma_lim)
limiarScore[limiarScoreC[2]] = fuzz.gaussmf(limiarScore.universe, 4 * g_lim, sigma_lim)
limiarScore[limiarScoreC[3]] = fuzz.gaussmf(limiarScore.universe, 6 * g_lim, sigma_lim)
limiarScore[limiarScoreC[4]] = fuzz.gaussmf(limiarScore.universe, 8 * g_lim, sigma_lim)
limiarScore[limiarScoreC[5]] = fuzz.gaussmf(limiarScore.universe, 10 * g_lim, sigma_lim)
limiarScore[limiarScoreC[6]] = fuzz.gaussmf(limiarScore.universe, 12 * g_lim, sigma_lim)
limiarScore[limiarScoreC[7]] = fuzz.gaussmf(limiarScore.universe, 14 * g_lim, sigma_lim)
limiarScore[limiarScoreC[8]] = fuzz.gaussmf(limiarScore.universe, 16 * g_lim, sigma_lim)
# Definição da nova base de regras (COMPLETA - sem poda)
rules = []

rules = []

rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[0]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[1]], limiarScore[limiarScoreC[0]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[2]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[3]], limiarScore[limiarScoreC[1]]))
rules.append(ctrl.Rule(ic[icC[0]] & coEscore[coEscoreC[4]], limiarScore[limiarScoreC[2]]))

rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[0]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[1]], limiarScore[limiarScoreC[3]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[2]], limiarScore[limiarScoreC[4]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[3]], limiarScore[limiarScoreC[5]]))
rules.append(ctrl.Rule(ic[icC[1]] & coEscore[coEscoreC[4]], limiarScore[limiarScoreC[5]]))

rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[0]], limiarScore[limiarScoreC[6]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[1]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[2]], limiarScore[limiarScoreC[7]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[3]], limiarScore[limiarScoreC[8]]))
rules.append(ctrl.Rule(ic[icC[2]] & coEscore[coEscoreC[4]], limiarScore[limiarScoreC[8]]))

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

sim.input["ic"] = 0
sim.input["coEscore"] = 0
sim.compute()
min_score = sim.output["limiarScore"]
sim.input["ic"] = 1
sim.input["coEscore"] = 1
sim.compute()
max_score = sim.output["limiarScore"]

def getLimiarScore_v4(coScoreTotal, IC, isNormalizado=False):

    sim.input["ic"] = IC
    sim.input["coEscore"] = coScoreTotal
    sim.compute()

    if isNormalizado == True:
        return (sim.output["limiarScore"] - min_score) / (max_score - min_score) # Normalizado
    else:
        return sim.output["limiarScore"] # Não normalizado

if __name__ == "__main__":
    print("LimiarScore: ", getLimiarScore_v4(
        0.6456, # coScoreTotal
        0.3, # IC
        True # isNormalizado  
    ))