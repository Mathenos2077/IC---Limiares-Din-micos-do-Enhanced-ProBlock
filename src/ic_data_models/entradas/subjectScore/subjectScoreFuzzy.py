import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

subjectScoreL = np.linspace(0, 1, 101)

g = 0.250
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
leigo = fuzz.gaussmf(subjectScoreL, 0*g, sigma)
intermediario = fuzz.gaussmf(subjectScoreL, 2*g, sigma)
especialista = fuzz.gaussmf(subjectScoreL, 4*g, sigma)

plt.figure(figsize=(8, 5))
plt.plot(subjectScoreL, leigo, "r", label="Leigo")
plt.plot(subjectScoreL, intermediario, "y", label="Intermediario")
plt.plot(subjectScoreL, especialista, "g", label="Especialista")
plt.title("Funções de pertinência do subjectScoreTotal (entrada)")
plt.xlabel("subjectScoreTotal")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()