import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

coEscore = np.linspace(0, 1, 101)

g = 0.250
incoerente = fuzz.trimf(coEscore, [0, 0, 2*g])
neutro = fuzz.trimf(coEscore, [0, 2*g, 4*g])
coerente = fuzz.trimf(coEscore, [2*g, 4*g, 6*g])


plt.figure(figsize=(8, 5))
plt.plot(coEscore, incoerente, "r", label="Incoerente")
plt.plot(coEscore, neutro, "y", label="Neutro")
plt.plot(coEscore, coerente, "g", label="Coerente")
plt.title("Funções de pertinência do CoEscore (entrada)")
plt.xlabel("coEscore")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
