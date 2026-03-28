import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

accLevel = np.linspace(0, 1, 101)

g = 0.125
accLevel0 = fuzz.trimf(accLevel, [0, 0, 2*g])
accLevel1 = fuzz.trimf(accLevel, [0, 2*g, 4*g])
accLevel2 = fuzz.trimf(accLevel, [2*g, 4*g, 6*g])
accLevel3 = fuzz.trimf(accLevel, [4*g, 6*g, 8*g])
accLevel4 = fuzz.trimf(accLevel, [6*g, 8*g, 10*g])

plt.figure(figsize=(8, 5))
plt.plot(accLevel, accLevel0, "r", label="Erro gravíssimo")
plt.plot(accLevel, accLevel1, "y", label="Erro grave")
plt.plot(accLevel, accLevel2, "b", label="Erro razoável")
plt.plot(accLevel, accLevel3, "c", label="Acerto razoável")
plt.plot(accLevel, accLevel4, "g", label="Acerto completo")
plt.title("Funções de pertinência do assertLevel (antecedente)")
plt.xlabel("assertLevel")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
