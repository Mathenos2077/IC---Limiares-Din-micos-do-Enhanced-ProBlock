import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

coEscore = np.linspace(0, 1, 101)

g = 0.125
muitoIncoerente = fuzz.trimf(coEscore, [0, 0, 2*g])
incoerente = fuzz.trimf(coEscore, [0, 2*g, 4*g])
neutro = fuzz.trimf(coEscore, [2*g, 4*g, 6*g])
coerente = fuzz.trimf(coEscore, [4*g, 6*g, 8*g])
muitoCoerente = fuzz.trimf(coEscore, [6*g, 8*g, 10*g])

plt.figure(figsize=(8, 5))
plt.plot(coEscore, muitoIncoerente, "r", label="Muito incoerente")
plt.plot(coEscore, incoerente, "y", label="Incoerente")
plt.plot(coEscore, neutro, "b", label="Neutro")
plt.plot(coEscore, coerente, "c", label="Coerente")
plt.plot(coEscore, muitoCoerente, "g", label="Muito Coerente")
plt.title("Funções de pertinência do coScore (consequente)")
plt.xlabel("coScore")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
