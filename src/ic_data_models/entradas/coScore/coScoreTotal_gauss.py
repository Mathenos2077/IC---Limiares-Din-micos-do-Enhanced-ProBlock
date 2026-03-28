import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

coScoreTotal = np.linspace(0, 1, 101)

g = 0.125
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
muitoIncoerente = fuzz.gaussmf(coScoreTotal, 0*g, sigma)
incoerente = fuzz.gaussmf(coScoreTotal, 2*g, sigma)
neutro = fuzz.gaussmf(coScoreTotal, 4*g, sigma)
coerente = fuzz.gaussmf(coScoreTotal, 6*g, sigma)
muitoCoerente = fuzz.gaussmf(coScoreTotal, 8*g, sigma)


plt.figure(figsize=(8, 5))
plt.plot(coScoreTotal, muitoIncoerente, "r", label="Muito Incoerente")
plt.plot(coScoreTotal, incoerente, "y", label="Incoerente")
plt.plot(coScoreTotal, neutro, "b", label="Neutro")
plt.plot(coScoreTotal, coerente, "c", label="Coerente")
plt.plot(coScoreTotal, muitoCoerente, "g", label="Muito Coerente")
plt.title("Funções de pertinência do coScoreTotal (entrada)")
plt.xlabel("coScoreTotal")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()